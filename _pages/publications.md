---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

<style>
.publication-card {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  align-items: flex-start;
}
.publication-image img {
  width: 100px;
  height: auto;
  border-radius: 4px;
}
</style>

{% for post in site.publications reversed %}
<div class="publication-card">
  <div class="publication-image">
    <a href="{{ post.paperurl }}">
      <img src="/images/publications/{{ post.permalink | split: '/' | last }}.png"
           alt="Thumbnail for {{ post.title }}">
    </a>
  </div>
  <div class="publication-content">
    <h3><a href="{{ post.paperurl }}">{{ post.title }}</a></h3>
    <p><em>{{ post.venue }}, {{ post.date | date: "%Y" }}</em></p>
    <p>{{ post.content | strip_html | truncatewords: 30 }}</p>
    <p><strong>Authors:</strong> {{ post.citation | replace: '<b>', '' | replace: '</b>', '' | replace: '<i>', '' | replace: '</i>', '' }}</p>
    <p>
      <a href="{{ post.doi }}">DOI</a>
      {% if post.paperurl != post.doi %}
        | <a href="{{ post.paperurl }}">PDF</a>
      {% endif %}
    </p>
  </div>
</div>
{% endfor %}