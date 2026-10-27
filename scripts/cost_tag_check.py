
"""Validate landlord-account cost tags in a Terraform plan."""
import json
import sys

REQUIRED_TAG = "landlord_account_id"


def check_plan(plan_path: str) -> int:
    """
    Return 0 if all created or updated resources have the required tag.
    Return 1 if any resource is missing it.
    """
    with open(plan_path, "r", encoding="utf-8") as plan_file:
        plan = json.load(plan_file)

    findings = set()

    for resource in plan.get("resource_changes", []):
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Skip no-op, read-only, and delete-only changes.
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after")
        if after is None:
            continue

        tags = after.get("tags") or {}
        if not isinstance(tags, dict) or not tags.get(REQUIRED_TAG):
            address = resource.get("address", "<unknown address>")
            findings.add(address)

    # Stable ordering and unique addresses ensure deterministic output.
    if findings:
        for address in sorted(findings):
            print(f"MISSING {REQUIRED_TAG}: {address}")
        print(f"FAILED: {len(findings)} resource(s) missing {REQUIRED_TAG}")
        return 1

    print(f"PASSED: all created or updated resources have {REQUIRED_TAG}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/cost_tag_check.py <plan.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))
