def get_all_aliases(char, character_aliases):
    """
    Returns a list of all aliases for a character, including the main name.
    """
    aliases = [char]
    for main, alias_list in character_aliases.items():
        if char == main or char in alias_list:
            aliases = [main] + alias_list
            break
    return aliases

def construct_tags(p1, p2, chars1, chars2, event_name, event_number, data):
    """
    Builds a comma-separated tag string:
    - Base tags: ssbu, Super Smash Bros. Ultimate, tournament, ssbu gameplay, etc.
    - Inserts one tag: "{event_name} {event_number}"
    - For each c1 in chars1 and c2 in chars2:
        • "c1 vs c2"
        • "p1 c1"
        • "p2 c2"
      For each alias of c1/c2, also include those tags.
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
    character_aliases = data.get("character_aliases", {})
    # For each character, get all aliases (including main name)
    chars1_aliases = [get_all_aliases(c1, character_aliases) for c1 in chars1]
    chars2_aliases = [get_all_aliases(c2, character_aliases) for c2 in chars2]

    # For each combination of aliases, generate tags
    for c1_aliases in chars1_aliases:
        for c2_aliases in chars2_aliases:
            for c1 in c1_aliases:
                for c2 in c2_aliases:
                    matchups.append(f"{c1} vs {c2}")
            # Also add player-character tags for all aliases
            for c1 in c1_aliases:
                matchups.append(f"{p1} {c1}")
        for c2_aliases in chars2_aliases:
            for c2 in c2_aliases:
                matchups.append(f"{p2} {c2}")

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