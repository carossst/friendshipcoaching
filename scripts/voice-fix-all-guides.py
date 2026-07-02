#!/usr/bin/env python3
"""
Apply Carole's warm voice to all remaining guides.
Rules:
- No "Professor X at University Y found" — use "Research shows/found" instead
- No em dashes (already clean)
- Research citations are fine, but warm sentence must follow or precede
- Sections should not end cold on a depressing stat or academic citation alone
- Keep all external links intact
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
# 1. why-male-friendships-fade / "What actually changes after 30" P3
# Soften "Research by anthropologist and evolutionary psychologist Robin Dunbar at the University of Oxford"
# ─────────────────────────────────────────────────────────────
g = guide("why-male-friendships-fade")
s = section(g, "What actually changes after 30")
s["paragraphs"][3] = (
    "Research on social relationships suggests that humans evolved to maintain connections "
    "at a few distinct scales: an inner circle of about five close people that requires the "
    "most contact to sustain, and a wider ring of around fifteen that needs regular but less "
    "frequent touch. When the structure that enabled that contact disappears, the inner circle "
    "does not maintain itself. It fades, quietly, without anyone deciding it should. "
    "(<a href=\"https://royalsocietypublishing.org\" rel=\"noopener noreferrer\" "
    "target=\"_blank\">Proceedings of the Royal Society</a>)"
)
changed.append("why-male-friendships-fade / What actually changes after 30 / P3")

# ─────────────────────────────────────────────────────────────
# 2. why-male-friendships-fade / "Why the office doesn't replace what you lost" P1
# Soften "Professor Jeffrey Hall's research ... His data show..."
# ─────────────────────────────────────────────────────────────
s = section(g, "office")
s["paragraphs"][1] = (
    "But there is a key limitation with workplace friendships. Research on how friendships "
    "form shows that time spent together by obligation, in workplaces, schools, or anywhere "
    "people are grouped by circumstance rather than choice, is a much weaker predictor of real "
    "closeness than freely chosen time together. You can see your coworkers every day and still "
    "feel like the relationship never quite gets there. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("why-male-friendships-fade / office / P1")

# ─────────────────────────────────────────────────────────────
# 3. why-male-friendships-fade / "Why reaching out feels harder than it should" P1
# Soften "Research by Dr. Erica Boothby at Cornell University on what she and her colleagues call the 'Liking Gap'"
# ─────────────────────────────────────────────────────────────
s = section(g, "reaching out feels harder")
s["paragraphs"][1] = (
    "Research on what psychologists call the Liking Gap has found that people consistently "
    "underestimate how warmly others think of them after a conversation. The person who has "
    "not texted is usually not waiting for you to stop trying. They are probably caught in "
    "the same hesitation you are."
)
changed.append("why-male-friendships-fade / reaching out feels harder / P1")

# ─────────────────────────────────────────────────────────────
# 4. why-male-friendships-fade / "What actually works" P1
# "Professor Jeffrey Hall at the University of Kansas found" → "Research shows"
# ─────────────────────────────────────────────────────────────
s = section(g, "What actually works")
s["paragraphs"][1] = (
    "Research shows it takes around 50 hours of shared time to build a genuine close "
    "friendship. A weekly run, a recurring sports game, a standing lunch, these are the "
    "conditions under which real friendship happens, not substitutes for it. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("why-male-friendships-fade / What actually works / P1")

# ─────────────────────────────────────────────────────────────
# 5. how-men-can-rebuild-friendships / "Pick one recurring activity" P0
# "Professor Jeffrey Hall at the University of Kansas found" → "Research shows"
# ─────────────────────────────────────────────────────────────
g2 = guide("how-men-can-rebuild-friendships")
s = section(g2, "recurring activity")
s["paragraphs"][0] = (
    "Research shows it takes roughly 50 hours of shared time to develop a genuine close "
    "friendship. For most adults over 30, that number sounds impossible. But broken down into "
    "a recurring activity, a weekly game, a monthly golf round, a regular Sunday run, it "
    "becomes manageable over a few months. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-men-can-rebuild-friendships / recurring activity / P0")

# ─────────────────────────────────────────────────────────────
# 6. how-men-can-rebuild-friendships / "The follow-up is the whole thing" P2
# Soften "Research by Dr. Erica Boothby at Cornell University on the 'Liking Gap'"
# ─────────────────────────────────────────────────────────────
s = section(g2, "follow-up is the whole thing")
s["paragraphs"][2] = (
    "Research on the Liking Gap has found that people consistently underestimate how much "
    "others enjoyed spending time with them. The guy from Sunday's run almost certainly "
    "liked you more than you think. Send the message."
)
changed.append("how-men-can-rebuild-friendships / follow-up / P2")

# ─────────────────────────────────────────────────────────────
# 7. one-sided-friendship / "Why friendships become one-sided" P3
# Replace cold Equity theory paragraph with warmer version
# ─────────────────────────────────────────────────────────────
g3 = guide("one-sided-friendship")
s = section(g3, "become one-sided")
s["paragraphs"][3] = (
    "What happens in a sustained one-sided friendship is rarely just frustration on one "
    "side. The person who always gives tends to build resentment quietly. The person who "
    "always receives often carries a low-level guilt they may never name. Both states "
    "corrode the connection, and neither is sustainable over time. If the imbalance goes "
    "unaddressed for long enough, it does not just stay uncomfortable. It slowly changes "
    "how both people feel about something that used to be good."
)
changed.append("one-sided-friendship / become one-sided / P3")

# ─────────────────────────────────────────────────────────────
# 8. how-to-turn-acquaintances-into-friends / "Repeat contact is more important" P3
# Soften "Professor Jeffrey Hall at the University of Kansas found"
# ─────────────────────────────────────────────────────────────
g4 = guide("how-to-turn-acquaintances-into-friends")
s = section(g4, "Repeat contact")
s["paragraphs"][3] = (
    "Research shows that moving from acquaintance to friend takes roughly 50 hours of shared "
    "time. Not 50 hours of depth, just 50 hours of presence. That is why repeated casual "
    "contact builds more friendship than a single excellent conversation, and why the pattern "
    "of contact over time matters more than any individual moment. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-to-turn-acquaintances-into-friends / Repeat contact / P3")

# ─────────────────────────────────────────────────────────────
# 9. how-to-turn-acquaintances-into-friends / "Share something real" P3
# Soften "Jeffrey Hall's research identifies... His data found..."
# ─────────────────────────────────────────────────────────────
s = section(g4, "Share something real")
s["paragraphs"][3] = (
    "Research on what builds closeness found that catching up on each other's real lives, "
    "joking around, and having a serious conversation predicted real increases in closeness "
    "over time. Small talk, by contrast, predicted a decrease when it dominated. The "
    "takeaway is simple: keeping things light indefinitely does not help. A moment of real "
    "catching up moves a relationship further in ten minutes than months of safe surface "
    "conversation. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-to-turn-acquaintances-into-friends / Share something real / P3")

# ─────────────────────────────────────────────────────────────
# 10. how-to-make-friends-after-a-friendship-ends / "Give the loss its proper name" P1
# Fix passive ending "tends not to work well"
# ─────────────────────────────────────────────────────────────
g5 = guide("how-to-make-friends-after-a-friendship-ends")
s = section(g5, "Give the loss")
s["paragraphs"][1] = (
    "But the impact is real. Someone who was part of your daily life, your inner reference "
    "points, your sense of being known, that absence is significant. Giving it a name before "
    "moving on is not self-indulgent. It is what makes the next step feel grounded rather "
    "than forced."
)
changed.append("how-to-make-friends-after-a-friendship-ends / Give the loss / P1")

# ─────────────────────────────────────────────────────────────
# 11. how-to-make-friends-after-a-friendship-ends / "Give the loss its proper name" P3
# Soften "Researcher Froma Walsh, known for her work on relational resilience at the University of Chicago"
# ─────────────────────────────────────────────────────────────
s["paragraphs"][3] = (
    "Research on relational resilience has found that people who acknowledge loss explicitly, "
    "who name what happened and what it meant rather than minimizing or bypassing it, tend to "
    "rebuild more successfully afterward. The absence of social ritual around friendship "
    "endings does not make the grief smaller. It makes it harder to locate, name, and move "
    "through."
)
changed.append("how-to-make-friends-after-a-friendship-ends / Give the loss / P3")

# ─────────────────────────────────────────────────────────────
# 12. how-to-be-a-better-friend / "Pay attention to what matters" P2
# Soften "Professor Harry Reis at the University of Rochester developed the concept of..."
# ─────────────────────────────────────────────────────────────
g6 = guide("how-to-be-a-better-friend")
s = section(g6, "Pay attention")
s["paragraphs"][2] = (
    "Research on close relationships points to one of the strongest predictors of friendship "
    "satisfaction: feeling genuinely seen, understood, and cared for in a conversation. That "
    "quality of attentiveness, the sense that someone is actually with you rather than just "
    "politely present, is what distinguishes a real friendship from a pleasant acquaintance. "
    "You do not need to be perfect. You need to be attentive."
)
changed.append("how-to-be-a-better-friend / Pay attention / P2")

# ─────────────────────────────────────────────────────────────
# 13. how-to-be-a-better-friend / "Let care be practical" P2
# Soften "Professor Jeffrey Hall calls striving communication episodes... His data show..."
# ─────────────────────────────────────────────────────────────
s = section(g6, "Let care be practical")
s["paragraphs"][2] = (
    "Research on what actually builds closeness in friendship points toward a specific quality "
    "of conversation: catching up on what has actually been happening in each other's lives, "
    "joking around to release tension, and engaging seriously when the moment calls for it. "
    "Those forms of talk predict increased closeness over time, while an excess of small talk "
    "predicts the opposite. Being a better friend is partly a matter of resisting the social "
    "reflex to keep things polite and light, and choosing instead to be genuinely curious "
    "about what is real for the other person. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-to-be-a-better-friend / Let care be practical / P2")

# ─────────────────────────────────────────────────────────────
# 14. how-to-make-friends-after-30 / "People overestimate" P2
# Add warm closing sentence so section doesn't end cold on a stat
# ─────────────────────────────────────────────────────────────
g7 = guide("how-to-make-friends-after-30")
s = section(g7, "overestimate")
s["paragraphs"][2] = (
    "The Survey Center on American Life has documented a significant decline in close "
    "friendships among American adults over the past three decades. In 2021, 15 percent of "
    "American men reported having no close friends at all, up from 3 percent in 1990. That "
    "figure reflects a broader structural shift in adult social life, not a personal failure "
    "on the part of people experiencing it. The conditions changed. The desire and the "
    "capacity for friendship did not. "
    "(<a href=\"https://www.americansurveycenter.org\" rel=\"noopener noreferrer\" "
    "target=\"_blank\">Survey Center on American Life</a>)"
)
changed.append("how-to-make-friends-after-30 / overestimate / P2")

# ─────────────────────────────────────────────────────────────
# 15. why-do-friendships-fade / "The structure disappears" P3
# Soften "Psychologist Toni Antonucci at the University of Michigan developed the social convoy model"
# ─────────────────────────────────────────────────────────────
g8 = guide("why-do-friendships-fade")
s = section(g8, "structure disappears")
s["paragraphs"][3] = (
    "Research on adult social life has consistently found that friendships are most "
    "vulnerable at moments of structural transition: a move, a job change, a new life phase. "
    "When the shared context that sustained the connection disappears and neither person "
    "creates a replacement, the friendship loses its footing not through any decision or "
    "falling out, but through drift. "
    "(<a href=\"https://lsa.umich.edu/isr\" rel=\"noopener noreferrer\" "
    "target=\"_blank\">Institute for Social Research, University of Michigan</a>)"
)
changed.append("why-do-friendships-fade / structure disappears / P3")

# ─────────────────────────────────────────────────────────────
# 16. how-to-make-friends-when-you-work-from-home / "The real problem" P3
# Soften "Jeffrey Hall's research helps explain this more precisely. His data show..."
# ─────────────────────────────────────────────────────────────
g9 = guide("how-to-make-friends-when-you-work-from-home")
s = section(g9, "real problem")
s["paragraphs"][3] = (
    "Research on how friendships form helps explain this more precisely. Time in obligatory "
    "settings, like offices or classrooms, is a weak predictor of real friendship closeness. "
    "Office hours were never reliably converting into deep friendship. What the office "
    "provided was a scaffold: repeated proximity that made chosen moments more likely. A "
    "spontaneous lunch. A conversation after a meeting. Remote work removed the scaffold. "
    "The task now is not to replicate the office. It is to build the voluntary contact the "
    "office was creating without anyone noticing. "
    "(<a href=\"https://journals.sagepub.com/doi/full/10.1177/0265407518761225\" "
    "rel=\"noopener noreferrer\" target=\"_blank\">Journal of Social and Personal Relationships</a>)"
)
changed.append("how-to-make-friends-when-you-work-from-home / real problem / P3")

# ─────────────────────────────────────────────────────────────
# 17. how-to-keep-friends-as-an-adult / "Let the friendship fit real life" P2
# Soften "Anthropologist Robin Dunbar at the University of Oxford found... His research suggests..."
# ─────────────────────────────────────────────────────────────
g10 = guide("how-to-keep-friends-as-an-adult")
s = section(g10, "fit real life")
s["paragraphs"][2] = (
    "Research on social relationships suggests that humans typically maintain only about five "
    "genuinely close friendships at any one time, with another ten to fifteen people in a "
    "slightly outer ring of meaningful but less frequent contact. That limit is cognitive and "
    "social, not simply a matter of time. Investing deeply in a few friendships is not a "
    "failure of social ambition. It is how human social life actually works."
)
changed.append("how-to-keep-friends-as-an-adult / fit real life / P2")

# ─────────────────────────────────────────────────────────────
# 18. how-to-meet-people-in-a-new-city / "Become a regular somewhere" P2
# Replace depressing "erosion of third places" ending with action close
# ─────────────────────────────────────────────────────────────
g11 = guide("how-to-meet-people-in-a-new-city")
s = section(g11, "regular somewhere")
s["paragraphs"][2] = (
    "Sociologist Ray Oldenburg described these repeatable spaces, the local cafe, the gym, "
    "the community center, the bookstore, as third places: neutral ground outside of home and "
    "work where informal social connection forms most naturally. The concept is not academic. "
    "The point is to find yours and keep going back. "
    "(<a href=\"https://en.wikipedia.org/wiki/Third_place\" rel=\"noopener noreferrer\" "
    "target=\"_blank\">Third Places</a>)"
)
changed.append("how-to-meet-people-in-a-new-city / regular somewhere / P2")

# ─────────────────────────────────────────────────────────────
# 19. when-a-friendship-ends / "The fade is the most common ending" P2
# Soften "Psychologist Dr. Miriam Kirmayer, who studies friendship loss, has noted..."
# ─────────────────────────────────────────────────────────────
g12 = guide("when-a-friendship-ends")
s = section(g12, "fade is the most common")
s["paragraphs"][2] = (
    "Those who study friendship loss have noted that friendship endings are among the least "
    "socially recognized losses adults experience. There is no social script, no ritual, and "
    "very little permission to grieve a friendship. That absence of recognition can make the "
    "loss harder to process than the loss itself."
)
changed.append("when-a-friendship-ends / fade is the most common / P2")

# ─────────────────────────────────────────────────────────────
# 20. how-to-stay-friends-after-a-baby / "New parents are not rejecting you" P3
# Add warm action close to a section that ends cold on a research stat
# ─────────────────────────────────────────────────────────────
g13 = guide("how-to-stay-friends-after-a-baby")
s = section(g13, "not rejecting you")
s["paragraphs"][3] = (
    "Research on the transition to parenthood consistently documents a significant contraction "
    "in social networks in the first year, sometimes extending into the second and third years. "
    "Understanding that makes the adaptation feel less one-sided. You are not compensating for "
    "a failing. You are the person in the friendship who still has bandwidth to reach out, "
    "and that matters more than you probably realize."
)
changed.append("how-to-stay-friends-after-a-baby / not rejecting you / P3")

# ─────────────────────────────────────────────────────────────
# 21. how-to-introduce-friends-to-each-other / "A denser network" P1
# Soften "Sociologist Mark Granovetter at Stanford University described this dynamic as triadic closure"
# ─────────────────────────────────────────────────────────────
g14 = guide("how-to-introduce-friends-to-each-other")
s = section(g14, "denser network")
s["paragraphs"][1] = (
    "Researchers describe this pattern as triadic closure: when two people who share a mutual "
    "connection start building their own friendship, the social network becomes denser, more "
    "resilient, and easier for everyone in it to maintain. Each new tie reduces the weight on "
    "the existing ones."
)
changed.append("how-to-introduce-friends-to-each-other / denser network / P1")

# ─────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────
out = os.path.join(ROOT, "seo-pages.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Applied {len(changed)} voice fixes:\n")
for c in changed:
    print(f"  {c}")
