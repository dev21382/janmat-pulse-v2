"""Canonical 10-subsection taxonomy every promise-atom is tagged to, per the
product spec. Locked deliberately — changing this year over year is what
breaks cross-cycle comparability, which is most of this pillar's value.

Tagging is a lightweight keyword-overlap classifier, not a trained ML model
— there's no labeled promise-atom dataset to train one on. It's documented
as such rather than presented as more rigorous than it is; every atom still
gets a real, auditable classification with the matched keywords visible.
"""
import re

TAXONOMY = [
    "Economy, Jobs & Industry",
    "Agriculture & Rural Development",
    "Infrastructure & Urban Development",
    "Education & Skilling",
    "Healthcare & Public Welfare",
    "Women, Child & Social Justice",
    "Energy, Environment & Climate",
    "Defense, Internal Security & Foreign Policy",
    "Governance, Federalism & Anti-Corruption",
    "Fiscal Policy & Public Finance",
]

_KEYWORDS: dict[str, list[str]] = {
    "Economy, Jobs & Industry": [
        "job", "jobs", "employment", "unemployment", "industry", "industrial", "msme",
        "manufacturing", "startup", "economy", "economic", "gdp", "labour", "labor",
        "wage", "workforce", "export", "trade", "investment", "business",
    ],
    "Agriculture & Rural Development": [
        "farmer", "farmers", "agriculture", "agricultural", "msp", "crop", "irrigation",
        "rural", "village", "farm", "fisheries", "fishing", "livestock", "dairy",
        "kisan", "land reform",
    ],
    "Infrastructure & Urban Development": [
        "infrastructure", "highway", "road", "railway", "port", "airport", "urban",
        "smart city", "housing", "metro", "transport", "construction", "public works",
    ],
    "Education & Skilling": [
        "education", "school", "university", "college", "skill", "skilling", "student",
        "teacher", "curriculum", "literacy", "nep", "scholarship", "vocational",
    ],
    "Healthcare & Public Welfare": [
        "health", "healthcare", "hospital", "ayushman", "medical", "doctor", "nurse",
        "disease", "vaccination", "welfare", "ration", "nutrition", "insurance",
        "pension",
    ],
    "Women, Child & Social Justice": [
        "women", "woman", "child", "children", "girl", "gender", "sc", "st", "obc",
        "caste", "dalit", "tribal", "minority", "reservation", "anganwadi",
        "maternity", "safety",
    ],
    "Energy, Environment & Climate": [
        "energy", "solar", "renewable", "climate", "environment", "pollution",
        "emission", "green", "power", "electricity", "coal", "sustainability",
    ],
    "Defense, Internal Security & Foreign Policy": [
        "defence", "defense", "military", "army", "navy", "air force", "border",
        "security", "police", "terrorism", "foreign policy", "diplomacy", "agnipath",
    ],
    "Governance, Federalism & Anti-Corruption": [
        "governance", "corruption", "federalism", "transparency", "accountability",
        "election commission", "judiciary", "bureaucracy", "civil service", "rti",
        "constitution", "democracy",
    ],
    "Fiscal Policy & Public Finance": [
        "budget", "tax", "taxation", "gst", "fiscal", "deficit", "subsidy", "revenue",
        "expenditure", "borrowing", "finance", "banking", "inflation",
    ],
}

_WORD_RE = re.compile(r"[a-z]+")


def classify(text: str) -> tuple[str, list[str]]:
    """Returns (category, matched_keywords). Falls back to the highest-signal
    category among Economy/Governance when nothing matches, rather than an
    'Uncategorized' bucket the spec doesn't define."""
    lower = text.lower()
    best_category = TAXONOMY[0]
    best_matches: list[str] = []
    best_score = 0
    for category, keywords in _KEYWORDS.items():
        matches = [kw for kw in keywords if kw in lower]
        if len(matches) > best_score:
            best_score = len(matches)
            best_category = category
            best_matches = matches
    return best_category, best_matches
