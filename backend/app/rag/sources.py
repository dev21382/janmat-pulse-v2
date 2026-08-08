"""Official 2024 Lok Sabha election manifesto sources.

BJP, INC, CPI(M) and TMC are sourced from data.opencity.in's public
"Parliamentary Elections 2024 Manifestos" dataset — a civic open-data
mirror — rather than each party's own domain, because bjp.org has been
observed to hang/time out for automated fetches from multiple networks
(likely bot mitigation) while the mirror serves the same documents
reliably. Verified directly: each URL was fetched and text-extracted
before being added here; ingestion still treats each source independently
and skips any that fail rather than blocking the whole corpus.
"""

MANIFESTOS = [
    {
        "party_id": "bjp",
        "party_name": "Bharatiya Janata Party (BJP)",
        "title": "Sankalp Patra 2024 (Modi Ki Guarantee)",
        "url": "https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/6210fb78-c1c3-4700-a61f-ed01daee9aff/download/7377fce3-f32d-4dba-8d1c-4969c25a3add.pdf",
        "hue": "#e0a455",
    },
    {
        "party_id": "inc",
        "party_name": "Indian National Congress (INC)",
        "title": "Nyay Patra 2024",
        "url": "https://manifesto.inc.in/assets/Congress-Manifesto-English-2024-Dyoxp_4E.pdf",
        "hue": "#56c8d0",
    },
    {
        "party_id": "cpim",
        "party_name": "Communist Party of India (Marxist) (CPI(M))",
        "title": "Election Manifesto 2024",
        "url": "https://cpim.org/wp-content/uploads/old/documents/election_manifesto_english_april_2024.pdf",
        "hue": "#e0768f",
    },
    {
        "party_id": "tmc",
        "party_name": "All India Trinamool Congress (AITC/TMC)",
        "title": "Didir Shopoth (Didi's Pledge) 2024",
        "url": "https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/628261ee-a164-4760-a475-7a7e10d78d44/download/5e073a4f-f293-4cb0-90f1-bf5847a0015b.pdf",
        "hue": "#79cf9a",
    },
    {
        "party_id": "dmk",
        "party_name": "Dravida Munnetra Kazhagam (DMK)",
        "title": "Election Manifesto 2024",
        "url": "https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/c86a0519-1a32-407c-8381-41659734f9a2/download/a7964b61-ee79-4f84-9e1b-e3e28be52e04.pdf",
        "hue": "#b58ae8",
    },
]
