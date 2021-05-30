from sys import stderr, stdout

FAIL = '\033[91m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'

class Logger:

    def __init__(self,verbosity=False):
        self.verbosity = verbosity
    
    def set_verbosity(self,verbosity):
        self.verbose = verbosity
    
    def log(self,msg,file=stdout):
        if self.verbose:
            print(f'{OKGREEN}{msg}{ENDC}', file=file)
    
    def warn(self,msg,file=stderr):
        print(f'{WARNING}{msg}{ENDC}',file=file)

    def error(self,msg,file=stderr):
        print(f'{FAIL}{msg}{ENDC}',file=file)
