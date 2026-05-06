---
layout: archive
title: "Publications"
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
      <a href="{{ post.paperurl }}">DOI</a>
      &nbsp;|&nbsp;
      <a href="/files/publications/{{ post.permalink | split: '/' | last }}.pdf">PDF</a>
    </p>
  </div>

  <div class="publication-body">
    <div class="publication-image">
      <a href="{{ post.permalink }}">
        <img src="/images/publications/{{ post.permalink | split: '/' | last }}.png"
             alt="{{ post.title }}">
      </a>
    </div>
    <div class="publication-summary">
      {{ post.summary }}
    </div>
  </div>

</div>
{% endfor %}