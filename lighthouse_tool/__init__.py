"""
lighthouse_tool
===============

A small, beginner friendly package that runs a Lighthouse audit on any public
web page (through the Google PageSpeed Insights API), summarises the result and
turns the failed audits into plain-English fix recommendations.

Modules
-------
pagespeed       - talks to the Google PageSpeed Insights API
analyzer        - turns the huge raw JSON response into a small summary dict
recommendations - maps failed Lighthouse audits to human readable fixes
"""

__version__ = "1.0.0"
