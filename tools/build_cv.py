#!/usr/bin/env python3
"""Generate the data-driven sections of the PDF CV from _data/cv/*.yml.

    python3 tools/build_cv.py && (cd cv && xelatex resume.tex)

Each section is written to cv/generated/<section>.tex, which cv/resume.tex
\\input's. The same YAML files are rendered on /cv/ by Liquid, so edit the
YAML, not the generated files (they are git-ignored and rebuilt by the
"Build CV PDF" Action). The publication list comes from the generated
_publications/*.md (see tools/build_publications.py), like the website's.
"""
import glob
import os
import re

import yaml

from build_publications import TRAINEE_MARK

OUT = "cv/generated"
LATEX_SPECIAL = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
                 "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
                 "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"}


def tex(s):
    """Plain text with **bold**, *italic*, [link](url), <sup>, <sub> and <u> -> LaTeX."""
    links = []

    def keep_link(m):
        links.append((m.group(1), m.group(2)))
        return f"\0{len(links) - 1}\0"

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", keep_link, str(s))
    s = "".join(LATEX_SPECIAL.get(c, c) for c in s)
    s = re.sub(r'"([^"]*)"', r"``\1''", s)  # straight quotes -> opening/closing quotes
    s = re.sub(r"<(sup|sub|u)>(.*?)</\1>", lambda m: r"\%s{%s}" % (
        {"sup": "textsuperscript", "sub": "textsubscript", "u": "underline"}[m.group(1)], m.group(2)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*(.+?)\*", r"\\textit{\1}", s)
    return re.sub(r"\0(\d+)\0", lambda m: r"\href{%s}{%s}" % (
        links[int(m.group(1))][1].replace("%", r"\%").replace("#", r"\#"),
        tex(links[int(m.group(1))][0])), s)


def cventry(e):
    items = "".join(f"            \\item {tex(i)}\n" for i in e.get("items", []))
    body = ("\n        \\begin{cvitems}\n" + items +
            "            \\vspace{\\cvvertspace}\n        \\end{cvitems}\n") if items else tex(e.get("description", ""))
    return (f"\\cventry\n    {{{tex(e.get('organization', ''))}}}\n    {{{tex(e.get('title', ''))}}}\n"
            f"    {{{tex(e.get('location', ''))}}}\n    {{{tex(e.get('dates', ''))}}}\n    {{{body}}}%\n")


def experience(entries):
    out = ["\\def \\cvvertspace {2.00mm}\n"]
    for group, heading in (("current", "Current position"), ("research", "Research experience")):
        shown = [e for e in entries if e.get("group") == group and not e.get("hide")]
        if shown:
            out.append(f"\\cvsection{{{heading}}}\n\\begin{{cventries}}%\n")
            out.extend(cventry(e) for e in shown)
            out.append("\\end{cventries}\n")
    return "".join(out)


def education(entries):
    shown = [e for e in entries if not e.get("hide")]
    return ("\\cvsection{Education}\n\\begin{cventries}%\n" +
            "\\vspace{\\cvvertspace}%\n".join(cventry(e) for e in shown) + "\\end{cventries}\n")


def collective(entries):
    shown = [e for e in entries if not e.get("hide")]
    return ("\\cvsection{Collective responsibilities}\n\\begin{cventries}%\n" +
            "".join(cventry(e) for e in shown) + "\\end{cventries}\n")


def interests(items):
    return ("\\cvsection{Research interests}\n\\begin{cventries}\n\n" +
            ", ".join(tex(i).replace(" ", "~") for i in items) + "\n\n\\end{cventries}\n")


def skills(entries):
    return ("\\cvsection{Skills}\n\\begin{cvskills}\n" +
            "".join(f"  \\cvskill\n    {{{tex(e['type'])}}}\n    {{{tex(e['skills'])}}}\n" for e in entries) +
            "\\end{cvskills}\n")


def html_tex(s):
    """Text with the bits of HTML the publication generator emits -> LaTeX; $...$ math is kept."""
    out = []
    for part in re.split(r"(\$[^$]*\$|</?(?:strong|sup|sub|i|em)>)", s):
        if part.startswith("$") and part.endswith("$") and len(part) > 1:
            out.append(part)
        else:
            out.append({"<strong>": r"\underline{", "<sup>": r"\textsuperscript{", "<sub>": r"\textsubscript{",
                        "<i>": r"\textit{", "<em>": r"\textit{"}.get(part, "}" if part.startswith("</") else
                       "".join(LATEX_SPECIAL.get(c, c) for c in part)))
    return "".join(out).replace(TRAINEE_MARK, r"{\symbolfont %s}" % TRAINEE_MARK)


def front_matter(path):
    return yaml.safe_load(open(path, encoding="utf-8").read().split("---", 2)[1])


def publications():
    pubs = sorted((front_matter(p) for p in glob.glob("_publications/*.md")),
                  key=lambda p: str(p["date"]), reverse=True)
    legend = front_matter("_pages/publications.md").get("trainee_legend", "")
    out = ["\\newpage\n\\cvsection{Publications}\n\\hyphenpenalty 10000\n\\singlespace\n\n\\small\n"
           "\\interlinepenalty 10000 % each entry is one paragraph: never split it across pages\n\n"]
    if legend:
        out.append(html_tex(f"{TRAINEE_MARK} {legend}") + "\n\\vskip 0.2cm\n\n")
    for p in pubs:
        out.append(f"\\textbf{{{html_tex(p['title'])}}}\\\\\n"
                   f"{html_tex(', '.join(a for a in p['authors'] if not a.startswith('(')))}"
                   f"{''.join(' ' + html_tex(a) for a in p['authors'] if a.startswith('('))}\\\\\n"
                   f"\\textbf{{\\textit{{{html_tex(p['venue'])}, {str(p['date'])[:4]}}}}}\\\\\n"
                   f"\\url{{{p['paperurl']}}}\n\\vskip 0.1cm\n\n")
    return "".join(out), len(pubs)


def teaching():
    """The entries of the PDF's "Teaching duties" section, from the _teaching/ collection."""
    courses = sorted((front_matter(p) for p in glob.glob("_teaching/*.md")),
                     key=lambda c: str(c["date"]), reverse=True)
    out = ["\\begin{cventries}%\n"]
    for c in courses:
        title = c["title"] + (f" ({c['title_en']})" if c.get("title_en") else "")
        out.append(cventry({"organization": ", ".join(x for x in (c.get("type"), c.get("venue")) if x),
                            "title": title, "location": c.get("location", ""),
                            "dates": c.get("dates", ""), "items": c.get("items", [])}))
    return "".join(out) + "\\end{cventries}\n", len(courses)


def supervision():
    """The PDF's Supervision section, from the _team/ collection (same lines as on /team/ and /cv/)."""
    people = sorted((front_matter(p) for p in glob.glob("_team/[!_]*.md")),
                    key=lambda m: str(m.get("start", "")), reverse=True)
    projects_heading = front_matter("_pages/team.md").get("projects_heading", "")

    def line(m):
        stages = []
        for st in m.get("stages", []):
            text = ", ".join(tex(st[k]) for k in ("level", "dates") if st.get(k))
            if st.get("topic"):
                text += f": {tex(st['topic'])}"
            if st.get("role"):
                text += f" ({tex(st['role'])}" + (f", with {tex(st['co_supervisors'])}" if st.get("co_supervisors") else "") + ")"
            stages.append(text)
        return f"  \\item \\textbf{{{tex(m['name'])}}} --- " + "; ".join(stages) + "\n"

    def block(members):
        return ("\\descriptionstyle{\\begin{cvitems}\n" + "".join(line(m) for m in members) +
                "  \\vspace{\\cvvertspace}\n\\end{cvitems}}\n")

    main = [m for m in people if m.get("kind") != "project"]
    projects = [m for m in people if m.get("kind") == "project"]
    out = ["\\newpage\n\\cvsection{Supervision}\n\\begin{cventries}%\n\\interlinepenalty 10000\n"]
    if main:
        out.append(block(main))
    if projects:
        if projects_heading:
            out.append(f"\\vspace{{\\cvvertspace}}\\makebox[\\linewidth][l]{{\\entrytitlestyle{{{tex(projects_heading)}}}}}\\par\n")
        out.append(block(projects))
    return "".join(out) + "\\end{cventries}\n\\vspace{\\cvvertspace}\n", len(people)


TALK_KINDS = (("invited", "Invited talks"), ("oral", "Oral communications"), ("poster", "Poster presentations"))


def talks():
    """The body of the PDF's Communications section, from _data/talks.yml."""
    data = yaml.safe_load(open("_data/talks.yml", encoding="utf-8")) or []
    out = ["\\interlinepenalty 10000 % never split an entry across pages\n\n"]
    for kind, heading in TALK_KINDS:
        shown = [t for t in data if t.get("kind") == kind]
        if shown:
            out.append(f"\\section*{{{heading}}}\n\n")
        for t in shown:
            line = ", ".join(tex(t[k]) for k in ("label", "venue", "location", "date") if t.get(k))
            if t.get("host"):
                line += f" (invited by {tex(t['host'])})"
            out.append((f"\\textbf{{{tex(t['title'])}}}\\\\\n" if t.get("title") else "") +
                       (f"{tex(t['authors'])}\\\\\n" if t.get("authors") else "") + line + "\n\\vskip 0.1cm\n\n")
    return "".join(out), len(data)


def qualification(lines):
    return "".join(f"{tex(l)}\n\n" for l in lines)


def reviewing(lines):
    return ("\\cvsection{Reviewing}\n\\begin{cventries}%\n\\descriptionstyle{\\begin{cvitems}\n" +
            "".join(f"  \\item {tex(l)}\n" for l in lines) +
            "  \\vspace{\\cvvertspace}\n\\end{cvitems}}\n\\end{cventries}\n\\vspace{\\cvvertspace}\n")


def funding(entries):
    shown = [dict(e, organization=e.get("role", "")) for e in entries if not e.get("hide")]
    return ("\\cvsection{Funding and resources}\n\\begin{cventries}%\n" +
            "".join(cventry(e) for e in shown) + "\\end{cventries}\n")


SECTIONS = {"experience": experience, "education": education, "collective": collective,
            "interests": interests, "skills": skills, "qualification": qualification,
            "reviewing": reviewing, "funding": funding}


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    os.makedirs(OUT, exist_ok=True)
    for name, render in SECTIONS.items():
        data = yaml.safe_load(open(f"_data/cv/{name}.yml", encoding="utf-8")) or []
        with open(f"{OUT}/{name}.tex", "w", encoding="utf-8") as f:
            f.write(f"% GENERATED by tools/build_cv.py from _data/cv/{name}.yml - do not edit\n")
            f.write(render(data))
        print(f"{OUT}/{name}.tex: {sum(not (isinstance(e, dict) and e.get('hide')) for e in data)} entries")
    for name, source, render in (("publications", "_publications/*.md", publications),
                                 ("talks", "_data/talks.yml", talks),
                                 ("teaching", "_teaching/*.md", teaching),
                                 ("supervision", "_team/*.md", supervision)):
        text, n = render()
        with open(f"{OUT}/{name}.tex", "w", encoding="utf-8") as f:
            f.write(f"% GENERATED by tools/build_cv.py from {source} - do not edit\n" + text)
        print(f"{OUT}/{name}.tex: {n} entries")


if __name__ == "__main__":
    main()
