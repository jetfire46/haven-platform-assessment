# Terminal Log

This log records the actual setup, validation, test, and cost-tag-check results observed during the assessment.

## 1. Environment setup

- Operating system: Windows 10 Pro, 64-bit
- Python: 3.13.17
- pytest: 9.1.1
- Terraform: 1.17.0
- Git: 2.56.0.windows.3
- Terraform AWS provider: hashicorp/aws v5.100.0

Commands run:

```powershell
python --version
python -m pytest --version
terraform version
git --version
terraform -chdir=terraform init
```

Terraform initialization succeeded and downloaded the AWS provider.

## 2. B0 — Reproduce the count issue

With `la-002` removed from the configured landlord list, I ran:

```powershell
terraform -chdir=terraform plan -refresh=false
```

Observed result:

```text
Plan: 4 to add, 0 to change, 3 to destroy.
```

The plan proposed replacing the buckets at indexes `[1]` and `[2]` and destroying index `[3]`, demonstrating the risk of positional resource identity.

## 3. B0 — Validate the remediation

After changing the resource to use `for_each` keyed by landlord account ID and adding four `moved` blocks, I restored the original four-account list and ran:

```powershell
terraform -chdir=terraform validate
terraform -chdir=terraform plan -refresh=false
```

Validation succeeded. The plan recognized all four address moves and reported:

```text
Plan: 2 to add, 0 to change, 0 to destroy.
```

The two additions were the separate listing-media bucket and lifecycle configuration. No landlord bucket replacement or destruction was proposed.

The lifecycle-rule warning was subsequently resolved by adding an explicit empty filter. A later validation returned:

```text
Success! The configuration is valid.
```

## 4. B2 — Access-control tests

Command:

```powershell
python -m pytest -v tests/test_access_control.py
```

Observed result:

```text
2 passed in 0.10s
```

The cross-landlord access test and same-landlord access test both passed.

## 5. B2 — Cost-tag tests

Command:

```powershell
python -m pytest -v tests/test_cost_tag_check.py
```

Observed result:

```text
3 passed in 0.24s
```

The fixture-check, repeated-run idempotency, and no-op/read skipping tests all passed.

## 6. B2 — Full test suite

Command:

```powershell
python -m pytest -v
```

Observed result:

```text
5 passed in 0.33s
```

All five tests passed.

## 7. B2 — Cost-tag checker, first run

Command:

```powershell
python scripts/cost_tag_check.py fixtures/plan.json
```

Actual output:

```text
MISSING landlord_account_id: aws_lambda_function.mls_feed_sync
MISSING landlord_account_id: aws_s3_bucket.listing_media
FAILED: 2 resource(s) missing landlord_account_id
```

The following command returned exit code `1`:

```powershell
$LASTEXITCODE
```

This was expected because the supplied fixture deliberately contains two resources missing `landlord_account_id`.

## 8. B2 — Cost-tag checker, second run

I ran the same checker command again:

```powershell
python scripts/cost_tag_check.py fixtures/plan.json
```

The same two findings appeared in the same order, and the final result was:

```text
FAILED: 2 resource(s) missing landlord_account_id
```

The subsequent `$LASTEXITCODE` was `1` again. This confirmed identical output and exit status for repeated runs against the same plan.

## 9. Safety

Terraform plans and validation were used to inspect the infrastructure changes. No `terraform apply` or `terraform destroy` was performed.