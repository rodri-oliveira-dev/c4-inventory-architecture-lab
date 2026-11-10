#!/usr/bin/env python3
"""Validate local Markdown links and extract the Mermaid source of truth.

No third-party Python packages are required. External links are not fetched;
they remain editorial checks to avoid flaky CI and rate limits.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
MERMAID_BLOCK = re.compile(r"^\x60{3}mermaid\s*\n(.*?)^\x60{3}\s*$", re.MULTILINE | re.DOTALL)
INLINE_LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPECTED = {
    "docs/01-contexto.md": ["C4Context"],
    "docs/02-containers.md": ["C4Container"],
    "docs/03-componentes.md": ["C4Component"],
    "docs/04-codigo.md": ["classDiagram"],
    "docs/fluxo-movimentacao.md": ["sequenceDiagram", "sequenceDiagram"],
}


def slug(text: str) -> str:
    """Approximate GitHub's heading slug algorithm, preserving Unicode letters."""
    text = re.sub(r"!?(?:\[([^\]]+)\]\([^)]*\))", r"\1", text)
    text = text.replace("\x60", "").replace("*", "").replace("~", "")
    text = "".join(
        c for c in text.lower()
        if c in "-_" or not unicodedata.category(c).startswith(("P", "S"))
    )
    return re.sub(r"\s", "-", text.strip())


def anchors(markdown: str) -> set[str]:
    used: Counter[str] = Counter()
    found: set[str] = set()
    for match in HEADING.finditer(markdown):
        base = slug(match.group(1))
        if not base:
            continue
        number = used[base]
        found.add(base if number == 0 else f"{base}-{number}")
        used[base] += 1
    return found


def local_target(source: Path, raw: str) -> tuple[Path, str] | None:
    destination = raw.strip()
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]
    # Optional Markdown link titles are not used in this repository.
    parts = urlsplit(destination)
    if parts.scheme or parts.netloc or destination.startswith("//"):
        return None
    if parts.path.startswith("/"):
        # GitHub repository-relative links should use explicit relative paths.
        return (ROOT / "__invalid_absolute_link__", "")
    path = source.parent / unquote(parts.path) if parts.path else source
    return path.resolve(), unquote(parts.fragment)


def validate_links(files: list[Path]) -> tuple[int, list[str]]:
    errors: list[str] = []
    links = 0
    cached_anchors: dict[Path, set[str]] = {}
    for source in files:
        markdown = source.read_text(encoding="utf-8")
        for match in INLINE_LINK.finditer(markdown):
            raw = match.group(1).strip()
            target = local_target(source, raw)
            if target is None:
                continue
            links += 1
            path, fragment = target
            position = markdown.count("\n", 0, match.start()) + 1
            display = f"{source.relative_to(ROOT)}:{position}"
            if not path.is_relative_to(ROOT):
                errors.append(f"{display}: link escapes repository: {raw}")
            elif not path.exists():
                errors.append(f"{display}: target not found: {raw}")
            elif fragment and path.is_file() and path.suffix.lower() == ".md":
                if path not in cached_anchors:
                    cached_anchors[path] = anchors(path.read_text(encoding="utf-8"))
                if fragment not in cached_anchors[path]:
                    errors.append(f"{display}: heading #{fragment} not found: {raw}")
            elif fragment and path.is_dir():
                errors.append(f"{display}: directory cannot have a heading: {raw}")
    return links, errors


def extract_mermaid(files: list[Path], out: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    out.mkdir(parents=True, exist_ok=True)
    for source in files:
        rel = source.relative_to(ROOT).as_posix()
        markdown = source.read_text(encoding="utf-8")
        diagrams = [m.group(1).strip() for m in MERMAID_BLOCK.finditer(markdown)]
        required = EXPECTED.get(rel)
        if required is not None:
            actual = [d.splitlines()[0] for d in diagrams if d]
            if actual != required:
                errors.append(f"{rel}: expected {required}, found {actual}")
        for index, diagram in enumerate(diagrams, 1):
            if not diagram:
                errors.append(f"{rel}: Mermaid block {index} is empty")
                continue
            filename = rel.removesuffix(".md").replace("/", "--")
            (out / f"{filename}-{index:02d}.mmd").write_text(diagram + "\n", encoding="utf-8")
            count += 1
    if count < 6:
        errors.append(f"Expected at least 6 Mermaid blocks (four C4 levels and two sequences), found {count}")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="Temporary directory for extracted .mmd files")
    args = parser.parse_args()
    files = sorted(
        p for p in ROOT.rglob("*.md")
        if not any(segment in {"node_modules", ".git", ".tmp"} for segment in p.relative_to(ROOT).parts)
    )
    count_links, link_errors = validate_links(files)
    count_diagrams, mermaid_errors = extract_mermaid(files, args.output_dir)
    for error in link_errors + mermaid_errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {len(files)} Markdown files, {count_links} local links, {count_diagrams} Mermaid blocks.")
    if link_errors or mermaid_errors:
        return 1
    print("Links and Mermaid source structure OK. Render diagrams with Mermaid CLI to check syntax.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
