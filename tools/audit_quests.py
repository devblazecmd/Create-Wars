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
  5. STACK          Automation-tab automate (auto_*) item tasks asking for less than a full stack (export max_stack)
  6. COVERAGE       mods (namespaces) with items in the registry but no quest mentioning any of them
  7. FARM_NEEDS     Agriculture milk/egg dependencies (frozen in the generator) vs the live recipes
  8. XP             XP points and levels per chapter
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
# Automation tab chapters (Quest Book v4: one per tier). An automate quest never "teaches" an item.
AUTOMATION_CHAPTERS = {ch["slug"] for ch in chapters if ch["group"] == "automation"}
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
    if key[0] in AUTOMATION_CHAPTERS:
        continue  # automate quests are challenges, not where an item is taught (Quest Book v4)
    for it, _ in task_items(q):
        taught[it].append(key)

# Order gaps the owner accepted on purpose (quest key -> why).
ACCEPTED_ORDER = {
    ("kinetics", s): "owner 2026-11-22: no lines from Shafts/Cogwheels to the Andesite Casing hub"
    for s in ("basin_mixer", "fan", "gearbox", "millstone", "press", "wrench_goggles")
}
ACCEPTED_ORDER.update({
    ("food", "fish_cod"): "2026-11-23: cod is fished; its only 'recipes' are CBC More Shells torpedo by-products",
    ("food", "sushi"): "2026-11-23: rolls need fish slices (Fishing branch) and cooked rice (Cooking Pot); the text says so",
})
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


report = collections.OrderedDict((k, []) for k in ("NO RECIPE", "HIDDEN", "DEAD RECIPE", "ORDER", "STACK"))
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
        if key[0] in AUTOMATION_CHAPTERS:
            continue  # challenge quests: inputs may come from anywhere; NO RECIPE still covers obtainability
        anc = ancestors(key)
        anc_ch = {a[0] for a in anc} - {key[0]}
        blockers = []
        for r in real:
            need = []
            for i in set(r["in"]):
                if i.startswith("#") or i == it or i.startswith("minecraft:"):
                    continue
                teachers = [t for t in taught.get(i, []) if t != key]
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

# STACK (owner 2026-11-23): "the automate tasks should require at min a full stack of the item". Every item task of
# an Automation-tab "auto_" quest asks for at least the item's max stack size (registry export "max_stack"; absent = 64).
max_stack = reg.get("max_stack")
if max_stack is None:
    report["STACK"].append("registry export has no max_stack (boot once with the current export_registry_ids.js)")
else:
    for key, q in quests.items():
        if key[0] not in AUTOMATION_CHAPTERS or not key[1].startswith("auto_"):
            continue  # only "Automate:" goals (e.g. Crushing Wheels is a build-the-machine quest)
        for kind, it, n in q["tasks"]:
            if kind == "item" and n < max_stack.get(it, 64):
                report["STACK"].append(f"{title(key)}: {it} x{n} < full stack {max_stack.get(it, 64)}")

for k, lines in report.items():
    print(f"\n=== {k} ({len(lines)})")
    for line in sorted(lines):
        print("  " + line)

# ---- Agriculture milk/egg rule (Quest Book v4) ----
# build_quests.FARM_NEEDS is frozen (the generator must run without an instance export). Recompute it here from the
# live recipes: an item needs milk/eggs when EVERY recipe does, recursively through intermediates (chocolate, tea,
# pie crust). Recipes that loop back to the item or a dish being checked (cake <- cake slices) are ignored, and an
# item with only looping recipes is natural (pumpkin <- pumpkin slices).
NEED_ROOTS = {"milk": {"minecraft:milk_bucket", "farmersdelight:milk_bottle", "#c:milk", "#c:drinks/milk",
                       "minecraft:milk", "neoforge:milk", "#c:buckets/milk"},
              "eggs": {"minecraft:egg", "#c:eggs"}}


NEED_MEMO = {}  # (item, kind) -> True/False once known; loop markers (ints) depend on the path, so not cached


def needs_ing(it, kind, stack=()):
    """True / False, or the stack index a looping recipe returns to (no information).
    Memoised: Create: Fishery Industry's bait-trap recipes (lobster <- fish <- steaks <- lobster ...) made the plain
    recursion exponential (2026-11-23)."""
    if (it, kind) in NEED_MEMO:
        return NEED_MEMO[(it, kind)]
    r = _needs_ing(it, kind, stack)
    if r is True or r is False:
        NEED_MEMO[(it, kind)] = r
    return r


def _needs_ing(it, kind, stack=()):
    if it in NEED_ROOTS[kind]:
        return True
    if it.startswith("#") or len(stack) > 6:
        return False
    if it in stack:
        return stack.index(it)
    rs = makes.get(it, [])
    if not rs:
        return False
    verdicts, here, loop_to = [], len(stack), len(stack)
    for r in rs:
        vs = [needs_ing(i, kind, stack + (it,)) for i in set(r["in"]) if not i.startswith("#c:tools")]
        if any(v is True for v in vs):
            verdicts.append(True)
            continue
        loops = [v for v in vs if v is not True and v is not False]
        if loops:
            loop_to = min(loop_to, min(loops))
            continue
        verdicts.append(False)
    if not verdicts:
        return loop_to if loop_to < here else False
    return all(verdicts)


farm_needs = {}
for _grp, iid, _n, _t in B.FARM:
    if isinstance(iid, tuple) or iid in ("minecraft:milk_bucket", "minecraft:egg"):
        continue  # trees (log + leaves) and the animal products themselves
    kinds = [k for k in ("milk", "eggs") if needs_ing(iid, k) is True]
    if kinds:
        farm_needs[iid] = kinds
diff = {i for i in set(farm_needs) | set(B.FARM_NEEDS) if farm_needs.get(i) != B.FARM_NEEDS.get(i)}
print(f"\n=== FARM_NEEDS (milk/egg rule) vs live recipes ({len(diff)})")
for i in sorted(diff):
    print(f"  {i}: generator {B.FARM_NEEDS.get(i)}  recipes {farm_needs.get(i)}")

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
    p = sum(q["xp"] * B.XP_SCALE * (B.AUTOMATE_XP_MULT if B.is_automate(ch, q) else 1) for q in ch["quests"])
    lv = sum(B.levels_for(ch, q) for q in ch["quests"])
    tot_p += p
    tot_l += lv
    print(f"  {ch['group']:16} {ch['title']:28} {len(ch['quests']):3} quests {p:6} xp {lv:4} levels")
print(f"  total {tot_p} xp, {tot_l} levels, {len(quests)} quests")
