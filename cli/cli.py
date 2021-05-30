import argparse
from pathlib import Path

def cli() -> argparse.Namespace :
    parser = argparse.ArgumentParser(
        prog='cp',
        description='cp command implementation in Python'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-o','--override',
        action='store_true',
        help='Override destination files if the already exists'
    )
    group.add_argument(
        '-i','--interactive',
        action='store_true',
        help='Prompt before overwrite'
    )
    parser.add_argument(
        '-r','--recursive',
        action='store_true',
        help='Copy directories recursively'
    )
    parser.add_argument(
        '-v','--verbose',
        action='store_true',
        help='Give details about actions being performed'
    )     
    parser.add_argument('source',help='Source directory or file',type=Path)
    parser.add_argument('destination',help='Destination directory or file',type=Path)
    return parser.parse_args()