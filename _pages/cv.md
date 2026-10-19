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

# Education

{% comment %}Generated from _data/cv/education.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.education %}{% unless e.hide or e.web == false %}
* **{{ e.title }}**, {{ e.organization }}, {{ e.dates | split: " " | last }}{% endunless %}{% endfor %}

# Qualification

<!-- TEXT: qualification -->

# Experience

{% comment %}Generated from _data/cv/experience.yml (also used for the PDF CV){% endcomment %}
{% for e in site.data.cv.experience %}{% unless e.hide %}
* **{{ e.dates }}: {{ e.title }}**
  * {{ e.organization }}, {{ e.location }}
{% for item in e.items %}  * {{ item }}
{% endfor %}{% endunless %}{% endfor %}

# Funding and resources

<!-- TEXT: funding and resources -->

# Supervision

<!-- TEXT: optional intro; the list below is generated from _team/ -->

{% assign supervised = site.team | sort: "start" | reverse %}
{% include team-compact.html members=supervised %}

# Teaching

<!-- TEXT: optional intro; the list below is generated from _teaching/ -->

{% assign courses = site.teaching | sort: "date" | reverse %}
<ul>
{% for course in courses %}
  <li><a href="{{ course.url }}">{{ course.title }}</a>, {{ course.type }}, <i>{{ course.venue }}</i>, {{ course.date | date: "%Y" }}</li>
{% endfor %}
</ul>

# Invited talks

<!-- TEXT: invited talks -->

# Reviewing

<!-- TEXT: reviewing -->

# Collective responsibilities

<!-- TEXT: collective responsibilities -->
