#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'David León'
SITENAME = 'Sitio Web de David León'
SITEURL = 'http://www.davfl.com.mx'

PATH = 'content'

TIMEZONE = 'America/Mexico_City'

DEFAULT_LANG = 'es'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = [os.path.dirname(os.path.abspath(__file__)) + '/pelican-plugins']

PLUGINS = ['sitemap']

SITEMAP = { 'format': 'xml' }

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = os.path.dirname(os.path.abspath(__file__)) + '/themes/davfl'
