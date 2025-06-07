def prompt_for_event_links(event, event_title):
    """Prompt user to add playlist and bracket links to the event if missing. Store in event dict."""
    updated = False
    if "playlist" not in event or not event["playlist"]:
        pl = input(f"Enter playlist link for '{event_title}' (or leave blank): ").strip()
        if pl:
            event["playlist"] = pl
            updated = True
    if "bracket" not in event or not event["bracket"]:
        br = input(f"Enter bracket/results link for '{event_title}' (or leave blank): ").strip()
        if br:
            event["bracket"] = br
            updated = True
    return updated