#!/usr/bin/env python3
"""
1. Add cultureRef to 3 guides that have none.
2. Simplify 7 dense research paragraphs to 8th-grade level.
"""
import json
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)


def find_guide(slug):
    for g in data["guides"]:
        if g["slug"] == slug:
            return g
    return None


def find_section(guide, h2):
    for s in guide.get("sections", []):
        if s["h2"] == h2:
            return s
    return None


errors = []

# ── 1. NEW CULTURE-REF ADDITIONS ─────────────────────────────────────────────

NEW_REFS = [
    (
        "how-to-make-friends-as-an-adult",
        "Build from mutual interest, not from perfection",
        "Hacks · HBO Max",
        "In Hacks, Deborah and Ava have nothing in common at the start. Deborah is a Las Vegas comedy legend in her sixties. Ava is a broke writer in her twenties. What creates the friendship is not choice or warmth. It is necessity and repeated time working together. They argue, collaborate, and slowly discover mutual respect. That is the model for adult friendship: not a perfect match from the start, but enough shared time to let the fit reveal itself.",
    ),
    (
        "how-to-reconnect-with-old-friends",
        "The shared foundation does not disappear",
        "The Big Chill · Film",
        "In The Big Chill, a group of college friends reunites after years apart. The gap between them is real. Lives have diverged. Values have shifted. But the shared history holds. Within hours, old rhythms return. Old jokes resurface. What had been suspended, not erased, comes back. The film shows that the foundation of an old friendship does not disappear during a long silence. It waits.",
    ),
    (
        "how-men-can-rebuild-friendships",
        "Pick one recurring activity and invite one person",
        "The Intouchables · Film",
        "In The Intouchables, Philippe and Driss build something neither of them expected. The setup is practical: Philippe needs a caregiver, Driss needs work. What grows between them is not sentiment. It is shared time in a recurring structure. Driss shows up every day. Philippe is there. The friendship forms not through emotional declaration but through the repeated act of being present. That is the film's real lesson: close male friendship is built through doing something alongside someone, not through talking about the friendship itself.",
    ),
]

for slug, h2, show, body in NEW_REFS:
    guide = find_guide(slug)
    if not guide:
        errors.append(f"Guide not found: {slug}")
        continue
    section = find_section(guide, h2)
    if not section:
        errors.append(f"Section not found: {slug} / {h2}")
        continue
    if "cultureRef" in section:
        errors.append(f"cultureRef already exists: {slug} / {h2}")
        continue
    section["cultureRef"] = {"show": show, "body": body}
    print(f"  + cultureRef: {slug} / {h2}")


# ── 2. RESEARCH PARAGRAPH SIMPLIFICATIONS ────────────────────────────────────

# (slug, h2, old_prefix, new_paragraph)
SIMPLIFICATIONS = [
    # Hall closed-system — why-making-friends-as-an-adult-is-hard
    (
        "why-making-friends-as-an-adult-is-hard",
        "There is less built-in repetition",
        "Hall's research also distinguishes between what he calls closed-system",
        'Hall\'s research makes a second distinction. He separates friendships formed by obligation, at work or school, from friendships that are freely chosen. His data show that hours in an obligatory context are poor predictors of closeness. Forty hours a week next to a coworker does not produce the same friendship as twenty hours chosen freely. This explains why a full calendar can still feel lonely. The people are there. The choice is not. (<a href="https://journals.sagepub.com/doi/full/10.1177/0265407518761225" rel="noopener noreferrer" target="_blank">Journal of Social and Personal Relationships</a>)',
    ),
    # Hall closed-systems scaffold — how-to-make-friends-when-you-work-from-home
    (
        "how-to-make-friends-when-you-work-from-home",
        "The real problem with remote work and friendship",
        "A related finding from Professor Jeffrey Hall",
        'Jeffrey Hall\'s research helps explain this more precisely. His data show that time in obligatory settings, like offices or classrooms, is a weak predictor of real friendship closeness. Office hours were never reliably converting into deep friendship. What the office provided was a scaffold: repeated proximity that made chosen moments more likely. A spontaneous lunch. A conversation after a meeting. Remote work removed the scaffold. The task now is not to replicate the office. It is to build the voluntary contact the office was creating without anyone noticing. (<a href="https://journals.sagepub.com/doi/full/10.1177/0265407518761225" rel="noopener noreferrer" target="_blank">Journal of Social and Personal Relationships</a>)',
    ),
    # HBR ambient contact — how-to-make-friends-when-you-work-from-home
    (
        "how-to-make-friends-when-you-work-from-home",
        "The real problem with remote work and friendship",
        "Research on communication and workplace social dynamics",
        'Research on workplace social dynamics shows that what remote work primarily eliminates is not collaboration. It is unplanned, ambient contact: the exchange in a hallway, the conversation before a meeting starts, the brief encounter at the coffee machine. These low-stakes, unscheduled interactions are what build social familiarity over time. Remote workers lose a significant portion of these informal touchpoints. Research published in the Harvard Business Review found they are disproportionately responsible for building interpersonal trust. (<a href="https://hbr.org" rel="noopener noreferrer" target="_blank">Harvard Business Review</a>)',
    ),
    # Hall striving communication — how-to-turn-acquaintances-into-friends
    (
        "how-to-turn-acquaintances-into-friends",
        "Share something real when the moment is right",
        "Research by Professor Jeffrey Hall also identifies which kinds",
        'Jeffrey Hall\'s research identifies which conversations build closeness and which ones stall it. His data found that catching up on each other\'s real lives, joking around, and having a serious conversation predicted real increases in closeness over time. Small talk, by contrast, predicted a decrease when it dominated. The implication is direct: keeping things light indefinitely does not help. A moment of real catching up moves a relationship further in ten minutes than months of safe surface conversation. (<a href="https://journals.sagepub.com/doi/full/10.1177/0265407518761225" rel="noopener noreferrer" target="_blank">Journal of Social and Personal Relationships</a>)',
    ),
    # Dunbar nuance — why-do-friendships-fade
    (
        "why-do-friendships-fade",
        "The structure disappears and the friendship goes with it",
        "Research by anthropologist Robin Dunbar at the University of Oxford, published",
        'Robin Dunbar at Oxford adds a useful nuance. His research shows that the type of contact that sustains a friendship varies by person. Some people stay close through conversation, even at a distance. Others need side-by-side activity to keep the friendship from fading. When the activity disappears and nothing replaces it, the friendship loses its maintenance mechanism without anyone noticing. Knowing which type works for a specific friendship makes it easier to know what to do when things start to drift. (<a href="https://www.pnas.org" rel="noopener noreferrer" target="_blank">Proceedings of the National Academy of Sciences</a>)',
    ),
    # Gottman Institute — how-to-make-friends-as-a-new-parent
    (
        "how-to-make-friends-as-a-new-parent",
        "You are not imagining how hard it is",
        "The Gottman Institute, which has studied the transition to parenthood",
        'The Gottman Institute has studied the transition to parenthood across decades of research. They found that 67 percent of new parents experience a significant drop in relationship satisfaction in the first three years after a baby. One of the main drivers is the collapse of the social infrastructure that used to support both partners. Their research is clear: the social isolation of new parenthood does not correct itself. It is a structural problem that requires deliberate attention. (<a href="https://www.gottman.com" rel="noopener noreferrer" target="_blank">The Gottman Institute</a>)',
    ),
    # Pew Research — how-to-make-friends-as-a-new-parent
    (
        "how-to-make-friends-as-a-new-parent",
        "You are not imagining how hard it is",
        "Time-use data from the",
        'Time-use data from the <a href="https://www.pewresearch.org/social-trends/2013/03/14/modern-parenthood-roles-of-moms-and-dads-converge-as-they-balance-work-and-family/" rel="noopener noreferrer" target="_blank">Pew Research Center on Modern Parenthood</a> shows that both parents lose discretionary social time after a baby, but in different ways. Mothers face the steepest overall reduction in social time. Fathers often retain slightly more leisure hours but spend them in isolated activities: screen time, solo exercise, rather than connection. In both cases, the social network contracts. The challenge is not finding more time. It is using the limited time that remains for connection rather than recovery alone.',
    ),
]

for slug, h2, prefix, new_para in SIMPLIFICATIONS:
    guide = find_guide(slug)
    if not guide:
        errors.append(f"Guide not found: {slug}")
        continue
    section = find_section(guide, h2)
    if not section:
        errors.append(f"Section not found: {slug} / {h2}")
        continue
    paras = section.get("paragraphs", [])
    idx = None
    for i, p in enumerate(paras):
        if p.startswith(prefix):
            idx = i
            break
    if idx is None:
        errors.append(f"Paragraph not found: {slug} / {h2} / prefix: {prefix[:50]}")
        continue
    paras[idx] = new_para
    print(f"  ~ simplified: {slug} / {prefix[:45]}...")


if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(f"  ERROR: {e}")
    sys.exit(1)

out_path = os.path.join(ROOT, "seo-pages.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nseo-pages.json updated: {len(NEW_REFS)} new refs + {len(SIMPLIFICATIONS)} simplifications.")
