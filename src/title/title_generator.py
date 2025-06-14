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

    evt_name_input = input_with_autocomplete(f"Enter event name [{default_name}]: ", unique_names)
    event_name = evt_name_input if evt_name_input else default_name

    highest_for_this = get_latest_event_number_for(event_name, data)

    num_input = input(f"Enter event number [{highest_for_this}]: ").strip()
    if num_input.isdigit():
        event_number = int(num_input)
    else:
        event_number = highest_for_this

    bracket_options = ["Winners", "Losers", "Pools"]
    round_type = ""
    while True:
        user_input = input_with_autocomplete(
            "Enter round type (Winners, Losers, Pools): ",
            bracket_options
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