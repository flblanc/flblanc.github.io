---
layout: archive
title: "Posts by Tags"
permalink: /rare-events/tags/
author_profile: true
---

{% assign tag_names = "" | split: "" %}
{% for tag in site.tags %}{% assign tag_names = tag_names | push: tag[0] %}{% endfor %}

{% assign tag_names = tag_names | sort_natural %}
{% for tag in tag_names %}
  <h2 id="{{ tag | slugify }}" class="archive__subtitle">{{ tag }}</h2>
  {% for post in site.tags[tag] %}
    {% include rare-events-item.html %}
  {% endfor %}
{% endfor %}
