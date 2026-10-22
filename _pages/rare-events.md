---
layout: archive
title: "Rare Events"
permalink: /rare-events/
author_profile: true
---

<!-- TEXT: short note identifying this section as personal writing -->
Personal writings.

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
  <h2 id="{{ year.name }}" class="archive__subtitle">{{ year.name }}</h2>
  {% for post in year.items %}
    {% include rare-events-item.html %}
  {% endfor %}
{% endfor %}
