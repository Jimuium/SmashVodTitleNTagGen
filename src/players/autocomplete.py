import readline


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