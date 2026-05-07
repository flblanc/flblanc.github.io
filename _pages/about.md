---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am a **CNRS Research Scientist** at the [Institut des Sciences Analytiques](https://www.isa-lyon.fr/), France, where I am part of the interdisciplinary [**Biophysics of Complex Systems**](http://nmrbiolchem.univ-lyon1.fr/) team. 

In my research, I use computer simulations to study how molecules move and interact. This helps understand biological and chemical processes at the atomic scale.  


My work sits at the intersection of **computational molecular biophysics**, **physical chemistry**, and **integrative structural biology**. 
My goal is to understand how the fast, near-random motions of atoms and molecules give rise to function, whether in biological systems or complex chemical assemblies.
 

To do this, I combine:
 - **Molecular dynamics simulations** to model how molecules behave over time and predict their properties.
 - **Machine learning** to extract patterns from complex simulation data.
 - **Experimental biophysics**  to connect my simulations to real-world measurements, thanks to top-notch collaborators in NMR, Cryo-EM and X-ray crystallography. 

The systems I study range from short **peptides** to large **molecular machines** (myosin, ATP synthase), with the occasional venture into **supra-molecular chemistry**.  I’ve also worked on the SARS-CoV-2 spike protein in the early days of the Covid-19 pandemic, 
helping to map its conformational dynamics and identify target sites for vaccines. More recently, I started to explore how **deep learning** can help us integrate experiments with simulations.

If you are a student curious about how molecules work at the atomic scale, and how we can use computers to understand this, I would love to hear from you.
Check out our [open positions](/open-positions/) or contact me directly at <a href="mailto:florian&#46;blanc&#64;cnrs&#46;com">florian.blanc [at] cnrs [dot] com</a>.


## [News](/news/)

<ul>
{% for item in site.data.news limit:8 %}
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



