import sys
sys.path.append('..')
from pathlib import Path
from .copy_file import copy_file
from .copy_directory import copy_directory
from classes.CpError import CpError

def copy(src: Path,dest: Path,verbose: bool,override=False,recursive=False,interactive=False):

    if src.is_file() and not recursive:
        confirm = override
        copy_file(src,dest,verbose,override,confirm)
    elif src.is_dir():
        dest_is_dir = dest.is_dir()
        if not dest_is_dir and dest.exists():
            raise CpError(f'Destination {dest} is not a directory')
        if not recursive:
            raise CpError(f'Skipping directory {src}, -r option not provided')
        if dest_is_dir:
            dest = dest / src.name
        dest.mkdir(exist_ok=True)
        copy_directory(src,dest,verbose,override,interactive)
    else:
        raise CpError('File type not supported or wrong -r argument passed')