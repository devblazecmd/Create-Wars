"""Check that every item/block ID referenced by the FTB Quests book exists in the pack.

Usage:
    python -I tools/check_quest_refs.py [quests_dir] [--instance <path>]

Defaults:
    quests_dir  pack/config/ftbquests/quests
    --instance  the Prism "Create Wars" instance (its mods/ folder must be synced from pack/)

Known IDs are collected from:
  * every mod jar in <instance>/minecraft/mods (and jars bundled inside them under META-INF/jarjar)
  * the vanilla 1.21.1 client jar from Prism's libraries
  * createwars:* items registered in pack/kubejs/startup_scripts/*.js
An ID counts as known if it has an item model (assets/<ns>/models/item/<path>.json) or an
item./block. lang key. Exit code 1 if any referenced ID is unknown.

Why: the most common modpack quest bug is a quest pointing at an item that was renamed or removed
(e.g. elytras, Mob Radar, the Air War launchers). See vault/03-Design/Quest Book.md.
"""
import io
import os
import re
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUESTS = os.path.join(REPO, "pack", "config", "ftbquests", "quests")
DEFAULT_INSTANCE = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "PrismLauncher",
                                "instances", "Create Wars")
VANILLA_JAR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "PrismLauncher", "libraries",
                           "com", "mojang", "minecraft", "1.21.1", "minecraft-1.21.1-client.jar")

MODEL_RE = re.compile(r"^assets/([a-z0-9_.-]+)/models/item/([a-z0-9_/.-]+)\.json$")
LANG_RE = re.compile(r"^assets/[a-z0-9_.-]+/lang/en_us\.json$")
# entity.* too, so kill-task entity IDs are checked (2026-11-21)
LANG_KEY_RE = re.compile(r'"(?:item|block|entity)\.([a-z0-9_-]+)\.([a-z0-9_/-]+)"\s*:')
KJS_ITEM_RE = re.compile(r"""event\.create\(\s*['"]([a-z0-9_.-]+:[a-z0-9_/.-]+)['"]""")
# Items that exist in the registry but the pack has taken out of play. Quests must not reference them.
# Keep in sync with pack/kubejs/server_scripts/elytra_removed.js, air_war_launchers_removed.js and
# potr_tools_removed.js.
BANNED = {
    "minecraft:elytra",
    "create_the_air_wars:anti_aircraft_launcher", "create_the_air_wars:c75",
    "create_the_air_wars:vihr", "create_the_air_wars:vihr_rocket",
    "create_the_air_wars:heattrap", "create_the_air_wars:heattrap_charge",
} | {f"adpother:{t}_{k}" for t in ("iron", "gold", "diamond")
     for k in ("filter_frame", "vacuum_bag", "vacuum_tube", "respirator")} | {"adpother:aerometer"}
# Any quoted namespaced ID in quest SNBT (quest object IDs are bare hex, so they never match).
REF_RE = re.compile(r'"#?([a-z0-9_.-]+:[a-z0-9_/.-]+)"')


def scan_jar(zf, known):
    for name in zf.namelist():
        m = MODEL_RE.match(name)
        if m:
            known.add(f"{m.group(1)}:{m.group(2)}")
        elif LANG_RE.match(name):
            text = zf.read(name).decode("utf-8", "replace")
            known.update(f"{a}:{b}" for a, b in LANG_KEY_RE.findall(text))
        elif name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
            try:
                with zipfile.ZipFile(io.BytesIO(zf.read(name))) as inner:
                    scan_jar(inner, known)
            except zipfile.BadZipFile:
                pass


def known_ids(instance):
    known = set()
    mods = os.path.join(instance, "minecraft", "mods")
    jars = [os.path.join(mods, f) for f in os.listdir(mods) if f.endswith(".jar")]
    jars.append(VANILLA_JAR)
    for path in jars:
        with zipfile.ZipFile(path) as zf:
            scan_jar(zf, known)
    startup = os.path.join(REPO, "pack", "kubejs", "startup_scripts")
    if os.path.isdir(startup):
        for f in os.listdir(startup):
            if f.endswith(".js"):
                with open(os.path.join(startup, f), encoding="utf-8") as fh:
                    known.update(KJS_ITEM_RE.findall(fh.read()))
    return known


def referenced_ids(quests_dir):
    refs = {}
    for root, _, files in os.walk(quests_dir):
        if os.path.basename(root) == "lang":
            continue  # display text only
        for f in files:
            if f.endswith(".snbt"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        for ref in REF_RE.findall(line):
                            refs.setdefault(ref, []).append(f"{os.path.relpath(path, quests_dir)}:{i}")
    return refs


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    instance = DEFAULT_INSTANCE
    if "--instance" in argv:
        instance = argv[argv.index("--instance") + 1]
        args.remove(instance)
    quests_dir = args[0] if args else DEFAULT_QUESTS

    known = known_ids(instance)
    refs = referenced_ids(quests_dir)
    unknown = {r: locs for r, locs in refs.items() if r not in known}
    banned = {r: locs for r, locs in refs.items() if r in BANNED}

    print(f"known IDs: {len(known)}  referenced: {len(refs)}  unknown: {len(unknown)}  banned: {len(banned)}")
    for ref, locs in sorted(unknown.items()):
        print(f"  UNKNOWN {ref}  at {', '.join(locs)}")
    for ref, locs in sorted(banned.items()):
        print(f"  BANNED  {ref}  at {', '.join(locs)}  (removed from play by a pack script)")
    return 1 if unknown or banned else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
