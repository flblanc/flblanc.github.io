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
           alt="{{ post.title }}">
    </a>
  </div>
  <div class="publication-content">
    <h3><a href="{{ post.paperurl }}">{{ post.title }}</a></h3>
    <p><em>{{ post.venue }}, {{ post.date | date: "%Y" }}</em></p>
    <p>{{ post.summary | strip_html | truncatewords: 300 }}</p>
    <p><strong>Authors:</strong> {{ post.authors | replace: '<b>', '' | replace: '</b>', '' | replace: '<i>', '' | replace: '</i>', '' }}</p>
    <p>
      <a href="{{ post.doi }}">DOI</a>
      <a href="/files/publications/{{ post.permalink | split: '/' | last }}.pdf">PDF</a>
    </p>
  </div>
</div>
{% endfor %}