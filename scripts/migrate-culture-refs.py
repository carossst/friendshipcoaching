#!/usr/bin/env python3
"""Migrate embedded cultural-reference paragraphs to cultureRef fields."""
import json
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "seo-pages.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# (slug, h2, paragraph_prefix, show_label, simplified_body)
MIGRATIONS = [
    (
        "why-making-friends-as-an-adult-is-hard",
        "There is less built-in repetition",
        "Marta Kauffman and David Crane",
        "Friends · NBC",
        "Friends shows what passive infrastructure looks like. Monica's group lives across the hall from each other. They share the same spot at Central Perk. Nobody plans their time together. It just happens. That contact adds up to the 50 hours Jeffrey Hall found it takes to build a real friendship. When Monica and Chandler move to the suburbs, the group starts to fracture. The friendship was not the special part. The infrastructure was. Without it, adults have to create contact on purpose.",
    ),
    (
        "why-making-friends-as-an-adult-is-hard",
        "Friendship is about shared context, not proximity",
        "Amy Sherman-Palladino",
        "The Marvelous Mrs. Maisel · Amazon",
        "Midge and Susie come from completely different worlds. One is a wealthy housewife. The other is a scrappy club manager barely making rent. What connects them is not where they live. It is a shared mission: comedy. That shared purpose creates its own context. Friendship built on shared purpose can cross lines that proximity never could.",
    ),
    (
        "why-making-friends-as-an-adult-is-hard",
        "Many adults are afraid of seeming awkward, eager, or needy",
        "In her book Platonic (2022), psychologist Dr. Marisa",
        "Platonic · Dr. Marisa G. Franco (2022)",
        "In her book Platonic (2022), Dr. Marisa G. Franco argues that waiting for friendship to happen by accident is a losing strategy. Her research found that people who build strong social lives are not the most charming. They are the most proactive. They reach out before they are certain the other person will respond. They follow through on plans. They keep investing before the connection is secure. Friendship does not happen to people who wait. It happens to people who keep acting.",
    ),
    (
        "how-to-keep-friends-as-an-adult",
        "Make contact repeatable, not heroic",
        "Elizabeth Meriwether",
        "New Girl · Fox",
        "In New Girl, Nick, Schmidt, and Winston do not stay close through emotional check-ins. They stay close through routines: the same couch, the loft's rituals, the side-by-side texture of daily life that nobody plans. When those routines are there, the friendship takes care of itself. When they are disrupted, someone has to make a conscious effort.",
    ),
    (
        "how-to-keep-friends-as-an-adult",
        "Act on the thought, micro-maintenance works",
        "Bill Lawrence's Scrubs shows this in practice",
        "Scrubs · NBC",
        "In Scrubs, J.D. and Turk do not stay close through deep conversations. They stay close through small rituals: the special handshake, the inside jokes, the habit of showing up in each other's day. Those habits cost almost nothing. But without them, the closeness has nowhere to live.",
    ),
    (
        "how-to-keep-friends-as-an-adult",
        "Let the friendship fit real life",
        "In his book Friends (2021), Dunbar extends",
        "Friends · Robin Dunbar (2021)",
        "In his book Friends (2021), Robin Dunbar explains why limits matter. Your brain can sustain only a small number of close friendships at once. Knowing this does not lower the bar. It clarifies the priority. The few relationships in your inner circle deserve consistent attention. The rest can stay at the surface.",
    ),
    (
        "how-to-be-a-better-friend",
        "Pay attention to what matters to the other person",
        "Greg Daniels and Michael Schur's Parks and Recreation",
        "Parks and Recreation · NBC",
        "In Parks and Recreation, Leslie Knope remembers everything about Ann. Her goals. Her struggles. Her small victories. Leslie is not always available. But she is always paying attention. Ann knows that what she shares with Leslie will not be forgotten by next week. That is what responsiveness looks like in practice.",
    ),
    (
        "how-to-be-a-better-friend",
        "Notice who is doing the pushing",
        "Issa Rae's Insecure tracks this dynamic",
        "Insecure · HBO",
        "In Insecure, Issa and Molly take turns being the one who pulls while the other pushes. At different points in the series, one of them barely shows up while the other carries the friendship. What eventually works is not patience or space. It is a direct conversation about the friendship itself. Dr. Miriam Kirmayer calls this meta-communication: naming the dynamic instead of letting it quietly erode the connection.",
    ),
    (
        "how-to-be-a-better-friend",
        "Ask for help, it deepens friendship both ways",
        "Marta Kauffman's Grace and Frankie",
        "Grace and Frankie · Netflix",
        "In Grace and Frankie, two women who never would have chosen each other end up becoming real friends. Their bond does not grow through warmth or shared values. It grows through necessity. They keep needing each other in specific ways. They have to ask for help directly. That mutual dependency is what makes the relationship real. Admitting that you need someone is one of the fastest ways to deepen a friendship.",
    ),
    (
        "how-to-be-a-better-friend",
        "Aim for friendships that lift both of you",
        "Ted Lasso shows what Aristotle",
        "Ted Lasso · Apple TV+",
        "In Ted Lasso, Rebecca and Keeley have almost nothing in common on the surface. What sustains their friendship is specific: each one invests in the other's growth. Rebecca encourages Keeley's ambition without competing with it. Keeley brings honesty into a space where Rebecca is guarded. They make each other's lives larger. That is what Aristotle called friendship of virtue.",
    ),
    (
        "how-to-be-a-better-friend",
        "Let care be practical, not only emotional",
        "Bill Lawrence, Jason Segel, and Brett Goldstein's Shrinking",
        "Shrinking · Apple TV+",
        "In Shrinking, Paul's approach to Jimmy's grief is not gentle. He pushes back. He holds Jimmy accountable. He refuses to let Jimmy disappear into avoidance. But he makes it clear the investment is real. That combination of firmness and care is what Jeffrey Hall calls showing up in usable ways. It is not the most comfortable form of friendship. It is sometimes the most useful one.",
    ),
    (
        "how-to-make-friends-after-30",
        "Build slowly, but keep building",
        "Liz Feldman's Dead to Me makes a related point about unlikely",
        "Dead to Me · Netflix",
        "In Dead to Me, Jen and Judy meet in a grief support group in their forties. They have almost nothing in common. Different temperaments. Different histories. Different ways of handling loss. What allows the friendship to grow is simple: they keep showing up in the same place. The connection is not instant. The fit is not obvious. It deepens slowly through repeated contact. That is how most adult friendships after 30 actually work.",
    ),
    (
        "how-to-stay-friends-after-a-baby",
        "New parents are not rejecting you. They are surviving.",
        "Carter Bays and Craig Thomas's How I Met Your Mother",
        "How I Met Your Mother · CBS",
        "In How I Met Your Mother, when Marshall and Lily have a baby, the group's social budget changes overnight. The spontaneous pub evenings and late plans disappear. The rest of the group takes time to adjust. The ones who adapt most successfully stop expecting the old rhythm and find a new one that actually fits. That adjustment does not happen on its own.",
    ),
    (
        "how-to-stay-friends-after-a-baby",
        "Lower the bar for what contact looks like",
        "Catherine Reitman's Workin' Moms",
        "Workin' Moms · CBC/Netflix",
        "In Workin' Moms, the friendships survive not because the women maintain them perfectly. They survive because they strip away the performance. Nobody is expected to have it together. A rushed conversation in a parking lot between nap schedules counts. A coffee that ends abruptly counts. Lowering that bar is not settling for less. It is the only format that works when everything is already too much.",
    ),
    (
        "one-sided-friendship",
        "Why friendships become one-sided",
        "Chuck Lorre's The Big Bang Theory",
        "The Big Bang Theory · CBS",
        "In The Big Bang Theory, Leonard absorbs Sheldon's demands at continuous cost to his own time and boundaries. He shields Sheldon from every friction of adult life. It looks like loyalty. But it functions like codependency. Carrying someone else's relational weight without limit drains the person doing it. It also removes any incentive for the other person to change. What gets called patience is often self-sabotage that helps neither side.",
    ),
    (
        "how-to-make-friends-when-you-work-from-home",
        "Choose one recurring context and commit to it",
        "Greg Daniels' The Office illustrates",
        "The Office · NBC",
        "In The Office, Jim and Pam's connection builds through hundreds of hours of ambient proximity. Shared glances. Small acts of solidarity. Tiny moments nobody scheduled. The office did all of that work automatically. Remote work removes not just the people but the system that turned proximity into friendship. Replacing it with one deliberate, recurring context is the closest adult equivalent.",
    ),
    (
        "how-to-follow-up-after-meeting-someone",
        "Why the follow-up feels so hard",
        "Steven Moffat and Mark Gatiss",
        "Sherlock · BBC",
        "In Sherlock, John Watson's first encounter with Sherlock Holmes is, by most social standards, a disaster. Chaotic. Confusing. Deeply unusual. By every conventional reading, there is no reason to follow up. Watson follows up anyway. He shows up for the second interaction despite the chaos of the first. That willingness to move past an imperfect first encounter is almost always what separates a connection that goes somewhere from one that stays a pleasant memory.",
    ),
    (
        "why-do-friendships-fade",
        "The structure disappears and the friendship goes with it",
        "Sex and the City makes this pattern",
        "Sex and the City · HBO",
        "In Sex and the City, Miranda moves to Brooklyn and the group starts to struggle. But the real issue is not geography. Brooklyn is close. What the others resist is adapting to Miranda's changed life: a baby, different hours, different priorities. The group expects Miranda to absorb all the adjustment herself. When a social circle makes someone maintain the old format alone after a life change, the friendship does not fade by accident. The group chooses not to adapt.",
    ),
    (
        "why-do-friendships-fade",
        "The friendship shifts but nobody names it",
        "Elena Ferrante's novel My Brilliant Friend",
        "My Brilliant Friend · Elena Ferrante",
        "In My Brilliant Friend, Elena and Lila begin as inseparable childhood friends in postwar Naples. As Elena pursues education and moves upward, the gap between their lives widens. The friendship does not break in one moment. It bends, contracts, goes silent, and resurfaces. Ferrante's insight is that the most enduring friendships are not the smoothest ones. They are the ones where at least one person eventually names what has shifted, rather than letting the gap become the permanent state.",
    ),
    (
        "how-to-turn-acquaintances-into-friends",
        "Why the acquaintance stage gets stuck",
        "Dan and Eugene Levy's Schitt's Creek",
        "Schitt's Creek · CBC",
        "In Schitt's Creek, David and Stevie interact for weeks in a purely transactional way: guest and front-desk attendant. The shift happens not through a dramatic conversation but through small accumulated moments: shared observations, a reluctant drink, a quiet act of mutual recognition. Neither of them announces that they are becoming friends. The repetition does it without anyone deciding.",
    ),
    (
        "how-to-turn-acquaintances-into-friends",
        "The move that changes things",
        "Dan Goor and Michael Schur's Brooklyn Nine-Nine",
        "Brooklyn Nine-Nine · NBC",
        "In Brooklyn Nine-Nine, Jake Peralta's investment in his friendship with Charles Boyle is not subtle. He makes it concrete. He shows up. He celebrates the connection without pretending it requires less than it does. Charles matches the investment. Neither of them waits for the friendship to become official on its own. They act like it already is. That willingness to go one step further than the situation technically requires is exactly what turns a colleague into something else.",
    ),
    (
        "how-to-turn-acquaintances-into-friends",
        "Repeat contact is more important than one great conversation",
        "George Kay's Lupin offers",
        "Lupin · Netflix",
        "In Lupin, Assane Diop and Benjamin Ferel begin as school acquaintances with no particular depth to their connection. What transforms them over the years is not one meaningful conversation. It is a series of situations where each one keeps showing up for the other. They build what researchers call operational trust: the kind created not through emotional disclosure but through repeated evidence that the other person can be counted on. That is a slower path to closeness than a breakthrough conversation. But it is a real one.",
    ),
    (
        "how-to-make-friends-as-an-expat",
        "Other expats are an easier starting point",
        "Darren Star's Emily in Paris captures",
        "Emily in Paris · Netflix",
        "In Emily in Paris, Emily's first real social anchor is Mindy, a fellow expat. Mindy already understands the specific mix of excitement and displacement that comes with living abroad. She has no expectation of who Emily was before. That shared situation creates an immediate shortcut to warmth. It does not produce the deepest friendships. But it provides a base while the harder work of connecting with locals takes shape.",
    ),
    (
        "how-to-make-friends-as-an-expat",
        "Lower your expectations for the timeline",
        "Eric Rochant's espionage series The Bureau",
        "The Bureau · Canal+",
        "In The Bureau, Malotru returns from years undercover in Syria to find that his old social network no longer fits. The people who knew him before remember who he was, not who the experience made him. Rebuilding connection after a long time abroad, whether from intelligence work or ordinary expat life, requires starting from what is true now. Picking up where things were left rarely works.",
    ),
    (
        "how-to-know-if-someone-wants-to-be-your-friend",
        "Signs someone is interested in becoming friends",
        "Ted Lasso makes this legible",
        "Ted Lasso · Apple TV+",
        "In Ted Lasso, Ted brings Rebecca a tin of shortbread biscuits every morning. Not once. Every morning. Rebecca is cold and gives him nothing in return for weeks. But she keeps the tin. She never tells him to stop. That pattern tells him something. In real life, the signals work the same way. Someone who keeps showing up in small ways, remembering the detail from last week, suggesting the specific plan, is doing the equivalent of bringing the biscuits.",
    ),
    (
        "when-a-friendship-ends",
        "When something needs to be said",
        "The adaptation of Sally Rooney's Normal People",
        "Normal People · Hulu/BBC Three",
        "In Normal People, Connell and Marianne's connection is repeatedly interrupted by status shifts. What makes each rupture so hard to repair is that neither of them names what has changed. They absorb each shift silently rather than saying: the dynamic between us has changed, here is what I need now. Most friendship fractures that deepen into endings do so not because the rupture was irreparable, but because nobody spoke to it clearly when it was still small.",
    ),
    (
        "when-a-friendship-ends",
        "How to close a friendship with care",
        "Netflix's French comedy series The Hook Up Plan",
        "Plan Coeur · Netflix",
        "In Plan Coeur, Charlotte and Milou secretly hire an escort to rebuild Elsa's confidence after a breakup. The intention is care. The method is control. What they reveal is a risk specific to long-term friendships: the assumption that shared history grants ownership. Because they have known Elsa since school, they decide they understand what she needs better than she does. The longer the history, the easier it becomes to treat someone as a project rather than a person. When that line is crossed, regardless of intent, the trust structure of the friendship breaks.",
    ),
    (
        "how-to-make-friends-as-a-new-parent",
        "The baby is the opening. You have to do the rest.",
        "Liz Feldman's Dead to Me makes a version of this point through",
        "Dead to Me · Netflix",
        "In Dead to Me, Jen and Judy meet in a grief support group, both overwhelmed and low on bandwidth. What works between them is not polish or patience. It is radical honesty from the start, cutting through the social performance that usually precedes real friendship. For parents who are already exhausted, the same principle applies. The warmth from a playground exchange is enough to act on. You do not need to wait until you have enough energy to be impressive.",
    ),
    (
        "how-to-keep-work-friendships-after-going-remote",
        "The real question: work friend or actual friend?",
        "Fanny Herrero's French series Dix pour cent",
        "Call My Agent · France.tv",
        "In Call My Agent, Mathias and Andrea spend years as rivals inside the same talent agency. They compete for clients, undermine each other's deals, and clash on almost every decision. What eventually transforms the rivalry into something durable is not warmth. It is the accumulation of high-stakes situations where each one keeps choosing to rely on the other's judgment. Friendship born from professional friction inside a shared system is not the warmest version. But it is often the most loyal.",
    ),
    # Older film batch
    (
        "why-making-friends-as-an-adult-is-hard",
        "The answer is not to force it. It is to practice it.",
        "The Shawshank Redemption offers",
        "The Shawshank Redemption · Film",
        "In The Shawshank Redemption, Andy and Red's bond is not just pleasant company. It is a psychological anchor. It keeps both men oriented and resilient under conditions designed to break them. Adults face far less extreme conditions. But the mechanism is the same. Close friendship is one of the most effective protections against the slow erosion of wellbeing that isolation produces.",
    ),
    (
        "how-to-meet-people-in-a-new-city",
        "Accept that building a social life takes repetition",
        "The film I Love You, Man illustrates",
        "I Love You, Man · Film",
        "In I Love You, Man, Peter's early attempts at friendship fail because he treats each encounter like a first date. He is searching for instant chemistry. It only works when he meets Sydney and they start doing the same activity together: jamming in a garage, walking the dog, spending time side by side without pressure. The hours accumulate. The friendship follows.",
    ),
    (
        "how-to-make-friends-after-30",
        "Stop comparing adult friendship to school friendship",
        "The film Frances Ha captures",
        "Frances Ha · Film",
        "In Frances Ha, Frances and Sophie are inseparable in their early twenties. Then Sophie moves forward: she marries, relocates, and builds a different life. The friendship strains. Their closeness depended on identical circumstances. When those circumstances changed, the friendship needed explicit renegotiation. Not just the assumption that things would stay the same. That renegotiation is exactly what friendship in your 30s requires.",
    ),
    (
        "why-male-friendships-fade",
        "What actually works",
        "Think of a film like Superbad",
        "Superbad · Film",
        "In Superbad, Evan and Seth's friendship holds not because of deep conversations. It holds because they share a mission and spend time side by side. That is exactly what Robin Dunbar's research describes. Adult male friendship is rarely sustained by phone calls. It is built through shared activity, common routines, and the hours that accumulate when two people are doing something together.",
    ),
    (
        "how-to-introduce-friends-to-each-other",
        "Consider whether there is enough in common to make an introduction worth it",
        "Bridesmaids shows what happens when the framing",
        "Bridesmaids · Film",
        "In Bridesmaids, Annie and Helen are forced into proximity through a mutual friend's engagement. Nobody manages the transition with care. People from different seasons of your life carry different histories and sometimes a quiet competition for the same loyalty. An introduction that ignores those tensions tends to amplify them. One that names the connection clearly and gives both people a reason to be glad the other exists starts from a much stronger position.",
    ),
    (
        "when-a-friendship-ends",
        "The fade is the most common ending, and the hardest to read",
        "Not all endings fade. The Banshees of Inisherin offers",
        "The Banshees of Inisherin · Film",
        "In The Banshees of Inisherin, Colm simply decides one day that the friendship is over. No conflict. No explanation. His remaining time has become more valuable to him than the connection. It is an extreme version of a real pattern. Sometimes a friendship ends not because of conflict or distance, but because one person has quietly reallocated their time. The person left behind has no fault to name and no clear reason to hold. That kind of ending is among the hardest to process, because there is nothing to argue with.",
    ),
    (
        "one-sided-friendship",
        "What to try before you give up",
        "The Cable Guy pushes this dynamic",
        "The Cable Guy · Film",
        "In The Cable Guy, a person so starved for connection ignores every signal of discomfort and escalates past every boundary. The exaggeration is comic. But the mechanism it parodies is real. Healthy repetition in an early friendship requires mutual consent. If only one person is driving the pace and the other is quietly retreating, the dynamic is already one-sided. Reading those signals early is what separates persistence from pressure.",
    ),
    (
        "how-to-make-friends-when-you-work-from-home",
        "The real problem with remote work and friendship",
        "The film Office Space illustrates this with unusual",
        "Office Space · Film",
        "In Office Space, friendships form not because anyone tries. They form because of shared space, shared grievances, and the same daily rhythm. Nobody is working to build connection. It just happens. When you move to remote work, that invisible infrastructure vanishes. The connections that formed passively have nothing left to sustain them.",
    ),
    (
        "how-to-keep-work-friendships-after-going-remote",
        "The office was doing the work. Now you have to.",
        "The Intern shows how much shared physical space",
        "The Intern · Film",
        "In The Intern, Jules and Ben's connection builds through daily proximity, small observations, and a steady stream of moments that nobody scheduled. He sees her under pressure. She sees him steady. When that shared space disappears, so does the effortless insight into each other's days. What was once automatic has to become deliberate: a proactive check-in, a question you would have asked in the hallway, attention that used to happen without anyone trying.",
    ),
    # Additional: Wine Country
    (
        "how-to-make-friends-after-a-friendship-ends",
        "Use what the loss taught you",
        "Wine Country illustrates",
        "Wine Country · Film",
        "In Wine Country, a group of friends in their late forties gather for a birthday trip. They spend much of it confronting how much has shifted since their twenties. Some of the closeness they assumed was still intact turns out to be sentiment about who they once were together. Letting go of a version of a friendship that no longer fits, even when the affection is real, clears the space to build something that fits your current life instead of your past one.",
    ),
]


def find_guide(data, slug):
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
successes = []

for slug, h2, prefix, show, body in MIGRATIONS:
    guide = find_guide(data, slug)
    if not guide:
        errors.append(f"Guide not found: {slug}")
        continue

    section = find_section(guide, h2)
    if not section:
        errors.append(f"Section not found: {slug} / {h2}")
        continue

    paras = section.get("paragraphs", [])
    idx_to_remove = None
    for i, p in enumerate(paras):
        if p.startswith(prefix):
            idx_to_remove = i
            break

    if idx_to_remove is None:
        errors.append(
            f"Paragraph not found: {slug} / {h2} / prefix: {prefix[:60]}"
        )
        continue

    paras.pop(idx_to_remove)
    section["cultureRef"] = {"show": show, "body": body}
    successes.append(f"OK: {slug} / {h2}")

print(f"Successes: {len(successes)}/{len(MIGRATIONS)}")
for s in successes:
    print(f"  {s}")
if errors:
    print(f"\nErrors: {len(errors)}")
    for e in errors:
        print(f"  ERROR: {e}")
    sys.exit(1)

out_path = os.path.join(ROOT, "seo-pages.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nseo-pages.json updated ({len(MIGRATIONS)} migrations applied).")
