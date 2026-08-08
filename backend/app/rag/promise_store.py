import json

from app.db.database import cursor


def clear_atoms() -> None:
    with cursor() as cur:
        cur.execute("DELETE FROM promise_atoms")


def save_atoms(atoms: list[dict]) -> None:
    with cursor() as cur:
        for a in atoms:
            cur.execute(
                """INSERT INTO promise_atoms
                   (party_id, page, number, text, taxonomy_category, taxonomy_method, matched_keywords, quantified)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    a["party_id"],
                    a["page"],
                    a["number"],
                    a["text"],
                    a["taxonomy_category"],
                    a.get("taxonomy_method", "keyword"),
                    json.dumps(a["matched_keywords"]),
                    1 if a["quantified"] else 0,
                ),
            )


def _row_to_dict(row) -> dict:
    d = dict(row)
    d["matched_keywords"] = json.loads(d["matched_keywords"] or "[]")
    d["quantified"] = bool(d["quantified"])
    return d


def count_atoms() -> int:
    with cursor() as cur:
        cur.execute("SELECT COUNT(*) as n FROM promise_atoms")
        return cur.fetchone()["n"]


def atoms_by_category(category: str, party_id: str | None = None) -> list[dict]:
    with cursor() as cur:
        if party_id:
            cur.execute(
                "SELECT * FROM promise_atoms WHERE taxonomy_category=? AND party_id=? ORDER BY page",
                (category, party_id),
            )
        else:
            cur.execute(
                "SELECT * FROM promise_atoms WHERE taxonomy_category=? ORDER BY party_id, page", (category,)
            )
        return [_row_to_dict(r) for r in cur.fetchall()]


def category_counts() -> list[dict]:
    with cursor() as cur:
        cur.execute(
            """SELECT taxonomy_category, party_id, COUNT(*) as n
               FROM promise_atoms GROUP BY taxonomy_category, party_id"""
        )
        return [dict(r) for r in cur.fetchall()]
