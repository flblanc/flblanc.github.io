---
layout: archive
title: "Publications"
description: "Publications by Florian Blanc on molecular dynamics, ATP synthase, myosin and integrative structural biology."
permalink: /publications/
author_profile: true
# Legend for the trainee mark; the symbol is TRAINEE_MARK in tools/build_publications.py. Shown only when filled.
trainee_legend: "Trainee under my supervision"
---

<link rel="stylesheet" href="/assets/css/publications.css">

{% if page.trainee_legend != "" %}
<p class="publication-legend">☉ {{ page.trainee_legend }}</p>
{% endif %}

{% for post in site.publications reversed %}
<div class="publication-card">

  <div class="publication-header">
    <h3 class="publication-title">
      <a href="{{ post.permalink }}">{{ post.title }}</a>
    </h3>
    <p class="publication-authors">{{ post.authors | join: ", " }}</p>
    <p class="publication-venue"><em>{{ post.venue }}</em>, {{ post.date | date: "%Y" }}</p>
    <p class="publication-links">
      <a href="{{ post.paperurl }}">URL</a>
      {% if post.pdf != "" %}&nbsp;|&nbsp;
      <a href="{{ post.pdf }}">PDF</a>{% endif %}
    </p>
  </div>

  {% if post.image != "" or post.video != "" or post.summary != "" %}
  <div class="publication-body">
    {% if post.video != "" %}
    <div class="publication-image">
      <a href="{{ post.permalink }}">
        <video src="{{ post.video }}"{% if post.image != "" %} poster="{{ post.image }}"{% endif %} autoplay muted loop playsinline aria-label="{{ post.title }}"></video>
      </a>
      {% if post.video_credit != "" %}<p class="publication-credit">{{ post.video_credit }}</p>{% endif %}
    </div>
    {% elsif post.image != "" %}
    <div class="publication-image">
      <a href="{{ post.permalink }}">
        <img src="{{ post.image }}" alt="{{ post.title }}">
      </a>
    </div>
    {% endif %}
    {% if post.summary != "" %}
    <div class="publication-summary">
      {{ post.summary | markdownify }}
    </div>
    {% endif %}
  </div>
  {% endif %}

</div>
{% endfor %}