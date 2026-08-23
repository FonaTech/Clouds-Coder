import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class _Response:
    def __init__(self, body: bytes):
        self.body = body
        self.headers = {"Content-Type": "application/rss+xml; charset=utf-8"}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit=-1):
        return self.body


class PublicWebDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.engine = cc.AgentWebSearchEngine(Path(self.tmp.name), obey_robots=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_public_rss_discovery_requires_no_api_credentials(self):
        feed = b"""<?xml version='1.0' encoding='utf-8'?>
        <rss><channel><item><title>Python release</title>
        <link>https://docs.python.org/3/whatsnew/3.14.html</link>
        <description>Official release notes</description></item></channel></rss>"""
        with (
            mock.patch.object(
                self.engine,
                "_validate_url",
                side_effect=lambda value: (True, value, "ok"),
            ),
            mock.patch.object(cc, "urlopen", return_value=_Response(feed)),
        ):
            payload = self.engine._public_search_feed_candidates(
                "Python 3.14 release", 5
            )
        self.assertEqual(payload["provider"], "bing-rss")
        self.assertEqual(payload["error"], "")
        self.assertEqual(
            payload["results"][0]["url"], "https://docs.python.org/3/whatsnew/3.14.html"
        )

    def test_cold_start_uses_public_results_without_sitemap_probes(self):
        page = {
            "ok": True,
            "url": "https://example.com/result",
            "title": "Result",
            "domain": "example.com",
            "source_type": "public_search_feed",
            "depth": 0,
            "description": "",
            "text": "target evidence",
            "links": [],
        }
        with (
            mock.patch.object(
                self.engine,
                "_public_search_feed_candidates",
                return_value={
                    "provider": "bing-rss",
                    "query": "target evidence",
                    "results": [{"url": page["url"], "title": page["title"]}],
                    "error": "",
                },
            ),
            mock.patch.object(self.engine, "_discover_sitemaps_and_feeds") as sitemap,
            mock.patch.object(self.engine, "fetch", return_value=page),
        ):
            payload = self.engine.discover("target evidence", max_pages=2, depth=0)
        self.assertEqual(payload["fetched"], 1)
        self.assertEqual(payload["pages"][0]["source_type"], "public_search_feed")
        self.assertEqual(payload["public_discovery"]["provider"], "bing-rss")
        sitemap.assert_not_called()


if __name__ == "__main__":
    unittest.main()
