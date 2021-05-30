import sys
sys.path.append('..')
from pathlib import Path
from .copy_file import copy_file
from classes.logger import Logger

def copy_directory(src_dir: Path,dest_dir: Path,verbose: bool,override=False,interactive=False):
    logger = Logger()
    logger.set_verbosity(verbose)
    for src_child in src_dir.iterdir():
        dest_child = dest_dir / src_child.name
        if src_child.is_dir():
            logger.log(f'Copy dir {src_child} -> {dest_child}')
            dest_child.mkdir(exist_ok=True)
            copy_directory(src_child,dest_child,override)
        elif src_child.is_file():
            confirm = True
            if dest_child.is_file():
                if interactive:
                    confirm = 'y' in input(f'Override {dest_child}? [no/yes]: ').lower()
                elif not override:
                    confirm = False
                    logger.warn(f'Skipping {src_child} -> {dest_child}, -o not provided')

            if confirm:
                copy_file(src_child,dest_child,override,confirm)
            else:
                logger.warn(f'Skipping {src_child} -> {dest_child}')
        else:
            logger.error(f'Skipping {src_child}, file type is not supported')
