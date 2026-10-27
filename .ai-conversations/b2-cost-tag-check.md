# B2 Cost-Tag Check — AI Conversation Summary

This file summarizes the cost-tag checker discussion and verification. It is not a verbatim transcript of the original conversation.## User prompt

The user provided the original `scripts/cost_tag_check.py` stub and its requirements:
- Check resources being created or changed.
- Require `landlord_account_id`, not `tenant_id`.
- Skip no-op/read changes.
- Return a non-zero code for missing tags.
- Print specific resource addresses.
- Produce identical output and exit status on repeated runs.

## AI response — implementation guidance

The AI recommended parsing the Terraform plan JSON, examining `resource_changes`, checking the actions and `change.after.tags`, collecting missing-tag findings in a set, sorting findings before printing, and returning exit code `1` when findings exist or `0` otherwise.

## Actual manual run

Command:

`python scripts/cost_tag_check.py fixtures/plan.json`

Actual output:

`MISSING landlord_account_id: aws_lambda_function.mls_feed_sync`

`MISSING landlord_account_id: aws_s3_bucket.listing_media`

`FAILED: 2 resource(s) missing landlord_account_id`

The user then ran the checker a second time. The same findings appeared in the same order, and `$LASTEXITCODE` was `1` after each run.

## Actual test results

The user ran `python -m pytest -v tests/test_cost_tag_check.py`. All three tests passed.

The user also ran `python -m pytest -v`. All five tests passed.
