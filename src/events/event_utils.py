from src.players.autocomplete import input_with_autocomplete


def generate_title_with_event(p1, p2, chars1, chars2, data):
    existing_events = [e["name"] for e in data.get("events", [])]
    unique_names = sorted(set(existing_events), key=lambda x: x.lower())

    if unique_names:
        print("\nAvailable events:")
        for name in unique_names:
            print(f"  {name}")
    else:
        print("\nNo existing events found.")

    if "PVL Weekly" in unique_names:
        default_name = "PVL Weekly"
    elif unique_names:
        default_name = unique_names[0]
    else:
        default_name = ""

    default_num = get_latest_event_number_for(default_name, data) if default_name else 1

    evt_name_input = input_with_autocomplete(
        f"Enter event name [{default_name}]: ", unique_names, required=False
    )
    event_name = evt_name_input if evt_name_input else default_name

    highest_for_this = get_latest_event_number_for(event_name, data)

    num_input = input(f"\033[91mEnter event number [{highest_for_this}]: \033[0m").strip()
    if num_input.isdigit():
        event_number = int(num_input)
    else:
        event_number = highest_for_this

    bracket_options = ["Winners", "Losers", "Pools"]
    round_type = ""
    while True:
        user_input = input_with_autocomplete(
            "Enter round type (Winners, Losers, Pools): ",
            bracket_options,
            required=True
        )
        normalized = user_input.strip().lower().capitalize()
        if normalized in bracket_options:
            round_type = normalized
            break
        else:
            print("Invalid input. Please enter one of: Winners, Losers, Pools.")

    if round_type in ["Winners", "Losers"]:
        detail_opts = (
            [f"r{i}" for i in range(1, 100)] +
            ["qf", "sf", "f", "gf", "Quarterfinals", "Semi-Finals", "Finals", "Grand Finals"]
        )
        print("\nAvailable rounds:")
        print("  Round N (rN)")
        print("  Quarterfinals (qf)")
        print("  Semi-Finals (sf)")
        print("  Finals (f)")
        print("  Grand Finals (gf)")

        raw = input_with_autocomplete("Enter round detail: ", detail_opts, required=False)

        parsed = parse_round_input(raw, round_type)
        bracket_title = f"{round_type.title()} {parsed}"
    else:
        bracket_title = round_type.title()

    p1_char = chars1[0] if chars1 else "Unknown"
    p2_char = chars2[0] if chars2 else "Unknown"

    character_aliases = data.get("character_aliases", {})
    def main_name(char):
        for main, aliases in character_aliases.items():
            if char == main or char in aliases:
                return main
        return char

    p1_char_main = main_name(p1_char)
    p2_char_main = main_name(p2_char)

    if event_name:
        record_event_if_new(data, event_name, event_number)

    title = f"{event_name} #{event_number} {bracket_title} - {p1} ({p1_char_main}) vs {p2} ({p2_char_main}) - SSBU"
    return title, event_name, event_number

def parse_round_input(raw, round_type):
    """
    Parses the round detail input and returns a formatted string for the bracket title.
    Accepts abbreviations like 'qf', 'sf', 'f', 'gf', or numbers like 'r1', 'r2', etc.
    """
    if not raw:
        return ""
    val = raw.strip().lower()
    mapping = {
        "qf": "Quarterfinals",
        "sf": "Semi-Finals",
        "f": "Finals",
        "gf": "Grand Finals",
        "quarterfinals": "Quarterfinals",
        "semi-finals": "Semi-Finals",
        "finals": "Finals",
        "grand finals": "Grand Finals"
    }
    if val in mapping:
        return mapping[val]
    if val.startswith("r") and val[1:].isdigit():
        return f"Round {val[1:]}"
    return raw.title()

def get_latest_event_number_for(name, data):
    events = data.get("events", [])
    nums = [e["number"] for e in events if e["name"].lower() == name.lower()]
    return max(nums) if nums else 1


def record_event_if_new(data, name, number):
    events = data.setdefault("events", [])
    for e in events:
        if e["name"].lower() == name.lower():
            if number > e["number"]:
                e["number"] = number
            return
    events.append({"name": name, "number": number})


def get_event_by_name_and_number(data, name, number):
    for e in data.get("events", []):
        if e["name"].lower() == name.lower() and e.get("number", None) == number:
            return e
    for e in data.get("events", []):
        if e["name"].lower() == name.lower():
            return e
    return None