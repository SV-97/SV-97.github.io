---
layout: archive
title: Posts
permalink: /archive/
collection: posts
entries_layout: grid
author_profile: false
---

{% for post in site.posts %}
  {% unless post.hidden %}
    {% include archive-single.html %}
  {% endunless %}
{% endfor %}
