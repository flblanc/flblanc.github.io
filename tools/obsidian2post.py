#!/usr/bin/env python3
# Obsidian note -> Rare Events post.
#   [[Name]], [[Name|alias]], [[Note#Section]] -> plain text as Obsidian displays it
#   [[citekey]] (lowercase surname + Words + year) -> numbered citation linked to ## References
#   inline $x$ -> $$x$$ (kramdown math); blank lines around display $$ blocks
# Front matter comes from _drafts/_template-<kind>.md, title from the note's filename.
# usage: obsidian2post.py NOTE.md OUTDIR [--kind essay|book-notes] [--bib FILE.bib]

import argparse, re, sys, unicodedata
from pathlib import Path

CITEKEY = re.compile(r"[a-z][A-Za-z]*[A-Z][A-Za-z]*\d{4}[a-z]?")
WIKI = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
CITE_RUN = re.compile(r"\[\[([^\]|#\n]+)(?:\|[^\]\n]*)?\]\](?:\s*[,;]?\s*\[\[([^\]|#\n]+)(?:\|[^\]\n]*)?\]\])*")
CODE = re.compile(r"(```.*?```|~~~.*?~~~|`[^`\n]*`)", re.S)

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327", "v": "\u030c", "=": "\u0304"}


def parse_bib(text):
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        typ, key, i = m.group(1).lower(), m.group(2), m.end()
        depth, j = 1, i
        while depth and j < len(text):
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        body, fields = text[i:j - 1], {"type": typ}
        for f in re.finditer(r"(\w+)\s*=\s*", body):
            k, p = f.group(1).lower(), f.end()
            if p < len(body) and body[p] in "{\"":
                close, depth, q = ("}" if body[p] == "{" else '"'), 1, p + 1
                while depth and q < len(body):
                    if body[q] == "{" and close == "}":
                        depth += 1
                    elif body[q] == close:
                        depth -= 1
                    q += 1
                fields.setdefault(k, body[p + 1:q - 1])
            else:
                fields.setdefault(k, re.match(r"[^,}\s]*", body[p:]).group(0))
        entries[key] = fields
    return entries


def tex(s):
    s = re.sub(r"\\([\'`^\"~cv=])\s*\{?\\?(\w)\}?", lambda m: m.group(2) + ACCENTS[m.group(1)], s)
    s = s.replace("\\&", "&").replace("---", "\u2014").replace("--", "\u2013")
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s).replace("{", "").replace("}", "")
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", s).strip())


def names(s):
    out = []
    for a in re.split(r"\s+and\s+", s.strip()):
        a = tex(a)
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
        else:
            parts = a.split()
            last, first = parts[-1], " ".join(parts[:-1])
        initials = " ".join(p[0] + "." for p in re.split(r"[\s.]+", first) if p)
        out.append(f"{last}, {initials}" if initials else last)
    if len(out) == 1:
        return out[0]
    return ", ".join(out[:-1]) + ", & " + out[-1]


def reference(e):
    year = e.get("year") or e.get("date", "")[:4] or "n.d."
    who = names(e["author"]) if "author" in e else (names(e["editor"]) + " (Ed.)" if "editor" in e else "")
    title = tex(e.get("title", ""))
    publisher = tex(e.get("publisher", ""))
    typ = e["type"]
    if typ == "article":
        journal, vol, num, pages = tex(e.get("journal", e.get("journaltitle", ""))), e.get("volume", ""), e.get("number", ""), tex(e.get("pages", ""))
        src = f"*{journal}*" + (f", {vol}" if vol else "") + (f"({num})" if num else "") + (f", {pages}" if pages else "")
        s = f"{who} ({year}). {title}. {src}."
    elif typ in ("incollection", "inbook", "inproceedings"):
        eds = f"{names(e['editor'])} (Eds.), " if "editor" in e else ""
        pages = tex(e.get("pages", ""))
        s = f"{who} ({year}). {title}. In {eds}*{tex(e.get('booktitle', ''))}*" + (f" (pp. {pages})" if pages else "") + "." + (f" {publisher}." if publisher else "")
    else:
        s = f"{who} ({year}). *{title}*." + (f" {publisher}." if publisher else "")
    if e.get("doi"):
        s += f" <https://doi.org/{e['doi']}>"
    return s


def display(target, alias):
    if alias is not None:
        return alias
    return " > ".join(p.lstrip("^") if i else p for i, p in enumerate(target.split("#")) if p)


def convert_text(text, bib):
    order = {}

    def cite_run(m):
        keys = re.findall(r"\[\[([^\]|#\n]+)", m.group(0))
        if not all(CITEKEY.fullmatch(k) for k in keys):
            return m.group(0)
        nums = [order.setdefault(k, len(order) + 1) for k in keys]
        return "(" + ", ".join(f"[{n}](#ref-{n})" for n in nums) + ")"

    def wiki(m):
        if m.group(1):
            print(f"warning: embed left as is: {m.group(0)}", file=sys.stderr)
            return m.group(0)
        target, _, alias = m.group(2).partition("|")
        return display(target, alias if "|" in m.group(2) else None)

    def math(seg):
        def block(m):
            pre, post = seg[:m.start()], seg[m.end():]
            if (pre == "" or pre.endswith("\n")) and (post == "" or post.startswith("\n")):
                return "\n" + m.group(0) + "\n"
            return m.group(0)
        seg = re.sub(r"^[ \t]*\$\$.*?\$\$[ \t]*$", block, seg, flags=re.S | re.M)
        seg = re.sub(r"(?<![\\$])\$(?=[^\s$])([^$\n]*?[^\s\\$])\$(?![$\d])", r"$$\1$$", seg)
        # remaining single $ (prices, \$) -> \\$, so MathJax shows a literal $
        bits = re.split(r"(\$\$.*?\$\$)", seg, flags=re.S)
        bits[::2] = [re.sub(r"\\?(?<!\$)\$(?!\$)", r"\\\\$", b) for b in bits[::2]]
        return "".join(bits)

    parts = CODE.split(text)
    for i in range(0, len(parts), 2):
        s = CITE_RUN.sub(cite_run, parts[i])
        s = WIKI.sub(wiki, s)
        parts[i] = math(s)
    text = re.sub(r"\n{3,}", "\n\n", "".join(parts))

    missing = [k for k in order if k not in bib]
    if missing:
        sys.exit("citekeys not in .bib: " + ", ".join(missing))
    if order:
        text = text.rstrip() + "\n\n## References\n\n" + "".join(
            f"{n}. {{: #ref-{n}}} {reference(bib[k])}\n" for k, n in order.items())
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("note", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--kind", choices=["essay", "book-notes"], default="essay")
    ap.add_argument("--bib", type=Path, help="default: NOTE with .bib extension, if it exists")
    a = ap.parse_args()

    bibfile = a.bib or a.note.with_suffix(".bib")
    bib = parse_bib(bibfile.read_text(encoding="utf-8")) if bibfile.exists() else {}
    if a.bib and not bib:
        sys.exit(f"no entries read from {a.bib}")

    template = (Path(__file__).resolve().parent.parent / "_drafts" / f"_template-{a.kind}.md").read_text(encoding="utf-8")
    title = a.note.stem.replace("\\", "\\\\").replace('"', '\\"')
    front = template.replace('title: ""', f'title: "{title}"', 1)
    body = convert_text(a.note.read_text(encoding="utf-8"), bib)

    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", a.note.stem).encode("ascii", "ignore").decode().lower()).strip("-")
    out = a.outdir / f"{slug}.md"
    if out.exists():
        sys.exit(f"{out} exists")
    out.write_text(front.rstrip() + "\n\n" + body.lstrip(), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
