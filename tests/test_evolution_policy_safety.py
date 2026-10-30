"""Host defaults and cross-task generalization survive candidate policy changes."""

import copy
import unittest

from liquid_kernel import normalize_evolution_config
from liquid_kernel.agentic import apply_execution_policy, preserve_recall_tool
from liquid_kernel.context import RECALL_TOOL
from liquid_kernel.control import (
    BASELINE_KERNEL_FILES,
    LiquidKernelError,
    StructuredPatchValidator,
)


class EvolutionPolicySafetyTests(unittest.TestCase):
    def test_admin_output_allowance_is_not_replaced_by_candidate_defaults(self):
        for host_allowance in (512, 4096, 16384):
            for candidate_limit in (128, 1024, 32000):
                _, _, actual = apply_execution_policy(
                    [], [], host_allowance, {"max_output_tokens": candidate_limit}
                )
                self.assertEqual(actual, host_allowance)

    def test_recall_schema_is_preserved_through_filtering_and_cannot_be_invented(self):
        ordinary = {"type": "function", "function": {"name": "read_file"}}
        recall = copy.deepcopy(RECALL_TOOL)
        _, tools, _ = apply_execution_policy(
            [], [ordinary, recall], 4096, {"allowed_tools": ["read_file"]}
        )
        self.assertEqual(tools[-1], recall)
        self.assertEqual(preserve_recall_tool([ordinary], [ordinary]), [ordinary])
        fake = copy.deepcopy(recall)
        fake["function"]["parameters"] = {}
        self.assertEqual(preserve_recall_tool([fake], [recall]), [recall])

    def test_history_selection_supplies_progress_and_exact_recall_identity(self):
        rows = [
            {"role": "user", "content": "Preserve the original requirement"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "write-1",
                        "function": {
                            "name": "write_file",
                            "arguments": {"path": "ready.py", "content": "x" * 20000},
                        },
                    }
                ],
            },
            {
                "role": "tool",
                "tool_call_id": "write-1",
                "name": "write_file",
                "content": '{"ok":true,"path":"ready.py"}',
            },
            {"role": "user", "content": "Keep the later correction"},
            {"role": "assistant", "content": "Current decision"},
            {"role": "tool", "content": "Current observation"},
        ]
        selected, _, _ = apply_execution_policy(
            rows, [RECALL_TOOL], 4096, {"recent_tool_exchanges": 1}
        )
        handoff = next(
            row["content"]
            for row in selected
            if row.get("content", "").startswith("<kernel-history-handoff>")
        )
        self.assertIn("ready.py", handoff)
        self.assertIn("write-1", handoff)
        self.assertIn('"ok"', handoff.replace('\\"', '"'))
        self.assertLess(len(handoff), 4000)
        self.assertEqual(
            [
                r["content"]
                for r in selected
                if r["role"] == "user"
                and not r.get("content", "").startswith("<kernel-history-handoff>")
            ],
            ["Preserve the original requirement", "Keep the later correction"],
        )

    def test_training_field_rules_do_not_leak_into_unrelated_task_prompts(self):
        validator = StructuredPatchValidator()
        config = normalize_evolution_config({"mode": "Thinking"})
        training = [
            {
                "goal": "Produce an evidence artifact with the field unchanged_disk_reads.",
                "followups": [],
            }
        ]
        candidate = dict(BASELINE_KERNEL_FILES)
        candidate["prompt_policy.py"] = (
            'def augment_prompt(prompt, *, role="", context=None):\n    return prompt + " Always define unchanged_disk_reads as a whole-run count."\n'
        )
        with self.assertRaises(LiquidKernelError) as caught:
            validator.check_generalization(
                BASELINE_KERNEL_FILES, candidate, training, config
            )
        self.assertEqual(caught.exception.code, "task_specific_policy")
        self.assertFalse(caught.exception.details["holdout_accessed"])
        candidate["prompt_policy.py"] = (
            'def augment_prompt(prompt, *, role="", context=None):\n    return prompt + " Validate types and counter scope against the current user schema; never infer them from a field name."\n'
        )
        self.assertEqual(
            validator.check_generalization(
                BASELINE_KERNEL_FILES, candidate, training, config
            )["contrastive_probe"],
            "passed",
        )

    def test_context_conditional_domain_guidance_is_allowed(self):
        candidate = dict(BASELINE_KERNEL_FILES)
        candidate["prompt_policy.py"] = (
            'def augment_prompt(prompt, *, role="", context=None):\n    if "unchanged_disk_reads" in (context or {}).get("goal", ""):\n        return prompt + " Inspect the task definition of unchanged_disk_reads."\n    return prompt\n'
        )
        meta = StructuredPatchValidator().check_generalization(
            BASELINE_KERNEL_FILES,
            candidate,
            [
                {
                    "goal": "The current task defines unchanged_disk_reads.",
                    "followups": [],
                }
            ],
            normalize_evolution_config({"mode": "Thinking"}),
        )
        self.assertEqual(meta["contrastive_probe"], "passed")
