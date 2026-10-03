# Organizational Science Brief: Evidence on Team Composition & Performance
**For the agent-forms project** — using organizational wisdom to design multi-agent AI teams.
Research date: 2026-10-02. Each section lists claims, numbers, sources, and an evidence-strength flag:
- 🟢 **Well-evidenced**: replicated / peer-reviewed / large samples
- 🟡 **Case evidence**: real orgs with documented outcomes, n=1 or few
- 🔴 **Anecdotal / practitioner lore**: widely repeated, thin data

---

## 1. Team Role Taxonomies (Belbin)

**The 9 roles** (Belbin, 1981 — *Management Teams: Why They Succeed or Fail*):
- **Action-oriented:** Shaper (drives action), Implementer (turns ideas into practice), Completer-Finisher (quality/precision).
- **People-oriented:** Coordinator (delegates/facilitates), Teamworker (harmony/cohesion), Resource Investigator (external links, enthusiasm).
- **Thought-oriented:** Plant (creative ideas), Monitor Evaluator (analytical judgment), Specialist (deep technical knowledge).

**Claims:**
- Belbin's conclusion: *"balanced teams perform best"* — mixed-role teams beat homogeneous ones. Prichard & Stanton (1999, *Journal of Management Development*): 6 mixed teams (1 Coordinator + 1 Plant + 1 Completer Finisher + 1 Teamworker) outperformed 6 all-Shaper teams on task performance. 🟡 (small n, supportive but thin)
- Senior & Swailes (2004, *Journal of Occupational and Organizational Psychology*): Belbin's Self-Perception Inventory has weak psychometric validity — the role measures overlap and self-report bias is real. So Belbin is a useful **design vocabulary**, not a validated measurement instrument. 🟢
- Meta-finding across reviews (e.g., Bedwell et al. 2014): **no single "golden" role mixture** has been empirically validated. What predicts success is (a) coverage of roles (fewer unfilled critical roles), (b) absence of destructive overlap (e.g., multiple Shapers with no Teamworker), and (c) role *behavior* exhibited, not role labels assigned. 🟢 (review-level)
- Belbin himself never prescribed percentages; the operative rule was "no critical gaps, no duplicate dominants." 🟡

**Link:** https://en.wikipedia.org/wiki/Team_Role_Inventories

**Agent-form takeaway:** initialize agents as behavioral personas covering all 9 clusters, not as 9 fixed agents — let coverage, not headcount, be the variable; penalize duplicate "dominant" personas (Shapers) without a coordinating/critiquing persona.

---

## 2. Optimal Team Size

**Findings:**
- Hackman & Vidmar (1970, *Sociometry*): dyads most satisfied; dissatisfaction rose ~linearly with size; participants rated groups of ~4–5 as "not too small, not too large" (the often-cited **4.6**). Performance effects of size were small for simple tasks. 🟢 (small samples, lab)
- Hackman (2002, *Leading Teams*): rule of thumb **≈6**; later formulations say **5–9**. 🟡 (expert synthesis)
- Amazon "two-pizza team" (Bezos rule, ~2002+): a team should be feedable by two pizzas → **~6–8 people**. 🔴 practitioner lore — but consistent with the research consensus band.
- Putnam & Myers (software, large corporation): **491 projects, 35,000–90,000 SLOC each**. Teams of 3–5 took **11.9 months**, 5–7 took **11.6 months**, 9–11 took **17.1 months**, 15–20 took **16.3 months** for similar-size work. A 9–11-person team took ~**2.5–3.5× the person-months** of a 3–5 team. 🟢 (large observational sample, software-specific)
- Wu, Evans & Wang (2019, *Nature*): **65M papers, patents, and software projects, 1954–2014**. Each additional member "dramatically declined" disruption — smaller teams generate disruptive ideas; larger teams consolidate existing knowledge. 🟢
- Dunbar (1992, *Journal of Human Evolution*): stable-social-relationship ceiling ~**148** (95% CI 100–230); layers: 5 / 15 / 50 / 150 / 500. ⚠️ Stockholm University 2021 critique says a hard cognitive limit "cannot be derived in this manner"; a 2021 PNAS model (West et al.) found networks of ~150 optimal for **information transport efficiency**. 🟡 contested — treat as heuristic, not law.
- **CIPD/CIPD-adjacent guidance:** keep membership ≤8; for virtual teams, 4–6. 🟡

**Agent-form takeaway:** working units of **4–7 agents**; scale by federating small teams (network of teams) rather than growing one big team. The Dunbar-150 layer suggests the ceiling for an agent "organization" that must maintain mutual state without formal hierarchy.

---

## 3. Collective Intelligence (Woolley et al.)

- Woolley, Chabris, Pentland, Hashmi & Malone (2010, *Science*, 330:686–688): two studies, **n=699**, groups of 2–5. A general **collective-intelligence factor ("c factor")** explains 30–40% of variance in group performance across tasks. It is **not** strongly correlated with average or max individual IQ, but **is** correlated with: (1) average **social sensitivity** (Reading-the-Mind-in-the-Eyes test), (2) **equal distribution of conversational turn-taking**, (3) proportion of females (via sensitivity). 🟢
- ⚠️ **Replication controversy:** Bates & Gupta (2017) found individual IQ accounts for ~**100% of latent group IQ** in their samples; Credé & Howardson (2017) re-analyzed 6 prior datasets and failed to find the c-factor pattern; a 2024 PLOS ONE study (n=85 participants, 29 groups) found **no significant correlation** of turn-taking (r=.19), social sensitivity (r=.27), or female proportion (r=−.17) with group-IQ composites. 🟢 (published failures to replicate — flag this as **contested, not settled**)
- Google **Project Aristotle** (Rozovsky et al., 2012–2014, published 2016): **~180 teams, 250 attributes**. Strongest predictor of effectiveness: **psychological safety** (Amy Edmondson's construct, 1999), then dependability, structure/clarity, meaning, impact. High-performing teams had equal speaking time; in weak teams 1–2 people dominated ~**80%** of discussion. Widely-cited numbers: +76% idea sharing, +40% revenue, +47% retention — but these circulate via secondary sources, not the primary internal report. 🟡 (company study, methodology partially disclosed)

**Agent-form takeaway:** even if the c-factor is contested, the two robust practical levers are (1) **turn-taking protocols** (no agent dominates context/tool calls) and (2) a **social-sensitivity analog** — an agent whose role is reading disagreement/emotion in shared state (a "Teamworker"). Edmondson's psychologically-safe hospital teams **reported more errors** (because they admitted them) yet performed better — direct analog for agent error-reporting incentives.

---

## 4. Cognitive Diversity & Specialization

- Hong & Page (2004, *PNAS*): **"diversity trumps ability"** — under 4 conditions (problem is hard, all solvers smart, calculus condition, reasonably sized teams from a large population), a random diverse group of problem solvers outperforms a group of the best individual performers. Mechanism: diverse heuristics escape shared local optima. 🟢 (math result, conditions matter)
- ⚠️ **Critique:** Thompson (2014, *Notices of the AMS*) showed the theorem's claim is vacuous/trivial as stated and the experiment contrived; the theorem does NOT show that cognitive diversity (in the ordinary sense) beats individual excellence without its narrow assumptions. Singer ("Diversity, Not Randomness, Trumps Ability") re-derives: random groups beat expert groups because of higher measured heuristic diversity (95.08% vs 87.19% non-overlap), not because randomness per se is good. 🟢 — **use the conditions, not the slogan.**
- Page (2007, *The Difference*; 2017, *The Diversity Bonus*): crowd error = average error − diversity (the **Diversity Prediction Theorem**, identity, not estimate). Real examples: Netflix Prize winners came from merging diverse teams (1st + 2nd + 5th); papers with co-authors from different universities get more citations; cross-ethnic co-authorship correlates with higher citation counts. 🟡
- **T-shaped people** (McKinsey/David Guest term, popularized by Tim Brown/IDEO): depth in one skill + breadth across others. No single large-scale causal study quantifies T-shaped payoff; it's supported by innovation research on boundary-spanning (e.g., Burt's structural holes — brokers who bridge groups produce better ideas). 🟡
- Stanford/Cowan et al.: research-group productivity — at **high heterogeneity (≥4 disciplines), adding members adds nothing** (interaction size × disciplines β = −.13, p<.01). Diversity of knowledge pays only with strong coordination. 🟢

**Agent-form takeaway:** maximize *heuristic* diversity (different tools/reasoning styles/prompts), keep all agents competent ("all solvers smart" is a theorem condition), and combine diverse specialists with a T-shaped coordinator agent to pay the heterogeneity coordination tax.

---

## 5. Coordination Costs & Social Loafing

- **Brooks's Law** (Brooks, 1975, *The Mythical Man-Month*): "Adding manpower to a late software project makes it later." Mechanisms: (1) **communication channels = n(n−1)/2** — 5 people → 10 channels, 10 → 45; (2) ramp-up/mentoring tax; (3) limited task divisibility. Brooks himself called it an "outrageous oversimplification." 🟡 (landmark practitioner theory; modern evidence mixed — e.g., some studies find late additions can help when work is partitionable)
- **Ringelmann effect** (Ringelmann, 1913): rope-pulling — individuals exerted **100% alone, 93% in pairs, 85% in trios, ~49% in groups of 8**. Two losses: coordination loss + motivation loss. 🟢 (classic, replicated)
- **Social loafing proper** (Latané, Williams & Harkins, 1979): clapping/shouting — people gave **82%** effort when they believed others were contributing, **74%** in groups of 5. Karau & Williams (1993) meta-analysis: loafing is **strongest when individual contributions are not identifiable** and when task/valence is low. 🟢
- **Price's Law** (de Solla Price): "50% of the work is done by √n of the people." E.g., 100 people → 10 do half the work. ⚠️ descriptive observation from scientific productivity (Lotka distributions), **not a controlled finding**; treat as folklore with a true heavy-tail kernel (productivity distributions are reliably power-law-ish in creative work). 🔴/🟡
- **Metcalfe's-law critique:** useful for channels, but agents have *cheaper* communication (shared context, structured messages) — the n² term is a design variable, not destiny. (Author's inference for the experiment section.)

**Agent-form takeaway:** loafing is driven by **non-identifiability of contributions** — the single most transferable design rule. Give every agent a logged, attributable workstream and visible performance surface. Coordination loss is the Ringelmann term you can engineer away (structured channels, broadcast summaries, sub-team partitions).

---

## 6. Hierarchy, Span of Control & Middle Management

- **Span of control:** Hamilton (1922, military) — leader can directly control **3–6**; Graicunas (1933) formulas — executive should supervise ≤**4–5**. Consensus band: **4–8** (complex work 5–7; standardized work 7–10+); managers-of-managers 4–6; CEO span ~6–7 (Bain survey: CEOs with 6–7 reports perform better; HBR survey modal ~7). Rajan & Wulf (2006): US firms delayered ~**25% of management layers 1986–1999** (1.6→1.2 positions between CEO and division heads) while CEO span rose from **4.5 to ~7** (later ~9.8). 🟢
- **Graicunas math:** 3 reports → 18 relationships; 5 → 100; 10 → **5,210** (direct + cross + group). Superlinear relationship load is the hard constraint on flattening. 🟢 (combinatorial fact)
- **The Peter Principle, tested:** Benson, Li & Shue (2018, *Quarterly Journal of Economics*; NBER wp): **53,035 salespeople, 214 US firms, 2005–2011**. Each higher sales rank → ~**15% higher** promotion probability, but each higher rank → **7.5% decline** in each subordinate's performance post-promotion. Sales and managerial performance **negatively correlated**. A random-promotion policy would outperform the current system; promoting on managerial traits could raise subordinate performance up to **30%**. 🟢 (landmark causal-ish evidence)
- **Manager quality matters:** Lazear, Shaw & Stanton (2015): best bosses raise subordinate output **>10%** vs worst bosses. 🟢
- **Middle-management cuts (evidence is thin/negative):** Uber's 2025-ish restructuring cut ~3,300 roles, ~20% of managers, ~half of micro-teams; span moved only **3.0→3.4** (~half a layer). Korn Ferry (June 2026): **41%** of firms removed layers in the past year. But: Gartner found **75%** of HR leaders say managers are overwhelmed; the "ownership threshold" critique — deleting the box moves judgment up to execs or down to unprepared ICs; coordination work doesn't disappear. Firstup (2025): **52–86%** of employees rely on their direct manager for updates/clarity/coaching. 🟡 (surveys + case commentary; no clean causal studies that cutting layers *raises* performance)
- **Manager vs IC ratios:** no validated universal ratio; industry pattern: engineering orgs ~1:7–10, with ~15–25% of engineering headcount in management at scale. Mark as 🔴 (benchmarks, not research).

**Agent-form takeaway:** **promote on coordination-relevant traits, never on raw task performance** — the Benson-Li-Shue result is the single most experiment-relevant finding for agent "promotion" (orchestrator selection). Keep spans 4–7; layers carry judgment, not just reporting — if you flatten, transfer the judgment explicitly or the orchestrator collapses under load (Graicunas math applies to attention budgets too).

---

## 7. Organizational Forms with Documented Outcomes

| Form | Key facts | Evidence |
|---|---|---|
| **Haier (RenDanHeYi)** | Zhang Ruimin; 2012: cut **12,000+ middle managers**, reorganized into **~4,000 microenterprises** (self-forming, ~10 people, own P&L, hiring authority, user contract); internal talent market + "catfish" competition; Nash-equilibrium framing. Outcomes: **23% annual gross profit growth** post-2012; **$57B** revenue (2024); new-product cycle time cut from **~6 months to ~2**; #1 appliance brand 12 yrs; acquired GE Appliances ($5.6B, 2016). | 🟡 (HBR/McKinsey case + company-reported financials; Hamel & Zanini 2018 HBR "The End of Bureaucracy") |
| **Buurtzorg (Netherlands)** | Founded 2006 (Jos de Blok); ~**900 self-managing nursing teams of ≤12**, ~50 admins + ~20 coaches, **2 directors, zero middle managers**; teams own scheduling, hiring, budgets. KPMG (2015, for Dutch Ministry): overhead **8% vs 25%** industry; care hours per client **108 vs 168/yr**; **~40% system cost savings**; E&Y 2009: used **40% of authorized hours vs 70%** industry; fewer emergency admissions, faster autonomy recovery; turnover <**half** industry; repeated "Best Employer" NL. | 🟡 (government-commissioned studies; strong but observational, founder-adjacent advocacy) |
| **Valve** | Flat, no formal managers; "rule of three" (projects need ≥3 people to proceed); cabal structure; employee handbook. Outcomes: very high revenue-per-employee, long-lived franchises — but **no controlled evidence**, and critiques (e.g., hidden hierarchies, firing difficulties, "high-school clique" dynamics per former employees). | 🔴 |
| **Morning Star** | Tomato processing, ~500–600 employees, **no managers, no titles**; CLOU (Colleague Letter of Understanding) peer contracts. Outcomes: world's largest tomato processor, high efficiency — documented via Hamel (2011, HBR) and academic cases. | 🟡 |
| **Toyota (TPS)** | Andon cord (any worker stops the line), kaizen, 5 Whys, jidoka; nemawashi consensus. Outcomes: Toyota's quality/productivity leadership 1980s–2000s; widely replicated (NUMMI). Note: TPS is **not flat** — it's layered hierarchy with radical information flow and stopped-line authority pushed down. | 🟡 (massive management literature; causal attribution contested) |
| **Military command (mission command / Auftragstaktik)** | Commander's intent + decentralized execution; doctrine since Moltke. Evidence: historical/comparative, McChrystal (2015 *Team of Teams* — flattened JSOC intelligence sharing: "shared consciousness"). | 🔴/🟡 (doctrinal, anecdotal) |
| **Holacracy** | Constitution-based circles, no managers; adopted by Zappos (2013), Medium, David Allen Co. Outcomes: **Zappos lost ~18% of staff** in the 2015 transition offer; Medium abandoned it (2016); no published evidence of performance gain; Zappos later moved on. | 🟡 (clear *failure* signal on adoption) |

**Common thread:** the successes (Haier, Buurtzorg, Toyota, Morning Star) all pair autonomy with **hard accountability surfaces** — P&L contracts, CLOUs, andon-quality metrics, patient-hour budgets. Flatness without an accountability substitute fails (holacracy at Zappos). 🟡 (cross-case inference)

**Agent-form takeaway:** test "microenterprise" swarms: small agent teams with a **contracted outcome + budget** (token/time budget), free self-organization inside, market-like selection across teams. And give every agent an **andon cord**: unilateral halt-and-escalate authority on detected errors.

---

## 8. Incentive & Selection Design

- **Tournament theory** (Lazear & Rosen, 1981, *JPE*): rank-order tournaments can be **optimal labor contracts** when individual output is hard to measure but relative rank is observable; prize spread (W1−W2) sets effort. Explains CEO pay (~**300:1** vs median worker); Shen & Zhang evidence: larger CEO-pay gaps correlate with **more innovation**. 🟢 (theory + correlational support)
- **Stack ranking evidence:** Scullen, Bergey & Aiman-Smith (2005, *Personnel Psychology*): simulation of 100 firms × 100 employees × 30 years, firing bottom **10%** yearly and replacing with best applicants → workforce quality **does** improve in simulation. BUT: gains **decay after a couple of years** (fewer C-players left); real-world: GE (Welch's 20-70-10 vitality curve) dropped it; Microsoft abandoned stack ranking (2013); Ford/Microsoft faced **discrimination lawsuits**; only **~2 of 330** SHRM-surveyed firms said forced ranking "always leads to terminations"; critics document cutthroat behavior, suppressed collaboration/help-seeking. 🟢 (simulation) + 🟡 (field critiques)
- **Pluchino, Rapisarda & Garofalo (2010)** (agent-based model; **Ig Nobel 2010**): under Peter-principle assumptions, **random promotion — or promote-randomly-from-best-and-worst shortlist — beats merit promotion**. 🟡 (model, not field data)
- **Identifying overachievers (what high-performers' orgs actually do):** research consensus (e.g., Chamorro-Premuzic; "Hiring for potential"): separate **performance** (current-role output) from **potential** (learning agility, drive, emotional intelligence); use structured assessments + peer calibration; guard against the Benson-Li-Shue trap by scoring **managerial traits separately** from IC output. 🟡

**Agent-form takeaway:** tournaments are the natural selection operator for agent populations (evaluate agents *relative* within a task pool, keep top-k, mutate/replace bottom) — but stack-ranking pathologies are directly predictable: agents will **stop sharing information** if ranked against teammates. Solution from the literature: rank teams, not individuals; or rank individuals only on **team-contingent** metrics (e.g., my score = f(my contribution × team outcome)).

---

## 9. "Too Many Cooks" — Quantified Diminishing Returns

1. **Ringelmann (1913):** per-capita effort falls 100→93→85→49% as group grows 1→2→3→8. 🟢
2. **Putnam & Myers (software):** 3–5-person teams finished similar-size projects in **11.9 mo**; 9–11 in **17.1 mo** (~44% slower in calendar time, ~3× in person-months). 🟢
3. **Wu/Evans/Wang (2019, *Nature*, 65M artifacts):** disruption **declines monotonically with each added member**; small teams disrupt, big teams develop. 🟢
4. **Cowan et al. (Stanford):** research groups — adding PIs helps homogeneous groups but adds **nothing** for groups spanning ≥4 disciplines / ≥7 institutions. 🟢
5. **Edmondson hospital teams (1999):** higher *reported* error rates predicted **better** outcomes — the mechanism: psychological safety converts hidden errors into learnable ones. 🟢
6. **LEGO experiment (UCLA, cited in practitioner literature):** 2-person team built the structure in **36 min**, 4-person in **56 min**. 🔴 (thin citation — verify before publishing)
7. **Graicunas:** 5 reports = 100 relationships; 10 = 5,210 — coordination load grows ~**exponentially**, not linearly. 🟢 (math)

**Synthesis rule of thumb:** per-capita marginal product turns negative somewhere around **n = 7–9** for tightly-coupled knowledge work; for disruptive/creative work the decline starts at **n = 3+**. Coordination losses dominate past ~8; motivation losses (loafing) compound them.

---

## Candidate Composition Formulas (testable hypotheses)

For multi-agent experiments. N = number of agents; roles use Belbin clusters as behavioral personas.

1. **"The 6-person balanced cell"**: N=6 — 1 Coordinator, 1 Plant, 1 Monitor Evaluator, 1 Implementer, 1 Completer Finisher, 1 Resource Investigator/Teamworker hybrid. Hypothesis: maximizes task-completion quality on novel, open-ended tasks (measured by blind judge score) vs. a 6-agent homogeneous (all-Shaper) team. *Based on: Belbin balance claim, Hackman n≈6, Prichard & Stanton 1999.*
2. **"T-shaped core + specialist satellites"**: N=7 — 3 generalist-coordinator agents (~40% coordination, 60% execution) + 4 deep specialists (1 each: domain knowledge, verification, external research, synthesis). Hypothesis: outperforms 7 all-generalists on complex multi-step tasks requiring factual accuracy. *Based on: Haier microenterprise size (~10), Page diversity conditions, T-shaped literature.*
3. **"Turn-taking protocol vs. free-for-all"**: N=5 identical agents, two conditions — (a) structured turn-taking with a dedicated "Teamworker" monitor enforcing equal speaking turns and social-sensitivity checks (disagreement surfacing), vs. (b) no protocol. Hypothesis: (a) wins on tasks where errors are costly, because error *reporting* rises (Edmondson mechanism). *Based on: Woolley et al. 2010, Project Aristotle.*
4. **"Market of microenterprises"**: 4 teams of 5 (N=20 total), each with a contracted outcome + token budget (P&L analog), competing; best team's approach is propagated. Hypothesis: beats a single 20-agent hierarchy on innovation metrics (novelty of solution) at equal total compute. *Based on: Haier RenDanHeYi, Wu/Evans/Wang small-team disruption finding.*
5. **"Promote-on-traits orchestrator"**: two-level agent org, N=8 — orchestrator selected by coordination traits (delegation quality, summarization accuracy, conflict resolution in prior episodes) vs. orchestrator = highest-scoring individual task agent. Hypothesis: trait-selected orchestrator yields ≥10% higher team output (cf. Lazear-Shaw-Stanton's >10% boss effect; Benson-Li-Shue negative correlation between IC skill and managerial skill). *Based on: Benson, Li & Shue 2018.*

**Design invariants to hold across all experiments** (best-evidenced levers):
- Attributable workstreams (anti-loafing; Karau & Williams 1993).
- Error-reporting rewarded, not punished (Edmondson 1999).
- Team-level, not individual, ranking (stack-ranking pathology avoidance).
- N ≤ 7 per cell; federate, don't grow (Ringelmann, Brooks, Putnam & Myers).

---

## References (quick index)

- Belbin, R.M. (1981). *Management Teams: Why They Succeed or Fail.*
- Prichard, J.S. & Stanton, N. (1999). Testing Belbin's team role theory. *J. Management Development*, 18(8).
- Hackman, J.R. & Vidmar, N. (1970). Effects of size and task type on group performance. *Sociometry*.
- Hackman, J.R. (2002). *Leading Teams.*
- Brooks, F.P. (1975). *The Mythical Man-Month.*
- Woolley, A.W. et al. (2010). Evidence for a collective intelligence factor. *Science*, 330, 686–688. DOI: 10.1126/science.1193147
- Edmondson, A. (1999). Psychological safety and learning behavior in work teams. *Admin. Sci. Quarterly*, 44(2).
- Hong, L. & Page, S. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. *PNAS*, 101(46).
- Page, S. (2007). *The Difference*; (2017). *The Diversity Bonus.*
- Thompson, A. (2014). Does diversity trump ability? *Notices of the AMS*.
- Ringelmann, M. (1913). rope-pulling experiments (reported in Kravitz & Martin, 1986).
- Latané, B., Williams, K. & Harkins, S. (1979). Many hands make light the work. *J. Personality and Social Psychology*.
- Karau, S.J. & Williams, K.D. (1993). Social loafing meta-analysis. *Psychological Bulletin*, 114(4).
- Benson, A., Li, D. & Shue, K. (2018). Promotions and the Peter Principle. *Quarterly J. Economics*.
- Lazear, E.P. & Rosen, S. (1981). Rank-order tournaments as optimum labor contracts. *J. Political Economy*.
- Scullen, S.E., Bergey, P.K. & Aiman-Smith, L. (2005). Forced distribution rating systems. *Personnel Psychology*, 58.
- Lazear, E.P., Shaw, K.L. & Stanton, C.T. (2015). The value of bosses. *J. Labor Economics*.
- Rajan, R. & Wulf, J. (2006). The flattening firm. *Review of Economics and Statistics*.
- Wu, L., Evans, J. & Wang, D. (2019). Large teams develop and small teams disrupt. *Nature*.
- Dunbar, R.I.M. (1992). Neocortex size as a constraint on group size. *J. Human Evolution*.
- Hamel, G. & Zanini, M. (2018). The end of bureaucracy. *Harvard Business Review*.
- Buurtzorg KPMG study (2015, for Dutch Ministry of Health); Commonwealth Fund case (Gray & Sarnak).
- McChrystal, S. (2015). *Team of Teams.*
