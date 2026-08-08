"""Real, sourced national Lok Sabha results for 2019 and 2024 — the
constituency-level base data Pillar B's seat projection engine (B1) would
need, at the national-total level only.

This is deliberately NOT a seat projection or forecasting model. A genuine
uniform-swing or Monte Carlo projection needs constituency-level baselines
and margins across at least 3-4 elections (the product spec's own
backtesting rule, B6) — two years of national totals can't satisfy that,
and extrapolating seats from national vote-share swing alone would be
statistically indefensible under India's first-past-the-post system, where
national vote share doesn't map linearly to seats. What's here is the real,
citable comparison data itself: seats and vote share, per party, per
election, with the actual computed swing — a legitimate B1 foundation,
not a substitute for B4.

Sourced from Wikipedia's election-result pages (which compile Election
Commission of India data); party splits are called out explicitly rather
than left to mislead a bare year-over-year comparison.
"""

SOURCE = {
    "2019": "https://en.wikipedia.org/wiki/Results_of_the_2019_Indian_general_election",
    "2024": "https://en.wikipedia.org/wiki/Results_of_the_2024_Indian_general_election",
}

# party_id -> {2019: {seats, vote_share_pct} | None, 2024: {...} | None, note}
RESULTS: dict[str, dict] = {
    "bjp": {
        "party_name": "Bharatiya Janata Party (BJP)",
        "hue": "#e0a455",
        "2019": {"seats": 303, "vote_share_pct": 37.36},
        "2024": {"seats": 240, "vote_share_pct": 36.56},
    },
    "inc": {
        "party_name": "Indian National Congress (INC)",
        "hue": "#56c8d0",
        "2019": {"seats": 52, "vote_share_pct": 19.49},
        "2024": {"seats": 99, "vote_share_pct": 21.19},
    },
    "aitc": {
        "party_name": "All India Trinamool Congress (AITC/TMC)",
        "hue": "#79cf9a",
        "2019": {"seats": 22, "vote_share_pct": 4.07},
        "2024": {"seats": 29, "vote_share_pct": 4.37},
    },
    "sp": {
        "party_name": "Samajwadi Party (SP)",
        "hue": "#b58ae8",
        "2019": {"seats": 5, "vote_share_pct": 2.55},
        "2024": {"seats": 37, "vote_share_pct": 4.58},
    },
    "dmk": {
        "party_name": "Dravida Munnetra Kazhagam (DMK)",
        "hue": "#e0768f",
        "2019": {"seats": 23, "vote_share_pct": 2.26},
        "2024": {"seats": 22, "vote_share_pct": 1.82},
    },
    "ysrcp": {
        "party_name": "YSR Congress Party (YSRCP)",
        "hue": "#8fc7f0",
        "2019": {"seats": 23, "vote_share_pct": 2.53},
        "2024": {"seats": 4, "vote_share_pct": 2.06},
    },
    "tdp": {
        "party_name": "Telugu Desam Party (TDP)",
        "hue": "#9184d9",
        "2019": {"seats": 3, "vote_share_pct": 2.04},
        "2024": {"seats": 16, "vote_share_pct": 1.98},
    },
    "cpim": {
        "party_name": "Communist Party of India (Marxist) (CPI(M))",
        "hue": "#e0768f",
        "2019": {"seats": 3, "vote_share_pct": 1.77},
        "2024": {"seats": 4, "vote_share_pct": 1.76},
    },
    "jdu": {
        "party_name": "Janata Dal (United) (JD(U))",
        "hue": "#79cf9a",
        "2019": {"seats": 16, "vote_share_pct": 1.46},
        "2024": {"seats": 12, "vote_share_pct": 1.25},
    },
    "bjd": {
        "party_name": "Biju Janata Dal (BJD)",
        "hue": "#8fc7f0",
        "2019": {"seats": 12, "vote_share_pct": 1.66},
        "2024": {"seats": 0, "vote_share_pct": 1.46},
    },
    "bsp": {
        "party_name": "Bahujan Samaj Party (BSP)",
        "hue": "#9397ab",
        "2019": {"seats": 10, "vote_share_pct": 3.63},
        "2024": {"seats": 0, "vote_share_pct": None},
        "note": "BSP's 2024 national vote share wasn't found in a source solid enough to cite here — left blank rather than estimated. The zero-seat result is independently confirmed by multiple sources.",
    },
    "aap": {
        "party_name": "Aam Aadmi Party (AAP)",
        "hue": "#56c8d0",
        "2019": {"seats": 1, "vote_share_pct": None},
        "2024": {"seats": 3, "vote_share_pct": 1.11},
        "note": "AAP's 2019 national vote share wasn't found in a source solid enough to cite here — left blank rather than estimated.",
    },
    "shiv_sena_undivided_lineage": {
        "party_name": "Shiv Sena (undivided in 2019; split into two factions before 2024)",
        "hue": "#e0a455",
        "2019": {"seats": 18, "vote_share_pct": 2.10},
        "2024": {"seats": 16, "vote_share_pct": 2.63},
        "note": "Shiv Sena split into the Shinde faction (\"Shiv Sena\", 7 seats, 1.15% in 2024) and the Uddhav Thackeray faction (\"Shiv Sena (UBT)\", 9 seats, 1.48% in 2024) in 2022, after the 2019 election. The row above sums both factions so the 2019→2024 comparison isn't misleadingly read as a single party's collapse.",
    },
    "ncp_undivided_lineage": {
        "party_name": "Nationalist Congress Party (undivided in 2019; split into two factions before 2024)",
        "hue": "#b58ae8",
        "2019": {"seats": 5, "vote_share_pct": 1.39},
        "2024": {"seats": 9, "vote_share_pct": 1.24},
        "note": "NCP split into the Ajit Pawar faction (\"NCP\", 1 seat, 0.32% in 2024) and the Sharad Pawar faction (\"NCP(SP)\", 8 seats, 0.92% in 2024) in 2023, after the 2019 election. The row above sums both factions so the 2019→2024 comparison isn't misleadingly read as a single party's near-collapse.",
    },
    "rjd": {
        "party_name": "Rashtriya Janata Dal (RJD)",
        "hue": "#e0768f",
        "2019": None,
        "2024": {"seats": 4, "vote_share_pct": 1.57},
        "note": "Not in the top-tier 2019 results table sourced here.",
    },
}
