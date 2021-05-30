from classes.logger import Logger
from cli.cli import cli
from funcs.copy import copy
from classes.CpError import CpError
 
def main():
    logger = Logger()
    args = cli()
    
    src = args.source
    dest = args.destination
    
    override = args.override
    recursive = args.recursive
    verbose = args.verbose
    interactive = args.interactive
    
    try:
        copy(src,dest,verbose,override,recursive,interactive)
    except CpError as e:
        logger.error(e)
        exit(1)
    except KeyboardInterrupt:
        logger.warn('\n\nInterrupted')

if __name__ == '__main__':
    main()