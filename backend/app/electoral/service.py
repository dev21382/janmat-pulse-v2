from app.electoral.results_data import RESULTS, SOURCE


def get_comparison() -> dict:
    rows = []
    for party_id, data in RESULTS.items():
        y2019 = data.get("2019")
        y2024 = data.get("2024")

        seat_swing = None
        vote_share_swing = None
        if y2019 and y2024:
            seat_swing = y2024["seats"] - y2019["seats"]
            if y2019["vote_share_pct"] is not None and y2024["vote_share_pct"] is not None:
                vote_share_swing = round(y2024["vote_share_pct"] - y2019["vote_share_pct"], 2)

        rows.append(
            {
                "party_id": party_id,
                "party_name": data["party_name"],
                "hue": data["hue"],
                "2019": y2019,
                "2024": y2024,
                "seat_swing": seat_swing,
                "vote_share_swing": vote_share_swing,
                "note": data.get("note"),
            }
        )

    rows.sort(key=lambda r: (r["2024"]["seats"] if r["2024"] else -1), reverse=True)

    return {
        "sources": SOURCE,
        "methodology_note": (
            "Historical results only — not a seat projection. A validated projection needs "
            "constituency-level data across 3-4+ elections to backtest per the product's own "
            "methodology rule; two years of national totals can't satisfy that, so none is "
            "attempted here. See ROADMAP.md."
        ),
        "parties": rows,
    }
