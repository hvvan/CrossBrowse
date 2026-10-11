"""Self-check for the CrossBrowse data file.

    python scripts/check_data.py [data/crossbrowse.jsonl]

Recomputes every answer from its supporting facts and prints dataset statistics.
Uses only the Python standard library.
"""
import collections
import json
import math
import sys

LANGS = ["en", "es", "ja", "ko", "hi", "ka", "ne"]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/crossbrowse.jsonl"
    items = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    facts, domains_by_lang = {}, collections.defaultdict(set)
    for it in items:
        values = [f["question_value"] for f in it["facts"]]
        expected = sum(values) if it["operation"] == "sum" else max(values) - min(values)
        assert math.isclose(expected, it["answer"], rel_tol=1e-9, abs_tol=1e-6), it["id"]
        assert set(it["questions"]) == set(LANGS) and all(it["questions"][lang] for lang in LANGS), it["id"]
        assert [f["language"] for f in it["facts"]][0] == "en" and len(it["facts"]) == int(it["type"][-1]) + 1, it["id"]
        for lang in LANGS:
            assert sorted(it["fact_order"][lang]) == list(range(len(it["facts"]))), it["id"]
        for f in it["facts"]:
            facts[f["fact_id"]] = f
            domains_by_lang[f["language"]].add(f["source_domain"])
    assert len({it["id"] for it in items}) == len(items)
    print(f"questions: {len(items)}")
    print("by type:", dict(sorted(collections.Counter(it["type"] for it in items).items())))
    print("by domain:", dict(collections.Counter(it["domain"] for it in items).most_common()))
    print("by topic:", dict(collections.Counter(it["topic"] for it in items).most_common()))
    print(f"supporting facts: {len(facts)}")
    print("facts by language:", {lang: sum(1 for f in facts.values() if f["language"] == lang) for lang in LANGS})
    print("source domains by language:", {lang: len(domains_by_lang[lang]) for lang in LANGS},
          "total", sum(len(v) for v in domains_by_lang.values()))
    print("all answers recomputed from supporting facts: OK")


if __name__ == "__main__":
    main()
