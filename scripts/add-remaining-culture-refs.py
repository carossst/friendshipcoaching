#!/usr/bin/env python3
"""Add cultureRef to remaining sections (conceptual, not tactical)."""
import json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def find_guide(slug):
    for g in data["guides"]:
        if g["slug"] == slug: return g
    return None

def find_section(guide, h2):
    for s in guide.get("sections", []):
        if s["h2"] == h2: return s
    return None

errors = []

NEW_REFS = [
    # ── how-to-make-friends-as-an-adult ──────────────────────────────────────
    (
        "how-to-make-friends-as-an-adult",
        "Start with places where repetition is normal",
        "Parks and Recreation · NBC",
        "In Parks and Recreation, the Pawnee Parks Department is not a place anyone chooses for its social potential. But Leslie Knope's friendships form there because the building keeps returning everyone to the same rooms. Ann shows up as a complaint. Ben arrives as a state auditor. April takes an internship. None of these are friendship choices. They are circumstances. Parks and Recreation shows that the right environment does the work that intention cannot.",
    ),
    (
        "how-to-make-friends-as-an-adult",
        "Treat the follow-up as part of the friendship, not as a test",
        "Seinfeld · NBC",
        "In Seinfeld, Jerry and George meet for coffee almost every episode. There is no planning. No checking in to see if the other wants to meet. One of them calls. The other shows up. A new plan gets made before the current one ends. The follow-up is never a test because it is never framed as one. It is just a habit. The friendship's maintenance is invisible because neither of them tracks it. That is the goal.",
    ),
    (
        "how-to-make-friends-as-an-adult",
        "The early phase is supposed to feel like trial and error",
        "Abbott Elementary · ABC",
        "Janine and Gregory's friendship in Abbott Elementary does not start well. He is guarded. She is relentless. The first attempts at connection are awkward. Neither of them reads the other correctly. But they keep showing up because the school keeps bringing them back. Over time, the awkwardness becomes familiarity. Abbott Elementary shows that early friction in a new friendship is not a warning sign. It is the normal cost of entry.",
    ),
    (
        "how-to-make-friends-as-an-adult",
        "Let friendship grow through practice",
        "Ted Lasso · Apple TV+",
        "In Ted Lasso, Coach Beard and Ted's friendship is never explained or discussed. They just show up together, through losing seasons, new countries, and personal crises. The friendship is built through repeated presence: the same locker room, the same bus rides, the same routines. Ted Lasso shows that deep friendships are not built through intention. They are built through practice: showing up so often that the relationship forms without anyone deciding to form it.",
    ),
    # ── how-to-reconnect-with-old-friends ────────────────────────────────────
    (
        "how-to-reconnect-with-old-friends",
        "Do not turn the message into a guilt performance",
        "Seinfeld · NBC",
        "In Seinfeld, George Costanza makes simple things complicated. Every reconnection attempt becomes a speech. Every apology requires a preamble. Every message gets drafted, revised, and overthought until the original point is buried. The joke is always the same: the simple version would have worked better. A short message that sounds like you is better than a long one that sounds like a confession. George never learns this. Most people do, eventually.",
    ),
    # ── why-making-friends-as-an-adult-is-hard ───────────────────────────────
    (
        "why-making-friends-as-an-adult-is-hard",
        "Friendship competes with everything else",
        "Fleabag · BBC / Amazon",
        "In Fleabag, Fleabag and her sister care about each other. That is never in question. But the friendship keeps getting crowded out. There is grief, a failing business, bad relationships, and the general weight of adult life. They love each other and keep failing to show up for each other. Fleabag shows that adult friendship does not fail because of indifference. It fails because everything else keeps winning the competition for time and attention.",
    ),
    # ── how-to-keep-friends-as-an-adult ──────────────────────────────────────
    (
        "how-to-keep-friends-as-an-adult",
        "Do not confuse warmth with maintenance",
        "This Is Us · NBC",
        "In This Is Us, the Pearson siblings love each other without question. The warmth is real. But the show tracks how warmth alone does not sustain closeness. Kevin drifts. Randall and Kevin's relationship corrodes over three seasons. The love was never the problem. The contact was. This Is Us shows that caring deeply about someone is not the same as maintaining the friendship. The two things require different actions.",
    ),
    # ── how-to-meet-people-in-a-new-city ─────────────────────────────────────
    (
        "how-to-meet-people-in-a-new-city",
        "Choose places where you can return",
        "Cheers · NBC",
        "In Cheers, Sam Malone's bar works as a social hub because everyone keeps coming back. Norm Peterson arrives every evening. Cliff has his stool. The friendships that form there don't start with anyone deciding to befriend anyone. They start because the bar gives everyone a reason to return. Cheers gets one thing exactly right: the place matters more than the plan. A good recurring location does more social work than any amount of deliberate effort.",
    ),
    (
        "how-to-meet-people-in-a-new-city",
        "Become a regular somewhere",
        "How I Met Your Mother · CBS",
        "In How I Met Your Mother, McLaren's Pub is where everything happens. Ted, Marshall, Lily, Barney, and Robin don't hold their friendships together through effort. They hold them together by returning to the same booth. The booth is always there. They are always there. The regularity makes the group feel inevitable. How I Met Your Mother shows that a recurring location is not background detail. It is the engine of the friendship.",
    ),
    # ── how-to-be-a-better-friend ─────────────────────────────────────────────
    (
        "how-to-be-a-better-friend",
        "Do not wait for the other person to do all the maintenance",
        "Schitt's Creek · CBC / Pop",
        "In Schitt's Creek, David and Stevie's friendship works because Stevie keeps showing up even when David doesn't invite her. She knocks on his motel room door. She makes dry offers to hang out. She does not wait for him to feel ready. David would not have initiated the friendship on his own. Schitt's Creek shows that one person choosing to keep showing up is often enough to start something real, even when the other person isn't sure they want it yet.",
    ),
    # ── how-to-make-friends-after-30 ─────────────────────────────────────────
    (
        "how-to-make-friends-after-30",
        "People overestimate how hard it is, and underestimate how many forms it can take",
        "I Love You Man · Film",
        "In I Love You Man, Peter Klaven is in his thirties and realizes he has no close male friends. The premise depends on how rare and intimidating adult friendship-making seems. But the film also shows how quickly things can change. One honest conversation with Sydney leads to a real friendship in a short time. Peter assumed he had missed his window. He had not. The film's quiet argument is that the obstacle was always smaller than it looked.",
    ),
    (
        "how-to-make-friends-after-30",
        "Use repeated environments instead of random chance",
        "The Holdovers · Film",
        "In The Holdovers, Paul Hunham and Angus Tully do not choose each other. They are left behind together at a boarding school over the winter break, with nowhere else to go. The environment forces the repetition that creates the friendship. They eat together, argue, and eventually trust each other because they keep returning to the same building. The Holdovers shows that adult friendships are not always chosen. Sometimes they are built by circumstance and time.",
    ),
    # ── why-male-friendships-fade ─────────────────────────────────────────────
    (
        "why-male-friendships-fade",
        "What actually changes after 30",
        "St. Elmo's Fire · Film",
        "In St. Elmo's Fire, a group of recent college graduates tries to stay close after moving to Washington D.C. The film shows what changes: jobs, relationships, geography, and ambition pull each person in a different direction. Nobody decides to drift. But the structures that held the group together no longer exist. There is no campus, no schedule, no shared reason to be in the same place. St. Elmo's Fire shows the problem exactly as it happens: not through a break, but through slow structural erosion.",
    ),
    (
        "why-male-friendships-fade",
        "Why the office doesn't replace what you lost",
        "The Office · NBC",
        "In The Office, Jim and Pam build much of their friendship through the rhythms of the workday: side conversations, lunch breaks, glances across the room. When Jim takes a job in Philadelphia, Pam discovers that proximity was doing most of the work. The Office shows how much of what feels like friendship at work is really shared schedule. When the schedule ends, most of what was built around it goes with it.",
    ),
    (
        "why-male-friendships-fade",
        "Why reaching out feels harder than it should",
        "Superbad · Film",
        "In Superbad, Seth and Evan are about to go to different colleges. Their friendship is real and close. But the film's emotional climax is the scene where they finally say, out loud, that they care about each other. It is played as both funny and sincere. The joke is that two close friends needed a full night of chaos to reach a moment of honest expression. Superbad captures something specific about male friendship: the depth is real, but the words to name it feel harder than they should.",
    ),
    # ── how-men-can-rebuild-friendships ──────────────────────────────────────
    (
        "how-men-can-rebuild-friendships",
        "You don't need to say anything uncomfortable",
        "Ford v Ferrari · Film",
        "In Ford v Ferrari, Ken Miles and Carroll Shelby are close. They fight constantly about engineering, racing lines, and strategy. But they never have a conversation about their friendship. They never name it. The relationship is built through doing things together: designing the car, testing it, driving it. Ford v Ferrari shows that close male friendships do not require emotional vocabulary. They require a shared task and someone willing to keep showing up for it.",
    ),
    (
        "how-men-can-rebuild-friendships",
        "Side-by-side time works differently than face-to-face",
        "Good Will Hunting · Film",
        "In Good Will Hunting, Will Hunting and Chuckie Sullivan spend most of their time doing things alongside each other rather than talking about their bond. Construction work, bar trips, driving around. The film does not show them in deep conversation about what they mean to each other. It shows them in motion, side by side. Good Will Hunting captures what most male friendships actually look like: two people doing something together, saying very little about it.",
    ),
    (
        "how-men-can-rebuild-friendships",
        "If it has been a long time",
        "The Shawshank Redemption · Film",
        "In The Shawshank Redemption, Andy Dufresne and Red's friendship is interrupted by Andy's escape. When Red is eventually paroled and makes it to Zihuatanejo, years have passed. The reunion requires no accounting of the gap. Red simply shows up. The Shawshank Redemption shows that a long absence does not require an explanation before reconnection is possible. Sometimes the gap explains itself. The right move is to appear.",
    ),
    # ── how-to-introduce-friends-to-each-other ───────────────────────────────
    (
        "how-to-introduce-friends-to-each-other",
        "Step back and let the friendship form on its own",
        "Bridesmaids · Film",
        "In Bridesmaids, Annie tries to manage who Lillian becomes close with after making introductions to a new friend group. The attempt backfires. Lillian's friendship with Helen develops on its own, outside Annie's control. Bridesmaids shows what most introductions eventually require: the connector has to leave the room. Two people will only find their own rhythm when the person who introduced them stops being present.",
    ),
    # ── when-a-friendship-ends ───────────────────────────────────────────────
    (
        "when-a-friendship-ends",
        "When distance is not the end, just a long pause",
        "Stand By Me · Film",
        "In Stand By Me, Gordie looks back on his friendship with Chris, Teddy, and Vern. The narration tells us that after that summer, the friends drifted into separate lives and never returned to what they had. But the film does not treat this as a failure. The friendship was real. The drift was real. Both can be true. Stand By Me shows that a long pause does not erase what came before it. The foundation stays, even when the contact stops.",
    ),
    (
        "when-a-friendship-ends",
        "Forgiveness and the possibility of return",
        "The Bear · FX / Hulu",
        "In The Bear, Carmy and Richie start the show hostile to each other. Their friendship is buried under resentment, grief, and competing claims on the restaurant. In the second season, Richie goes on a stage at a fine dining restaurant and comes back changed. The repair happens not through a conversation but through renewed shared purpose. The Bear shows that forgiveness in a male friendship often looks less like a talk and more like deciding to work alongside someone again.",
    ),
    # ── how-to-stay-friends-after-a-baby ─────────────────────────────────────
    (
        "how-to-stay-friends-after-a-baby",
        "The long game: what the friendship looks like on the other side",
        "Parenthood · NBC",
        "In Parenthood, the Braverman siblings stay close through multiple rounds of new babies, job changes, and relocations. The friendships don't look the same after a baby arrives. Dinners become shorter. Plans become less spontaneous. But the group adjusts. Parenthood shows that the friendship on the other side of a baby is not the same friendship. It is a different version that has learned to work around something new. Different is not the same as worse.",
    ),
    # ── one-sided-friendship ─────────────────────────────────────────────────
    (
        "one-sided-friendship",
        "What one-sided actually means",
        "Grease · Film",
        "In Grease, Sandy arrives at Rydell High hoping her summer connection with Danny will translate into a real friendship. Danny, surrounded by his friends and his social persona, is awkward and inconsistent about it. The film shows what one-sided actually looks like: not cruelty, but a mismatch in priorities. Danny cares privately but does not make it visible in his behavior. Grease shows that one-sidedness is usually not about one person being wrong. It is about two people not agreeing, without saying so, on how much the connection matters.",
    ),
    # ── why-do-friendships-fade ───────────────────────────────────────────────
    (
        "why-do-friendships-fade",
        "Nobody makes the next plan",
        "Entourage · HBO",
        "In Entourage, Vince, E, Drama, and Turtle are close for the first several seasons because they are in each other's lives every day. When Vince's career stalls and the group disperses, the show quietly shows what happens when nobody makes the next plan. Scenes stop happening. Episodes pass without the group together. Nobody has a falling out. Nobody stops caring. They just stop scheduling. Entourage shows how easy it is to let a friendship run on inertia until the inertia runs out.",
    ),
    (
        "why-do-friendships-fade",
        "Life intervenes and the gap becomes the problem",
        "About Time · Film",
        "In About Time, Tim reconnects with his old friend Jay after years apart. The distance was not chosen. Life moved them in different directions: jobs, families, geography. When they meet again, the gap between them is awkward at first. It is not that the friendship broke. It is that the gap grew large enough to feel like an obstacle. About Time shows that the gap is the most common friendship problem. It is also the most solvable, once both people decide to close it.",
    ),
    # ── how-to-turn-acquaintances-into-friends ────────────────────────────────
    (
        "how-to-turn-acquaintances-into-friends",
        "Share something real when the moment is right",
        "New Girl · Fox",
        "In New Girl, Nick Miller and Jess Day share a loft for a long time before they actually connect. They stay in surface territory: awkward jokes, housemate logistics, polite conversation. The friendship shifts when Jess shares something real about her divorce and Nick responds with something honest about his own situation. New Girl shows how long two people can live alongside each other without connecting, and how quickly that changes once one person takes the first real step.",
    ),
    # ── how-to-make-friends-as-an-expat ──────────────────────────────────────
    (
        "how-to-make-friends-as-an-expat",
        "Why making friends as an expat is its own challenge",
        "Emily in Paris · Netflix",
        "In Emily in Paris, Emily arrives convinced that her openness and energy will quickly translate into friendships. It doesn't. The existing social networks are formed. The cultural references are different. The humor doesn't land the same way. It takes much longer than expected, and the friendships that form do so through persistence and repeated proximity, not through charm alone. Emily in Paris shows the expat challenge clearly: the social scripts that worked at home do not transfer automatically.",
    ),
    (
        "how-to-make-friends-as-an-expat",
        "Find recurring contexts in local life",
        "Amélie · Film",
        "In Amélie, Amélie Poulain finds her community in the recurring rhythms of her neighborhood: the same cafe, the same market, the same corner of Montmartre. Her path back to connection goes through places she returns to regularly. Amélie shows that recurring local contexts are how community forms: not through grand gestures, but through showing up to the same places enough times that people start to know your face. The neighborhood becomes the social infrastructure.",
    ),
    (
        "how-to-make-friends-as-an-expat",
        "Do not wait to be invited",
        "Brooklyn · Film",
        "In Brooklyn, Eilis Lacey moves from Ireland to New York and waits, at first, for someone to include her. She sits on the edge of dances and dinners, hoping for an invitation that doesn't come. It is only when she stops waiting and places herself in situations that things begin to change. Brooklyn shows what the expat experience teaches most people eventually: waiting to be invited is the slower path. The faster one is deciding to show up without one.",
    ),
    # ── how-to-know-if-someone-wants-to-be-your-friend ───────────────────────
    (
        "how-to-know-if-someone-wants-to-be-your-friend",
        "The difference between being liked and being chosen",
        "Mean Girls · Film",
        "In Mean Girls, Cady Heron is liked by almost everyone she meets. The Plastics like her. Janis and Damian like her. But being liked and being chosen are different things. The Plastics perform friendship without actually offering it. Janis and Damian choose her, even after she betrays them, because the connection was real. Mean Girls shows the distinction clearly: being liked is a social signal. Being chosen is a decision someone makes when they don't have to.",
    ),
    # ── how-to-make-friends-as-a-new-parent ──────────────────────────────────
    (
        "how-to-make-friends-as-a-new-parent",
        "You are not imagining how hard it is",
        "Catastrophe · Amazon",
        "In Catastrophe, Sharon and Rob's social life contracts noticeably after their baby arrives. Old friendships don't disappear, but they become harder to reach. Plans cancel. Schedules shift. The people without children have lives that no longer align with theirs. Catastrophe shows the social contraction of new parenthood without dramatizing it. It is just there, in the background: the world has narrowed, and nobody warned them how narrow it would get.",
    ),
    (
        "how-to-make-friends-as-a-new-parent",
        "Parenting contexts are full of potential friends",
        "Workin' Moms · Netflix",
        "In Workin' Moms, Kate, Anne, Frankie, and Jenny meet in a postpartum support group. None of them would have chosen each other in any other context. Their personalities are wildly different. But they keep showing up to the same room at the same time, which is enough. The friendships that form are real: imperfect, strange, and durable. Workin' Moms shows that parenting contexts create forced proximity, and forced proximity is often where the most unexpected adult friendships start.",
    ),
    (
        "how-to-make-friends-as-a-new-parent",
        "Lower the bar for what the friendship looks like early on",
        "Friends · NBC",
        "In Friends, Rachel's social life changes completely after Emma is born. The group still shows up for her, but on different terms: shorter visits, quieter evenings, more scheduling. The friendships don't end. But they change shape. Friends shows what lower-bar parenting friendship looks like in practice: the standard for a good evening drops, the threshold for showing up drops with it, and both sides learn to accept that. A shorter visit that actually happens is better than a perfect one that never does.",
    ),
    # ── how-to-keep-work-friendships-after-going-remote ──────────────────────
    (
        "how-to-keep-work-friendships-after-going-remote",
        "Create a structure to replace the one that disappeared",
        "Silicon Valley · HBO",
        "In Silicon Valley, the Pied Piper team's closeness depends on sharing a physical space. When the group is forced to work separately at key moments, the dynamic shifts. The friendships don't disappear, but they require real effort to maintain once the building is gone. Silicon Valley shows how much social cohesion depends on shared physical structure. When the structure disappears, the connections have to be rebuilt deliberately, or they quietly fade.",
    ),
    # ── how-to-make-friends-after-a-friendship-ends ───────────────────────────
    (
        "how-to-make-friends-after-a-friendship-ends",
        "Give the loss its proper name",
        "Fleabag · BBC / Amazon",
        "In Fleabag, Fleabag's grief over Boo is named properly: it is a friendship loss, not just a death. The show distinguishes between the two things. Boo is gone, but the loss includes the friendship itself, what it meant, and the ways it was already ending before it ended. Fleabag shows that naming a loss precisely matters. Calling a friendship ending what it actually is, a loss worth grieving, changes how recovery from it can begin.",
    ),
    (
        "how-to-make-friends-after-a-friendship-ends",
        "You are not looking for a replacement",
        "Inside Out · Film",
        "In Inside Out, Riley's childhood imaginary friend Bing Bong is not replaced after he fades. Riley does not find a new imaginary friend to fill the same space. She finds new kinds of connection that fit who she has become. Inside Out shows that friendships at different life stages are not interchangeable. The next friendship is not meant to fill the same space as the one before it. It is meant to fit who you are now, not who you were then.",
    ),
    (
        "how-to-make-friends-after-a-friendship-ends",
        "New friendship after loss builds differently",
        "A Beautiful Day in the Neighborhood · Film",
        "In A Beautiful Day in the Neighborhood, Fred Rogers befriends Lloyd Vogel after Lloyd has been through estrangement, resentment, and real emotional closure. The friendship that forms is quieter, more deliberate, and more careful than Lloyd's earlier relationships. A Beautiful Day in the Neighborhood shows that friendships formed after loss are often built more carefully. The person who has lost something knows, in a specific way, how much friendship is worth.",
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
    print(f"  + {slug} / {h2}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(f"  ERROR: {e}")
    sys.exit(1)

out_path = os.path.join(ROOT, "seo-pages.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nseo-pages.json updated: {len(NEW_REFS)} new cultureRefs.")
