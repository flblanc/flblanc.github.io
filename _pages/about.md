---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am a **CNRS Research Scientist** in the [**Biophysics of Complex Systems**](http://nmrbiolchem.univ-lyon1.fr/) team at [Institut des Sciences Analytiques](https://www.isa-lyon.fr/), France. I study how molecules move with computer simulations.


My research falls under **computational molecular biophysics**, **physical chemistry**, and **integrative structural biology**.

My motivation is to understand how **biomolecular function** emerges from **structural dynamics** by describing the **atomically-detailed mechanisms** involved. 
For this, I combine **molecular dynamics simulations**, **machine learning**, and **experimental biophysics**. 

I investigate **complex molecular mechanisms** in systems ranging from short peptides to large **molecular motors** (myosin, ATP synthase), with the occasional venture into **supra-molecular chemistry**. I also contributed to characterizing the conformational dynamics and 
immunogenic sites of the **SARS-CoV-2 spike protein** in the early days of the Covid-19 pandemic. More recently, I started to explore how to apply **deep learning** methods to the analysis of **biophysical experiments**. 


I am always looking for motivated students to work with,
so check out the [open positions](/open-positions/) or contact me directly at <a href="mailto:florian&#46;blanc&#64;cnrs&#46;com">florian.blanc [at] cnrs [dot] com</a>.


## [News](/news/)

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

[See all news](/news/)



