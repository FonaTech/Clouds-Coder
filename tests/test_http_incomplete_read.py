import unittest
from http.client import IncompleteRead
from unittest import mock

import Clouds_Coder as cc


class FakeHTTPResponse:
    def __init__(self, *, body=b"", read_error=None, lines=None, length=None, content_type="application/json"):
        self.body = body
        self.read_error = read_error
        self.lines = list(lines or [])
        self.length = length
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        if self.read_error is not None:
            raise self.read_error
        return self.body

    def readline(self):
        if not self.lines:
            return b""
        value = self.lines.pop(0)
        if isinstance(value, BaseException):
            raise value
        if isinstance(self.length, int):
            self.length = max(0, self.length - len(value))
        return value


class IncompleteHTTPReadTests(unittest.TestCase):
    def client(self):
        return cc.OllamaClient(
            "http://model.test",
            "demo-model",
            provider="openai_compat",
        )

    def retry_patches(self, client):
        return (
            mock.patch.object(client, "_wait_with_cancel", return_value=None),
            mock.patch.object(client, "_set_endpoint_cooldown", return_value=None),
            mock.patch.object(client, "_cooldown_remaining", return_value=0.0),
        )

    def test_non_stream_json_discards_partial_body_and_reissues_full_request(self):
        client = self.client()
        partial = IncompleteRead(b'{"partial": true', 14771)
        first = FakeHTTPResponse(read_error=partial)
        second = FakeHTTPResponse(body=b'{"complete": true}')
        wait_patch, cooldown_patch, remaining_patch = self.retry_patches(client)

        with mock.patch.object(cc, "urlopen", side_effect=[first, second]) as opened, \
                wait_patch, cooldown_patch, remaining_patch:
            result = client._post_json("/v1/chat/completions", {"messages": []})

        self.assertEqual(result, {"complete": True})
        self.assertEqual(opened.call_count, 2)

    def test_stream_retries_when_declared_body_ends_before_any_line_is_emitted(self):
        client = self.client()
        first = FakeHTTPResponse(lines=[b""], length=12)
        second = FakeHTTPResponse(lines=[b'data: {"ok":true}\n', b""], length=None)
        wait_patch, cooldown_patch, remaining_patch = self.retry_patches(client)

        with mock.patch.object(cc, "urlopen", side_effect=[first, second]) as opened, \
                wait_patch, cooldown_patch, remaining_patch:
            lines = list(client._iter_response_lines_url_with_retries(
                "http://model.test/v1/chat/completions",
                {"stream": True},
                max_attempts=1,
            ))

        self.assertEqual(lines, ['data: {"ok":true}\n'])
        self.assertEqual(opened.call_count, 2)

    def test_stream_never_retries_after_a_line_has_been_emitted(self):
        client = self.client()
        response = FakeHTTPResponse(lines=[
            b'data: {"delta":"first"}\n',
            IncompleteRead(b"", 20),
        ])
        wait_patch, cooldown_patch, remaining_patch = self.retry_patches(client)

        with mock.patch.object(cc, "urlopen", return_value=response) as opened, \
                wait_patch, cooldown_patch, remaining_patch:
            stream = client._iter_response_lines_url_with_retries(
                "http://model.test/v1/chat/completions",
                {"stream": True},
                max_attempts=2,
            )
            self.assertEqual(next(stream), 'data: {"delta":"first"}\n')
            with self.assertRaises(cc.OllamaError) as caught:
                next(stream)

        self.assertEqual(opened.call_count, 1)
        self.assertFalse(caught.exception.retryable)
        self.assertTrue(caught.exception.transient)
        self.assertTrue(caught.exception.stream_emitted)
        self.assertIn("IncompleteRead", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
