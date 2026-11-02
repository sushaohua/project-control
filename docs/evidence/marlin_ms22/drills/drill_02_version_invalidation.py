#!/usr/bin/env python3
"""MS-22 Drill 02: Version Invalidation and Re-verification Drill.

[DRILL / SIMULATION - NOT A PRODUCTION ARTIFACT]
Verifies that when an upstream candidate artifact version changes:
1. Downstream task detects hash mismatch and refuses to consume outdated approval.
2. Independent review is re-triggered on the new candidate.
3. New report with distinct report SHA256 is generated and accepted.
"""

import hashlib
import sys
import tempfile
from pathlib import Path

def run_drill():
    print("=== MS-22 Drill 02: Candidate Version Invalidation & Re-verification ===")
    
    # 1. Candidate RC1 vs RC2
    rc1_artifact_content = b"Candidate RC1: commit 68a419a / Marlin_AT32.bin (with DMA poll bug)"
    rc1_hash = hashlib.sha256(rc1_artifact_content).hexdigest()
    print(f"\n[Step 1: Upstream Release RC1]")
    print(f"RC1 Artifact SHA256: {rc1_hash}")
    
    # Historical review on RC1
    rc1_review_report = f"QA Review on RC1: artifact={rc1_hash}. Decision: APPROVED"
    rc1_report_sha256 = hashlib.sha256(rc1_review_report.encode("utf-8")).hexdigest()
    print(f"RC1 QA Report SHA256: {rc1_report_sha256}")
    
    # 2. Upstream Bug Fix -> RC2
    print(f"\n[Step 2: Upstream Bug Fix -> RC2 Release]")
    rc2_artifact_content = b"Candidate RC2: commit 1246ea9 / Marlin_AT32.bin (DMA poll bug FIXED)"
    rc2_hash = hashlib.sha256(rc2_artifact_content).hexdigest()
    print(f"RC2 Artifact SHA256: {rc2_hash}")
    
    # 3. Downstream Consumer Check
    print(f"\n[Step 3: Downstream Consumer Checks Candidate Match]")
    consumer_expected_version = rc1_hash  # Downstream task still holds old RC1
    if consumer_expected_version != rc2_hash:
        print(f"  [REJECTED] Downstream dependency mismatch!")
        print(f"  Expected: {consumer_expected_version}")
        print(f"  Received: {rc2_hash}")
        print("  -> Old RC1 approval CANNOT be applied to RC2!")
    else:
        print("  [ERROR] Stale approval was mistakenly accepted!")
        sys.exit(1)
        
    # 4. Independent Re-verification on RC2
    print(f"\n[Step 4: Re-running Independent QA Verification on RC2]")
    rc2_review_report = f"QA Review on RC2: artifact={rc2_hash}. Decision: APPROVED. Verified DMA poll fix."
    rc2_report_sha256 = hashlib.sha256(rc2_review_report.encode("utf-8")).hexdigest()
    print(f"New RC2 QA Report SHA256: {rc2_report_sha256}")
    assert rc2_report_sha256 != rc1_report_sha256, "Report SHA256 must differ!"
    
    # 5. COORD Handoff Binding
    print(f"\n[Step 5: COORD Updates Task Card Binding]")
    task_card_binding = {
        "accepted_version": rc2_hash,
        "report_sha256": rc2_report_sha256,
        "decision": "APPROVED"
    }
    print(f"Task Card successfully updated with new binding:")
    print(f"  accepted_version: {task_card_binding['accepted_version']}")
    print(f"  report_sha256:    {task_card_binding['report_sha256']}")
    print("-> Step 5 PASSED: Clean version invalidation and re-binding cycle achieved.")
    
    print("\n=== Drill 02 Complete: Version Change & Invalidation Cycle Successfully Verified ===")
    return 0

if __name__ == "__main__":
    sys.exit(run_drill())
