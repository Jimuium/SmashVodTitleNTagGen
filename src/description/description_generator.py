def generate_description(p1, p2, chars1, chars2, event_name, event_number, event, data, date_str=None):
    """
    Generate a YouTube video description for the match.
    """
    character_aliases = data.get("character_aliases", {})
    # Use only the main character names for the description
    def main_name(char):
        for main, aliases in character_aliases.items():
            if char == main or char in aliases:
                return main
        return char

    p1_char = main_name(chars1[0]) if chars1 else "Unknown"
    p2_char = main_name(chars2[0]) if chars2 else "Unknown"
    event_title = f"{event_name} #{event_number}"

    # Determine format based on round in event_title (from main())
    format_str = "Best-of-3"
    import inspect
    stack = inspect.stack()
    round_str = None
    for frame in stack:
        if 'title' in frame.frame.f_locals:
            t = frame.frame.f_locals['title']
            parts = t.split(" - ")[0].split(" ")
            if len(parts) > 3:
                round_str = " ".join(parts[3:]).strip()
            break

    if round_str:
        r = round_str.lower()
        if (
            r == "losers semi-finals"
            or r == "losers finals"
            or r == "winners finals"
            or r == "winners grand finals"
        ):
            format_str = "Best-of-5"

    desc = []
    desc.append(f"{event_title} – {p1} vs {p2} – Super Smash Bros. Ultimate\n")
    desc.append(f"This is a recorded match from {event_title}, part of our ongoing weekly Super Smash Bros. Ultimate series. In this set, {p1} and {p2} face off using {p1_char} and {p2_char} respectively.\n")
    desc.append("Match Details:")
    desc.append("Game: Super Smash Bros. Ultimate")
    desc.append(f"Event: {event_title}")
    desc.append(f"Players: {p1} vs {p2}")
    desc.append(f"Characters: {p1_char} vs {p2_char}")
    desc.append(f"Format: {format_str}")
    # No date line
    desc.append("")

    # Playlist link
    if event and event.get("playlist"):
        desc.append(f"Watch more matches from {event_title} in the full playlist: {event['playlist']}")
    else:
        desc.append(f"Watch more matches from {event_title} in the full playlist: [insert playlist link]")
    
    # Bracket link
    if event and event.get("bracket"):
        desc.append(f"Full bracket and results: {event['bracket']}")

    
    desc.append("\nSubscribe for more competitive Super Smash Bros. Ultimate content, including full sets, tournament highlights, and weekly uploads.\n")
    
    # Hashtags
    event_hashtag = f"#{event_name.replace(' ', '')}{event_number}"
    hashtags = [
        "#SuperSmashBrosUltimate",
        f"#{p1_char.replace(' ', '')}Vs{p2_char.replace(' ', '')}",
        "#SmashUltimateTournament",
        f"#{p1.replace(' ', '')}",
        f"#{p2.replace(' ', '')}",
        event_hashtag
    ]
    desc.append(" ".join(hashtags))
    return "\n".join(desc)