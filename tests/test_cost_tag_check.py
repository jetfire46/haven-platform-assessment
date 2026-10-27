"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export).
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

Use a test double / your own in-memory plan dict where you don't need a real file on disk —
you don't need to shell out to the real script for every case.
"""

import json

from scripts.cost_tag_check import check_plan


def test_fixture_flags_resources_missing_landlord_tag(capsys):
    result = check_plan("fixtures/plan.json")
    output = capsys.readouterr().out

    assert result == 1
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output
    assert "aws_s3_bucket.landlord_media[0]" not in output
    assert "aws_lambda_function.screening_report_export" not in output


def test_repeated_runs_produce_identical_results(capsys):
    first_result = check_plan("fixtures/plan.json")
    first_output = capsys.readouterr().out

    second_result = check_plan("fixtures/plan.json")
    second_output = capsys.readouterr().out

    assert first_result == second_result
    assert first_output == second_output


def test_noop_and_read_resources_are_skipped(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.unchanged",
                "change": {
                    "actions": ["no-op"],
                    "after": {"tags": {}},
                },
            },
            {
                "address": "aws_s3_bucket.read_only",
                "change": {
                    "actions": ["read"],
                    "after": {"tags": {}},
                },
            },
        ]
    }

    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    result = check_plan(str(plan_path))
    output = capsys.readouterr().out

    assert result == 0
    assert "PASSED" in output
    assert "unchanged" not in output
    assert "read_only" not in output
