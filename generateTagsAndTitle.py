import json
import os
import itertools
import readline
import re

DATA_FILE = "data.json"


def load_data():
    """
    Loads the JSON from DATA_FILE.
    - If it’s already in the new format (top-level “players” & “events”), use it.
    - If it’s an older flat dict of players, migrate it under “players”.
    """
    if not os.path.exists(DATA_FILE):
        return {"players": {}, "events": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "players" in raw and "events" in raw:
        return raw

    return {"players": raw, "events": []}


def save_data(data):
    """
    Saves the combined structure ({ "players": {...}, "events": [...] }) back to disk.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def case_insensitive_autocomplete(options):
    """
    Sets up readline’s completer so that pressing TAB will autocomplete
    among ‘options’, matching case-insensitively.
    """
    def completer(text, state):
        text_lower = text.lower()
        matches = [o for o in options if o.lower().startswith(text_lower)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")


def input_with_autocomplete(prompt, options):
    """
    Prompts the user, but enables TAB-completion among the given options.
    After input, the completer is cleared.
    """
    if options:
        case_insensitive_autocomplete(options)
    try:
        return input(prompt).strip()
    finally:
        readline.set_completer(None)


def get_characters(player_input, data):
    """
    1. Finds or creates the player entry under data["players"].
    2. Lists up to 10 top characters with their usage counts.
    3. Asks “How many characters did X play?”, then for each:
       - If they type a name (or tab-complete), use that.
       - Otherwise auto-select the next-most-used unused character.
       - If none remain, use "Unknown".
    4. Increments the usage count for each chosen character.
    Returns (display_name, [chosen_char1, chosen_char2, ...]).
    """
    player_key = player_input.lower()
    players = data["players"]

    if player_key in players:
        display_name, char_dict = players[player_key]
    else:
        display_name = player_input
        char_dict = {}
        players[player_key] = [display_name, char_dict]

    sorted_chars = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)
    top_characters = [c[0] for c in sorted_chars][:10]

    print(f"\nTop characters for {display_name}:")
    if top_characters:
        for i, char in enumerate(top_characters, 1):
            print(f"  {i}. {char} ({char_dict[char]} times played)")
    else:
        print("  (none yet)")

    while True:
        try:
            num = int(input(f"\nHow many characters did {display_name} play? "))
            if num > 0:
                break
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid number, try again.")

    chosen = []
    used_chars = set()
    for i in range(num):
        prompt = f"Character {i+1} for {display_name} (leave blank to auto-select): "
        char_input = input_with_autocomplete(prompt, top_characters)

        if char_input:
            chosen_char = char_input
        else:
            next_top = next((c for c in top_characters if c not in used_chars), "Unknown")
            chosen_char = next_top
            if chosen_char != "Unknown":
                print(f"→ Auto-selected: {chosen_char}")

        chosen.append(chosen_char)
        used_chars.add(chosen_char)
        if chosen_char != "Unknown":
            char_dict[chosen_char] = char_dict.get(chosen_char, 0) + 1

    return display_name, chosen


def construct_tags(p1, p2, chars1, chars2, event_name, event_number):
    """
    Builds a comma-separated tag string:
    - Base tags: ssbu, Super Smash Bros. Ultimate, tournament, ssbu gameplay, etc.
    - Inserts one tag: "{event_name} {event_number}"
    - For each c1 in chars1 and c2 in chars2:
        • "c1 vs c2"
        • "p1 c1"
        • "p2 c2"
    - Also: "p1 vs p2" and "p2 vs p1".
    - Removes duplicates (case-insensitive), then keeps adding
      until reaching 400 characters total.
    """
    base = [
        "ssbu", "Super Smash Bros. Ultimate", "tournament", "ssbu gameplay",
        "competitive smash", "smash ultimate 2025",
        f"{event_name} {event_number}",
        p1, p2
    ]

    matchups = []
    for c1, c2 in itertools.product(chars1, chars2):
        matchups += [
            f"{c1} vs {c2}",
            f"{p1} {c1}",
            f"{p2} {c2}",
        ]

    matchups += [
        f"{p1} vs {p2}",
        f"{p2} vs {p1}"
    ]

    seen = set()
    unique = []
    for tag in base + matchups:
        low = tag.lower()
        if low not in seen:
            seen.add(low)
            unique.append(tag)

    final = []
    length = 0
    for tag in unique:
        addition = len(tag) + 1  # +1 for comma
        if length + addition <= 400:
            final.append(tag)
            length += addition
        else:
            break

    return ",".join(final)


def get_latest_event_number_for(name, data):
    """
    Given an event name, find the highest 'number' in data["events"]
    for that exact name (case-insensitive). If none exist, return 1.
    """
    events = data.get("events", [])
    nums = [e["number"] for e in events if e["name"].lower() == name.lower()]
    return max(nums) if nums else 1


def record_event_if_new(data, name, number):
    """
    Adds or updates the event list so that for `name`, the stored number
    is at least `number`. Doesn’t duplicate if it’s already >=.
    """
    events = data.setdefault("events", [])
    for e in events:
        if e["name"].lower() == name.lower():
            if number > e["number"]:
                e["number"] = number
            return
    events.append({"name": name, "number": number})


def parse_round_input(user_input, bracket_type):
    """
    Maps shorthand or full inexact strings to standard round names.
    Ensures Grand Finals only appears in Winners bracket.
    """
    m = user_input.lower().strip()
    mapping = {
        "qf": "Quarterfinals",
        "quarterfinals": "Quarterfinals",
        "sf": "Semifinals",
        "semifinals": "Semifinals",
        "f": "Finals",
        "final": "Finals",
        "finals": "Finals",
        "gf": "Grand Finals",
        "grandfinals": "Grand Finals",
        "grand finals": "Grand Finals",
    }

    if m.startswith("r") and m[1:].isdigit():
        return f"Round {int(m[1:])}"

    if m in mapping:
        out = mapping[m]
        if out == "Grand Finals" and bracket_type != "Winners":
            print("Grand Finals only allowed in Winners bracket → using Finals.")
            return "Finals"
        return out

    # fallback
    return user_input.title()

def generate_title_with_event(p1, p2, chars1, chars2, data):
    """
    1) Lists all existing event names.
    2) Prompts (with autocomplete) for event name, allowing selecting one or typing new.
    3) Determines highest number for that chosen event name.
    4) Prompts for event number [default = highest_for_that_name].
    5) Asks for round type (Winners/Losers/Pools) with autocomplete.
    6) If Winners/Losers, shows round-detail options and uses parse_round_input.
    7) Records (event_name, event_number) into data["events"] if non-empty.
    8) Returns (title, event_name, event_number).
    """
    existing_events = [e["name"] for e in data.get("events", [])]
    unique_names = sorted(set(existing_events), key=lambda x: x.lower())

    if unique_names:
        print("\nAvailable events:")
        for name in unique_names:
            print(f"  {name}")
    else:
        print("\nNo existing events found.")

    # Determine default_name as "PVL Weekly" if it exists, else first of unique_names, else ""
    if "PVL Weekly" in unique_names:
        default_name = "PVL Weekly"
    elif unique_names:
        default_name = unique_names[0]
    else:
        default_name = ""

    default_num = get_latest_event_number_for(default_name, data) if default_name else 1

    # Prompt for event name with autocomplete among unique_names
    evt_name_input = input_with_autocomplete(f"Enter event name [{default_name}]: ", unique_names)
    event_name = evt_name_input if evt_name_input else default_name

    # Now figure out the highest number for THIS event_name
    highest_for_this = get_latest_event_number_for(event_name, data)

    num_input = input(f"Enter event number [{highest_for_this}]: ").strip()
    if num_input.isdigit():
        event_number = int(num_input)
    else:
        event_number = highest_for_this

    bracket_options = ["Winners", "Losers", "Pools"]
    round_type = ""
    while round_type not in bracket_options:
        round_type = input_with_autocomplete(
            "Enter round type (Winners, Losers, Pools): ",
            bracket_options
        ).lower().strip()

    if round_type in ["Winners", "Losers"]:
        # Show the available round details (e.g., Round 1 to Round 12)
        detail_opts = (
            [f"r{i}" for i in range(1, 100)] +
            ["qf", "sf", "f", "gf", "Quarterfinals", "Semifinals", "Finals", "Grand Finals"]
        )
        print("\nAvailable rounds:")
        print("  Round N (rN)")
        print("  Quarterfinals (qf)")
        print("  Semifinals (sf)")
        print("  Finals (f)")
        print("  Grand Finals (gf)")

        raw = input_with_autocomplete("Enter round detail: ", detail_opts)

        parsed = parse_round_input(raw, round_type)
        bracket_title = f"{round_type.title()} {parsed}"


    p1_char = chars1[0] if chars1 else "Unknown"
    p2_char = chars2[0] if chars2 else "Unknown"

    if event_name:
        record_event_if_new(data, event_name, event_number)

    title = f"{event_name} #{event_number} {bracket_title} - {p1} ({p1_char}) vs {p2} ({p2_char}) - SSBU"
    return title, event_name, event_number


def main():
    data = load_data()

    # PLAYER 1
    player_keys = [data["players"][k][0] for k in data["players"]]
    p1_input = input_with_autocomplete("Enter player 1 name: ", player_keys)
    if not p1_input:
        print("Player 1 name is required.")
        return

    # PLAYER 2
    p2_input = input_with_autocomplete("Enter player 2 name: ", player_keys)
    if not p2_input:
        print("Player 2 name is required.")
        return

    p1_display, p1_chars = get_characters(p1_input, data)
    p2_display, p2_chars = get_characters(p2_input, data)

    # Generate TITLE (with event info) first:
    title, evt_name, evt_num = generate_title_with_event(
        p1_display, p2_display, p1_chars, p2_chars, data
    )
    print("\nGenerated YouTube title:")
    print(title)

    # Now generate TAGS (including "{event_name} {event_number}" instead of "PVL"):
    tags = construct_tags(p1_display, p2_display, p1_chars, p2_chars, evt_name, evt_num)
    print("\nGenerated YouTube tags:")
    print(tags)
    print(f"\nCharacter count: {len(tags)}")

    save_data(data)


if __name__ == "__main__":
    main()
