#!/usr/bin/env python3
"""Provenance-preserving local text retrieval. No network, no semantic scoring."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata


def digest(data):
    return hashlib.sha256(data).hexdigest()


def emit(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def load_manifest(root, library_id, create=False):
    path = root / "manifest.json"
    if not path.exists():
        if create:
            return {"schema_version": 1, "library_id": library_id, "sources": []}
        raise ValueError("corpus_unavailable: manifest.json 不存在")
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1 or doc.get("library_id") != library_id:
        raise ValueError("library_mismatch: 缓存不属于本次指定古籍库")
    return doc


def read_source(root, source):
    path = (root / source["path"]).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise ValueError("invalid_source_path: 路径超出缓存目录")
    data = path.read_bytes()
    if digest(data) != source["sha256"]:
        raise ValueError("source_changed: 原文快照哈希不一致: " + source["id"])
    return data.decode("utf-8")


def add(args, root, doc):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", args.id):
        raise ValueError("invalid_id: 使用小写英文、数字、下划线或连字符")
    if any(s["id"] == args.id for s in doc["sources"]):
        raise ValueError("source_exists: 不覆盖已有来源，请使用新版本 ID")
    data = Path(args.file).read_bytes()
    content = data.decode("utf-8")
    if not content.strip():
        raise ValueError("empty_source: 不能导入空文本")
    source = {
        "id": args.id, "book": args.book, "volume": args.volume,
        "chapter": args.chapter, "source_url": args.source_url,
        "edition": args.edition, "locator": args.locator,
        "coverage": args.coverage, "revision": args.revision,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": digest(data), "path": "texts/" + args.id + ".txt",
        "lines": len(content.splitlines()),
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "texts").mkdir(exist_ok=True)
    with (root / source["path"]).open("xb") as handle:
        handle.write(data)
    doc["sources"].append(source)
    tmp = root / "manifest.json.tmp"
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(root / "manifest.json")
    return {"status": "imported", "source": source}


def search(args, root, doc):
    groups = [[term for term in group.split("|") if term] for group in args.term]
    if any(not group for group in groups):
        raise ValueError("empty_query: 关键词组不能空")
    results = []
    examined = []
    total_matches = 0
    for source in doc["sources"]:
        if args.book and source["book"] != args.book:
            continue
        content = read_source(root, source)
        examined.append({"id": source["id"], "coverage": source["coverage"]})
        lines = content.splitlines()
        last_end = -1
        for i, line in enumerate(lines):
            if not any(term in line for group in groups for term in group):
                continue
            lo, hi = max(0, i - args.window), min(len(lines), i + args.window + 1)
            window = "\n".join(lines[lo:hi])
            if lo <= last_end or not all(any(term in window for term in group) for group in groups):
                continue
            last_end = hi - 1
            total_matches += 1
            if len(results) < args.limit:
                results.append({"source": source, "line_start": lo + 1, "line_end": hi,
                                "text": window,
                                "matched_terms": [[t for t in g if t in window] for g in groups]})
    return {"status": "matches" if total_matches else "no_match_in_cached_scope",
            "library_id": doc["library_id"], "query_groups": groups,
            "searched_sources": examined, "results": results,
            "returned": len(results), "total_windows": total_matches,
            "truncated": total_matches > len(results),
            "boundary": "仅为缓存范围的词面命中，不是语义匹配或全书穷尽"}


def normalized_with_positions(text):
    pairs = [(char, pos) for pos, char in enumerate(text)
             if not char.isspace() and not unicodedata.category(char).startswith("P")]
    return "".join(c for c, _ in pairs), [pos for _, pos in pairs]


def verify(args, root, doc):
    source = next((s for s in doc["sources"] if s["id"] == args.id), None)
    if source is None:
        raise ValueError("unknown_source: 来源 ID 不存在")
    text = read_source(root, source)
    if not args.quote.strip():
        raise ValueError("empty_quote: 引文不能空")
    pos = text.find(args.quote)
    state = "exact" if pos >= 0 else "not_found"
    end = pos + len(args.quote) if pos >= 0 else -1
    if pos < 0 and args.normalize:
        norm, positions = normalized_with_positions(text)
        needle, _ = normalized_with_positions(args.quote)
        if not needle:
            raise ValueError("empty_normalized_quote: 引文归一化后不能空")
        hit = norm.find(needle)
        if hit >= 0:
            pos, end = positions[hit], positions[hit + len(needle) - 1] + 1
            state = "normalized_only"
    found = pos >= 0
    return {"status": state, "source": source, "requested_quote": args.quote,
            "source_quote": text[pos:end] if found else None,
            "char_start": pos if found else None, "char_end_exclusive": end if found else None,
            "line_start": text.count("\n", 0, pos) + 1 if found else None,
            "line_end": text.count("\n", 0, end - 1) + 1 if found else None,
            "context": text[max(0, pos - 120):min(len(text), end + 120)] if found else None,
            "boundary": "只校验文本一致性，不证明历史真实性、因果关系或古今适用性"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ["add", "search", "verify"]:
        sub = subs.add_parser(command)
        sub.add_argument("--corpus", required=True)
        sub.add_argument("--library-id", required=True)
        if command == "add":
            for key in ["id", "file", "volume", "chapter", "source-url", "edition", "locator", "coverage"]:
                sub.add_argument("--" + key, required=True)
            sub.add_argument("--book", required=True, choices=["史记", "资治通鉴"])
            sub.add_argument("--revision")
        elif command == "search":
            sub.add_argument("--term", action="append", required=True)
            sub.add_argument("--book", choices=["史记", "资治通鉴"])
            sub.add_argument("--window", type=int, default=1)
            sub.add_argument("--limit", type=int, default=8)
        else:
            sub.add_argument("--id", required=True)
            sub.add_argument("--quote", required=True)
            sub.add_argument("--normalize", action="store_true")
    args = parser.parse_args()
    if args.command == "search" and (not 0 <= args.window <= 20 or not 1 <= args.limit <= 100):
        parser.error("window 必须为 0–20，limit 必须为 1–100")
    root = Path(args.corpus)
    try:
        doc = load_manifest(root, args.library_id, args.command == "add")
        result = {"add": add, "search": search, "verify": verify}[args.command](args, root, doc)
        emit(result)
        return 1 if result["status"] in ("not_found", "normalized_only", "no_match_in_cached_scope") else 0
    except (ValueError, KeyError, OSError, UnicodeError) as exc:
        emit({"status": "error", "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
