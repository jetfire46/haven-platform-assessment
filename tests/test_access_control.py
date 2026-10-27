"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""

from app.access_control import can_access_screening_report


def test_manager_cannot_access_other_landlord_report(
    property_managers, properties, tenants, screening_reports
):
    manager = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-002")

    assert can_access_screening_report(
        manager,
        report,
        properties=properties,
        tenants=tenants,
    ) is False


def test_manager_can_access_own_landlord_report(
    property_managers, properties, tenants, screening_reports
):
    manager = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-001")

    assert can_access_screening_report(
        manager,
        report,
        properties=properties,
        tenants=tenants,
    ) is True
