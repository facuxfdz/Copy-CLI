import sys
sys.path.append('..')
from pathlib import Path
from .dump import dump
from classes.logger import Logger
from classes.CpError import CpError

def copy_file(src: Path,dest: Path,verbose: bool,override=False,confirm=False):
    logger = Logger()
    logger.set_verbosity(verbose)
    if dest.is_dir():
        dest = dest / src.name
    if dest.is_file() and not override and not confirm:
        raise CpError(f'Cannot override {dest}, specify -o option')
    logger.log(f'Copy file {src} -> {dest}')
    dest.touch() # Create file in dest
    dump(src,dest) # Copy file content from src to dest
