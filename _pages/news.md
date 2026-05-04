---
layout: single
title: "News"
permalink: /news/
author_profile: true
---

<ul>
{% for item in site.data.news limit:5 %}
  <li>
    <strong>{{ item.date }}</strong> —
    {% if item.url %}
      <a href="{{ item.url }}">{{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</a>
    {% else %}
      {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}
    {% endif %}
  </li>
{% endfor %}
</ul>