---
layout: archive
title: "Publications"
description: "Publications by Florian Blanc on molecular dynamics, ATP synthase, myosin and integrative structural biology."
permalink: /publications/
author_profile: true
---

<link rel="stylesheet" href="/assets/css/publications.css">

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

  {% if post.image != "" or post.summary != "" %}
  <div class="publication-body">
    {% if post.image != "" %}
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