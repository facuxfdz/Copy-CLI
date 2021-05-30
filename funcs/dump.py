from pathlib import Path

def dump(src: Path,dest: Path):
    with open(src,'rb') as s, open(dest, 'wb') as d:
        d.write(s.read())