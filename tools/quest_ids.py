"""Snapshot and diff every quest / task / reward ID in the generated quest book (Quest Book v4, 2026-11-23).

Restructures (moving quests between chapters, renaming tabs) must not change any ID or reward amount,
or teams lose progress / can re-claim rewards. This checks that by machine.

Usage:
    python -I tools/quest_ids.py snapshot <out.json>    # record the current pack/config/ftbquests/quests
    python -I tools/quest_ids.py diff <snapshot.json>   # compare the current book against a snapshot

Each entry: id -> {file, kind (quest|task|reward), quest (parent quest id), type, amount, deps}.
Diff reports ADDED, REMOVED, MOVED (same id, different chapter file) and CHANGED (type/amount/deps).
Exit code 1 if anything other than MOVED shows up, so it can gate a restructure.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(REPO, "pack", "config", "ftbquests", "quests")

# Commas are optional separators: the generator writes newlines, the game's own re-save uses commas on one line.
TOKEN = re.compile(r'[\s,]*(?:(?P<str>"(?:[^"\\]|\\.)*")|(?P<punct>[{}\[\]:])|(?P<atom>[^\s,{}\[\]:"]+))')


def parse_snbt(text):
    """Minimal SNBT reader for FTB Quests files (compounds, lists, strings, numbers with suffixes)."""
    toks = []
    pos = 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            if text[pos:].strip() == "":
                break
            raise ValueError(f"bad SNBT near {text[pos:pos + 40]!r}")
        pos = m.end()
        if m.group("str") is not None:
            toks.append(("s", json.loads(m.group("str"))))
        elif m.group("punct"):
            toks.append(("p", m.group("punct")))
        else:
            toks.append(("a", m.group("atom")))
    i = 0

    def atom(a):
        if a in ("true", "false"):
            return a == "true"
        m = re.fullmatch(r"(-?\d+(?:\.\d+)?)([dDfFlLbBsS]?)", a)
        if m:
            num, suf = m.groups()
            return float(num) if ("." in num or suf in "dDfF" and suf) else int(num)
        return a

    def value():
        nonlocal i
        kind, v = toks[i]
        i += 1
        if kind == "s":
            return v
        if kind == "a":
            return atom(v)
        if v == "{":
            out = {}
            while toks[i] != ("p", "}"):
                key = toks[i][1]
                assert toks[i + 1] == ("p", ":"), f"expected ':' after {key}"
                i += 2
                out[key] = value()
            i += 1
            return out
        if v == "[":
            out = []
            while toks[i] != ("p", "]"):
                out.append(value())
            i += 1
            return out
        raise ValueError(f"unexpected {v!r}")

    return value()


AMOUNT_KEYS = ("xp", "xp_levels", "count", "value", "table_id")


def amount(obj):
    out = {k: obj[k] for k in AMOUNT_KEYS if k in obj}
    for k in ("item", "entity"):
        if k in obj:
            out[k] = obj[k]["id"] if isinstance(obj[k], dict) else obj[k]
    return out


def collect():
    entries = {}
    chapters = os.path.join(BOOK, "chapters")
    for fname in sorted(os.listdir(chapters)):
        if not fname.endswith(".snbt"):
            continue
        with open(os.path.join(chapters, fname), encoding="utf-8") as fh:
            ch = parse_snbt(fh.read())
        for q in ch.get("quests", []):
            entries[q["id"]] = dict(file=fname, kind="quest", quest=None, type=None, amount={},
                                    deps=sorted(q.get("dependencies", [])))
            for kind in ("task", "reward"):
                for o in q.get(kind + "s", []):
                    assert o["id"] not in entries, f"duplicate id {o['id']} in {fname}"
                    entries[o["id"]] = dict(file=fname, kind=kind, quest=q["id"], type=o.get("type"),
                                            amount=amount(o), deps=[])
    return entries


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("snapshot", "diff"):
        print(__doc__)
        sys.exit(2)
    cmd, path = sys.argv[1:]
    now = collect()
    if cmd == "snapshot":
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(now, fh, indent=1, sort_keys=True)
        print(f"snapshot: {len(now)} ids -> {path}")
        return
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    added = sorted(set(now) - set(old))
    removed = sorted(set(old) - set(now))
    moved, changed = [], []
    for k in sorted(set(now) & set(old)):
        a, b = old[k], now[k]
        if a["file"] != b["file"]:
            moved.append(k)
        if (a["type"], a["amount"], a["deps"]) != (b["type"], b["amount"], b["deps"]):
            changed.append(k)
    for label, ids, src in (("ADDED", added, now), ("REMOVED", removed, old), ("CHANGED", changed, now)):
        for k in ids:
            e = src[k]
            extra = f"  was {old[k]['amount']} {old[k]['deps']}" if label == "CHANGED" else ""
            print(f"{label:8} {k} {e['kind']:6} {e['file']:28} {e['type'] or ''} {e['amount']} {e['deps']}{extra}")
    files = {}
    for k in moved:
        files.setdefault((old[k]["file"], now[k]["file"]), 0)
        files[(old[k]["file"], now[k]["file"])] += 1
    for (a, b), n in sorted(files.items()):
        print(f"MOVED    {n:4} ids  {a} -> {b}")
    print(f"summary: {len(added)} added, {len(removed)} removed, {len(changed)} changed, {len(moved)} moved")
    sys.exit(1 if (added or removed or changed) else 0)


if __name__ == "__main__":
    main()
