"""Print how items are made, from the live recipe export (boot once first; see audit_quests.py).
Usage: python tools/recipe_lookup.py ITEM_ID [ITEM_ID ...]
Shows each recipe's type and its inputs with counts. Used to write quest descriptions that match the pack."""
import collections, json, os, sys

inst = os.path.join(os.environ.get("APPDATA", ""), "PrismLauncher", "instances", "Create Wars", "minecraft")
rec = json.load(open(os.path.join(inst, "kubejs", "exported", "createwars_recipes.json")))
by_out = collections.defaultdict(list)
for r in rec["recipes"]:
    for o in set(r["out"]):
        by_out[o].append(r)
for it in sys.argv[1:]:
    rs = by_out.get(it, [])
    print(f"{it}: {len(rs)} recipe(s)" + ("" if rs else "  <-- NONE"))
    for r in rs[:4]:
        c = collections.Counter(i for i in r["in"] if i != it or r["type"] != "create:sequenced_assembly")
        ins = ", ".join(f"{n}x {i.split(':')[1]}" if n > 1 else i.split(":")[1] for i, n in c.items())
        print(f"   [{r['type'].split(':')[1]}] {ins}   ({r['id']})")
