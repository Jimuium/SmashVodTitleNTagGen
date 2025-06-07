from src.data.loader import load_data
from src.players.autocomplete import input_with_autocomplete
from src.players.characters import get_characters
from src.events.event_utils import generate_title_with_event, get_event_by_name_and_number, record_event_if_new
from src.events.links import prompt_for_event_links
from src.tags.tag_generator import construct_tags
from src.description.description_generator import generate_description
from src.data.saver import save_data

def main():
    data = load_data()

    player_keys = [data["players"][k][0] for k in data["players"]]
    p1_input = input_with_autocomplete("Enter player 1 name: ", player_keys)
    if not p1_input:
        print("Player 1 name is required.")
        return

    p2_input = input_with_autocomplete("Enter player 2 name: ", player_keys)
    if not p2_input:
        print("Player 2 name is required.")
        return

    p1_display, p1_chars = get_characters(p1_input, data)
    p2_display, p2_chars = get_characters(p2_input, data)

    title, evt_name, evt_num = generate_title_with_event(
        p1_display, p2_display, p1_chars, p2_chars, data
    )
    print("\nGenerated YouTube title:")
    print(title)

    tags = construct_tags(p1_display, p2_display, p1_chars, p2_chars, evt_name, evt_num, data)
    print("\nGenerated YouTube tags:")
    print(tags)
    print(f"\nCharacter count: {len(tags)}")

    event_obj = get_event_by_name_and_number(data, evt_name, evt_num)
    event_title = f"{evt_name} #{evt_num}"
    if event_obj:
        if prompt_for_event_links(event_obj, event_title):
            print("Event links updated.")

    description = generate_description(
        p1_display, p2_display, p1_chars, p2_chars, evt_name, evt_num, event_obj, data
    )
    print("\nGenerated YouTube description:\n")
    print(description)

    save_data(data)

if __name__ == "__main__":
    main()