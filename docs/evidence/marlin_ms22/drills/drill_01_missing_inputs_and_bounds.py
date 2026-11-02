#!/usr/bin/env python3
"""MS-22 Drill 01: Missing Inputs and Out-of-Bounds Rejection Drill.

[DRILL / SIMULATION - NOT A PRODUCTION ARTIFACT]
Verifies that the task graph gating mechanism blocks tasks with:
1. Missing input commit/diff binding.
2. Missing predecessor completion.
3. Unbounded or out-of-scope write paths.
"""

import sys
import tempfile
import yaml
from pathlib import Path

# Add project-control tools to sys.path
WORKSPACE = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WORKSPACE / "project-control" / "tools"))
import check_task_graph

def run_drill():
    print("=== MS-22 Drill 01: Missing Inputs & Out-of-Bounds Rejection ===")
    
    # 1. Test Card with missing dispatch binding
    test_card_missing_input = {
        "id": "DRILL-INP-01",
        "title": "Drill Task Missing Inputs",
        "revision": 1,
        "task_kind": "implementation",
        "dispatchable": True,
        "status": "Ready",
        "blocked": False,
        "owner": "DRILL-AGENT-01",
        "executor": {"role": "ENG-FWD", "agent_id": "DRILL-AGENT-01", "run_id": "run_01"},
        "review_assignments": {
            "reviewer_sessions": [
                {"role": "QA", "session": "DRILL-QA-01", "decision": None, "artifact_version": None, "evidence": None}
            ]
        },
        "worktree": "soc-ap",
        "base_commit": "4445c8fedc21bafef5e6c971fcb54cec703f0e71",
        "dispatch_binding": {
            "source_commit": None,  # MISSING
            "workspace_diff_sha256": None  # MISSING
        },
        "lease": {
            "owner": "DRILL-AGENT-01",
            "task_revision": 1,
            "lease_id": "lease-drill-01",
            "expires_at": "2026-10-29T18:00:00+08:00"
        },
        "handoff": {
            "receiver_role": "COORD",
            "receiver_session": "main",
            "transport": "docs",
            "evidence_location": "docs/evidence/drill"
        },
        "depends_on": ["NON-EXISTENT-PRED"],
        "dependency_conditions": [
            {"task": "NON-EXISTENT-PRED", "accepted_version": "v1.0", "acceptance_evidence": "docs/none.md"}
        ]
    }
    
    cards = {"DRILL-INP-01": test_card_missing_input}
    blockers = check_task_graph.readiness_blockers(test_card_missing_input, cards, WORKSPACE)
    
    print("\n[Case 1: Missing Dispatch Binding & Unmet Predecessor]")
    print(f"Card Status: {test_card_missing_input['status']}")
    print(f"Blockers Detected ({len(blockers)}):")
    for b in blockers:
        print(f"  - [BLOCKED] {b}")
    
    assert any("dispatch input commit/diff" in b for b in blockers), "Failed to detect missing dispatch binding!"
    assert any("NON-EXISTENT-PRED is not Done" in b for b in blockers), "Failed to detect unmet predecessor!"
    print("-> Case 1 PASSED: Gating mechanism successfully intercepted missing inputs and unmet predecessor.")

    # 2. Test Out-of-bounds Write Scope
    print("\n[Case 2: Escaping / Unbounded Write Scope]")
    test_card_escaping_path = {
        "id": "DRILL-BOUND-02",
        "title": "Drill Task Escaping Path",
        "allowed_repositories": ["soc-ap"],
        "write_scope": {
            "soc-ap": ["core/forward/**", "../../etc/passwd", "**"]
        },
        "allowed_paths": ["soc-ap/core/forward/**"]
    }
    scope_problems, _ = check_task_graph._check_write_scope("DRILL-BOUND-02", test_card_escaping_path, WORKSPACE)
    print(f"Scope Violations Detected ({len(scope_problems)}):")
    for p in scope_problems:
        print(f"  - [VIOLATION] {p}")
        
    assert any("unbounded/escaping write path" in p for p in scope_problems), "Failed to detect escaping path!"
    assert any("allowed_paths differs from write_scope" in p for p in scope_problems), "Failed to detect allowed_paths discrepancy!"
    print("-> Case 2 PASSED: Gating mechanism successfully intercepted path escape and boundary discrepancy.")

    print("\n=== Drill 01 Complete: All 2 Gating Defenses Successfully Verified ===")
    return 0

if __name__ == "__main__":
    sys.exit(run_drill())
