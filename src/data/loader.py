def load_data():
    """
    Loads the JSON from data.json.
    - If it’s already in the new format (top-level “players” & “events”), use it.
    - If it’s an older flat dict of players, migrate it under “players”.
    """
    import os
    import json

    DATA_FILE = "data.json"

    if not os.path.exists(DATA_FILE):
        return {"players": {}, "events": [], "character_list": [], "character_aliases": {}}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "players" in raw and "events" in raw:
        if "character_list" not in raw:
            raw["character_list"] = []
        if "character_aliases" not in raw:
            raw["character_aliases"] = {}
        return raw

    return {"players": raw, "events": [], "character_list": [], "character_aliases": {}}