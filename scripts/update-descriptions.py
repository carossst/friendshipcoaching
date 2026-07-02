#!/usr/bin/env python3
"""Update 12 meta-descriptions with sharper angles and proper length (<160 chars)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def g(slug):
    for guide in data["guides"]:
        if guide["slug"] == slug:
            return guide
    raise KeyError(slug)

DESCS = {
    # Hall framing corrected: quality of time, not just quantity
    "how-to-make-friends-as-an-adult":
        "It takes roughly 50 hours of meaningful shared time to move from stranger to casual friend, and 200 for a close one. Here is how to make those hours happen.",

    # Infrastructure line — best of the batch
    "why-making-friends-as-an-adult-is-hard":
        "Adulthood didn't kill your social skills. It destroyed your infrastructure. Here is why adult friendship requires deliberate design, not just more willpower.",

    # Friendship breakup as real grief — under-used angle
    "when-a-friendship-ends":
        "Friendship breakups can hurt as much as romantic ones, but nobody talks about them. Here is how to navigate the grief, accept the closure, and heal.",

    # Practical + specific, addresses the real adaptation needed
    "how-to-stay-friends-after-a-baby":
        "When your friend has a baby, their free time drops to zero overnight. If you want to keep the bond, you have to change the rules. Here is how.",

    # Direct address, names the exhaustion
    "one-sided-friendship":
        "Are you the only one making plans, sending texts, and checking in? Here is how to spot a one-sided friendship and decide what to do about it.",

    # Liking Gap + fear of looking eager
    "how-to-follow-up-after-meeting-someone":
        "Afraid to text someone you just met in case you seem too eager? Research shows people like us more than we think. Here is how to follow up without the stress.",

    # Coaching vs therapy distinction upfront
    "what-is-friendship-coaching":
        "Friendship coaching isn't therapy. It is a step-by-step strategy for your social life, like a personal trainer for your friendships.",

    # Real and unfiltered vs polished social facade
    "how-to-make-friends-as-a-new-parent":
        "New parenthood is isolating, and polite coffee dates aren't the answer. Here is how to find other parents who get it and build real connections fast.",

    # Void + room for something better
    "how-to-make-friends-after-a-friendship-ends":
        "Losing a close friend leaves a real void. Clearing out a broken connection makes room for something healthier. Here is how to rebuild with confidence.",

    # Drift framing, fixes grammar error from source
    "why-do-friendships-fade":
        "Friendships rarely end in a big fight. They drift away when nobody makes the next plan. Here is why it happens and how to catch it before it is too late.",

    # Know vs trust distinction
    "how-to-turn-acquaintances-into-friends":
        "How do you cross from someone you know to someone you trust? It takes more than hello. Here is what actually moves an acquaintance into a real friend.",

    # Hallway moments as the real loss
    "how-to-keep-work-friendships-after-going-remote":
        "When you go remote, you lose the hallway moments that kept work friendships alive. Here is how to replace that structure before the friendships quietly fade.",
}

for slug, desc in DESCS.items():
    guide = g(slug)
    old = guide.get("description", "")
    assert len(desc) <= 165, f"Too long ({len(desc)}): {slug}"
    guide["description"] = desc
    print(f"  {len(desc):3d} chars: {slug}")

out = os.path.join(ROOT, "seo-pages.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nUpdated {len(DESCS)} descriptions.")
