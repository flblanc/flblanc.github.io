---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
# Number of items in the news block; see _includes/home-news.html
home_news_count: 4
---

<link rel="stylesheet" href="{{ '/assets/css/home.css' | relative_url }}">

{% comment %}
  PAGE ORDER follows the content brief's message sequence:
    1. Identity                      -> lead paragraph below
    2. Track record  (motor line)    -> _data/research.yml, entry `motors`
    3. Current question (disorder)   -> same entry, `cases`
    4. The gap                       -> same entry, `note`
    5. Silver-binding line           -> _data/research.yml, entry `silver`
    6. Link between the two lines    -> connective line below
    7. Close                         -> closing line below
  Standing site furniture (recruitment note, news) follows after.

  News items flagged `landing: false` in _data/news.yml are hidden here but
  still shown on /news/, so the front page stays on-message.

  Key papers are rendered inside the research line they support, not in a
  separate highlights block.

  OFF THIS PAGE by decision: SARS-CoV-2 work, ML/methods work, and one-off
  collaborations (peroxiredoxin, TNAP, lignin). They remain on /publications/.
  The previous version of this intro mentioned SARS-CoV-2 and machine
  learning; that text is preserved in git history on `master` if needed.
{% endcomment %}

<!-- TEXT: affiliation line (kept verbatim from the previous version) -->
I am a **CNRS Research Scientist** at the [Institut des Sciences Analytiques](https://www.isa-lyon.fr/), France, where I am part of the interdisciplinary [**Biophysics of Complex Systems**](https://nmrbiolchem.univ-lyon1.fr/) team.

<!-- TEXT (brief message 1 — identity): you study how molecular motors work,
     using molecular simulation to extract general functional principles.
     Two or three sentences; this is the first thing a committee reads. -->

<!-- Research lines: motor line (primary) then silver-binding line (secondary).
     Content and key papers: _data/research.yml -->
{% include home-research.html %}

<!-- TEXT (brief message 6 — the link): both lines draw on your expertise in
     disordered and flexible proteins, and this is where that expertise was
     built. One or two sentences. -->

<!-- TEXT (brief message 7 — close): simulation coupled with experimental
     collaborators; CNRS, ISA Lyon. One or two sentences. -->

<!-- TEXT: recruitment note, 1-2 lines, linking /application-advice/ and /open-positions/ (kept verbatim from the previous version) -->
If you are a student curious about how molecules work at the atomic scale, and how we can use computers to understand this, I would love to hear from you.
Read my [advice for applicants](/application-advice/) to get an idea of what I expect and how I like to work. If this looks like a fit, check out our [open positions](/open-positions/) or contact me directly at <a href="mailto:florian&#46;blanc&#64;cnrs&#46;fr">florian.blanc [at] cnrs [dot] fr</a> !
{: .notice}

<!-- Latest news, from _data/news.yml -->
{% include home-news.html %}
