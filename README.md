# Stuck in Time tools

This is a collection of tools to help interact with the Stuck in Time game [Steam link](https://store.steampowered.com/app/1814010/Stuck_In_Time/).

This tools help to:
- Decompress the save files (so they can be inspected and modified)
- Compress the save files (so they can be loaded in the game)
- Extract or inject the list of commands in the save files
- Extract the status of the whole map to a csv file
- Type the commands directly in the game (this only works on windows)

This is at the same time a library to be used, a command line tool, and a GUI application. 

## Requirements

- Python 3 (most versions should work)
If running the GUI application:
- flet
If typing the commands in the game:
- pyautogui

## How to use

The easiest way to use this is to download the latest release from the [releases page](https://github.com/Daniferrito/Stuck-in-Time-Tools/releases) and run the executable.

If you want to run the code directly, just running it with python should work.
`time_tools.py`  for the command line tool or library, and `time_tools_flet.py` for the GUI application.

## Extras

There are two extra files that might be useful if you are using this tool. They are both in the other_data folder.
- WorldTerrain_Layer_tiledata.csv contains the terrain of each tile in the game. This are things like grass, water, walls, etc. 
- WorldElements_Layer_tiledata.csv contains the entity of each tile in the game. This entities are things like fireflies, enemies, npcs, etc.

Both include only the id of the tile or entity. 
Some mapping exists for the tiles, included in the `WorldElements_mapping.json` file. It is not complete, but it is a start, and contributions are welcome
No mapping is provided, for the terrain but it can be easily done by matching the ids with what exists in the game, and contributions are welcome.
