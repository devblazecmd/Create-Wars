"""Deep audit of the quest book against the live game (2026-11-22).

Needs a boot first: pack/kubejs/server_scripts/export_registry_ids.js writes
  <instance>/kubejs/exported/createwars_registry.json   (items, entities)
  <instance>/kubejs/exported/createwars_recipes.json    (every loaded recipe's outputs/inputs, hidden tag)

Checks:
  1. NO RECIPE      item tasks whose item no loaded recipe makes (fine for ores/drops; review the rest)
  2. HIDDEN         tasks/rewards that ask for or give an item hidden from JEI by a pack script
  3. DEAD RECIPE    items whose every recipe needs a hidden item (directly, not via tag)
  4. ORDER          quest asks for X, every recipe for X needs Y, and Y is the task of another quest that
                    is NOT a prerequisite (so the book can send you to X before teaching Y)
  5. COVERAGE       mods (namespaces) with items in the registry but no quest mentioning any of them
  6. XP             XP points and levels per chapter
Usage: python tools/audit_quests.py [--instance PATH]
"""
import collections, copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "quests"))
import build_quests as B  # noqa: E402

inst = os.path.join(os.environ.get("APPDATA", ""), "PrismLauncher", "instances", "Create Wars", "minecraft")
if "--instance" in sys.argv:
    inst = sys.argv[sys.argv.index("--instance") + 1]
reg = json.load(open(os.path.join(inst, "kubejs", "exported", "createwars_registry.json")))
rec = json.load(open(os.path.join(inst, "kubejs", "exported", "createwars_recipes.json")))
hidden = set(rec["hidden"])

# ---- book model (layout applied, same as the generator) ----
chapters = copy.deepcopy(B.CHAPTERS)
for ch in chapters:
    B.apply_layout(ch)
quests = {}  # (chapter, slug) -> quest
for ch in chapters:
    for i, q in enumerate(ch["quests"]):
        deps = [tuple(d.split("/")) if "/" in d else (ch["slug"], d) for d in q["deps"]]
        if i == 0:
            deps += [tuple(r) for r in ch["unlock"]]
        q["_deps"] = deps
        q["_ch"] = ch
        quests[(ch["slug"], q["slug"])] = q


def ancestors(key, memo={}):
    if key in memo:
        return memo[key]
    memo[key] = set()  # cycle guard
    out = set()
    for d in quests[key]["_deps"]:
        out.add(d)
        out |= ancestors(d)
    memo[key] = out
    return out


def task_items(q):
    return [(t[1], t[2]) for t in q["tasks"] if t[0] == "item"]


# ---- recipe index ----
makes = collections.defaultdict(list)  # item -> [recipe]
for r in rec["recipes"]:
    for o in set(r["out"]):
        if not o.startswith("#"):
            makes[o].append(r)
taught = collections.defaultdict(list)  # item -> [(chapter, slug)] quests that ask for it
for key, q in quests.items():
    for it, _ in task_items(q):
        taught[it].append(key)

# Order gaps the owner accepted on purpose (quest key -> why).
ACCEPTED_ORDER = {
    ("kinetics", s): "owner 2026-11-22: no lines from Shafts/Cogwheels to the Andesite Casing hub"
    for s in ("basin_mixer", "fan", "gearbox", "millstone", "press", "wrench_goggles")
}
ACCEPTED_ORDER.update({
    ("brass_and_precision", s): "owner 2026-11-22: no lines from Brass Hand/Electron Tube to the Brass Casing hub"
    for s in ("deployer", "crafter")
})
ACCEPTED_ORDER.update({
    ("copper", s): "owner 2026-11-22: no lines from Capacitor/Copper Spool to the Electric Motor"
    for s in ("electric_motor", "alternator", "electric_pump", "portable_energy_interface", "tesla_coil",
              "modular_accumulator")
})

NATURAL_HINTS = ("_ore", "raw_", "_log", "_sapling", "_seeds", "spawn_egg")


def title(key):
    return f"{key[0]}/{key[1]} \"{quests[key]['title']}\""


report = collections.OrderedDict((k, []) for k in ("NO RECIPE", "HIDDEN", "DEAD RECIPE", "ORDER"))
for key, q in quests.items():
    for it, n in task_items(q):
        if it in hidden:
            report["HIDDEN"].append(f"{title(key)} asks for hidden {it}")
        rs = [r for r in makes.get(it, []) if not r.get("encode_failed")]
        if not rs and makes.get(it):
            report["NO RECIPE"].append(f"{title(key)}: {it} (only custom recipe types: "
                                       f"{', '.join(sorted({r['type'] for r in makes[it]}))})")
            continue
        if not rs:
            ns, path = it.split(":")
            if ns != "minecraft" and not any(h in path for h in NATURAL_HINTS):
                report["NO RECIPE"].append(f"{title(key)}: {it}")
            continue
        # skip uncrafting/decompacting style recipes that need the item's own block
        real = [r for r in rs if it not in r["in"]]
        if real and all(any(i in hidden for i in r["in"]) for r in real):
            report["DEAD RECIPE"].append(f"{title(key)}: {it} (every recipe needs a hidden item)")
        # ORDER: every recipe for X needs some item Y that the book teaches somewhere the player may not
        # have been yet. Y counts as known if a teaching quest is a prerequisite, or if it is taught in another
        # chapter the player must already have progressed through. Vanilla items are always known.
        anc = ancestors(key)
        anc_ch = {a[0] for a in anc} - {key[0]}
        blockers = []
        for r in real:
            need = []
            for i in set(r["in"]):
                if i.startswith("#") or i == it or i.startswith("minecraft:"):
                    continue
                teachers = [t for t in taught.get(i, []) if t != key]
                if len(teachers) > 1:
                    teachers = [t for t in teachers if t[0] != "automation"] or teachers
                if teachers and not any(t in anc or t[0] in anc_ch for t in teachers):
                    need.append((i, teachers))
            blockers.append(need)
        if real and all(blockers) and key not in ACCEPTED_ORDER:
            need = min(blockers, key=len)
            same = all(t[0] == key[0] for _, ts in need for t in ts)
            kind = "same chapter" if same else "other chapter"
            what = "; ".join(f"{i} <- {', '.join(title(t) for t in ts[:2])}" for i, ts in need)
            report["ORDER"].append(f"[{kind}] {title(key)} needs: {what}")
    for it, n in q["items"]:
        if it in hidden:
            report["HIDDEN"].append(f"{title(key)} REWARDS hidden {it}")
for slug, tb in B.REWARD_TABLES.items():
    for it, n, w in tb["entries"]:
        if it in hidden:
            report["HIDDEN"].append(f"reward table {slug} gives hidden {it}")

for k, lines in report.items():
    print(f"\n=== {k} ({len(lines)})")
    for line in sorted(lines):
        print("  " + line)

# ---- coverage ----
refs = set()
for q in quests.values():
    refs |= {t[1] for t in q["tasks"] if t[0] in ("item", "kill") and t[1]}
    refs |= {i for i, _ in q["items"]}
    if q.get("icon"):
        refs.add(q["icon"])
used_ns = collections.Counter(r.split(":")[0] for r in refs)
all_ns = collections.Counter(i.split(":")[0] for i in reg["items"])
print("\n=== COVERAGE: mods with items but no quest reference (item count)")
for ns, n in sorted(all_ns.items(), key=lambda x: -x[1]):
    if ns not in used_ns and ns != "minecraft":
        print(f"  {ns:40} {n}")
print("\n=== COVERAGE: quest references per mod")
print("  " + ", ".join(f"{ns} {n}" for ns, n in used_ns.most_common()))

# ---- xp ----
print("\n=== XP per chapter (points x XP_SCALE, levels)")
tot_p = tot_l = 0
for ch in chapters:
    p = sum(q["xp"] * B.XP_SCALE for q in ch["quests"])
    lv = sum(B.levels_for(ch, q) for q in ch["quests"])
    tot_p += p
    tot_l += lv
    print(f"  {ch['group']:16} {ch['title']:28} {len(ch['quests']):3} quests {p:6} xp {lv:4} levels")
print(f"  total {tot_p} xp, {tot_l} levels, {len(quests)} quests")
