# coding=utf-8
"""Regression tests for KaggleApi._parse_duration (auth print-access-token --expiration)."""

import pytest
from dateutil.relativedelta import relativedelta


@pytest.mark.parametrize(
    "duration_str, expected",
    [
        ("30s", relativedelta(seconds=30)),
        ("5m", relativedelta(minutes=5)),
        ("6h", relativedelta(hours=6)),
        ("2d", relativedelta(days=2)),
        ("2w", relativedelta(weeks=2)),
        ("1h", relativedelta(hours=1)),
    ],
)
def test_parse_duration_valid_formats(api, duration_str, expected):
    result = api._parse_duration(duration_str)
    assert isinstance(result, relativedelta)
    assert result == expected


def test_parse_duration_normalizes_weeks_to_days(api):
    # relativedelta stores weeks as days; 2w == 14 days.
    assert api._parse_duration("2w") == relativedelta(days=14)


@pytest.mark.parametrize(
    "duration_str",
    [
        "",  # empty
        "6",  # missing unit
        "h",  # missing value
        "6x",  # unknown unit
        "6H",  # units are case-sensitive
        "2:30",  # colon format is not supported
        "2h30s",  # compound format is not supported
        "abc",  # not numeric
        "-5m",  # non-positive value
        "0h",  # zero is not a valid duration
        "1.5h",  # non-integer value
    ],
)
def test_parse_duration_invalid_formats_raise_value_error(api, duration_str):
    with pytest.raises(ValueError) as exc_info:
        api._parse_duration(duration_str)
    # Users must get the friendly guidance, never a raw TypeError traceback.
    assert "Invalid duration format" in str(exc_info.value)


def test_parse_duration_does_not_raise_type_error(api):
    # The original bug passed single-letter kwargs to relativedelta, raising an
    # uncaught TypeError. Ensure malformed input never surfaces a TypeError.
    for bad in ["6h", "2d", "30s", "5m", "2w", "6x", ""]:
        try:
            api._parse_duration(bad)
        except ValueError:
            pass  # acceptable, friendly error
        except TypeError as exc:  # pragma: no cover - regression guard
            pytest.fail(f"_parse_duration({bad!r}) raised TypeError: {exc}")
