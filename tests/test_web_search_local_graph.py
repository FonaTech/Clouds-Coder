import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class QueryLocalLinkGraphTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.engine = cc.AgentWebSearchEngine(Path(self.tmp.name), obey_robots=False)
        self.clock = 1_800_000_000.0

    def tearDown(self):
        self.tmp.cleanup()

    def add_page(
        self,
        url,
        *,
        title="Page",
        text="",
        description="",
        links=None,
        canonical_url="",
        source_type="fetch",
    ):
        self.engine._store_page(
            {
                "url": url,
                "canonical_url": canonical_url or url,
                "domain": cc.urlparse(url).hostname or "",
                "title": title,
                "description": description,
                "text": text,
                "fetched_at": self.clock,
                "status": 200,
                "content_type": "text/html",
                "source_type": source_type,
                "depth": 0,
                "metadata": {},
                "links": list(links or []),
            }
        )

    def result_for(self, results, url):
        return next(row for row in results if row["url"] == url)

    def test_independent_referring_domains_and_shared_original_source(self):
        original = "https://vendor.gov/docs/target-protocol"
        ref_a = "https://analysis-one.example.net/article"
        ref_b = "https://analysis-two.example.org/report"
        self.add_page(
            original,
            title="Target protocol specification",
            text="target protocol reference",
        )
        self.add_page(
            ref_a,
            title="Target protocol analysis one",
            text="target protocol analysis",
            links=[{"url": original, "anchor": "original specification"}],
        )
        self.add_page(
            ref_b,
            title="Target protocol analysis two",
            text="target protocol report",
            links=[{"url": original, "anchor": "source specification"}],
        )

        results, graph = self.engine._search_index_with_graph(
            "target protocol", max_results=10
        )
        target = self.result_for(results, original)
        self.assertEqual(target["source_role"], "official")
        self.assertEqual(target["link_graph"]["referring_domain_count"], 2)
        self.assertEqual(target["link_graph"]["external_referring_domain_count"], 2)
        common = next(
            row
            for row in graph["shared_original_sources"]
            if row["original_url"] == original
        )
        self.assertEqual(common["citing_page_count"], 2)
        self.assertEqual(common["independent_citing_domains"], 2)
        self.assertIn(
            original,
            self.result_for(results, ref_a)["link_graph"]["shared_original_sources"],
        )

    def test_subdomains_and_duplicate_placements_do_not_inflate_domain_authority(self):
        target = "https://source.example.org/research/result"
        self.add_page(target, title="Graph result research", text="graph result")
        repeated_links = [{"url": target, "anchor": "Graph result"}] * 3
        self.add_page(
            "https://news.publisher.example.com/one",
            title="Graph result one",
            text="graph result",
            links=repeated_links,
        )
        self.add_page(
            "https://blog.publisher.example.com/two",
            title="Graph result two",
            text="graph result",
            links=[{"url": target, "anchor": "Graph result"}],
        )

        results, graph = self.engine._search_index_with_graph(
            "graph result", max_results=10
        )
        target_row = self.result_for(results, target)
        self.assertEqual(target_row["link_graph"]["referring_domain_count"], 1)
        self.assertEqual(target_row["link_graph"]["duplicate_link_count"], 2)
        self.assertEqual(graph["signals"]["duplicate_edges"], 1)
        with self.engine._connect() as conn:
            stored = conn.execute(
                "SELECT occurrences FROM links WHERE src = ? AND dst = ?",
                ("https://news.publisher.example.com/one", target),
            ).fetchone()
        self.assertEqual(int(stored["occurrences"]), 3)

        # A refetch replaces the source snapshot; it must not accumulate
        # historical copies.
        self.add_page(
            "https://news.publisher.example.com/one",
            title="Graph result one",
            text="graph result",
            links=repeated_links,
        )
        with self.engine._connect() as conn:
            stored = conn.execute(
                "SELECT occurrences FROM links WHERE src = ? AND dst = ?",
                ("https://news.publisher.example.com/one", target),
            ).fetchone()
        self.assertEqual(int(stored["occurrences"]), 3)

    def test_reciprocal_duplicate_and_suspected_seo_links_are_flagged(self):
        page_a = "https://alpha.example.com/topic"
        page_b = "https://beta.example.net/topic"
        spam_anchor = "cheap casino backlink backlink backlink"
        self.add_page(
            page_a,
            title="Topic alpha",
            text="topic evidence",
            links=[{"url": page_b, "anchor": spam_anchor}] * 3,
        )
        self.add_page(
            page_b,
            title="Topic beta",
            text="topic evidence",
            links=[{"url": page_a, "anchor": spam_anchor}],
        )

        results, graph = self.engine._search_index_with_graph(
            "topic evidence", max_results=10
        )
        row_b = self.result_for(results, page_b)
        self.assertEqual(graph["signals"]["reciprocal_edges"], 1)
        self.assertGreaterEqual(graph["signals"]["suspected_seo_edges"], 1)
        self.assertGreaterEqual(row_b["link_graph"]["duplicate_link_count"], 2)
        self.assertGreaterEqual(row_b["link_graph"]["reciprocal_link_count"], 1)
        self.assertIn(
            "commercial_or_link_scheme_anchor",
            row_b["link_graph"]["suspected_seo_reasons"],
        )

    def test_personalized_pagerank_is_deterministic_and_normalized(self):
        urls = [f"https://domain-{index}.example/page" for index in range(4)]
        for index, url in enumerate(urls):
            self.add_page(
                url,
                title=f"Deterministic graph {index}",
                text="deterministic graph evidence",
                links=[
                    {"url": urls[(index + 1) % len(urls)], "anchor": "next evidence"}
                ],
            )
        candidates, _summary = self.engine._search_index_with_graph(
            "deterministic graph", max_results=10
        )
        first = self.engine._query_local_link_analysis(
            "deterministic graph", candidates
        )
        second = self.engine._query_local_link_analysis(
            "deterministic graph", candidates
        )
        first_scores = {
            url: row["personalized_pagerank"] for url, row in first["nodes"].items()
        }
        second_scores = {
            url: row["personalized_pagerank"] for url, row in second["nodes"].items()
        }
        self.assertEqual(first_scores, second_scores)
        self.assertAlmostEqual(sum(first_scores.values()), 1.0, places=9)
        self.assertAlmostEqual(first["summary"]["pagerank"]["score_sum"], 1.0, places=9)

    def test_source_roles_cover_primary_repost_and_aggregator(self):
        title = "A sufficiently distinctive original research paper title"
        original = "https://arxiv.org/abs/2601.12345"
        mirror = "https://mirror.example.net/copied-paper"
        aggregator = "https://links.example.com/tag/research"
        self.add_page(original, title=title, text="distinctive research paper")
        self.add_page(mirror, title=title, text="distinctive research paper")
        self.add_page(
            aggregator, title="Research links", text="distinctive research paper"
        )

        results, _graph = self.engine._search_index_with_graph(
            "distinctive research paper", max_results=10
        )
        self.assertEqual(self.result_for(results, original)["source_role"], "primary")
        self.assertEqual(self.result_for(results, mirror)["source_role"], "repost")
        self.assertEqual(
            self.result_for(results, aggregator)["source_role"], "aggregator"
        )

    def test_graph_node_and_edge_budgets_are_enforced(self):
        target = "https://target.example.org/docs/budget"
        self.add_page(target, title="Budget graph target", text="budget graph")
        for index in range(12):
            self.add_page(
                f"https://ref-{index}.example.net/page",
                title=f"Budget graph ref {index}",
                text="budget graph",
                links=[{"url": target, "anchor": "budget graph target"}],
            )
        with (
            mock.patch.object(cc, "AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES", 5),
            mock.patch.object(cc, "AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES", 4),
        ):
            _results, graph = self.engine._search_index_with_graph(
                "budget graph", max_results=30
            )
        self.assertLessEqual(graph["node_count"], 5)
        self.assertLessEqual(graph["edge_count"], 4)
        self.assertTrue(graph["budgets"]["nodes_truncated"])
        self.assertTrue(graph["budgets"]["edges_truncated"])

    def test_link_authority_cannot_override_strong_content_relevance(self):
        official = "https://agency.gov/docs/quantum-flux-protocol"
        popular = "https://popular.example.com/page"
        self.add_page(
            official,
            title="Quantum flux protocol official reference",
            description="quantum flux protocol",
            text="quantum flux protocol quantum flux protocol",
        )
        self.add_page(popular, title="Popular page", text="quantum")
        for index in range(10):
            self.add_page(
                f"https://referrer-{index}.example.net/page",
                title=f"Unrelated referrer {index}",
                text="other material",
                links=[{"url": popular, "anchor": "popular source"}],
            )

        results, graph = self.engine._search_index_with_graph(
            "quantum flux protocol", max_results=10
        )
        popular_row = self.result_for(results, popular)
        self.assertEqual(results[0]["url"], official)
        self.assertGreater(
            popular_row["link_graph"]["external_referring_domain_count"], 0
        )
        self.assertLessEqual(
            popular_row["link_authority_bonus"], popular_row["base_score"] * 0.12 + 1e-6
        )
        self.assertLessEqual(
            popular_row["link_authority_bonus"],
            cc.AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX,
        )
        self.assertEqual(
            graph["authority_policy"]["priority"],
            "content_relevance_and_source_trust_first",
        )

    def test_search_payload_exposes_local_graph_and_bounded_ranking_note(self):
        self.add_page(
            "https://docs.example.org/docs/local-graph",
            title="Local graph local graph",
            description="local graph local graph",
            text="local graph local graph local graph local graph",
        )
        payload = self.engine.search("local graph", max_results=5, max_pages=1, depth=0)
        self.assertIn("local_link_graph", payload)
        self.assertEqual(payload["local_link_graph"]["scope"], "query_local")
        self.assertIn("Personalized PageRank", payload["ranking_note"])
        self.assertIn("base_score", payload["results"][0])
        self.assertIn("link_authority_bonus", payload["results"][0])


if __name__ == "__main__":
    unittest.main()
