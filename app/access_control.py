"""
B2, part 1 — implement can_access_screening_report().

Read README.md's domain model first. A ScreeningReport belongs to a Tenant, a Tenant belongs to
a Property, and a Property belongs to a LandlordAccount. A PropertyManager is scoped to exactly
one LandlordAccount.

A PropertyManager may view a ScreeningReport only if that report's tenant lives in a property
under the PropertyManager's own landlord account.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant



def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Allow access only when the report's tenant belongs to a property
    under the actor's landlord account. Fail closed if records are missing.
    """
    tenant = next(
        (t for t in tenants if t.id == report.tenant_id),
        None,
    )
    if tenant is None:
        return False

    prop = next(
        (p for p in properties if p.id == tenant.property_id),
        None,
    )
    if prop is None:
        return False

    return prop.landlord_account_id == actor.landlord_account_id
