import unittest

import Clouds_Coder as cc


class KimiToolHistoryCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.client = cc.OllamaClient(
            "https://ark.cn-beijing.volces.com/api/coding/v1",
            "kimi-k3",
            provider="kimi",
        )

    def test_dangling_multi_tool_calls_are_removed_before_kimi_request(self):
        messages = [
            {"role": "user", "content": "Build the UI"},
            {
                "role": "assistant",
                "content": "I will inspect two paths.",
                "tool_calls": [
                    {
                        "id": "bash_0",
                        "type": "function",
                        "function": {"name": "bash", "arguments": '{"command":"ls"}'},
                    },
                    {
                        "id": "bash_1",
                        "type": "function",
                        "function": {"name": "bash", "arguments": '{"command":"pwd"}'},
                    },
                ],
            },
            {"role": "user", "content": "Create the required Todo list first."},
        ]

        prepared = self.client._prepare_request_messages(messages, "kimi")

        self.assertEqual([row["role"] for row in prepared], ["user", "assistant", "user"])
        self.assertNotIn("tool_calls", prepared[1])
        self.assertEqual(prepared[1]["content"], "I will inspect two paths.")

    def test_complete_multi_tool_block_is_preserved(self):
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "bash_0",
                        "type": "function",
                        "function": {"name": "bash", "arguments": '{"command":"ls"}'},
                    },
                    {
                        "id": "bash_1",
                        "type": "function",
                        "function": {"name": "bash", "arguments": '{"command":"pwd"}'},
                    },
                ],
            },
            {"role": "tool", "tool_call_id": "bash_0", "name": "bash", "content": "files"},
            {"role": "tool", "tool_call_id": "bash_1", "name": "bash", "content": "path"},
            {"role": "user", "content": "Continue"},
        ]

        prepared = self.client._prepare_request_messages(messages, "kimi")

        self.assertEqual([row["role"] for row in prepared], ["assistant", "tool", "tool", "user"])
        self.assertEqual(
            [row["id"] for row in prepared[0]["tool_calls"]],
            ["bash_0", "bash_1"],
        )

    def test_partial_multi_tool_block_keeps_only_complete_pairs(self):
        messages = [
            {
                "role": "assistant",
                "content": "Inspecting.",
                "tool_calls": [
                    {
                        "id": "bash_0",
                        "type": "function",
                        "function": {"name": "bash", "arguments": "{}"},
                    },
                    {
                        "id": "bash_1",
                        "type": "function",
                        "function": {"name": "bash", "arguments": "{}"},
                    },
                ],
            },
            {"role": "tool", "tool_call_id": "bash_0", "name": "bash", "content": "ok"},
            {"role": "user", "content": "Continue"},
        ]

        prepared = self.client._prepare_request_messages(messages, "kimi")

        self.assertEqual([row["role"] for row in prepared], ["assistant", "tool", "user"])
        self.assertEqual([row["id"] for row in prepared[0]["tool_calls"]], ["bash_0"])
        self.assertEqual(prepared[1]["tool_call_id"], "bash_0")


if __name__ == "__main__":
    unittest.main()
