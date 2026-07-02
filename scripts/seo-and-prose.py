#!/usr/bin/env python3
"""
3. Improve meta-descriptions (remove generic openers, sharpen CTR).
4. Shorten long intro and authorNote blocks to one strong idea.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def g(slug):
    for guide in data["guides"]:
        if guide["slug"] == slug:
            return guide
    raise KeyError(slug)

# ── 3. META-DESCRIPTIONS ─────────────────────────────────────────────────────
DESCS = {
    "how-to-make-friends-as-an-adult":
        "Research shows it takes 50 hours to go from stranger to casual friend, and 200 hours for a close one. Here is how to make those hours happen as an adult.",

    "how-to-reconnect-with-old-friends":
        "The story you tell yourself before you send the message is always harder than the message itself. Here is how to reconnect without guilt or a long explanation.",

    "how-to-keep-friends-as-an-adult":
        "Adult friendships don't end in fights. They end in drift. Here is how to maintain them through consistent small acts, not grand gestures or perfect timing.",

    "how-to-meet-people-in-a-new-city":
        "Meeting people in a new city runs on repetition, not luck. Here is how to create the repeated contact that turns early acquaintances into real friendships.",

    "how-to-be-a-better-friend":
        "Being a better friend is less about grand gestures and more about reliable small ones: following up, showing up, and being easy to reach when it matters.",

    "how-to-make-friends-after-30":
        "After 30, friendship doesn't stop being possible. It stops being automatic. Here is how to build it deliberately without pretending adult life works like college.",

    "how-to-introduce-friends-to-each-other":
        "A good introduction is about preparation, not spontaneity. Here is who to ask first, what to say, and when to step back and let the friendship form on its own.",

    "how-to-follow-up-after-meeting-someone":
        "The follow-up after meeting someone new is where most adult friendships either begin or die. Here is what to say, when to send it, and how to suggest a next step.",

    "how-to-make-friends-as-an-expat":
        "Making friends as an expat adds a layer to an already difficult challenge: no existing network, different cultural scripts, and often a clock ticking on how long you'll stay.",

    "friendship-quotes":
        "Eight observations on adult friendship by Carole Stromboni, friendship coach: on following up, loneliness, repetition, and what actually builds closeness.",
}

for slug, desc in DESCS.items():
    guide = g(slug)
    old = guide.get("description", "")
    guide["description"] = desc
    print(f"  desc: {slug} ({len(old)} -> {len(desc)})")

# ── 4. INTROS ─────────────────────────────────────────────────────────────────
INTROS = {
    "how-to-make-friends-as-an-adult":
        "Jeffrey Hall's research at the University of Kansas found it takes roughly 50 hours to move from stranger to casual friend, and around 200 hours for a close one. The method that follows: find a place where you can see the same person more than once, follow up after a warm exchange, and let the hours accumulate.",

    "why-male-friendships-fade":
        "Something shifts between 25 and 35 for most men. Friends who were a constant presence start to feel like people you used to know. Not because anything went wrong. Because everything got in the way. This is the predictable result of structural changes, not a personal failure.",

    "how-men-can-rebuild-friendships":
        "Most men who want more friendship in their lives are not looking for a therapist substitute. They want the kind of relationship that used to happen naturally: doing something alongside someone, seeing each other enough that it becomes normal, without making a big deal out of any of it.",

    "friendship-quotes":
        "Friendship is not something that happens to charismatic people. It is a practice. The observations on this page are not motivational phrases. They are diagnostic tools: they name the exact places where adult friendship breaks down, and what to do about it.",

    "how-to-keep-work-friendships-after-going-remote":
        "Keeping work friendships after going remote is different from maintaining any other friendship. The relationship formed in a context that no longer exists. Both people have to decide, usually without saying so, whether to move it somewhere else. Most never make that decision. The friendship fades, and nobody is sure who let it go.",

    "how-to-make-friends-after-a-friendship-ends":
        "Making friends after a significant friendship ends is not the same as making friends from scratch. You are doing it while carrying a loss, often with a lower appetite for the vulnerability that new friendship requires. This is not weakness. It is the normal aftermath of losing something that mattered.",
}

for slug, intro in INTROS.items():
    guide = g(slug)
    old = guide.get("intro", "")
    guide["intro"] = intro
    print(f"  intro: {slug} ({len(old)} -> {len(intro)})")

# ── 4. AUTHOR NOTES ──────────────────────────────────────────────────────────
NOTES = {
    "how-to-reconnect-with-old-friends":
        "Living between continents means I've reached out after long gaps many times: across time zones, after years of silence. What I know from all of those: the story you tell yourself before you send the message is always harder than the message itself. Most people are happy to hear from you.",

    "why-making-friends-as-an-adult-is-hard":
        "What made friendship hard for me was not the absence of people. It was the absence of structure. I had people I liked. I just was not creating enough repetition. And here is what I tell almost everyone I work with: you are not uniquely bad at this. Most adults feel exactly the way you feel right now. They just don't say it.",

    "how-to-keep-friends-as-an-adult":
        "What I've learned from keeping friendships across time zones and long gaps: consistency beats frequency every time. A short message every few weeks does more for a friendship than one long conversation every six months. Friendship is simpler to keep than you think, once you stop waiting for the right moment.",

    "how-to-meet-people-in-a-new-city":
        "I know that first feeling in a new place: surrounded by people, with nobody to text. What helped me most was not finding the perfect event. It was becoming a regular somewhere, showing up until my face was familiar, until 'oh, you're the one who...' started to happen. That's when things opened up.",

    "how-to-be-a-better-friend":
        "At the end of the day, what stays are the people. The trip fades. The job changes. The things you accumulated get sold or given away. The people who knew you across versions of yourself, those are what last. Becoming a better friend is one of the most worthwhile things you can work on.",

    "how-to-make-friends-after-30":
        "I've made some of my closest friends after 30. It took longer than at 20 and required more intention. But there are so many people who want the same thing you do, and most of them don't know how to start either. The friendships that come from that effort feel different: chosen more consciously, and more solid for it.",

    "how-to-make-friends-as-a-new-parent":
        "New parents surrounded by potential friends at baby groups and playgrounds still feel entirely alone six months later, because nobody had the bandwidth to follow up. The window is short and the energy is low. That is exactly why you have to make the move deliberately.",

    "how-to-keep-work-friendships-after-going-remote":
        "I have spoken to many people who went remote and lost friendships they genuinely valued. Not because the other person stopped caring, but because the office had been doing most of the maintenance. The ones who kept those friendships did one thing differently: they created a new structure.",

    "how-to-make-friends-after-a-friendship-ends":
        "Friendship loss is one of the most under-acknowledged forms of grief in adult life. There is no ceremony for it, no language for it, rarely anyone who asks how you are doing. But losing someone who was part of your daily life and your sense of being known is a real loss. The work of rebuilding starts with naming it as such.",
}

for slug, note in NOTES.items():
    guide = g(slug)
    old = guide.get("authorNote", "")
    guide["authorNote"] = note
    print(f"  note: {slug} ({len(old)} -> {len(note)})")

# ── WRITE ─────────────────────────────────────────────────────────────────────
out = os.path.join(ROOT, "seo-pages.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nDone: {len(DESCS)} descriptions + {len(INTROS)} intros + {len(NOTES)} authorNotes updated.")
