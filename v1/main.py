#!/usr/bin/env python

from requests_html import HTMLSession
from string import Template
from weasyprint import HTML

session = HTMLSession()

HTML_TEMPLATE = "template.html"

# SLUG = "haiti-pigs-for-kids/"
SLUG = "step-thailand-children-of-night-light-employees"

BASE = "https://www.internationalministries.org/"


def main(slug):
    """
    Runs the main script.
    """
    url = BASE + slug
    print("Fetching {0}".format(url))
    page = session.get(url).html

# make a dictionary of substitutions
    substitutions = {}
    substitutions["TITLE"] = page.find(".post_title > strong", first=True).text

    goal_text = page.find("#campaign_goal .value", first=True).text
    substitutions["GOAL_TEXT"] = goal_text

# attempt at clever parsing to get the goal amount.  Gets $ to next empty space
    start = goal_text.find("$")
    end = goal_text.find(" ", start)
    goal_amount = goal_text[start:end]
    substitutions["GOAL"] = goal_amount if len(goal_amount) > 1 else "Undesignated"

    substitutions["SUMMARY"] = page.find("#campaign_summary .value", first=True).html
    substitutions["IMG"] = page.find(".post_main_image", first=True).attrs.get("src")

# descriptions can be too long.  Only take the first three paragraphs
    description = page.find("#campaign_description .value", first=True).html

    short_description = list(filter(lambda x : x != '', description.splitlines()))
    short_description = "\n\n".join(short_description[:3])
    substitutions["DESCRIPTION"] = short_description

    # substitutions["CAPTION"] = "No idea what to do here.."

    gifts = page.find("#campaign_suggested_gifts .value", first=True)
    substitutions["GIFTS"] = gifts.html if gifts else ""

# not all templates include prayer requests, avoid if they aren't provided
    prayer = page.find("#campaign_prayer_requests .value", first=True)
    prayer = prayer.html if prayer else ""
    substitutions["PRAYER"] = prayer if len(prayer) > 0 and len(prayer) < 200 else ""

    templated = template(substitutions)
    fname = "output/" + slug + ".pdf"
    compile(templated, fname)
    return

def template(defns):
    """
    Accepts the parsed definitions and templates them into the HTML string.

    Returns a templated string.
    """
    with open(HTML_TEMPLATE, "r") as f:
        tmpl = f.read().replace("\n", "")
        templated = Template(tmpl).safe_substitute(defns)
    return templated

def compile(templated, fname):
    """
    Turns the templated HTML file into a PDF and writes it to disk.
    """
    document = HTML(string=templated)
    document.write_pdf(fname)
    print("Wrote output to {0}!".format(fname))

slugs = [
    "rwanda-sewing-machines-stitch-by-stitch",
    "white-cross-india-nine-hospitals-clinics-and-mobile-units",
    "thailand-building-for-nightlight-and-song-sawang-church",
    "nicaragua-healthy-homes",
    "lebanon-insaaf-center",
    "mexico-school-uniforms-and-books",
    "haiti-pigs-for-kids",
    "congo-mitendi-primary-school-annual-fund",
    "haiti-restoring-eyesight-to-children-and-youth",
    "congo-mitendi-womens-center-annual-fund",
    "india-sponsor-indian-baptists-to-attend-summit-2019"
]

for slug in slugs:
    main(slug)
