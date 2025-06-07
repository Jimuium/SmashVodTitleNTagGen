import readline

# ANSI color codes
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
LIGHT_GRAY = "\033[37m"
RESET = "\033[0m"


def input_with_autocomplete(prompt, options, required=False):
    """
    Prompts the user, but enables TAB-completion among the given options.
    After input, the completer is cleared.
    Colors:
      - Required input: red prompt
      - Optional input: orange prompt
      - Autocomplete suggestions: light gray (display only, if supported)
    """
    if options:
        case_insensitive_autocomplete(options)
    # Color the prompt
    color = RED if required else ORANGE
    try:
        return input(f"{color}{prompt}{RESET}").strip()
    finally:
        readline.set_completer(None)
        # Only clear display hook if it exists (for cross-platform)
        if hasattr(readline, "set_completion_display_matches_hook"):
            readline.set_completion_display_matches_hook(None)


def case_insensitive_autocomplete(options):
    """
    Sets up readline’s completer so that pressing TAB will autocomplete
    among ‘options’, matching case-insensitively.
    Suggestions are shown in light gray (display only, if supported).
    """
    def completer(text, state):
        text_lower = text.lower()
        matches = [o for o in options if o.lower().startswith(text_lower)]
        if state < len(matches):
            return matches[state]
        return None

    readline.set_completer(completer)
    # Only set display hook if available (not on Windows)
    if hasattr(readline, "set_completion_display_matches_hook"):
        def display_matches(substitution, matches, longest_match_length):
            # Print suggestions in light gray
            print()
            for match in matches:
                print(f"{LIGHT_GRAY}{match}{RESET}")
        readline.set_completion_display_matches_hook(display_matches)
    readline.parse_and_bind("tab: complete")