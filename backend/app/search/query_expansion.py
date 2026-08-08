"""Query-understanding layer for the free-text search bar (product spec A8):
expands a user's query with synonyms, common transliterations, and hashtags
before fanning out to sources, so one phrasing doesn't silently miss most of
the actual conversation (e.g. "GST" alone misses "जीएसटी").

This is a hand-curated dictionary of ~30 terms that come up constantly in
Indian political discourse, not a general translation model — real
multilingual query expansion at scale needs the IndicNLP-class models the
product spec calls for in Pillar A2, which isn't in scope here (see
ROADMAP.md). What's here is genuinely useful for the terms it covers, and
transparently limited to them.
"""
import re

EXPANSIONS: dict[str, list[str]] = {
    "gst": ["जीएसटी", "goods and services tax"],
    "msp": ["न्यूनतम समर्थन मूल्य", "minimum support price"],
    "farmer": ["किसान", "kisan", "annadata"],
    "farmers": ["किसान", "kisan", "annadata"],
    "unemployment": ["बेरोजगारी", "berozgari", "jobless"],
    "inflation": ["महंगाई", "mehngai", "price rise"],
    "caa": ["नागरिकता संशोधन कानून", "citizenship amendment act"],
    "nrc": ["राष्ट्रीय नागरिक रजिस्टर", "national register of citizens"],
    "agnipath": ["अग्निपथ", "agniveer"],
    "reservation": ["आरक्षण", "quota"],
    "corruption": ["भ्रष्टाचार", "bhrashtachar"],
    "healthcare": ["स्वास्थ्य सेवा", "ayushman bharat"],
    "education": ["शिक्षा", "nep", "national education policy"],
    "election": ["चुनाव", "lok sabha polls", "elections"],
    "evm": ["इलेक्ट्रॉनिक वोटिंग मशीन", "electronic voting machine"],
    "farm laws": ["किसान कानून", "farm bills", "kisan andolan"],
    "neet": ["नीट परीक्षा", "neet exam"],
    "budget": ["बजट", "union budget"],
    "gdp": ["सकल घरेलू उत्पाद", "economic growth"],
    "women safety": ["महिला सुरक्षा", "women security"],
    "jobs": ["रोजगार", "rozgar", "employment"],
    "poverty": ["गरीबी", "garibi"],
    "pension": ["पेंशन"],
    "electricity": ["बिजली", "power supply"],
    "water": ["पानी", "jal jeevan"],
    "housing": ["आवास", "awas yojana"],
    "caste census": ["जाति जनगणना", "jati janganana"],
    "ration": ["राशन", "pds", "public distribution"],
    "fuel prices": ["पेट्रोल डीजल", "petrol diesel price"],
    "border": ["सीमा", "seema", "national security"],
}

_WORD_RE = re.compile(r"[a-zA-Z]+")


def expand_query(query: str) -> str:
    """Returns an OR-joined query string: the original text plus any
    dictionary expansions matched against its words/phrases."""
    lower = query.lower()
    matched: list[str] = []

    for phrase, expansions in EXPANSIONS.items():
        if phrase in lower:
            matched.extend(expansions)

    if not matched:
        return query

    unique_expansions = list(dict.fromkeys(matched))
    parts = [query] + unique_expansions
    return " OR ".join(f'"{p}"' if " " in p else p for p in parts)
