---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
<!--   <ul>{% for post in site.education reversed %} -->
<!--     {{ post.qualification }} -->
<!--   {% endfor %}</ul> -->
<!-- Education test -->
  <ul>
    {% for qualification in site.education reversed %}
      <li>{{ qualification }}</li>
    {% endfor %}
  </ul>

Work experience
======
  
Skills
======

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Service and leadership
======
