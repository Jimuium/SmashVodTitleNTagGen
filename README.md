# SmashVodTitleNTagGen

## Overview
SmashVodTitleNTagGen is a Python application designed to assist in generating titles, tags, and descriptions for YouTube videos featuring Super Smash Bros. Ultimate matches. The application allows users to input player names, select characters, and automatically generate formatted titles and tags based on event details.

## Project Structure
The project is organized into several directories and modules, each serving a specific purpose:

- **src/**: The main source code directory containing all application logic.
  - **data/**: Contains modules for loading and saving data.
    - `loader.py`: Handles loading JSON data from `data.json`.
    - `saver.py`: Manages saving modified data back to `data.json`.
  - **players/**: Contains modules related to player management.
    - `autocomplete.py`: Provides input functionality with autocomplete for player names.
    - `characters.py`: Manages character selection and usage tracking.
  - **events/**: Contains modules for event management.
    - `event_utils.py`: Includes utility functions for generating event titles and managing event data.
    - `links.py`: Prompts for event links if they are missing.
  - **tags/**: Contains the tag generation logic.
    - `tag_generator.py`: Generates a comma-separated string of tags based on player and event information.
  - **title/**: Contains the title generation logic.
    - `title_generator.py`: Creates formatted titles for YouTube videos.
  - **description/**: Contains the description generation logic.
    - `description_generator.py`: Generates YouTube video descriptions based on match details.
  
## Usage
1. Ensure you have Python installed on your machine.
2. Clone the repository or download the source code.
3. Install any required dependencies (if applicable).
4. Run the application using the command:
   ```
   python src/main.py
   ```
5. Follow the prompts to enter player names, select characters, and generate titles, tags, and descriptions for your videos.

## Data
The application uses a `data.json` file to store character, player, and event information. This file is structured to facilitate easy loading and saving of data.

## Contributing
Contributions to the project are welcome! Please feel free to submit issues or pull requests for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.