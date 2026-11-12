#!/usr/bin/env python3
"""Flatten all skills into a DSH (DeepSeek Harness) friendly layout at repo root.

DSH's skill discovery only scans DIRECT children of a skill root
(`<root>/<id>/SKILL.md` or `<root>/<id>.md`). The Kimi Code layout
`skills/external/<collection>/<skill>/SKILL.md` is nested too deep, so this
script mirrors every SKILL.md into `<repo-root>/<skill-name>/SKILL.md`,
normalizing the frontmatter per DSH rules:

- name: forced to equal the directory name, kebab-case
- description: single line, escaped, truncated to 500 chars (catalog limit)
- body: byte-for-byte identical to the source

A `.nacl-dsh-skills.json` manifest tracks generated dirs so re-runs only
touch directories this script created. Kimi Code is unaffected: plugin.json
still points at ./skills/.

Run from repo root: python scripts/build_dsh_layout.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
EXTERNAL_DIR = SKILLS_DIR / "external"
MANIFEST_PATH = ROOT / ".nacl-dsh-skills.json"
DESC_MAX = 500  # dsh catalogDescriptionMaxLength default


def parse_frontmatter(skill_md: Path):
    """Extract name and description from YAML frontmatter (best effort)."""
    name, desc = None, None
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None, ""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, None, text
    for line in m.group(1).splitlines():
        if line.startswith("name:") and name is None:
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:") and desc is None:
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
    return name, desc, text


def normalize(name: str) -> str:
    """kebab-case, matching DSH skill-name validation."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def rewrite_frontmatter(text: str, name: str, desc: str) -> str:
    """Replace name/description lines inside the frontmatter, keep the rest."""
    desc = desc.replace("\\", "\\\\").replace('"', '\\"')
    desc = re.sub(r"\s+", " ", desc)[:DESC_MAX]
    fm_re = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.DOTALL)
    m = fm_re.match(text)
    if not m:
        # No frontmatter: prepend a minimal one
        return f'---\nname: {name}\ndescription: "{desc}"\n---\n\n{text}'
    block = m.group(2)
    block = re.sub(r"(?m)^name:.*$", f"name: {name}", block, count=1)
    if re.search(r"(?m)^description:", block):
        block = re.sub(r'(?m)^description:.*$', f'description: "{desc}"', block, count=1)
    else:
        block += f'\ndescription: "{desc}"'
    return fm_re.sub(lambda mm: mm.group(1) + block + mm.group(3), text, count=1)


def collect():
    """Yield (source_skill_md, default_name, collection) for every skill."""
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        yield skill_md, skill_md.parent.name, None
    for collection_dir in sorted(p for p in EXTERNAL_DIR.iterdir() if p.is_dir()):
        for skill_md in sorted(collection_dir.glob("*/SKILL.md")):
            yield skill_md, skill_md.parent.name, collection_dir.name


def load_manifest():
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"generated": []}


def main():
    if not SKILLS_DIR.exists():
        sys.exit(f"skills dir not found: {SKILLS_DIR}")

    manifest = load_manifest()
    # Clean up dirs written by a previous run (only our own)
    for name in manifest.get("generated", []):
        stale = ROOT / name
        if stale.is_dir():
            shutil.rmtree(stale)

    used = {}          # out dir name -> source path
    generated = []     # sorted dir names written this run
    collisions = []
    count = 0

    for skill_md, default_name, collection in collect():
        fm_name, fm_desc, text = parse_frontmatter(skill_md)
        name = normalize(fm_name or default_name)
        if collection and name in used:
            name = normalize(f"{collection}-{name}")
        if name in used:
            collisions.append(str(skill_md))
            continue
        target = ROOT / name
        if target.exists():
            print(f"  ! '{name}/' already exists at repo root and is not "
                  f"script-generated, skipping source: {skill_md}")
            continue
        used[name] = skill_md
        target.mkdir()
        (target / "SKILL.md").write_text(
            rewrite_frontmatter(text, name, fm_desc or default_name),
            encoding="utf-8",
        )
        generated.append(name)
        count += 1
        print(f"  + {name}/SKILL.md  ({collection or 'native'})")

    # Persist manifest sorted, so regeneration order is stable
    manifest["generated"] = sorted(set(generated) | set()) or manifest.get("generated", [])
    manifest["generated"] = sorted(used.keys())
    MANIFEST_PATH.write_text(
        json.dumps({"generated": manifest["generated"]}, indent=2) + "\n",
        encoding="utf-8",
    )
    if collisions:
        print(f"warning: {len(collisions)} source(s) skipped due to duplicate names")
    print(f"Done: {count} skills flattened at repo root (manifest: {MANIFEST_PATH.name})")


if __name__ == "__main__":
    main()
