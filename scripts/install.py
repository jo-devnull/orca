import os
import sys
import shutil

from pathlib import Path
from subprocess import run

ROOT = Path(os.getcwd())

TYPE_MAP = {
    'datapacks': 'packs/datapacks',
    'resourcepacks': 'packs/resourcepacks'
}

def platform_of(url: str):
    if "modrinth.com" in url:
        return "modrinth"
    elif "curseforge.com" in url:
        return "curseforge"
    elif "github.com" in url:
        return "github"
    else:
        raise ValueError("Unsupported platform")

def is_mod(type: str):
    return not type.endswith("packs")

def install(type: str, url: str):
    platform = platform_of(url)
    tempdir = Path(".temp")
    modfile: Path = None

    if tempdir.exists():
        shutil.rmtree(".temp")

    os.makedirs(tempdir, exist_ok=True)

    if is_mod(type):
        try:
            run(["packwiz.exe", "-y", platform, "add", url, "--meta-folder", tempdir], check=True)
        except Exception:
            return

        for file in tempdir.glob("*.pw.toml"):
            modname = file.name.replace(".pw.toml", "")

            if modname in url:
                modfile = file

            text = file.read_text(encoding='utf-8')
            text = text.replace('filename = "', 'filename = "../')
            text = text.replace('side = "server"', 'side = "both"')

            file.write_text(text, encoding='utf-8')

        if modfile == None or not modfile.exists():
            raise FileNotFoundError("Mod not found")

        modpath = ROOT / f"mods/{type}/{modfile.name}"

        if not modpath.exists():
            modfile.rename(modpath)

        for file in tempdir.glob("*.pw.toml"):
            libpath = ROOT / f"mods/library" / file.name

            if not libpath.exists() and file != modfile:
                shutil.move(file, libpath)

    else:
        run(f"packwiz.exe -y {platform} add {url} --meta-folder {TYPE_MAP[type]}", shell=True)

    if tempdir.exists():
        shutil.rmtree(".temp")

    run(f"packwiz.exe refresh", shell=True)

if __name__ == "__main__":
    urls = [path.strip() for path in sys.argv[2].split(";")]

    for url in urls:
        if len(url) > 0:
            print(f"\nInstalling {url}")
            install(sys.argv[1], url)
