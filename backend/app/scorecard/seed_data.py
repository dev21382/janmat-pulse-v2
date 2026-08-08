"""Promise-to-Performance Scorecard — seed dataset.

This is a small, hand-curated set of real, independently sourced entries
demonstrating the scorecard methodology end to end. It is explicitly NOT a
live PFMS/CAG/budget ingestion pipeline — building that for real (parsing
indiabudget.gov.in, linking PFMS scheme codes, ingesting CAG performance
audits) is a substantial data-engineering project on its own, and faking the
numbers instead would be actively harmful for a product whose entire premise
is trustworthy government-delivery data. Every figure below is cited to a
government or CAG source; anything not found in a citable primary source is
left null rather than estimated.

Structural note on "equal treatment": every entry here is a scheme run by
the currently governing party (BJP/NDA), because a Promise-to-Performance
scorecard can only score delivery against promises a party had the power to
implement. Opposition parties' manifesto promises for this cycle have no
delivery history yet — that's a structural fact about incumbency, not a
methodology bias, and the same rule (score only what was governed) would
apply symmetrically if the ruling party changed.
"""

SCORECARD_ENTRIES = [
    {
        "id": "pmay-urban-housing",
        "party_id": "bjp",
        "scheme_name": "Pradhan Mantri Awas Yojana – Urban (PMAY-U)",
        "promise_summary": "“Housing for All” (urban) — complete all sanctioned houses",
        "taxonomy_category": "Infrastructure & Urban Development",
        "target_value": 12_269_000,
        "target_unit": "houses sanctioned (as of 31 Mar 2022)",
        "achieved_value": 6_200_000,
        "achieved_unit": "houses completed",
        "delivery_index": round(6_200_000 / 12_269_000, 3),
        "allocation_ratio": None,
        "utilization_rate": None,
        "status": "Goalpost Moved",
        "status_note": (
            "Original mission period ended 2022; completion deadline for already-sanctioned houses "
            "was extended to 31 Dec 2024, then again to 31 Dec 2025, while roughly half of sanctioned "
            "houses remained incomplete at the time of the first extension."
        ),
        "sources": [
            {
                "label": "PIB — Cabinet approves continuation of PMAY-U to Dec 2024",
                "url": "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1850679",
            },
        ],
        "last_updated": "2024-02",
    },
    {
        "id": "pmay-gramin-housing",
        "party_id": "bjp",
        "scheme_name": "Pradhan Mantri Awas Yojana – Gramin (PMAY-G)",
        "promise_summary": "“Housing for All” (rural) by 2022",
        "taxonomy_category": "Infrastructure & Urban Development",
        "target_value": 29_400_000,
        "target_unit": "houses sanctioned",
        "achieved_value": 25_500_000,
        "achieved_unit": "houses completed (as of 1 Feb 2024)",
        "delivery_index": round(25_500_000 / 29_400_000, 3),
        "allocation_ratio": None,
        "utilization_rate": None,
        "status": "Goalpost Moved",
        "status_note": (
            "Original 2022 completion target extended to March 2024. Completion rate (~87%) is "
            "substantially higher than the urban component of the same overall promise."
        ),
        "sources": [
            {"label": "IndiaSpend — Pradhan Mantri Awas Yojana Gramin tracker", "url": "https://www.indiaspend.com/pradhan-mantri-awas-yojana-gramin"},
        ],
        "last_updated": "2024-02",
    },
    {
        "id": "pm-kisan-income-support",
        "party_id": "bjp",
        "scheme_name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "promise_summary": "Guaranteed minimum income support to every eligible farmer family",
        "taxonomy_category": "Agriculture & Rural Development",
        "target_value": None,
        "target_unit": None,
        "achieved_value": None,
        "achieved_unit": None,
        "delivery_index": None,
        "allocation_ratio": None,
        "utilization_rate": None,
        "narrative_metric": "Over ₹4.09 lakh crore disbursed across 21 installments since the scheme's 2019 launch",
        "status": "Fulfilled",
        "status_note": (
            "PM-KISAN is an entitlement scheme with no fixed physical/financial target by design "
            "(every eligible farmer family qualifies), so Allocation Ratio and Delivery Index don't "
            "apply the way they do for a target-based scheme like PMAY — shown as a continuity metric "
            "instead of forcing a ratio that isn't meaningful here."
        ),
        "sources": [
            {"label": "PIB — PM-KISAN disbursement figures", "url": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2090993"},
        ],
        "last_updated": "2026-02",
    },
    {
        "id": "ayushman-bharat-pmjay",
        "party_id": "bjp",
        "scheme_name": "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PMJAY)",
        "promise_summary": "Universal health coverage — ₹5 lakh/family/year hospitalisation cover",
        "taxonomy_category": "Healthcare & Public Welfare",
        "target_value": None,
        "target_unit": None,
        "achieved_value": None,
        "achieved_unit": None,
        "delivery_index": None,
        "allocation_ratio": None,
        "utilization_rate": None,
        "narrative_metric": "Budget allocation raised from ₹6,800 cr (FY24) to ₹7,300 cr (FY25)",
        "status": "Not Proven",
        "status_note": (
            "No independently verified national utilization-rate figure was found for FY2024-25 at "
            "the time this entry was written — allocation alone doesn't establish delivery, and it "
            "would be false precision to compute one without a sourced actual-spend number. "
            "Separately, CAG's 2023 audit found 40.65% of a large rejected-claims sample had a match "
            "confidence score that should have qualified them for approval, and flagged inconsistent "
            "approval thresholds across states — a real, sourced implementation-quality concern "
            "distinct from the funding question."
        ),
        "sources": [
            {"label": "PRS Legislative Research — Demand for Grants 2024-25, Health & Family Welfare", "url": "https://prsindia.org/budgets/parliament/demand-for-grants-2024-25-analysis-health-and-family-welfare"},
        ],
        "last_updated": "2024-07",
    },
]

STATUS_OPTIONS = [
    "Fulfilled",
    "Partially Fulfilled",
    "In Progress",
    "Not Started",
    "Goalpost Moved",
    "Not Proven",
]
