---
layout: archive
title: "Team"
permalink: /team/
author_profile: true
# TEXT: optional page description (used by search engines)
# TEXT: block headings; leave empty to hide a heading
current_heading: ""
open_heading: ""
past_heading: ""
---

<link rel="stylesheet" href="/assets/css/team.css">

<!-- TEXT: optional intro -->

{% assign current = site.team | where: "status", "current" | sort: "start" | reverse %}
{% assign past = site.team | where: "status", "past" | sort: "start" | reverse %}

{% if current.size > 0 %}
{% if page.current_heading != "" %}<h2>{{ page.current_heading }}</h2>{% endif %}
{% for m in current %}
<div class="team-member">
  <h3 class="team-name">{{ m.name }}</h3>
  {% for s in m.stages %}
  <div class="team-stage">
    <p class="team-stage-title"><strong>{{ s.level }}</strong>{% if s.dates and s.dates != "" %}, {{ s.dates }}{% endif %}</p>
    {% if s.topic and s.topic != "" %}<p class="team-topic">{{ s.topic | markdownify | remove: '<p>' | remove: '</p>' | strip }}</p>{% endif %}
    <p class="team-details">
      {% if s.role and s.role != "" %}<span>Role: {{ s.role }}</span>{% endif %}
      {% if s.co_supervisors and s.co_supervisors != "" %}<span>Co-supervisors: {{ s.co_supervisors | markdownify | remove: '<p>' | remove: '</p>' | strip }}</span>{% endif %}
      {% if s.funding and s.funding != "" %}<span>Funding: {{ s.funding | markdownify | remove: '<p>' | remove: '</p>' | strip }}</span>{% endif %}
    </p>
  </div>
  {% endfor %}
</div>
{% endfor %}
{% endif %}

{% if site.open-positions.size > 0 %}
{% if page.open_heading != "" %}<h2>{{ page.open_heading }}</h2>{% endif %}
<ul class="team-open">
{% for post in site.open-positions %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>
{% endif %}

{% if past.size > 0 %}
{% if page.past_heading != "" %}<h2>{{ page.past_heading }}</h2>{% endif %}
<ul class="team-past">
{% for m in past %}
  <li><strong>{{ m.name }}</strong>
  {%- for s in m.stages %}{% if forloop.first %} — {% else %}; {% endif %}{{ s.level }}{% if s.dates and s.dates != "" %}, {{ s.dates }}{% endif %}{% if s.topic and s.topic != "" %}: {{ s.topic | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% endif %}{% if s.role and s.role != "" %} ({{ s.role }}){% endif %}{% endfor %}</li>
{% endfor %}
</ul>
{% endif %}
