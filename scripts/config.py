import os
import sys

from pathlib import Path

ROOT = Path(os.getcwd())
INST = Path(sys.argv[1]).resolve()
CONFIG = INST / "config"
CONFIG.mkdir(exist_ok=True)

sources = [
    "config/",
    "emi.json",
    "options.txt",
]

def updateFiles(files: list[Path]):
    for file in files:
        target = ROOT / file
        source = INST / file

        if source.exists():
            target.write_bytes(source.read_bytes())
            print(f'[Updated] {file}')

def listFiles(path: str):
    return [p for p in Path(path).rglob('*') if p.is_file()]

for path in sources:
    if path.endswith('/'):
        updateFiles(listFiles(path))
    else:
        updateFiles([path])
