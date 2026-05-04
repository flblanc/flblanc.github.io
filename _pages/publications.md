---
layout: publications  # Use your new layout
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include base_path %}

<!-- Link to your publications.css -->
<link rel="stylesheet" href="{{ '/assets/css/publications.css'   relative_url }}">

<!-- Loop through publications and render each as a card -->
{% for post in site.publications reversed %}
  {% include archive-single-publication.html %}
{% endfor %}
