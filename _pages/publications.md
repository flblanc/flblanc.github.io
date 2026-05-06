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
}
.publication-image img {
  width: 100%;
  height: auto;
  border-radius: 4px;
}
</style>
 
{% for post in site.publications reversed %}
<div class="publication-card">
  <div class="publication-image">
    <a href="{{ post.permalink }}">
      <img src="/images/publications/{{ post.permalink | split: '/' | last }}.png"
           alt="{{ post.title }}">
    </a>
  </div>
  <div class="publication-content">
    <h3 class="publication-title"><a href="{{ post.permalink }}">{{ post.title }}</a>
    </h3>
    <p>{{ post.authors | join: ", " }}</p>
    <p><em>{{ post.venue }}, {{ post.date | date: "%Y" }}</em></p>
    <p>{{ post.summary | strip_html }}</p>
    <p>
      <a href="{{ post.paperurl }}">URL</a>
      <a href="/files/publications/{{ post.permalink | split: '/' | last }}.pdf">PDF</a>
    </p>
  </div>
</div>
{% endfor %}
