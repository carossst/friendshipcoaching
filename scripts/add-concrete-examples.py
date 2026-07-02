#!/usr/bin/env python3
"""
Add concrete activity examples (Pickleball, volunteering, associations)
to guide sections that currently use generic lists.
Edits are minimal — slipping examples into existing list-style sentences.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def guide(slug):
    for g in data["guides"]:
        if g["slug"] == slug:
            return g
    raise KeyError(slug)

def section(g, h2_substr):
    for s in g.get("sections", []):
        if h2_substr.lower() in s["h2"].lower():
            return s
    raise KeyError(f"No section matching '{h2_substr}' in {g['slug']}")

changed = []

# ─────────────────────────────────────────────────────────────
# 1. how-to-make-friends-as-an-adult / "Start with places" P2
# Add concrete examples to the "pick one recurring context" sentence
# ─────────────────────────────────────────────────────────────
g = guide("how-to-make-friends-as-an-adult")
s = section(g, "Start with places")
s["paragraphs"][2] = (
    "Pick one recurring context and commit to showing up for at least a month. "
    "A Pickleball court, a running club, a weekly volunteer shift, a neighborhood "
    "association, a community class. The goal is not to make friends on the first day. "
    "The goal is to be there enough times that familiarity starts doing its work."
)
changed.append("how-to-make-friends-as-an-adult / Start with places / P2")

# ─────────────────────────────────────────────────────────────
# 2. how-to-meet-people-in-a-new-city / "Choose places where you can return" P0
# Expand the generic list with associations + concrete sentence
# ─────────────────────────────────────────────────────────────
g2 = guide("how-to-meet-people-in-a-new-city")
s = section(g2, "places where you can return")
s["paragraphs"][0] = (
    "The fastest way to feel less alone in a new city is to stop chasing one-off "
    "encounters and start choosing repeatable environments. Sports leagues, volunteer "
    "organizations, neighborhood associations, classes, coworking spaces, language "
    "exchanges, and recurring community events work better than random big nights out. "
    "A Pickleball club, a weekly food bank shift, a community garden, a running group: "
    "the specific format matters less than the fact that it brings the same people "
    "together on a predictable schedule."
)
changed.append("how-to-meet-people-in-a-new-city / places where you can return / P0")

# ─────────────────────────────────────────────────────────────
# 3. how-to-meet-people-in-a-new-city / "Become a regular somewhere" P0
# Add Pickleball, neighborhood association, volunteer project to the list
# ─────────────────────────────────────────────────────────────
s = section(g2, "regular somewhere")
s["paragraphs"][0] = (
    "A city becomes less anonymous when your face is recognized. That can happen at a "
    "cafe, a class, a Pickleball court, a climbing gym, a neighborhood association "
    "meeting, a volunteer project, or a community walking group. Regularity creates "
    "familiarity, and familiarity makes social interaction easier."
)
changed.append("how-to-meet-people-in-a-new-city / regular somewhere / P0")

# ─────────────────────────────────────────────────────────────
# 4. how-to-make-friends-when-you-work-from-home / "Choose one recurring context" P0
# Add Pickleball, volunteer shift, association to the list
# ─────────────────────────────────────────────────────────────
g3 = guide("how-to-make-friends-when-you-work-from-home")
s = section(g3, "recurring context")
s["paragraphs"][0] = (
    "The most effective move for remote workers is to pick one activity that happens "
    "on a regular schedule and show up consistently for at least two months. A Pickleball "
    "club, a weekly volunteer shift at a local organization, a neighborhood association, "
    "a community class, a coworking space on the same days each week. The format does "
    "not matter. The regularity does."
)
changed.append("how-to-make-friends-when-you-work-from-home / recurring context / P0")

# ─────────────────────────────────────────────────────────────
# 5. how-to-make-friends-after-30 / "Use repeated environments" P0
# Add Pickleball and associations to the list
# ─────────────────────────────────────────────────────────────
g4 = guide("how-to-make-friends-after-30")
s = section(g4, "repeated environments")
s["paragraphs"][0] = (
    "If you want new friends after 30, one-off social luck is usually not enough. "
    "Repeated environments work better: sports leagues, volunteer organizations, "
    "neighborhood associations, parent communities, classes, professional communities, "
    "or regular local events. A Pickleball game every Sunday, a monthly neighborhood "
    "association meeting, a standing volunteer shift at a food bank: these are the "
    "kinds of structures that turn strangers into familiar faces."
)
changed.append("how-to-make-friends-after-30 / repeated environments / P0")

# ─────────────────────────────────────────────────────────────
# 6. how-men-can-rebuild-friendships / "Pick one recurring activity" P0
# Add Pickleball and volunteer to the example list
# ─────────────────────────────────────────────────────────────
g5 = guide("how-men-can-rebuild-friendships")
s = section(g5, "recurring activity")
s["paragraphs"][0] = (
    "Research shows it takes roughly 50 hours of shared time to develop a genuine close "
    "friendship. For most adults over 30, that number sounds impossible. But broken down "
    "into a recurring activity, a weekly Pickleball game, a monthly golf round, a regular "
    "Sunday run, a volunteer shift that repeats, it becomes manageable over a few months. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-men-can-rebuild-friendships / recurring activity / P0")

# ─────────────────────────────────────────────────────────────
# 7. why-male-friendships-fade / "What actually works" P1
# Add Pickleball to the recurring activities examples
# ─────────────────────────────────────────────────────────────
g6 = guide("why-male-friendships-fade")
s = section(g6, "What actually works")
s["paragraphs"][1] = (
    "Research shows it takes around 50 hours of shared time to build a genuine close "
    "friendship. A Pickleball game every Sunday, a recreational sports league, a standing "
    "lunch: these are the conditions under which real friendship happens, not substitutes "
    "for it. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("why-male-friendships-fade / What actually works / P1")

# ─────────────────────────────────────────────────────────────
# 8. how-to-make-friends-as-an-expat / "Find recurring contexts in local life" P1
# Add Pickleball and neighborhood association to the list
# ─────────────────────────────────────────────────────────────
g7 = guide("how-to-make-friends-as-an-expat")
s = section(g7, "recurring contexts")
s["paragraphs"][1] = (
    "The most reliable way to meet locals is through repeated shared activity: a sports "
    "team, a Pickleball or tennis club, a class, a neighborhood association, a volunteer "
    "project, a professional community with a social dimension. Something where you see "
    "the same faces week after week."
)
changed.append("how-to-make-friends-as-an-expat / recurring contexts / P1")

# ─────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────
out = os.path.join(ROOT, "seo-pages.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Applied {len(changed)} example insertions:\n")
for c in changed:
    print(f"  {c}")
