---
layout: archive
title: "Datasets"
description: "Open simulation datasets from Florian Blanc's research on molecular machines."
permalink: /datasets/
author_profile: true
---

I have made several simulation datasets publicly available:

{% include base_path %}

{% for post in site.datasets reversed %}
  {% include archive-single.html %}
{% endfor %}
