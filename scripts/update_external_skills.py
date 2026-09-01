#!/usr/bin/env python3
"""Sync bundled external skills from upstream repos and refresh manifest.json.

Reads skills/external/manifest.json for source repos, clones each one,
mirrors all SKILL.md files into skills/external/<collection>/<skill-name>/,
and regenerates the skills lists and bundledAt timestamps.

Run from repo root: python scripts/update_external_skills.py
"""
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTERNAL_DIR = ROOT / "skills" / "external"
MANIFEST = EXTERNAL_DIR / "manifest.json"
TMP_DIR = ROOT / ".tmp-skill-sync"


def run(cmd):
    subprocess.run(cmd, check=True)


def _force_rmtree(path: Path):
    """rmtree that handles Windows read-only files (git pack files) and retries."""
    def onerror(func, fname, exc_info):
        try:
            os.chmod(fname, stat.S_IWRITE)
            func(fname)
        except Exception:
            print(f"  ! could not remove: {fname}")

    for attempt in range(3):
        if not path.exists():
            return
        try:
            shutil.rmtree(path, onerror=onerror)
            return
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)  # file may be locked briefly, retry


def clone(url, branch, dest):
    if dest.exists():
        _force_rmtree(dest)
    run(["git", "clone", "--depth", "1", "--branch", branch, url, str(dest)])


def parse_frontmatter(skill_md: Path):
    """Extract name and description from YAML frontmatter (best effort)."""
    name, desc = None, None
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, None
    for line in m.group(1).splitlines():
        if line.startswith("name:") and name is None:
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:") and desc is None:
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
    return name, desc


def sync_collection(collection: str, repo_dir: Path, old_skills: list):
    """Mirror SKILL.md files from a cloned repo into skills/external/<collection>/.

    Only top-level files (e.g. collection-SKILL.md) are preserved as-is;
    skill subdirectories are mirrored against the source. Returns the new
    skills list for the manifest.
    """
    target = EXTERNAL_DIR / collection
    target.mkdir(parents=True, exist_ok=True)
    old_desc = {s["id"]: s.get("description", "") for s in old_skills}

    # Discover skills: last path segment of each SKILL.md's directory
    src = {}
    for skill_md in repo_dir.rglob("SKILL.md"):
        rel = skill_md.relative_to(repo_dir).parent
        if not rel.parts or ".git" in rel.parts:
            continue  # skip repo-root SKILL.md and anything inside .git
        src[rel.parts[-1]] = skill_md

    # Remove stale skill dirs (root-level files untouched)
    for child in target.iterdir():
        if child.is_dir() and child.name not in src:
            print(f"  - removing stale skill: {collection}/{child.name}")
            shutil.rmtree(child)

    skills = []
    for skill_name in sorted(src):
        skill_md = src[skill_name]
        out_dir = target / skill_name
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(skill_md, out_dir / "SKILL.md")
        fm_name, fm_desc = parse_frontmatter(skill_md)
        skills.append({
            "id": skill_name,
            "path": f"{collection}/{skill_name}",
            "name": fm_name or skill_name,
            "description": fm_desc or old_desc.get(skill_name, ""),
        })
        print(f"  + {collection}/{skill_name}")
    return skills


def main():
    if not MANIFEST.exists():
        sys.exit(f"manifest not found: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    today = date.today().isoformat()

    for key, source in manifest["sources"].items():
        print(f"Syncing {key} from {source['repo']} ({source['branch']})")
        repo_dir = TMP_DIR / key
        clone(source["repo"], source["branch"], repo_dir)
        source["skills"] = sync_collection(key, repo_dir, source.get("skills", []))
        source["bundledAt"] = today

    manifest["updatedAt"] = today
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    try:
        _force_rmtree(TMP_DIR)
    except Exception:
        print(f"warning: could not fully clean {TMP_DIR}")
    print("External skills synced.")


if __name__ == "__main__":
    main()
