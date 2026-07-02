#!/usr/bin/env python3
"""
5. Add missing internal links to fix zero-inbound and zero-outbound guides.

Zero inbound (no other guide links to them):
  - one-sided-friendship
  - how-to-keep-work-friendships-after-going-remote
  - how-to-make-friends-after-30

Zero outbound (they link to no other guide):
  - friendship-quotes
  - how-to-follow-up-after-meeting-someone
  - how-to-introduce-friends-to-each-other
  - how-to-make-friends-as-an-expat
  - how-to-make-friends-when-you-work-from-home
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def section(slug, h2):
    for g in data["guides"]:
        if g["slug"] == slug:
            for s in g.get("sections", []):
                if s["h2"] == h2:
                    return s
    raise KeyError(f"{slug} / {h2}")

errors = []

# Each tuple: (slug, h2, appended_sentence)
# Sentence is appended as a new final paragraph in that section's paragraphs list.
ADDITIONS = [
    # ── Fix zero-outbound: how-to-follow-up-after-meeting-someone ────────────
    # → links to how-to-turn-acquaintances-into-friends (natural next step)
    (
        "how-to-follow-up-after-meeting-someone",
        "What happens after the follow-up",
        'Once the follow-up has created a second meeting, the work shifts to deepening the connection. See <a href="/guides/how-to-turn-acquaintances-into-friends/">how to turn acquaintances into friends</a> for the specific moves that cross that gap.',
    ),
    # ── Fix zero-outbound: how-to-introduce-friends-to-each-other ────────────
    # → links to how-to-make-friends-as-an-adult
    (
        "how-to-introduce-friends-to-each-other",
        "A denser network means less maintenance for everyone",
        'Making introductions is one tool inside a broader approach to adult friendship. For the full picture, see <a href="/guides/how-to-make-friends-as-an-adult/">how to make friends as an adult</a>.',
    ),
    # ── Fix zero-outbound: how-to-make-friends-as-an-expat ───────────────────
    # → links to how-to-make-friends-after-30 (fixes its zero-inbound too)
    (
        "how-to-make-friends-as-an-expat",
        "Do not wait to be invited",
        'The skills that work for expats, choosing recurring environments, following up consistently, and not waiting for the perfect moment, are the same ones that work in any adult context. See <a href="/guides/how-to-make-friends-after-30/">how to make friends after 30</a> for how they apply to adult life more broadly.',
    ),
    # ── Fix zero-outbound: how-to-make-friends-when-you-work-from-home ───────
    # → links to how-to-keep-work-friendships-after-going-remote (fixes its zero-inbound)
    (
        "how-to-make-friends-when-you-work-from-home",
        "Online communities can be a starting point, not an endpoint",
        'If you already have work friendships from a previous office job and are trying to maintain them remotely, that is a separate and more specific challenge. See <a href="/guides/how-to-keep-work-friendships-after-going-remote/">how to keep work friendships after going remote</a>.',
    ),
    # ── Fix zero-outbound: friendship-quotes ─────────────────────────────────
    # → links to how-to-make-friends-as-an-adult
    (
        "friendship-quotes",
        "On what builds closeness",
        'For how these ideas translate into daily practice, the most direct guide is <a href="/guides/how-to-make-friends-as-an-adult/">how to make friends as an adult</a>.',
    ),
    # ── Fix zero-inbound: one-sided-friendship ────────────────────────────────
    # → link FROM how-to-keep-friends-as-an-adult / "Do not confuse warmth with maintenance"
    (
        "how-to-keep-friends-as-an-adult",
        "Do not confuse warmth with maintenance",
        'If you find that you are consistently the one initiating, the one following up, and the one making plans, the problem may go beyond maintenance habits. See <a href="/guides/one-sided-friendship/">what to do when a friendship feels one-sided</a>.',
    ),
    # ── Fix zero-inbound: how-to-make-friends-after-30 ───────────────────────
    # → link FROM why-making-friends-as-an-adult-is-hard / "Friendship competes with everything else"
    (
        "why-making-friends-as-an-adult-is-hard",
        "Friendship competes with everything else",
        'If you are specifically in your thirties and wondering whether the window has closed, see <a href="/guides/how-to-make-friends-after-30/">how to make friends after 30</a>.',
    ),
]

for slug, h2, sentence in ADDITIONS:
    try:
        s = section(slug, h2)
    except KeyError as e:
        errors.append(f"Not found: {e}")
        continue
    paras = s.setdefault("paragraphs", [])
    paras.append(sentence)
    print(f"  + link: {slug} / {h2}")

if errors:
    print(f"\nErrors:")
    for e in errors:
        print(f"  ERROR: {e}")
    import sys; sys.exit(1)

out = os.path.join(ROOT, "seo-pages.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nseo-pages.json updated: {len(ADDITIONS)} internal links added.")
