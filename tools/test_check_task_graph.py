#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_check_task_graph.py - 任务图静态检查与门禁规则反例测试套件 (CR-03D)
依据 PLAN-CASCADE-RECOVERY-20261027 第 6.1 节验收矩阵设计。
全部测试在隔离临时副本/内存数据中执行，严禁修改正式任务卡。
符合 c_cpp_coding_standard 函数 <= 50 行、参数 <= 4 硬性门禁。
"""

import ast
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
import yaml

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import check_task_graph as ctg


class TestTaskGraphNegativeCases(unittest.TestCase):
    """第 6.1 节任务工具反例隔离核查"""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="test_ctg_"))
        self.workspace = self.tmp_dir
        self.control = self.tmp_dir / "project-control"
        self.control.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _create_minimal_card(self, path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n# Test Card\n"
        path.write_text(content, encoding="utf-8")

    def test_twin_cards_use_full_microtask_gates(self):
        """新任务族不得绕过结构、依赖和Ready门禁。"""
        self.assertTrue(ctg.is_microtask("TWIN-01", {}))
        path = self.control / ".agents/kanban/microtasks/vmware_soc_twin/TWIN-01.md"
        self._create_minimal_card(path, {"id": "TWIN-01", "status": "Backlog"})
        cards, report = ctg.check(self.workspace)
        self.assertIn("TWIN-01: missing write_scope", report["errors"])
        self.assertIn("TWIN-01", report["readiness_blockers"])

    def test_unquoted_colon_yaml_causes_error(self):
        """反例 1: YAML 含未引用冒号导致解析异常，工具必须报错并定位"""
        bad_card = self.control / ".agents/kanban/milestones/bad_ms.md"
        bad_card.parent.mkdir(parents=True, exist_ok=True)
        bad_card.write_text("---\nid: MS-BAD\ntitle: Bad: Unquoted Colon\n---\nBody\n", encoding="utf-8")
        cards, report = ctg.check(self.workspace)
        self.assertIn("bad_ms.md", " ".join(report["errors"]))

    def test_duplicate_task_id_rejected(self):
        """反例 2: 重复 Task ID 必须非零退出并报告错误"""
        card_data = {"id": "V2-P99A", "status": "Backlog"}
        p1 = self.control / ".agents/kanban/microtasks/minimc_v2/card1.md"
        p2 = self.control / ".agents/kanban/microtasks/minimc_v2/card2.md"
        self._create_minimal_card(p1, card_data)
        self._create_minimal_card(p2, card_data)
        cards, report = ctg.check(self.workspace)
        self.assertTrue(any("duplicate task id: V2-P99A" in e for e in report["errors"]))

    def test_glob_write_scope_overlap_detected(self):
        """反例 3: glob 路径包含（如 ** 与具体文件）无依赖顺序时必须被拦截"""
        left = {
            "id": "CR-01A", "status": "Backlog", "task_kind": "implementation", "dispatchable": True,
            "allowed_paths": ["project-control/docs/specs/**"], "depends_on": []
        }
        right = {
            "id": "CR-01B", "status": "Backlog", "task_kind": "implementation", "dispatchable": True,
            "allowed_paths": ["project-control/docs/specs/test.md"], "depends_on": []
        }
        microtasks = {"CR-01A": left, "CR-01B": right}
        cards = {"CR-01A": left, "CR-01B": right}
        overlaps, errors = ctg.check_path_overlaps(microtasks, cards)
        self.assertEqual(len(overlaps), 1)
        self.assertTrue(any("shared writes lack dependency ordering" in e for e in errors))

    def test_readiness_blocker_on_blocked_task(self):
        """反例 4: 带有 blocked=true 的任务必须阻止推进到 Ready/InProgress"""
        card = {"id": "CR-02", "blocked": True}
        blockers = ctg.readiness_blockers(card, {})
        self.assertIn("task is marked blocked", blockers)

    def test_readiness_blocker_on_expired_lease(self):
        """反例 5: 租约过期的任务必须生成 blocker"""
        card = {
            "id": "CR-02", "owner": "agent-1", "revision": 1,
            "executor": {"agent_id": "agent-1"},
            "lease": {
                "owner": "agent-1", "task_revision": 1,
                "lease_id": "l-1", "expires_at": "2000-01-01T00:00:00+08:00"
            }
        }
        blockers = ctg.readiness_blockers(card, {})
        self.assertIn("lease has expired", blockers)

    def test_readiness_blocker_on_bogus_commit(self):
        """反例 6: dispatch_binding 中填入 bogus commit 时必须拦截"""
        card = {
            "id": "CR-02", "base_commit": "not-a-commit",
            "dispatch_binding": {
                "source_commit": "not-a-commit",
                "workspace_diff_sha256": "not-a-sha256"
            }
        }
        blockers = ctg.readiness_blockers(card, {})
        self.assertTrue(any("invalid/bogus hash" in b for b in blockers))

    def test_done_acceptance_rejects_self_review(self):
        """反例 7: 作者兼独立评审者必须拒绝 Done 验收"""
        card = {
            "id": "CR-02", "status": "Done", "owner": "agent-author", "depends_on": [],
            "review_assignments": {
                "reviewer_sessions": [
                    {"role": "QA", "session": "agent-author", "decision": "APPROVED",
                     "artifact_version": "sha256:1234", "evidence": "ev.md"}
                ]
            }
        }
        errs = ctg.done_acceptance_errors("CR-02", card, {})
        self.assertTrue(any("author (agent-author) cannot be own independent reviewer" in e for e in errs))

    def test_done_acceptance_rejects_rejected_decision(self):
        """反例 8: 独立评审结论为 REJECTED 必须拒绝 Done 验收"""
        card = {
            "id": "CR-02", "status": "Done", "owner": "agent-author", "depends_on": [],
            "review_assignments": {
                "reviewer_sessions": [
                    {"role": "QA", "session": "agent-qa", "decision": "REJECTED",
                     "artifact_version": "sha256:1234", "evidence": "ev.md"}
                ]
            }
        }
        errs = ctg.done_acceptance_errors("CR-02", card, {})
        self.assertTrue(any("review decision is not accepted" in e for e in errs))

    def test_done_acceptance_rejects_uncompleted_predecessor(self):
        """反例 9: 前置任务非 Done 时，本任务不能被接受为 Done"""
        card = {
            "id": "CR-02", "status": "Done", "owner": "agent-author", "depends_on": ["CR-01"],
            "review_assignments": {
                "reviewer_sessions": [
                    {"role": "QA", "session": "agent-qa", "decision": "APPROVED",
                     "artifact_version": "sha256:1234", "evidence": "ev.md"}
                ]
            }
        }
        cards = {"CR-01": {"id": "CR-01", "status": "Backlog"}}
        errs = ctg.done_acceptance_errors("CR-02", card, cards)
        self.assertTrue(any("predecessor CR-01 is Backlog" in e for e in errs))

    def test_candidate_descriptor_rejects_bogus_commits(self):
        """反例 10: 候选清单中填入全 0/全 1 等伪造 commit 必须报错"""
        cand_file = self.control / "cand.yaml"
        cand_data = {
            "candidate_id": "CAND-01", "scope": "test", "protocol": "proto",
            "verification": "v", "limitations": "l", "handoff": "h",
            "repositories": {
                "soc-ap": {"commit": "0" * 40},
                "project-control": {"commit": "1" * 40}
            }
        }
        cand_file.write_text(yaml.safe_dump(cand_data), encoding="utf-8")
        issues = ctg._check_candidate_descriptor(cand_file, self.workspace)
        self.assertTrue(any("commit is invalid/bogus" in i for i in issues))


class TestCodingStandards(unittest.TestCase):
    """硬性门禁：check_task_graph.py 100% 符合函数 <= 50 行、参数 <= 4"""

    def test_check_task_graph_scale_and_params(self):
        file_path = TOOLS_DIR / "check_task_graph.py"
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        violations = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno + 1
                params = len(node.args.posonlyargs) + len(node.args.args) + len(node.args.kwonlyargs)
                if lines > 50 or params > 4:
                    violations.append((node.name, lines, params))
        self.assertEqual(violations, [], f"check_task_graph.py 存在超限函数: {violations}")


if __name__ == "__main__":
    unittest.main()
