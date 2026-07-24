# coding=utf-8
import io
import json
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, "../..")

from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.search.types.search_api_service import (
    ApiListType,
    ApiOrganizationCard,
    ApiUserAvatar,
    ListEntitiesDocument,
)
from kagglesdk.search.types.search_enums import DocumentType, ListSearchContentOrderBy


def _avatar(user_name):
    avatar = ApiUserAvatar()
    avatar.user_name = user_name
    return avatar


def _org(slug):
    org = ApiOrganizationCard()
    org.slug = slug
    return org


def _doc(document_type, title="", slug="", user=None, org=None, votes=0, doc_id=0):
    document = ListEntitiesDocument()
    document.document_type = document_type
    document.title = title
    document.slug = slug
    document.votes = votes
    document.id = doc_id
    if user is not None:
        document.owner_user = _avatar(user)
    if org is not None:
        document.owner_organization = _org(org)
    return document


def _response(documents=None, next_page_token=""):
    response = MagicMock()
    response.documents = documents if documents is not None else []
    response.next_page_token = next_page_token
    return response


class TestSearchApi(unittest.TestCase):
    """Tests for the request-building behavior of KaggleApi.search."""

    def setUp(self):
        self.api = KaggleApi.__new__(KaggleApi)

    def _patch_client(self, response):
        captured = {}
        mock_kaggle = MagicMock()

        def _list_entities(request):
            captured["request"] = request
            return response

        mock_kaggle.search.search_api_client.list_entities.side_effect = _list_entities
        patcher = patch.object(KaggleApi, "build_kaggle_client")
        mock_client = patcher.start()
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_kaggle)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)
        self.addCleanup(patcher.stop)
        captured["client"] = mock_client
        return captured

    def test_search_builds_request(self):
        captured = self._patch_client(_response())
        self.api.search("weather")
        request = captured["request"]
        self.assertEqual(request.filters.query, "weather")
        self.assertEqual(request.page_size, 20)
        self.assertEqual(
            request.canonical_order_by,
            ListSearchContentOrderBy.LIST_SEARCH_CONTENT_ORDER_BY_UNSPECIFIED,
        )

    def test_search_defaults_to_cli_supported_types(self):
        # When no --type is given, the CLI restricts the pool to the supported
        # content types rather than sending an empty filter (which would let the
        # backend include unrenderable types like comments and blogs).
        captured = self._patch_client(_response())
        self.api.search("weather")
        self.assertEqual(
            list(captured["request"].filters.document_types),
            [
                DocumentType.COMPETITION,
                DocumentType.DATASET,
                DocumentType.KERNEL,
                DocumentType.MODEL,
                DocumentType.USER,
                DocumentType.TOPIC,
                DocumentType.BENCHMARK,
            ],
        )

    def test_search_uses_authenticated_client(self):
        captured = self._patch_client(_response())
        self.api.search("weather")
        captured["client"].assert_called_once()

    def test_search_strips_query(self):
        captured = self._patch_client(_response())
        self.api.search("  weather  ")
        self.assertEqual(captured["request"].filters.query, "weather")

    def test_search_multiple_document_types(self):
        captured = self._patch_client(_response())
        self.api.search("llm", document_types=["dataset", "model"])
        self.assertEqual(
            list(captured["request"].filters.document_types),
            [DocumentType.DATASET, DocumentType.MODEL],
        )

    def test_search_notebook_alias_maps_to_kernel_and_dedupes(self):
        captured = self._patch_client(_response())
        self.api.search("x", document_types=["notebook", "kernel", "notebooks"])
        self.assertEqual(list(captured["request"].filters.document_types), [DocumentType.KERNEL])

    def test_search_discussion_maps_to_topic(self):
        captured = self._patch_client(_response())
        self.api.search("x", document_types=["discussion"])
        self.assertEqual(list(captured["request"].filters.document_types), [DocumentType.TOPIC])

    def test_search_benchmark_type(self):
        captured = self._patch_client(_response())
        self.api.search("llm", document_types=["benchmark", "benchmarks"])
        self.assertEqual(list(captured["request"].filters.document_types), [DocumentType.BENCHMARK])

    def test_search_rejects_unsupported_backend_type(self):
        # "comment" is a real DocumentType member but is not CLI-supported; it
        # must be rejected even though lookup_enum could resolve it.
        with self.assertRaises(ValueError):
            self.api.search("x", document_types=["comment"])

    def test_search_mine_sets_list_type(self):
        captured = self._patch_client(_response())
        self.api.search("x", mine=True)
        self.assertEqual(captured["request"].filters.list_type, ApiListType.API_LIST_TYPE_YOUR_WORK)

    def test_search_sort_by_votes(self):
        captured = self._patch_client(_response())
        self.api.search("x", sort_by="votes")
        self.assertEqual(
            captured["request"].canonical_order_by,
            ListSearchContentOrderBy.LIST_SEARCH_CONTENT_ORDER_BY_VOTES,
        )

    def test_search_sort_by_camelcase_resolves_via_lookup_enum(self):
        captured = self._patch_client(_response())
        self.api.search("x", sort_by="dateCreated")
        self.assertEqual(
            captured["request"].canonical_order_by,
            ListSearchContentOrderBy.LIST_SEARCH_CONTENT_ORDER_BY_DATE_CREATED,
        )

    def test_search_sort_by_relevance_maps_to_unspecified(self):
        captured = self._patch_client(_response())
        self.api.search("x", sort_by="relevance")
        self.assertEqual(
            captured["request"].canonical_order_by,
            ListSearchContentOrderBy.LIST_SEARCH_CONTENT_ORDER_BY_UNSPECIFIED,
        )

    def test_search_pagination(self):
        captured = self._patch_client(_response())
        self.api.search("x", page_size=50, page_token="tok")
        self.assertEqual(captured["request"].page_size, 50)
        self.assertEqual(captured["request"].page_token, "tok")

    def test_search_page_size_capped_at_100(self):
        captured = self._patch_client(_response())
        self.api.search("x", page_size=500)
        self.assertEqual(captured["request"].page_size, 100)

    def test_search_empty_query_raises(self):
        with self.assertRaises(ValueError):
            self.api.search("   ")

    def test_search_none_query_raises(self):
        with self.assertRaises(ValueError):
            self.api.search(None)

    def test_search_invalid_document_type_raises(self):
        with self.assertRaises(ValueError):
            self.api.search("x", document_types=["frobnicate"])

    def test_search_invalid_sort_by_raises(self):
        with self.assertRaises(ValueError):
            self.api.search("x", sort_by="nonsense")

    def test_search_invalid_page_size_raises(self):
        with self.assertRaises(ValueError):
            self.api.search("x", page_size=0)

    def test_search_backend_failure_propagates(self):
        patcher = patch.object(KaggleApi, "build_kaggle_client")
        mock_client = patcher.start()
        self.addCleanup(patcher.stop)
        mock_kaggle = MagicMock()
        mock_kaggle.search.search_api_client.list_entities.side_effect = RuntimeError("boom")
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_kaggle)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)
        with self.assertRaises(RuntimeError):
            self.api.search("x")


class TestSearchRenderer(unittest.TestCase):
    """Tests for the mixed-entity row normalization."""

    def setUp(self):
        self.api = KaggleApi.__new__(KaggleApi)

    def test_dataset_ref_is_owner_slash_slug(self):
        row = self.api._search_document_to_row(
            _doc(DocumentType.DATASET, "Wine Reviews", "wine-reviews", user="zynicide", votes=10)
        )
        self.assertEqual(row.type, "dataset")
        self.assertEqual(row.ref, "zynicide/wine-reviews")
        self.assertEqual(row.owner, "zynicide")
        self.assertEqual(row.title, "Wine Reviews")
        self.assertEqual(row.votes, 10)

    def test_competition_ref_is_slug_only(self):
        row = self.api._search_document_to_row(_doc(DocumentType.COMPETITION, "Titanic", "titanic", org="kaggle"))
        self.assertEqual(row.type, "competition")
        self.assertEqual(row.ref, "titanic")
        self.assertEqual(row.owner, "kaggle")

    def test_kernel_labelled_notebook(self):
        row = self.api._search_document_to_row(_doc(DocumentType.KERNEL, "EDA", "titanic-eda", user="startupsci"))
        self.assertEqual(row.type, "notebook")
        self.assertEqual(row.ref, "startupsci/titanic-eda")

    def test_model_ref_uses_organization_owner(self):
        row = self.api._search_document_to_row(_doc(DocumentType.MODEL, "Gemma", "gemma", org="google"))
        self.assertEqual(row.type, "model")
        self.assertEqual(row.ref, "google/gemma")
        self.assertEqual(row.owner, "google")

    def test_user_owner_is_dash(self):
        row = self.api._search_document_to_row(_doc(DocumentType.USER, "Dan Becker", "dansbecker"))
        self.assertEqual(row.type, "user")
        self.assertEqual(row.ref, "dansbecker")
        self.assertEqual(row.owner, "-")

    def test_discussion_falls_back_to_id(self):
        row = self.api._search_document_to_row(_doc(DocumentType.TOPIC, "Welcome", "", doc_id=42))
        self.assertEqual(row.type, "discussion")
        self.assertEqual(row.ref, "42")

    def test_benchmark_ref_is_owner_slash_slug(self):
        row = self.api._search_document_to_row(
            _doc(DocumentType.BENCHMARK, "LLMs understand images", "llms-understand-images", user="gpreda", votes=7)
        )
        self.assertEqual(row.type, "benchmark")
        self.assertEqual(row.ref, "gpreda/llms-understand-images")
        self.assertEqual(row.owner, "gpreda")
        self.assertEqual(row.votes, 7)


class TestSearchCli(unittest.TestCase):
    """Tests for the output formatting of KaggleApi.search_cli."""

    def setUp(self):
        self.api = KaggleApi.__new__(KaggleApi)

    def _capture(self, **kwargs):
        captured = io.StringIO()
        sys.stdout = captured
        try:
            self.api.search_cli(**kwargs)
        finally:
            sys.stdout = sys.__stdout__
        return captured.getvalue()

    @patch.object(KaggleApi, "search")
    def test_search_cli_table(self, mock_search):
        mock_search.return_value = _response(
            documents=[
                _doc(DocumentType.DATASET, "Wine Reviews", "wine-reviews", user="zynicide", votes=10),
                _doc(DocumentType.COMPETITION, "Titanic", "titanic", org="kaggle"),
            ]
        )
        out = self._capture(query="x")
        self.assertIn("dataset", out)
        self.assertIn("zynicide/wine-reviews", out)
        self.assertIn("competition", out)
        self.assertIn("titanic", out)

    @patch.object(KaggleApi, "search")
    def test_search_cli_no_matches(self, mock_search):
        mock_search.return_value = _response(documents=[])
        self.assertIn("No matches found", self._capture(query="x"))

    @patch.object(KaggleApi, "search")
    def test_search_cli_prints_next_page_token(self, mock_search):
        mock_search.return_value = _response(
            documents=[_doc(DocumentType.DATASET, "D", "d", user="u")],
            next_page_token="NEXT",
        )
        self.assertIn("Next Page Token = NEXT", self._capture(query="x"))

    @patch.object(KaggleApi, "search")
    def test_search_cli_csv(self, mock_search):
        mock_search.return_value = _response(
            documents=[_doc(DocumentType.DATASET, "Wine", "wine-reviews", user="zynicide", votes=10)]
        )
        lines = [line for line in self._capture(query="x", csv_display=True).splitlines() if line]
        self.assertEqual(lines[0], "type,ref,title,owner,votes")
        self.assertTrue(any("zynicide/wine-reviews" in line for line in lines))

    @patch.object(KaggleApi, "search")
    def test_search_cli_json(self, mock_search):
        mock_search.return_value = _response(
            documents=[_doc(DocumentType.MODEL, "Gemma", "gemma", org="google", votes=5)]
        )
        data = json.loads(self._capture(query="x", output_format="json"))
        self.assertEqual(data[0]["type"], "model")
        self.assertEqual(data[0]["ref"], "google/gemma")
        self.assertEqual(data[0]["owner"], "google")
        self.assertEqual(data[0]["votes"], 5)

    @patch.object(KaggleApi, "search")
    def test_search_cli_json_projection(self, mock_search):
        mock_search.return_value = _response(
            documents=[_doc(DocumentType.MODEL, "Gemma", "gemma", org="google", votes=5)]
        )
        data = json.loads(self._capture(query="x", output_format="json(type,ref)"))
        self.assertEqual(list(data[0].keys()), ["type", "ref"])
        self.assertEqual(data[0]["ref"], "google/gemma")

    @patch.object(KaggleApi, "search")
    def test_search_cli_splits_document_type(self, mock_search):
        mock_search.return_value = _response(documents=[])
        self._capture(query="x", document_type="dataset,model")
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["document_types"], ["dataset", "model"])

    @patch.object(KaggleApi, "search")
    def test_search_cli_passes_arguments(self, mock_search):
        mock_search.return_value = _response(documents=[])
        self._capture(query="llm", sort_by="votes", mine=True, page_size=50, page_token="tok")
        _, kwargs = mock_search.call_args
        self.assertEqual(kwargs["query"], "llm")
        self.assertEqual(kwargs["sort_by"], "votes")
        self.assertEqual(kwargs["mine"], True)
        self.assertEqual(kwargs["page_size"], 50)
        self.assertEqual(kwargs["page_token"], "tok")


if __name__ == "__main__":
    unittest.main()
