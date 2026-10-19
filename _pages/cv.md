---
layout: archive
title: ""
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

![](/images/CV_frise_chronologique.png)

Download my detailed CV [here](/files/FlorianBlanc_CV.pdf).

# Research interests

{% comment %}Generated from _data/cv/interests.yml (also used for the PDF CV){% endcomment %}
{{ site.data.cv.interests | join: ", " }}

# Education

{% comment %}Generated from _data/cv/education.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.education %}{% unless e.hide or e.web == false %}
* **{{ e.title }}**, {{ e.organization }}, {{ e.dates | split: " " | last }}{% endunless %}{% endfor %}

# Qualification

{% comment %}Generated from _data/cv/qualification.yml (also used for the PDF CV){% endcomment %}
{% for line in site.data.cv.qualification %}
* {{ line }}
{%- endfor %}

# Experience

{% comment %}Generated from _data/cv/experience.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.experience %}{% unless e.hide %}
* **{{ e.dates }}: {{ e.title }}**
  * {{ e.organization }}, {{ e.location }}
{% for item in e.items %}  * {{ item }}
{% endfor %}{% endunless %}{% endfor %}

# Funding and resources

{% comment %}Generated from _data/cv/funding.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.funding %}{% unless e.hide %}
* **{% if e.dates %}{{ e.dates }}: {% endif %}{{ e.title }}**{% if e.role %} ({{ e.role }}){% endif %}
{%- for item in e.items %}
  * {{ item }}
{%- endfor %}
{%- endunless %}{% endfor %}

# Supervision

<!-- TEXT: optional intro; the list below is generated from _team/ -->

{% assign supervised = site.team | sort: "start" | reverse %}
{% include team-compact.html members=supervised %}

# Teaching

<!-- TEXT: optional intro; the list below is generated from _teaching/ -->

{% assign courses = site.teaching | sort: "date" | reverse %}
<ul>
{% for course in courses %}
  <li><a href="{{ course.url }}">{{ course.title }}</a>{% if course.title_en %} ({{ course.title_en }}){% endif %}, {{ course.type }}, <i>{{ course.venue }}</i>, {% if course.dates %}{{ course.dates }}{% else %}{{ course.date | date: "%Y" }}{% endif %}</li>
{% endfor %}
</ul>

# Invited talks

{% comment %}Generated from _data/talks.yml (also shown on /talks/){% endcomment %}
{% include talks-list.html kind="invited" %}

# Reviewing

{% comment %}Generated from _data/cv/reviewing.yml (also used for the PDF CV){% endcomment %}
{% for line in site.data.cv.reviewing %}
* {{ line }}
{%- endfor %}

# Collective responsibilities

{% comment %}Generated from _data/cv/collective.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.collective %}{% unless e.hide %}
* **{% if e.dates %}{{ e.dates }}: {% endif %}{{ e.title }}**
{%- if e.organization or e.location %}
  * {{ e.organization }}{% if e.organization and e.location %}, {% endif %}{{ e.location }}
{%- endif %}
{%- for item in e.items %}
  * {{ item }}
{%- endfor %}
{%- endunless %}{% endfor %}

# Skills

{% comment %}Generated from _data/cv/skills.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.skills %}
* **{{ e.type }}**: {{ e.skills }}
{%- endfor %}
