from src.players.autocomplete import input_with_autocomplete


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
        num_input = input(f"\033[91m\nHow many characters did {display_name} play? [1] \033[0m")
        if not num_input.strip():
            num = 1
            break
        try:
            num = int(num_input)
            if num > 0:
                break
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid number, try again.")

    chosen = []
    used_chars = set()
    character_list = data.get("character_list", [])
    autocomplete_options = top_characters if top_characters else character_list
    for i in range(num):
        prompt = f"Character {i+1} for {display_name} (leave blank to auto-select): "
        char_input = input_with_autocomplete(prompt, autocomplete_options, required=False)

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