import json


def save_data(data):
    """
    Saves the combined structure ({ "players": {...}, "events": [...] }) back to disk.
    """
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)