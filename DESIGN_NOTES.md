# Design Notes

## B2 — idempotency key

The idempotency key is the resource address, such as `aws_s3_bucket.listing_media`. The checker stores reported addresses in a set, which prevents duplicate findings for the same resource within one run. Findings are sorted before printing to ensure deterministic output.

The checker is stateless between runs. It recalculates findings from the plan file each time rather than storing previously checked plans. Running it twice against the same plan produces identical output and the same exit code, as verified by the repeated-run test.

## Any other decision with a non-obvious alternative

**Access control:** Authorization is based on `landlord_account_id`, not `tenant_id`. The function resolves the report's tenant and property, compares the property's landlord account with the manager's landlord account, and denies access if either record is missing.

**Terraform resource identity:** Replaced positional `count` with `for_each` keyed by landlord account ID. Four `moved` blocks preserve the existing resource addresses in state, avoiding unnecessary bucket replacements and destruction.

**Cost-tag validation:** The checker requires `landlord_account_id` on resources being created or updated. It skips no-op, read-only, and delete-only changes, and sorts findings to keep output deterministic.

**Lifecycle costs:** Deleting an object before S3 Glacier Flexible Retrieval's 90-day minimum storage duration can incur an early-deletion charge. The deletion SLA takes precedence over avoiding this fee, so archival eligibility and storage class should reflect actual retention and deletion patterns.