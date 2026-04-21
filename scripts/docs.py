import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent

def get_mods():
  mods = {}

  for file in (ROOT / "mods").glob("**/*.pw.toml"):
    if file.name.startswith("!"):
      continue

    category = file.parent.name

    if category == "dependency":
      continue

    if category not in mods:
      mods[category] = []
    mods[category].append(file)

  return mods

def get_link(file: Path, meta: dict):
  slug = file.name.replace('.pw.toml', '')
  update = meta['update']

  if 'modrinth' in update:
    return f'https://modrinth.com/mod/{slug}'
  elif 'curseforge' in update:
    return f'https://www.curseforge.com/minecraft/mc-mods/{slug}'
  elif 'github' in update:
    return f'https://github.com/{update['slug']}'

  return '#'

def main():
  mods = get_mods()

  for category in mods:
    print(f'## {category.title()}')
    print()
    print('| Mod | Link |')
    print('|------|------|')

    for mod in mods[category]:
      with open(mod, 'rb') as io:
        meta = tomllib.load(io)
        try:
          print(f'| {meta['name']} | {get_link(mod, meta)} |')
        except:
          pass

    print()

if __name__ == "__main__":
  main()
