#!/usr/bin/env python3
# Obsidian notes -> Rare Events posts. Converts every _notes/*.md (run locally or by the
# "Rare Events posts" Action); edit the notes, never the generated files.
#   front matter: the note's Properties, passed through (title defaults to the filename,
#     kind to essay); publish: true + date -> _posts/DATE-slug.md, otherwise _drafts/slug.md
#   [[Name]], [[Name|alias]], [[Note#Section]] -> plain text as Obsidian displays it
#   [[citekey]] (lowercase surname + Words + year) -> numbered citation linked to ## References,
#     resolved from _notes/blog-posts.bib
#   inline $x$ -> $$x$$ (kramdown math); blank lines around display $$ blocks; other $ escaped
# Generated files carry `source_note:`; those whose note is gone or moved are deleted.
# usage: obsidian2post.py [NOTES_DIR]   (default: _notes next to tools/)

import re, sys, unicodedata
from pathlib import Path

CITEKEY = re.compile(r"[a-z][A-Za-z-]*[A-Z][A-Za-z]*\d{4}[a-z]?")
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


def rel(p, root):
    return p.relative_to(root).as_posix() if p.is_relative_to(root) else p.as_posix()


def scalar(front, key):
    m = re.search(rf"^{key}:[ \t]*(.*?)[ \t]*$", front, re.M)
    return m.group(1).strip("'\"") if m else ""


def build(note, bib, root):
    text = note.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?\n)---[ \t]*\n", text, re.S)
    front, body = (m.group(1), text[m.end():]) if m else ("", text)
    front = WIKI.sub(lambda w: display(*w.group(2).partition("|")[::2]) if "|" in w.group(2) else display(w.group(2), None), front)
    publish, date = scalar(front, "publish").lower() == "true", scalar(front, "date")[:10]
    front = re.sub(r"^(publish:.*|date:[ \t]*)\n", "", front, flags=re.M)
    if not scalar(front, "title"):
        front = re.sub(r"^title:.*\n", "", front, flags=re.M)
        front = 'title: "' + note.stem.replace("\\", "\\\\").replace('"', '\\"') + '"\n' + front
    if not scalar(front, "kind"):
        front = re.sub(r"^kind:.*\n", "", front, flags=re.M) + "kind: essay\n"
    front += f'source_note: "{rel(note, root)}"\n'

    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", note.stem).encode("ascii", "ignore").decode().lower()).strip("-")
    if publish:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            raise ValueError("publish: true needs date: YYYY-MM-DD")
        out = root / "_posts" / f"{date}-{slug}.md"
    else:
        out = root / "_drafts" / f"{slug}.md"
    return out, "---\n" + front + "---\n\n" + convert_text(body, bib).lstrip()


def main():
    root = Path(__file__).resolve().parent.parent
    notes = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / "_notes"
    bibfile = notes / "blog-posts.bib"
    bib = parse_bib(bibfile.read_text(encoding="utf-8")) if bibfile.exists() else {}

    old = {}
    for f in [*(root / "_drafts").glob("*.md"), *(root / "_posts").glob("*.md")]:
        m = re.search(r'^source_note: "(.*)"$', f.read_text(encoding="utf-8"), re.M)
        if m:
            old.setdefault(m.group(1), []).append(f)

    written, failed = set(), set()
    for note in sorted(notes.glob("*.md")):
        if note.name.startswith("_"):
            continue
        src = rel(note, root)
        try:
            out, text = build(note, bib, root)
        except (ValueError, SystemExit) as e:
            print(f"{src}: {e}", file=sys.stderr)
            failed.add(src)
            continue
        if out in written:
            print(f"{src}: {out.name} already written by another note", file=sys.stderr)
            failed.add(src)
            continue
        if out.exists() and out not in old.get(src, []):
            print(f"{src}: {out.relative_to(root)} exists and was not generated from this note", file=sys.stderr)
            failed.add(src)
            continue
        out.parent.mkdir(exist_ok=True)
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            out.write_text(text, encoding="utf-8")
            print(f"wrote {out.relative_to(root)}")
        written.add(out)

    for src, files in old.items():
        for f in files:
            if f not in written and src not in failed:
                f.unlink()
                print(f"removed {f.relative_to(root)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
