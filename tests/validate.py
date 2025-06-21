"""python -m tests.validate path/to/*.json
Checks:
  • duplicate ids
  • broken parent pointers
  • orphan leaf elements
  • "trash" metadata leftover.
"""
import collections
import json
import pathlib
import re
import sys

TRASH = re.compile(r"(Field:\s*(Rule-)?Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)", re.IGNORECASE)


def check(path):
    raw = json.loads(path.read_text())
    els = raw["all_elements_truncated"]

    # Extract IDs and check duplicates
    id_list = [e["id"] for e in els if "id" in e]
    id_counts = collections.Counter(id_list)
    dups = [k for k, v in id_counts.items() if v > 1]

    # Build ID set for parent validation
    ids = {e["id"] for e in els if "id" in e}

    orphans = [e["id"] for e in els if e.get("level", 0) > 1
               and (not e.get("parent_id") or e["parent_id"] not in ids)]
    trash_samples = [f"{e['class_name']}: {e['text'][:80]}" for e in els if TRASH.search(e.get("text", ""))]

    return dups, orphans, trash_samples[:3]      # first 3 samples


if __name__ == "__main__":
    for fp in map(pathlib.Path, sys.argv[1:]):
        d, o, t = check(fp)
