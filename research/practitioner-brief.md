# Practitioner Brief: How Real Organizations Compose Teams
### Research for the "Agent Forms" experiment — surveyed Oct 2, 2026

> Purpose: collect practitioner wisdom (Reddit, Hacker News, forums, books, company cases) on how humans compose high-performing groups, to inform experiments with multi-agent "agent forms." Each entry carries: the pattern/advice, numbers/ratios where cited, and the source. A final section distills quantified rules of thumb to test. **Widely-repeated lore is flagged as lore** vs. sourced data.

---

## 1. Optimal team size — the numbers that keep recurring

### 1a. Research data
- **Putnam & Myers (491 software projects, large corporation):** teams of **3–5 and 5–7 people completed similar-sized projects in ~11.9 and ~11.6 months**, vs. 9–11 people in ~17.1 months and 15–20 in ~16.3 months. In person-months, teams of 9–11 took **2.5–3.5× as long** as teams of 5–7 or 3–5. Conclusion: teams larger than ~7 were "just a way to spend money faster." *(sourced data, cited in an essay on team size — mirrored PDF at https://oriental-kitchens.com/userfiles/files/f4bf6eab-d643-4821-8536-9a60e82f19cc.pdf)*
- **Richard Hackman's rule of thumb:** optimal group size ≈ **4.6 people**; by *Leading Teams* he rounded to **6**. *(sourced research, same citation)*
- **Jennifer Mueller (Wharton):** "Above and beyond five, and you begin to see **diminishing motivation**"; beyond 5, cliques form and fewer people speak at a time. *(sourced research, same citation)*
- **Google Project Aristotle** (internal study of 180+ Google teams): the #1 predictor of team effectiveness was **psychological safety**, not size or talent mix — but teams that maintained it tended to be small. *(Google's published research; widely cited, from training knowledge)*

### 1b. Practitioner lore (repeated across Reddit/HN, consistent with data)
- **Scrum guide:** ≤10 people incl. Product Owner & Scrum Master; **3–9** developers. *(formal, but widely ignored in practice)*
- **Amazon "two-pizza" rule (Bezos):** no team larger than two pizzas can feed — in practice **5–10 people** (AWS ebook; Medium retrospectives cite **5–8**). Amazon's stated rationale: communication links scale as **n(n−1)/2**; a team of 6 has 15 links, a team of 12 has 66. AWS explicitly names the **Ringelmann effect** (individual productivity drops in larger groups / social loafing) as what two-pizza teams mitigate. Sources: https://d1.awsstatic.com.rproxy.goskope.com/onedam/marketing-channels/website/aws/en_US/whitepapers/approved/executive-insights/two-pizza-teams-ebook.pdf and https://medium.com/@sphoorti.patil/the-fall-of-the-headcount-mafia-ba7f1f7b9a00
- **Basecamp "Shape Up":** teams of **2–3 max** (one designer + one or two programmers), 6-week cycles, **no PMs, no standups**. "We think three is the ideal size for most things — complexity begins to increase exponentially beyond that." Source: https://signalvnoise.com/svn3/how-we-structure-our-work-and-teams-at-basecamp/
- **Spotify squads:** **6–12 people**, cross-functional, own one feature/service end-to-end; **no coordination roles** (architect Anders Ivarsson: "We deliberately didn't create coordination roles... teams that could coordinate themselves"). Source: https://blog.crisp.se/wp-content/uploads/2012/11/SpotifyScaling.pdf (via summaries at https://medium.com/the-post-project-world/why-most-companies-fail-when-the-copy-spotifys-squad-model-bed4585c3896)
- **Buurtzorg (Dutch home care):** self-managing nursing teams **max 12**; **split into two if >12, merge if <6**. ~10–12 nurses care for 40–60 patients per neighborhood. *(founder Jos de Blok; multiple case studies)* Source: https://www.andycleff.com/2025/05/buurtzorg-evolution-self-organizing-healthcare/
- **Big Tech practitioner (Pragmatic Engineer, Gergely Orosz):** "Each team of **5–15 people** has a clear vision and mission" — empowered autonomous teams are the building block; cross-functional for product teams. Source: https://blog.pragmaticengineer.com/project-management-at-big-tech/
- **Practitioner scrum essay (Medium, 2025):** ideal scrum team is **4–5 devs, 6th is the max**; specialists minimized; never 2 PMs over one team. Source: https://medium.com/@theproductref/this-staffing-is-wildly-wrong-for-a-scrum-team-e198bc019afe
- **Community engineering-manager playbook (GitHub):** split at **>8 people** ("split before communication overhead kills velocity"); standup >15 min = too many threads. Source: https://github.com/kesslerio/xagent/blob/HEAD/skills/skills/1kalin/afrexai-engineering-manager/SKILL.md *(lore — useful but not research)*

**Reddit color:** an r/programming thread on pair-programming formalizes the "too many cooks" micro-rule: **3+ people on one task = 1 driver + 2+ navigators** → the driver can't listen to 2+ directions. https://www.reddit.com/r/programming/comments/vj52oi/pair_programming_is_difficult/ ; a Blizzard game-forum thread generalizes it: "'Democratically' creating a video game is a very bad idea... too many cooks in the kitchen will mess with all the spices."

**Notable counter-current (2026):** Upwork CEO Hayden Brown declared in a May 2026 layoff memo (24% of workforce) that **"two-pizza teams are dead"** — arguing AI collapses the need for small coordinated teams because one person + AI can carry a whole team's workload. Widely reported; content aggregator link: https://www.mulvanecoop.com/news/story/1887311/upwork-stock-plunges-amid-24-layoffs-ceo-says-two-pizza-teams-are-dead *(corporate rhetoric, not data — but it's the first open break with the two-pizza orthodoxy)*

---

## 2. Coordination math — why small wins (sourced)

- **Communication channels = n(n−1)/2** (Brooks, *The Mythical Man-Month*, 1975): 4→6 links, 8→28, 20→190, 50→1,225. Bezos's justification for splitting rather than growing teams.
- **Brooks's Law:** "Adding manpower to a late software project makes it later." *(book)*
- **Ringelmann effect / social loafing:** individual effort declines as group size rises — named explicitly in AWS's two-pizza ebook as the failure mode the structure prevents.
- **Key structural choice from Amazon:** when demand grows, **spin off a new team instead of growing the existing one** — "prevent the accumulation of organizational mass from becoming a substitute for organizational performance." Each new team gets its own **single-threaded owner**. (Medium retrospective; also AWS ebook)

---

## 3. Span of control & middle management — cut it or keep it?

### 3a. What the 2023–2026 waves actually did (sourced numbers)
- **Uber restructuring (2026):** cut ~3,300 roles, trimmed manager population **~20%**, eliminated **close to half of "micro-teams"** (teams of 1–2 direct reports). Average span of control moved from **~3.0 to ~3.4** — i.e., only *half a management layer* removed, despite "flat org" narratives. Where did the work go? "Instead of decision-making moving down to the front line, things move up toward the CEO." Source: https://www.linkedin.com/pulse/should-you-eliminate-small-teams-ownership-threshold-test-cotton-uxpae
- **Meta:** managers forced to convert to IC rather than be laid off (reduces layers without exits). *(HN thread reports, anecdotal — https://news.ycombinator.com/item?id=37916545)*
- **Apple (Sept 2026, per Reuters via Substack):** new CEO John Ternus "considering an engineering-led overhaul that could include removing some middle-management roles to connect engineers more directly with senior executives" — explicitly tying it to AI acceleration. Source: https://laszlocser.substack.com/p/the-hollow-middle *(reporting-based, not confirmed company statement)*
- **Gartner:** 75% of HR leaders say managers are overwhelmed by expanded responsibilities; 69% say they aren't equipped to lead change. **McKinsey Health Institute:** middle managers report higher burnout than any other group. *(survey data, cited in LinkedIn analysis above)*
- **WSJ (Sept 2026):** "Why the Purge of Middle Managers Could Backfire" — economist David Deming (Harvard): "A manager doesn't produce any output, but they often coordinate the allocation of resources, and that coordination function can actually be done decently well with some technological tools" (e.g., AI agents in Slack). Source: https://www.wsj.com/lifestyle/careers/why-the-purge-of-middle-managers-could-backfire-6f9168bc

### 3b. HN wisdom — "Ask HN: Is middle management the most vulnerable/disposable?" (https://news.ycombinator.com/item?id=37916545)
Representative, high-signal comments (paraphrased; full thread linked):
- **The anti-myth top comment:** "A VP can't have 120 direct reports... It just doesn't scale." Layoffs hit wherever the company overhired — there's no evidence companies overhire middle management *more* than other roles. The "cut it all and nothing breaks" trope is a trope.
- **The rebuttal:** "Spans and layers" optimization *specifically* targets middle management — there's no equivalent lever for ICs alone.
- **Growth-phase trap:** companies hire middle managers on the *plan* of growing teams; when headcount targets change, there's a glut of managers whose teams never materialized. Vulnerability comes from **hiring-ahead-of-growth**, not from the role being useless.
- **The military analogy (highly upvoted):** "Do you think Captains are no longer needed in the military? What do they do that Majors, Colonels, and Generals can't? They *execute*... Lieutenants and Captains are on the actual battlefield... They're middle management." A middle manager that isn't in the trenches leading should be replaced — but the layer has a function.
- **Value-legibility rule:** "The 'safety' of your job depends on the value you add, *and on making that value legible to the company*." Management value is harder to make visible than IC value; managers produce long-term value, so they're the easy cut when cash runs out — "you can always hire them back if you survive."
- **The operational-layer cut:** "Middle management is vulnerable because it's operational (not tactical or strategic)... tech companies... cut out the managers that didn't have the minimum wingspan." Increasing managers' span while cutting managers-of-managers was the standard playbook.
- **Meta lesson:** middle managers forced to IC — keep technical chops current, since value is simpler to prove as a senior engineer than as a VP.

### 3c. Practitioner span-of-control guidance
- **Commonly cited reading of Grove (*High Output Management*):** effective span ~**6–8 direct reports**; wider spans for highly standardized/mature work, narrower for complex or junior work. *(lore-adjacent — Grove discusses task-relevant maturity and leverage, not a single magic number)*
- **Community EM playbook (GitHub):** 3–5 ICs → player-coach (still coding ~30–40%); 5–8 → full-time manager; 8–12 → split or add tech lead; **12+ → must split**. Source: https://github.com/kesslerio/xagent/blob/HEAD/skills/skills/1kalin/afrexai-engineering-manager/SKILL.md *(practitioner lore)*
- **Buurtzorg in the wild:** ~52 coaches + ~50 back-office staff + 2 directors supporting **10,000–11,000 nurses in ~1,200 teams** — i.e., coaches are explicitly *not* line managers ("coaches help teams work through problem-solving methods, but hold no conventional line-management authority"). Source: https://www.andycleff.com/2025/05/buurtzorg-evolution-self-organizing-healthcare/

### 3d. The nuance both sides agree on
- **Grove (*High Output Management*, 1983):** management's output = the output of the organization under it; **managerial leverage** is the test. One-on-ones exist to exchange information, not to report status; mode of control should match the task-relevant maturity of the report.
- **Google Project Oxygen** (2008+, people-analytics study): set out to prove managers don't matter — **found they measurably do** (impact on satisfaction, retention, performance). Identified 8 behaviors of good managers, in order: (1) be a good coach, (2) empower the team, don't micromanage, (3) care about success & well-being, (4) be productive/results-oriented, (5) be a good communicator/listener, (6) help with career development, (7) have clear vision/strategy, (8) have key technical skills to advise. **Technical skill ranked LAST** — "being a great developer doesn't necessarily make you a great manager." Sources: Forbes/HBR coverage; e.g. https://www.chegg.com/homework-help/questions-and-answers/section-case-study-google-s-project-oxygen-managers-matter-executive-summary-paper-present-q99832881
- **The "ownership threshold" test (LinkedIn, 2026):** "Remove the layer without transferring the judgment it was carrying and the work reappears one level up, on people who were already stretched." Cut the box only if you relocate the judgment.

---

## 4. Promoting top ICs to managers vs. keeping IC tracks

- **Charity Majors (Honeycomb CTO, QCon 2023):** the assumption "the best engineers make the best managers" is "crap." Making top IC a tech lead is treated as a one-way trip; the person stops coding, gets trapped, loses employability. She advocates the **manager–IC pendulum** — moving back and forth builds depth + breadth. "The best line managers should have already achieved senior engineer status" — but management and IC are different jobs, not rungs of one ladder. Source: https://thenewstack.io/tech-works-how-to-get-promoted-without-becoming-a-manager/?p=22740600
- **HN thread "If management isn't a promotion, then engineering isn't a demotion" (https://news.ycombinator.com/item?id=24444644):** counter-argument widely debated — the EM synthesizes inputs from team, staff/principal ICs, PMs, directors into staffing/roadmap/resource decisions, which "usurps and supersedes" staff-IC work *plus* career growth, hiring, budgets; some HNers argue EM legitimately sits atop the pyramid. Rejoinder that won broad agreement: **"If one group has firing power, and the other does not, they are not equal, regardless of what's written down."**
- **The dual-ladder failure mode (Medium, 2026):** companies create the Staff title on paper but management holds all real authority — the IC path becomes "ceremonial" and engineers keep choosing management. "A Principal Engineer should be able to change the direction of the company without needing twenty direct reports." Source: https://medium.com/@gkhanalkan_71996/your-best-developer-should-not-become-a-manager-companies-keep-promoting-them-anyway-b5911b5c618e
- **HN "Common Mistakes of New Engineering Managers" (https://news.ycombinator.com/item?id=26474947):** recurring trap — promoted IC keeps coding in the critical path and becomes the bottleneck; "tech lead" as title for "manager who still codes" confuses the org.
- **Net practitioner wisdom:** (1) separate ladders need *equal influence*, not equal titles; (2) promotion to management must be a *choice of craft*, not the only path to senior pay; (3) a technical bar for managers (Grove's task-relevant maturity; Oxygen's behavior #8) ≠ assuming the best coder becomes the best manager.

---

## 5. Self-managing / flat company cases (with numbers)

| Company | Model | Team unit | Scale / management layer | Source |
|---|---|---|---|---|
| **Valve** | No managers, no assigned projects; desks on wheels; teams self-form by "voting with their feet"; pay set by peer ranking (can't rank yourself); hiring/firing by teams. ~300 employees at the time. Handbook: "Nobody 'reports to' anybody else... This company is yours to steer." | Fluid project groups | 0 managers; founder/president "isn't your manager" | https://www.inc.com/... (handbook via https://warincontext.org/2012/06/24/whos-the-boss-there-isnt-one/) |
| Valve — the critique | Former employee **Jeri Ellsworth**: "a hidden layer of powerful management structure... it felt a lot like high school. There are popular kids that have acquired power." Old-timers vetoed hires as "not fitting the culture." | — | Flatness decays into informal hierarchy without explicit anti-mechanisms | https://Wiki.P2PFoundation.net/Jeri_Ellsworth_on_Problems_with_the_Flat_Management_at_Valve |
| **Morning Star** (world's largest tomato processor) | Self-management: no managers, no titles, no promotions. Coordination via **CLOUs** — Colleague Letters of Understanding: written personal commitments between colleagues. "400 leaders, 0 bosses." Swells to **2,400+ employees** in tomato season. | Mission-based groups bound by CLOUs | 0 managers | https://www.inc.com/audacious-companies/leigh-buchanan/morning-star.html |
| **W.L. Gore** (Gore-Tex) | **Lattice organization**: sponsors not bosses, associates not employees, "natural leadership defined by followership." Founder Bill Gore noticed he didn't know everyone at 200 people → policy: **no facility >150–200 people** ("get big by staying small" — split plants, pre-Dunbar, later confirmed by Dunbar's research). Peer-ranked compensation by quartile. | Small product teams; plants capped at ~150 | ~9,000+ associates across 45+ facilities | https://www.industryweek.com/leadership/companies-executives/article/21932742/the-right-chemistry ; https://www.scribd.com/document/261834146/Case-study-WL-Gore-Associates |
| **Haier** (China, appliances) | **Rendanheyi**: dismantled hierarchy into **4,000+ microenterprises** of **10–15 people** each owning a P&L and customer outcome. Internal markets replace approvals: microenterprises contract with each other for engineering/manufacturing/marketing. "Zero distance to the customer." | 10–15-person microenterprise with own P&L | ~40,000-person company run as a market of micro-firms | https://orbaos.com/downloads/case-study-haier.pdf ; https://en.wikipedia.org/wiki/Zhang_Ruimin |
| **Buurtzorg** | See §1b + §3c: teams ≤12, split/merge rule, coaches-not-managers, **60–65% of time** target on direct client care, BuurtzorgWeb IT platform "replaces middle managers," ~100 overhead staff for 10k+ nurses. | 10–12 nurse neighborhood teams | 52 coaches / 50 HQ / 2 directors | https://commandandscale.substack.com/p/management-never-disappears-it-just |
| **Spotify** (early 2010s) | Squads (6–12) → Tribes (40–150, capped at **Dunbar's number**) → Chapters (same-skill, cross-squad, chapter lead is line manager) → Guilds (interest communities). Deliberately **no PM/project-manager coordination roles**. | 6–12 squads; 40–150 tribes | Tribe lead = strategic direction only | https://medium.com/the-post-project-world/why-most-companies-fail-when-the-copy-spotifys-squad-model-bed4585c3896 |
| **GitLab** | All-remote; **handbook-first** culture: 5,000+ page public handbook as single source of truth; async by default (Slack messages auto-delete after 80 days; every meeting has a pre-circulated agenda doc). | Standard teams; coordination via writing, not meetings | ~2,000 employees, no offices | https://twosigmaventures.com/blog/article/going-remote-pt-i-five-lessons-from-scaling-gitlab/ |

**Cross-case pattern:** the successful flat/self-managing firms don't have *less* structure — they have structure of a different kind: explicit size caps with split rules (Gore, Buurtzorg), written commitment contracts (Morning Star CLOUs), internal markets (Haier), or a shared written record (GitLab handbook). As one 2026 essay puts it: **"Management never disappears; it just moves somewhere else."** (https://commandandscale.substack.com/p/management-never-disappears-it-just)

---

## 6. What the books say (actionable composition advice)

- ***Team of Teams* (McChrystal, 2015):** In Iraq, Task Force speed came from **"shared consciousness + empowered execution"**: liaison officers embedded across units, daily O&I briefs (60–90 seconds per unit), and leaders shifting to **"eyes on, hands off."** Composition advice: don't reorganize the boxes — build the *lateral network* (liaisons) so small teams can act on a common picture without waiting up the chain.
- ***High Output Management* (Grove, 1983):** judge every activity by **managerial leverage** (org output vs. your own output); match the mode of control to the subordinate's **task-relevant maturity**; use one-on-ones for information exchange, not status. Composition implication: the manager's unit size should be set by the maturity of the work, not by a fixed span.
- ***Team Topologies* (Skelton & Pais, 2019):** organize around four team types (stream-aligned, enabling, complicated-subsystem, platform) and three interaction modes (collaboration, X-as-a-service, facilitating). The binding constraint is **team cognitive load** — keep it within what one team can hold, and change team boundaries or interactions when it overflows. *(book; Skelton/Pais later wrote the "Team Guide" with similar heuristics)*
- ***The Culture Code* (Coyle, 2018):** high-performing groups build culture via three skills — **(1) build safety** (belonging cues: "we are connected, we share a future"), **(2) share vulnerability** (vulnerability loops: leader goes first), **(3) establish purpose** (simple, repeated narratives). Cases: SEAL Team 6, Pixar, San Antonio Spurs, Johnson & Johnson's Tylenol response.
- ***Reinventing Organizations* (Laloux, 2014):** three "teal" breakthroughs — **self-management, wholeness, evolutionary purpose** — with cases Buurtzorg, Morning Star, AES, FAVI, Patagonia. Practical devices: advice process (anyone can decide after seeking advice), peer-based conflict resolution, no fixed job descriptions.
- ***Good to Great* (Collins, 2001):** **"First who, then what"** — get the right people on the bus before deciding where to drive it; **Level 5 leadership** (humility + fierce resolve); confront the brutal facts. Composition implication: selection (who) dominates structure (how).
- ***Accelerate* (Forsgren, Humble & Kim, 2018):** DORA's four key metrics — **deployment frequency, lead time for changes, change failure rate, time to restore**. 2017 findings: elite performers deploy **46× more frequently**, with **440× faster lead time**, **96× faster recovery**, **5× lower change failure**. Of 24 capabilities, the strongest predictors included **loosely coupled architecture AND loosely coupled teams**, lean product management, and generative (Westrum) culture. Composition implication: team boundaries should mirror service boundaries (Conway's law, deliberately applied).

---

## 7. Military & tribal analogues — the "village" the user asked about

### 7a. US Marine Corps rifle squad — the canonical small-unit template
- **13 Marines**: 1 squad leader (sergeant) + **3 fire teams of 4**.
- Each fire team: **corporal team leader/grenadier** + **automatic rifleman** + **assistant automatic rifleman** + **rifleman**.
- After years of experimentation with 14–15-person squads (2025 Force Design decision), the Corps **settled on 13**: "any less than that indicated risk regarding resilience within the formation" (casualty tolerance). The 2025 revamp adds an **organic precision-fires specialist** (drone operator) to each squad.
- Sources: https://military.com/daily-news/2025/04/08/top-marine-says-service-has-finally-settled-13-grunt-rifle-squads.html ; composition detail: https://www.scribd.com/presentation/216600473/Composition-of-Rifle-Squad-and-Formations
- **US Army infantry squad** (contrast): squad leader + **two fire teams**; the **medic is attached at platoon level** (platoon medic + RTO), not inside the squad. Source: https://www.globalsecurity.org/military/library/policy/army/accp/in0503/ch1.htm
- **Role pattern for agent forms:** every viable small unit has (a) a leader who owns the mission, (b) peer sub-teams/pairs with defined specialties (heavy fire = builder/coder; grenadier = flexible problem-solver; medic = healer/reviewer; RTO = communicator/propagandist-broadcaster), and (c) **redundant capability** — the assistant automatic rifleman exists so the team survives losing a member. Casualty resilience, not efficiency, set the size.

### 7b. Dunbar's layers — the anthropology of group sizes
From evolutionary anthropologist **Robin Dunbar** (brain-size/social-group correlation research):
- **5** — support clique ("shoulders to cry on"; ~40% of social time goes here)
- **12–15** — sympathy group ("if someone died in this group you would be devastated"; +20% of social time; 60% of total social effort goes to these 15)
- **30–50** — band / close friends
- **150** — active network (Dunbar's number; stable relationships ceiling)
- **500** — acquaintances; **1,500** — name-to-face recognition
- Each layer ≈ **3×** the previous; layers appear in phone records, social media, hunter-gatherer bands, and military company sizes.
- Sources: Dunbar himself on the Jim Rutt Show transcript (https://jimruttshow.blubrry.net/the-jim-rutt-show-transcripts/transcript-of-episode-140-robin-dunbar-on-friendship/); summary (https://podcastnotes.org/investors-field-guide/robin-dunbar-optimizing-human-connection-with-dunbars-number-invest-like-the-best-with-patrick-oshaughnessy-ep-367/)
- **Organizational instantiations:** Gore's 150-person plant cap; Spotify tribes capped at 40–150 "beyond which informal coordination breaks down."

### 7c. Traditional village craft specialization (lore, clearly labeled)
- Medieval/traditional craft organization ran on **master–journeyman–apprentice** tiers inside guilds: a small number of masters set standards, journeymen did the bulk of production, apprentices learned by doing. The ratio logic (few teachers, many practitioners) parallels Dunbar's support-clique of ~5 and the modern "player-coach" manager span.
- Tribal bands (~30–50) typically sustained full-time specialists only at small ratios — healers/shamans, toolmakers, and storytellers/propagandists were usually **1 per band**, i.e., ~2–3% specialist density with the rest generalist producers. *(general anthropological pattern, not a single sourced study — treat as lore to test, not data)*
- The user's "village" intuition maps cleanly onto the military squad and the Spotify squad: **generalist producers + 1–2 embedded specialists + a mission-owning leader**, held together by a shared purpose narrative (the "propagandist" role = internal culture/story function).

---

## 8. Failure modes to avoid (from the sources above)

1. **Too many cooks:** beyond ~7–8 per team, coordination cost dominates; Putnam & Myers measured 2.5–3.5× worse person-month efficiency. *(data)*
2. **Hidden hierarchy:** Valve's flatness decayed into "high-school" informal power (Ellsworth); Morning Star avoids it with written CLOUs. Flatness needs explicit anti-mechanisms. *(case)*
3. **20% do 80%:** Pareto/Price's-law lore is widely repeated; the sourced version is **Microsoft's finding that 80% of Windows/Office crashes came from 20% of bugs** — i.e., output concentration shows up in *defects*, not proven in code authorship. Avoid designing around an unverified 80/20 authorship claim. *(DEV discussion: https://dev.to/ceri_anne_dev/comment/d1l8)*
4. **Promoting the best IC into a mediocre manager** — kills both the IC's output and adds management drag. *(Majors, Oxygen #8)*
5. **Cutting the layer without moving the judgment:** Uber's span 3.0→3.4 saved money but pushed decisions *up* to the CEO. *(sourced 2026)*
6. **Growing teams instead of splitting them** when demand rises — Amazon's anti-pattern; communication mass substitutes for performance. *(Amazon lore)*
7. **Copying Spotify's boxes without its principles** — renaming teams "squads" while keeping old governance "defeats the whole purpose" (ING via McKinsey). *(multiple sources)*
8. **Ceremonial IC ladders:** titles without influence push everyone back toward management. *(2026 practitioner essay)*

---

## 9. Rules of thumb to test (quantified heuristics for the agent-forms experiments)

> Flagged **[D]** = backed by data/research; **[L]** = widely-repeated practitioner lore; **[C]** = company case. Design experiments that try to *falsify* each.

1. **Team size 5–9 for a delivery unit; never >12 without splitting.** [D: Hackman ~4.6/6; Putnam & Myers 3–7 optimal; L: two-pizza 5–10; C: Buurtzorg split>12/merge<6, Spotify 6–12] — *Test: does agent-team throughput per unit cost peak at 5–7 agents and degrade measurably beyond 9?*
2. **One mission, one owner.** [L/C: Amazon single-threaded owner; USMC squad leader owns "all the squad does or fails to do"] — *Test: agent teams with a designated "owner" agent vs. leaderless teams on the same task.*
3. **Split, don't grow.** When workload doubles, spawn a second team with its own owner rather than adding agents to the first. [L: Amazon two-pizza split rule; C: Gore plant splits, Buurtzorg team splits] — *Test: 2×(5-agent teams) vs. 1×(10-agent team) on a decomposable task.*
4. **1 coordinator per 5–9 producers; player-coach below 5.** [L: EM playbook ratios; C: Buurtzorg coaches-not-managers; D-adjacent: Grove task-relevant maturity] — *Test: overhead agents (planners/critics) at ratios 1:4, 1:7, 1:12 — where does coordination cost exceed benefit?*
5. **Specialist density ~1 per 10–15 generalists.** [L: tribal band 1 healer/toolmaker per ~30–50; C: USMC 1 medic per platoon (~40), 1 drone specialist per squad of 13 in 2025] — *Test: reviewer/researcher/critic specialist agents at 1:5, 1:10, 1:15.*
6. **Redundancy ≥2 deep on every critical role.** [C: USMC assistant automatic rifleman; "settled on 13 because fewer indicated casualty risk"] — *Test: agent teams with backup capability on the planner/coder/reviewer roles vs. single points of failure; inject agent "casualties" (context loss) and measure resilience.*
7. **Tribe cap ~40–150 for informal coordination; beyond that, formalize.** [D: Dunbar 150; C: Gore plant cap 150–200, Spotify tribes 40–150] — *Test: at what agent count does a shared-context (broadcast) coordination scheme break down vs. structured protocols?*
8. **Keep the IC track influential, not ceremonial.** [L: Majors pendulum; HN "firing power" argument; D: Oxygen — coaching/empowerment outrank technical skill] — *Test: give top-performing agent specialists veto/advisory power (not just the manager agent) and measure whether decision quality improves vs. manager-only authority.*
9. **Measure the 20/80 concentration; don't assume it.** [D: Microsoft 80/20 bugs; putnam-myers person-month data] — *Test: instrument which agents produce the output vs. idle; prune or re-role chronic idlers (the user's "80% idling" failure mode) and measure delta.*
10. **Written commitments beat org charts.** [C: Morning Star CLOUs; GitLab handbook; Amazon 6-pager/PR-FAQ] — *Test: agent teams initialized with explicit written role contracts vs. implicit roles; measure drift and duplication.*

---

*Method note: web research conducted Oct 2, 2026 via search + direct page reads. Book summaries are from the published texts (chapter-level advice), not from fresh reads this session. Reddit results were thin on direct thread URLs for "optimal team size" debates — the quantitative core above comes from cited research and HN threads instead; Reddit links included where found. No code written per task instructions.*
