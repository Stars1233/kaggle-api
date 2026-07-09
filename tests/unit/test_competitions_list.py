# coding=utf-8
import io
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

sys.path.insert(0, "../..")

from kagglesdk.competitions.types.competition_api_service import ApiCompetition, ApiListCompetitionsResponse

from kaggle.api.kaggle_api_extended import KaggleApi


def _make_api():
    api = KaggleApi.__new__(KaggleApi)
    api.already_printed_version_warning = True
    return api


def _make_competition(user_rank=784, user_has_entered=True):
    competition = ApiCompetition()
    competition.ref = "https://www.kaggle.com/competitions/example-comp"
    competition.deadline = datetime(2026, 8, 1, 0, 0, 0)
    competition.category = "Playground"
    competition.reward = "Swag"
    competition.team_count = 1200
    competition.user_has_entered = user_has_entered
    competition.user_rank = user_rank
    return competition


class TestCompetitionsList(unittest.TestCase):
    """Tests for competitions_list_cli userRank output."""

    def setUp(self):
        self.api = _make_api()

    def test_competition_fields_includes_user_rank(self):
        self.assertIn("userRank", KaggleApi.competition_fields)

    @patch.object(KaggleApi, "competitions_list")
    def test_competitions_list_cli_csv_includes_user_rank(self, mock_list):
        response = ApiListCompetitionsResponse()
        response.competitions = [_make_competition(user_rank=784)]
        mock_list.return_value = response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.api.competitions_list_cli(group="entered", csv_display=True)

        output = mock_stdout.getvalue()
        self.assertIn("userRank", output)
        self.assertIn("784", output)

    @patch.object(KaggleApi, "competitions_list")
    def test_competitions_list_cli_csv_shows_zero_rank(self, mock_list):
        response = ApiListCompetitionsResponse()
        response.competitions = [_make_competition(user_rank=0, user_has_entered=True)]
        mock_list.return_value = response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.api.competitions_list_cli(group="entered", csv_display=True)

        output = mock_stdout.getvalue()
        self.assertIn("userRank", output)
        self.assertIn(",0", output.splitlines()[-1])

    @patch.object(KaggleApi, "print_results")
    @patch.object(KaggleApi, "competitions_list")
    def test_competitions_list_cli_passes_user_rank_to_print_results(self, mock_list, mock_print_results):
        response = ApiListCompetitionsResponse()
        response.competitions = [_make_competition()]
        mock_list.return_value = response

        self.api.competitions_list_cli(group="entered")

        mock_print_results.assert_called_once()
        fields = mock_print_results.call_args[0][1]
        self.assertEqual(fields, KaggleApi.competition_fields)
        self.assertIn("userRank", fields)

    @patch.object(KaggleApi, "competitions_list")
    def test_competitions_list_cli_no_results(self, mock_list):
        response = ApiListCompetitionsResponse()
        response.competitions = []
        mock_list.return_value = response

        with patch("builtins.print") as mock_print:
            self.api.competitions_list_cli(group="entered")

        mock_print.assert_called_once_with("No competitions found")


if __name__ == "__main__":
    unittest.main()
