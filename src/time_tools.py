from typing import List
import re
import zlib
import argparse
import sys
import json
from pathlib import Path

actions = {
    'o_AL_up': 'up',
    'o_AL_down': 'down',
    'o_AL_left': 'left',
    'o_AL_right': 'right',
    
    'o_AL_Interact': 'interact',
    'o_AL_Speak': 'speak',
    'o_AL_Fight': 'fight',
}

actions_reversed = {
    'up': 'o_AL_up',
    'down': 'o_AL_down',
    'left': 'o_AL_left',
    'right': 'o_AL_right',
    
    'interact': 'o_AL_Interact',
    'spirit': 'o_AL_Interact',
    'firefly': 'o_AL_Interact',
    'bonfire': 'o_AL_Interact',
    's potion': 'o_AL_Interact',
    'scarecrow': 'o_AL_Interact',
    'shield 1': 'o_AL_Interact',

    'speak': 'o_AL_Speak',
    'heart': 'o_AL_Speak',

    'fight': 'o_AL_Fight',
    'body': 'o_AL_Fight',
    'fence': 'o_AL_Fight',
    'rat': 'o_AL_Fight',
    'bat': 'o_AL_Fight',
    'critter': 'o_AL_Fight',
    'were-critter': 'o_AL_Fight',
    'beast': 'o_AL_Fight',
    'hydra': 'o_AL_Fight',
}

actions_keys = {
    'o_AL_up': 'w',
    'o_AL_down': 's',
    'o_AL_left': 'a',
    'o_AL_right': 'd',
    
    'o_AL_Interact': 'e',

    'o_AL_Speak': 'r',

    'o_AL_Fight': 't',
}

def map_command(command: List[str]) -> tuple[str, int]:
    if command[0] not in actions_reversed:
        raise Exception(f'Unknown command: {command[0]}')
    if len(command) == 1:
        return (actions_reversed[command[0]], 1)
    return (actions_reversed[command[0]], int(command[-1]))

def decompress(source_path: Path, dest_path: Path):
    with source_path.open('rb') as source_file:
        with dest_path.open('wb') as dest_file:
            raw = zlib.decompress(source_file.read())
            data = json.loads(raw.strip(b'\x00'))
            dest_file.write(json.dumps(data, indent=4).encode())

def compress(source_path: Path, dest_path: Path):
    with source_path.open('rb') as source_file:
        with dest_path.open('wb') as dest_file:
            dest_file.write(zlib.compress(source_file.read()))

def insert(source_path: Path, dest_path: Path, separator: str = r'[\t,;]'):
    with source_path.open('r', encoding='utf-8') as source_file:
        with dest_path.open('r+b') as dest_file:
            commands = [map_command(re.split(separator, l)) for l in source_file.read().splitlines()]

            raw = zlib.decompress(dest_file.read())
            data = json.loads(raw.strip(b'\x00'))

            data['ActionListData'] = [{"Type": c[0], "RepeatNumber": c[1]} for c in commands]
            dest_file.seek(0)
            dest_file.truncate()
            dest_file.write(zlib.compress(json.dumps(data).encode()))

def extract(source_path: Path, dest_path: Path, separator: str = '\t'):
    with source_path.open('rb') as source_file:
        with dest_path.open('w', encoding='utf-8') as dest_file:
            raw = zlib.decompress(source_file.read())
            data = json.loads(raw.strip(b'\x00'))
            for command in data['ActionListData']:
                dest_file.write(actions[command['Type']] + separator + str(int(command['RepeatNumber']))+ '\n')

def map(source_path: Path, dest_path: Path, separator: str = '\t'):
    with source_path.open('rb') as source_file:
        with dest_path.open('w', encoding='utf-8') as dest_file:
            raw = zlib.decompress(source_file.read())
            data = json.loads(raw.strip(b'\x00'))
            fmt = ['X', 'Y']
            fmt2 = ['CXp', 'IXp', 'SXp', 'FXp']
            for tile in data['TerrainData']:
                dest_file.write(separator.join([str(int(tile[f])) for f in fmt]) + separator + separator.join([str(float(tile[f])) for f in fmt2]) + '\n')

def type(source_path: Path, separator: str = r'[\t,;]'):
    with source_path.open('r', encoding='utf-8') as source_file:
        commands = [map_command(re.split(separator, l)) for l in source_file.read().splitlines()]
        commands = [actions_keys[c[0]] * c[1] for c in commands]

        import pywinauto
        import warnings
        warnings.simplefilter('ignore', category=UserWarning)
        import time
        
        app = pywinauto.Application().connect(title="Loop Odyssey", class_name="YYGameMakerYY")

        for window in app.windows():
            if window.class_name() == "YYGameMakerYY":
                for key in "".join(commands):
                    window.send_keystrokes(key)
                    time.sleep(0.05)
                break

split_argv0 = re.split('[\\\\/]', sys.argv[0])[-1]
executable = split_argv0 if split_argv0.endswith('.exe') else f'python {split_argv0}'

example_text = f'''Examples:

 Decompress a save file:
   {executable} decompress LoopOdyssey.save LoopOdyssey.json
 Compress a save file:
   {executable} compress LoopOdyssey.json LoopOdyssey.save
 Insert a list of commands into a save file:
   {executable} insert commands.tsv LoopOdyssey.json
 Extract a list of commands from a save file:
   {executable} extract LoopOdyssey.json commands.tsv
 Map a save file to a list of tiles:
   {executable} map LoopOdyssey.json tiles.tsv
 Type a list of commands into the game:
   {executable} type commands.tsv
   
Files with commands can be separated by tabs, commas, or semicolons.
Exported files are separated by tabs by default.'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tools to work with Stuck in Time.', epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title="action", required=True, dest='action')

    decompress = subparsers.add_parser('decompress')
    decompress.add_argument('source_path', type=Path)
    decompress.add_argument('dest_path', type=Path)

    compress = subparsers.add_parser('compress')
    compress.add_argument('source_path', type=Path)
    compress.add_argument('dest_path', type=Path)

    insert = subparsers.add_parser('insert')
    insert.add_argument('source_path', type=Path)
    insert.add_argument('dest_path', type=Path)
    insert.add_argument('-s', '--separator', type=str, default=r'[\t,;]')

    extract = subparsers.add_parser('extract')
    extract.add_argument('source_path', type=Path)
    extract.add_argument('dest_path', type=Path)
    extract.add_argument('-s', '--separator', type=str, default='\t')

    map = subparsers.add_parser('map')
    map.add_argument('source_path', type=Path)
    map.add_argument('dest_path', type=Path)
    map.add_argument('-s', '--separator', type=str, default='\t')

    type = subparsers.add_parser('type')
    type.add_argument('source_path', type=Path)
    type.add_argument('-s', '--separator', type=str, default=r'[\t,;]')

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if 'decompress' == args.action:
        decompress(args.source_path, args.dest_path)
    elif 'compress' == args.action:
        compress(args.source_path, args.dest_path)
    elif 'insert' == args.action:
        insert(args.source_path, args.dest_path, args.separator)
    elif 'extract' == args.action:
        extract(args.source_path, args.dest_path, args.separator)
    elif 'map' == args.action:
        map(args.source_path, args.dest_path, args.separator)
    elif 'type' == args.action:
        type(args.source_path, args.separator)
    else:
        raise Exception(f'Unknown action: {args.action}')