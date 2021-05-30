import argparse
from pathlib import Path
from sys import stderr, stdout

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CpError(Exception):
    pass

class Logger:
    def __init__(self,verbosity=False):
        self.verbosity = verbosity
    
    def set_verbosity(self,verbosity):
        self.verbose = verbosity
    
    def log(self,msg,file=stdout):
        if self.verbose:
            print(f'{bcolors.OKGREEN}{msg}{bcolors.ENDC}', file=file)
    
    def warn(self,msg,file=stderr):
        print(f'{bcolors.WARNING}{msg}{bcolors.ENDC}',file=file)

    def error(self,msg,file=stderr):
        print(f'{bcolors.FAIL}{msg}{bcolors.ENDC}',file=file)

    
logger = Logger()

def dump(src: Path,dest: Path):
    with open(src,'rb') as s, open(dest, 'wb') as d:
        d.write(s.read())

def copy_directory(src_dir: Path,dest_dir: Path,override=False,interactive=False):
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

def copy_file(src: Path,dest: Path,override=False,confirm=False):
    if dest.is_dir():
        dest = dest / src.name
    if dest.is_file() and not override and not confirm:
        raise CpError(f'Cannot override {dest}, specify -o option')
    logger.log(f'Copy file {src} -> {dest}')
    dest.touch() # Create file in dest
    dump(src,dest) # Copy file content from src to dest

def copy(src: Path,dest: Path,override=False,recursive=False,interactive=False):
    if src.is_file():
        confirm = override
        copy_file(src,dest,override,confirm)
    elif src.is_dir():
        dest_is_dir = dest.is_dir()
        if not dest_is_dir and dest.exists():
            raise CpError(f'Destination {dest} is not a directory')
        if not recursive:
            raise CpError(f'Skipping directory {src}, -r option not provided')
        if dest_is_dir:
            dest = dest / src.name
        dest.mkdir(exist_ok=True)
        copy_directory(src,dest,override,interactive)
    else:
        raise CpError('File type not supported')


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

def main():
    args = cli()
    src = args.source
    dest = args.destination
    override = args.override
    recursive = args.recursive
    verbose = args.verbose
    interactive = args.interactive
    try:
        logger.set_verbosity(verbose)
        copy(src,dest,override,recursive,interactive)
    except CpError as e:
        logger.error(e)
        exit(1)
    except KeyboardInterrupt:
        logger.warn('\n\nInterrupted')

if __name__ == '__main__':
    main()