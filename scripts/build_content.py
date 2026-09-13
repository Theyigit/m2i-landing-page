#!/usr/bin/env python3
"""
Builds src/data/guides.json from the Moving to Ireland app's bundled content.

The app ships its articles as Google Docs HTML exports (one file per article,
listed in content.json). Those exports are ~90% inline CSS and generated class
names, so this script parses each file into a small tree, keeps only the
semantic structure (headings, paragraphs, lists, links, bold, tables) and
rewrites it as clean HTML.

Only the opening PREVIEW_SHARE of each article is written to the JSON. The
rest of the article is never emitted, so the built site cannot leak it: the
"read the rest in the app" panel is a real gate, not a CSS one.

Run with `npm run content:build` whenever the app's content changes. Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP_CONTENT = Path.home() / "Developer/ProgressApp/ProgressApp/ProgressApp/Content"
OUT = Path(__file__).resolve().parent.parent / "src/data/guides.json"

# Share of each article's visible text that the website publishes.
PREVIEW_SHARE = 0.20

# Titles in the app that are misspelt or ambiguous once they leave the app's
# category screens. Keyed by article file stem.
TITLE_FIXES = {
    "4-arrange-your-temporary-accommodation": "Arrange your temporary accommodation",
    "1-minimum-standarts-for-moving-with-pet": "Minimum standards for moving with a pet",
    "3-getting-here-I-airlines": "Getting here I: Airlines",
    "4-getting-here-II-airports": "Getting here II: Airports",
    "4-exchange-your-existing-driving-license-non-recognized-state": "Exchange a driving licence from a non-recognised state",
    "5-exchange-your-existing-driving-license-recognized-state": "Exchange a driving licence from a recognised state",
    "4-the-foreign-earned-income-exclusion-for-U.S.-expat": "The Foreign Earned Income Exclusion for US expats",
    "1-premove": "Getting a passport",
}

# The app's profile filters, in words a website reader understands.
AUDIENCE = {
    "usCitizen": "US citizens",
    "nonEUCitizen": "Non-EU citizens",
    "kid": "Parents",
    "pet": "Pet owners",
    "premove": "Before you move",
    "recognisedDriverLicense": "Recognised licence holders",
    "nonRecognisedDriverLicense": "Non-recognised licence holders",
}

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table", "hr"}
VOID_TAGS = {"br", "hr", "img", "meta", "link"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: dict[str, str] | None = None, parent: "Node | None" = None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children: list["Node | str"] = []
        self.parent = parent

    def text(self) -> str:
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root
        self.style_text = ""
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self._in_style = True
            return
        node = Node(tag, dict(attrs), self.cur)
        self.cur.children.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
            return
        if tag in VOID_TAGS:
            return
        # Walk up to the nearest matching open element; tolerate stray closes.
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self._in_style:
            self.style_text += data
        elif data:
            self.cur.children.append(data)


def bold_classes(css: str) -> set[str]:
    return {m.group(1) for m in re.finditer(r"\.(c\d+)\{([^}]*)\}", css) if "font-weight:700" in m.group(2)}


def clean_href(href: str) -> str:
    """Google Docs wraps every link in a google.com/url redirect. Unwrap it."""
    if href.startswith("https://www.google.com/url"):
        q = parse_qs(urlparse(href).query).get("q")
        if q:
            href = q[0]
    return href.strip()


def norm_text(s: str) -> str:
    return re.sub(r"[ \t\r\n\xa0]+", " ", s)


class Renderer:
    """Serialises a Google Docs body as minimal semantic HTML blocks."""

    def __init__(self, bold: set[str]):
        self.bold = bold

    # ---- inline -----------------------------------------------------------
    def inline(self, node: Node | str) -> str:
        if isinstance(node, str):
            return escape(norm_text(node), quote=False)
        tag = node.tag
        inner = "".join(self.inline(c) for c in node.children)
        if tag == "br":
            return "<br>"
        if tag == "a":
            href = clean_href(node.attrs.get("href", ""))
            if not href or not inner.strip():
                return inner
            if href.startswith("mailto:"):
                return f'<a href="{escape(href)}">{inner}</a>'
            return f'<a href="{escape(href)}" target="_blank" rel="noopener nofollow">{inner}</a>'
        if tag == "span":
            if node.classes() & self.bold and inner.strip():
                return f"<strong>{inner}</strong>"
            return inner
        if tag in ("b", "strong"):
            return f"<strong>{inner}</strong>" if inner.strip() else inner
        if tag in ("i", "em"):
            return f"<em>{inner}</em>" if inner.strip() else inner
        if tag == "sup":
            return f"<sup>{inner}</sup>"
        # Anything else (nested p inside td, etc.) is flattened.
        return inner

    def inline_children(self, node: Node) -> str:
        return "".join(self.inline(c) for c in node.children).strip()

    # ---- blocks -----------------------------------------------------------
    def list_items(self, node: Node) -> str:
        out = []
        for c in node.children:
            if isinstance(c, Node) and c.tag == "li":
                inner = self.inline_children(c)
                if inner:
                    out.append(f"<li>{inner}</li>")
        return "".join(out)

    def table(self, node: Node) -> str:
        rows = []
        for tr in node_iter(node, "tr"):
            cells = []
            for td in tr.children:
                if isinstance(td, Node) and td.tag in ("td", "th"):
                    cells.append(f"<td>{self.inline_children(td)}</td>")
            if cells:
                rows.append("<tr>" + "".join(cells) + "</tr>")
        return '<div class="scroll-x"><table>' + "".join(rows) + "</table></div>" if rows else ""

    def block(self, node: Node) -> tuple[str, str, str] | None:
        """Returns (kind, html, plain_text) or None when the block is empty."""
        tag = node.tag
        cls = node.classes()
        if tag == "p" and "title" in cls:
            return None  # the page layout renders the title as its H1
        if tag == "hr":
            return ("hr", "<hr>", "")
        if tag in ("ul", "ol"):
            items = self.list_items(node)
            return (tag, f"<{tag}>{items}</{tag}>", norm_text(node.text())) if items else None
        if tag == "table":
            html = self.table(node)
            return ("table", html, norm_text(node.text())) if html else None
        inner = self.inline_children(node)
        if not inner or not re.sub(r"<[^>]+>|&nbsp;", "", inner).strip():
            return None
        if tag == "p" and "subtitle" in cls:
            out_tag = "h2"
        elif tag == "h1":
            out_tag = "h2"
        elif tag == "h2":
            out_tag = "h3"
        elif tag in ("h3", "h4", "h5", "h6"):
            out_tag = "h4"
        else:
            out_tag = "p"
        # A paragraph that is entirely bold and short is a heading in disguise.
        if out_tag == "p" and re.fullmatch(r"<strong>[^<]{3,80}</strong>", inner):
            out_tag = "h3"
            inner = inner[8:-9]
        kind = "heading" if out_tag != "p" else "p"
        return (kind, f"<{out_tag}>{inner}</{out_tag}>", norm_text(node.text()))


def node_iter(node: Node, tag: str):
    for c in node.children:
        if isinstance(c, Node):
            if c.tag == tag:
                yield c
            else:
                yield from node_iter(c, tag)


def find_body(root: Node) -> Node:
    for b in node_iter(root, "body"):
        return b
    return root


def render_article(path: Path) -> tuple[list[tuple[str, str, str]], str]:
    parser = TreeBuilder()
    parser.feed(path.read_text(encoding="utf-8"))
    body = find_body(parser.root)
    r = Renderer(bold_classes(parser.style_text))
    blocks = []
    title = ""
    for c in body.children:
        if not isinstance(c, Node):
            continue
        if c.tag == "p" and "title" in c.classes():
            title = norm_text(c.text()).strip()
            continue
        if c.tag in BLOCK_TAGS:
            b = r.block(c)
            if b:
                blocks.append(b)
    # Collapse runs of <hr> and drop leading/trailing rules.
    cleaned: list[tuple[str, str, str]] = []
    for b in blocks:
        if b[0] == "hr" and (not cleaned or cleaned[-1][0] == "hr"):
            continue
        cleaned.append(b)
    while cleaned and cleaned[-1][0] == "hr":
        cleaned.pop()
    return cleaned, title


def preview_blocks(blocks: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    total = sum(len(b[2]) for b in blocks)
    budget = total * PREVIEW_SHARE
    out: list[tuple[str, str, str]] = []
    seen = 0
    for b in blocks:
        if seen >= budget:
            break
        # A single long list or table can blow well past the budget. Stop
        # before it once most of the budget is already spent.
        if seen >= budget * 0.6 and seen + len(b[2]) > budget * 1.5:
            break
        out.append(b)
        seen += len(b[2])
    # Never end on a heading or a rule: the gate should cut mid-argument, not
    # promise a section that is not there.
    while out and out[-1][0] in ("heading", "hr"):
        out.pop()
    return out or blocks[:1]


def description_from(blocks, limit=155) -> str:
    text = next((b[2].strip() for b in blocks if b[0] == "p"), "")
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def slugify(stem: str) -> str:
    s = re.sub(r"^\d+-", "", stem)
    s = s.replace(".", "").replace("_", "-").lower()
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def load_catalogue() -> list[dict]:
    raw = (APP_CONTENT / "content.json").read_text(encoding="utf-8")
    raw = re.sub(r",(\s*[\]}])", r"\1", raw)  # the app's JSON has trailing commas
    return json.loads(raw)


def category_dir(name: str) -> Path:
    for d in APP_CONTENT.iterdir():
        if d.is_dir() and d.name.lower() == name.lower():
            return d
    sys.exit(f"no content directory for category {name!r}")


def main() -> None:
    catalogue = load_catalogue()
    categories = []
    slugs_seen: set[str] = set()
    total_words = 0
    n_articles = 0

    for cat in catalogue:
        cdir = category_dir(cat["name"])
        cslug = slugify(cat["name"]).replace("pre-move", "pre-move")
        articles = []
        for a in cat["contents"]:
            path = cdir / f"{a['url']}.html"
            if not path.exists():
                sys.exit(f"missing article file {path}")
            blocks, doc_title = render_article(path)
            if not blocks:
                sys.exit(f"no content parsed from {path}")
            slug = slugify(a["url"])
            key = f"{cslug}/{slug}"
            if key in slugs_seen:
                sys.exit(f"duplicate slug {key}")
            slugs_seen.add(key)

            words = sum(len(b[2].split()) for b in blocks)
            preview = preview_blocks(blocks)
            preview_words = sum(len(b[2].split()) for b in preview)
            note = (a.get("description") or "").replace("☆", "").strip()
            title = TITLE_FIXES.get(a["url"], a["name"]).strip()
            # Headings the preview stops short of — what the gate promises.
            upcoming = [re.sub(r"<[^>]+>", "", b[1]) for b in blocks[len(preview):] if b[0] == "heading"]

            articles.append(
                {
                    "slug": slug,
                    "title": title,
                    "appTitle": doc_title or a["name"],
                    "note": note,
                    "audience": [AUDIENCE.get(f, f) for f in a.get("filters", [])],
                    "description": description_from(blocks),
                    "wordCount": words,
                    "readMinutes": max(1, round(words / 220)),
                    "previewWordCount": preview_words,
                    "previewShare": round(preview_words / words, 3),
                    "previewHtml": "\n".join(b[1] for b in preview),
                    "sections": upcoming,
                }
            )
            total_words += words
            n_articles += 1

        categories.append(
            {
                "slug": cslug,
                "name": cat["name"].replace("Pre-Move", "Pre-move"),
                "tagline": (cat.get("description") or "").replace("☆", "").strip(),
                "audience": [AUDIENCE.get(f, f) for f in cat.get("filters", [])],
                "articles": articles,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "previewShare": PREVIEW_SHARE,
                "articleCount": n_articles,
                "wordCount": total_words,
                "categories": categories,
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    shares = [a["previewShare"] for c in categories for a in c["articles"]]
    print(
        f"wrote {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}: "
        f"{n_articles} articles, {total_words:,} words, "
        f"preview share {min(shares):.0%}–{max(shares):.0%}"
    )


if __name__ == "__main__":
    main()
