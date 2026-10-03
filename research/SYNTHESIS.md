# Agent Forms — Synthesis: From Organizational Wisdom to Testable Agent Compositions

**Date:** 2026-10-02
**Status:** Design doc. Implements the research in `research/org-science-brief.md`, `research/agent-systems-brief.md`, `research/practitioner-brief.md`.

---

## 1. The question

Enterprises behave like super-organisms — a company or a country functions as one giant intelligence composed of specialized sub-agents (people). The question this project answers empirically:

> **What composition of agent roles and personalities maximizes organizational performance — and can we write it down as a formula?**

Measured two ways, as the user specified:
- **Discovery** (scientific-discovery analog): finding novel, high-quality solutions in a rugged space.
- **Revenue** (production analog): net value produced per unit cost.

With two failure modes to avoid explicitly:
- **Too many cooks**: coordination overhead swamping productive work.
- **The 80/20 idleness trap**: most agents contributing little while a few carry the load (Price's law / social loafing).

## 2. The village → agent role map

The user's village archetypes map cleanly onto Belbin clusters + practitioner roles. Six archetypes form one "village cell":

| Village archetype | Agent role | Behavioral policy | Belbin analog |
|---|---|---|---|
| Problem-sizers | **Framer** | Scopes the problem, proposes high-variance novel directions | Plant |
| Blue-collar | **Builder** | Does the core work, converts proposals into tested outputs | Implementer |
| White-collar (analyst) | **Analyst** | Evaluates, kills bad candidates, measures | Monitor Evaluator |
| Tradescraft experts | **Specialist** | Deep narrow skill; hill-climbs within a subdomain | Specialist |
| Healers | **Healer** | Repairs cohesion, surfaces errors/negative results, preserves diversity | Teamworker |
| Propagandists | **Herald** | External links: imports outside information, broadcasts narrative | Resource Investigator |
| (village chief) | **Coordinator** | Allocates budget/attention, owns the mission | Coordinator |

A balanced cell of 6 = one of each (Coordinator included, Healer covers the Teamworker slot). This is the "village cell" hypothesis: **n=6, full role coverage, no duplicate dominants.**

## 3. Personality initialization

Each agent is initialized with four traits (means set per role, plus noise — roles are *behavioral priors*, not straitjackets):

- **diligence** (effort level; Specialists/Builders high, Framers lower)
- **creativity** (proposal variance; Framers high, Analysts low)
- **sociability** (communication propensity; Heralds/Coordinators high)
- **conformity** (herding tendency; low conformity preserves dissent — the Healer enforces low effective conformity by re-surfacing discarded alternatives)

Trait-mix is itself an experimental variable (E9): mixed-trait teams vs uniform-trait teams, roles held fixed. Literature basis: Big5-Scaler trait knobs move outcomes; Toronto 2026 complementarity finding; Hong–Page heuristic-diversity conditions.

## 4. Micro-foundations (parameters from literature, not tuned to taste)

All simulation parameters are set from the research briefs, with citations in code comments:

1. **Social loafing** — per-capita effort multiplier L(n) from Ringelmann (1913): L(1)=1.00, L(2)=0.93, L(3)=0.85, L(8)=0.49, interpolated. **Attributable workstreams halve the loafing penalty** (Karau & Williams 1993: identifiability reduces loafing).
2. **Coordination cost** — per-round cost = c × E, E = active communication edges. Default all-to-all: E = n(n−1)/2 (Graicunas). Hierarchy (star via Coordinator): E = n−1, but adds decision latency (+rounds) and distortion (manager mis-aggregation probability).
3. **Diversity bonus** — homogeneous-heuristic teams have *correlated* errors (all stuck in the same local optimum); diverse heuristics give independent errors so selection across proposals works (Hong & Page 2004, under its stated conditions; Singer's re-derivation).
4. **Turn-taking** — free-for-all: high-sociability agents consume the communication budget; others' information never surfaces (Project Aristotle: 1–2 dominate ~80%). Protocol: equal turns + Healer-enforced error surfacing → reported errors rise, escaped defects fall (Edmondson 1999).
5. **Orchestrator quality** — orchestrator effectiveness = coordination trait, uncorrelated with task skill (Benson, Li & Shue 2018: promoting top sellers *hurt* subordinate performance 7.5% per sales rank).
6. **Disruption vs development** — small cells explore; large groups consolidate (Wu, Evans & Wang 2019). Implemented: per-agent novelty bonus decays as cell size grows.

## 5. The two task environments

**T1 — Discovery (rugged landscape search).** A synthetic rugged function (sum of Gaussians + noise; many local optima). Each round, agents propose candidate points per their role policy; Builders "test" them (evaluate); Analysts kill dominated ones; Specialists hill-climb locally; Framers jump; Heralds import external candidates; Healers reintroduce diverse discarded candidates and share negative results; Coordinator allocates the evaluation budget. Metrics: best value found, novelty (distance from initialization region), evaluations used.

**T2 — Production / revenue (pipeline).** Each round: Builders produce units (output = skill × effort); Specialists multiply quality on their subtask; Analysts catch defects (uncaught defects destroy revenue); Herald outreach sets the demand multiplier; Coordinator overhead is subtracted. Revenue = Σ(units × quality × demand) − coordination cost − defect cost. Metrics: net revenue, revenue per unit compute.

## 6. Experiments (v1)

| ID | Name | Manipulation | Hypothesis (from literature) | Falsifier |
|---|---|---|---|---|
| E1 | Role-mix sweep | n=6: balanced village vs all-Builder vs all-Framer vs random mix vs no-roles | Balanced wins on T1 (discovery); Builder/Specialist-heavy wins on T2 (production) — **task-contingent**, no golden mix (Bedwell review) | Balanced loses everywhere |
| E2 | Size sweep | n=2..14, proportions held balanced | Throughput per unit cost peaks at 5–7, degrades past ~9 (Putnam & Myers; Ringelmann) | Monotonic improvement with n |
| E3 | Coordinator ratio | Overhead (Coord+Analyst) : producers at 1:4, 1:7, 1:12 | Optimum ~1:5–1:7; past 1:10 cost exceeds benefit (EM playbook; Grove leverage) | More overhead always helps or never helps |
| E4 | Split don't grow | 2×5-cell federation vs 1×10 team, decomposable T1 | Federation wins on novelty at equal compute (Wu/Evans/Wang; Buurtzorg split rule) | 10-team wins on novelty |
| E5 | Turn-taking protocol | Protocol vs free-for-all, n=6 | Protocol surfaces more errors, fewer escaped defects (Edmondson; Aristotle) | No difference in defect escape |
| E6 | Orchestrator selection | Promote-by-coordination-trait vs promote-top-task-scorer | Trait-selected ≥10% better team output (Benson-Li-Shue; Lazear-Shaw-Stanton boss effect) | Top-scorer wins |
| E7 | Rank-and-prune | Mid-run deactivation of bottom-2 contributors (DyLAN analog) vs no prune; instrument contribution concentration | Pruning idlers improves efficiency; 80/20 concentration is measurable, not assumed | Pruning hurts (lost diversity) |
| E8 | Written contracts | Explicit role contracts (adherence enforced) vs implicit (drift allowed) | Contracts reduce duplication/drift, gap widens with n (Morning Star CLOU) | Drift helps (adaptability) |
| E9 | Personality mix | Mixed traits vs uniform traits, roles fixed | Mixed wins on T1 (complementarity; Hong-Page conditions) | Uniform wins |

**Sensitivity analyses (required):** E2 re-run with loafing strength ×0.5/×1.5 and coordination cost c ×0.5/×2 — conclusions must be robust to parameter choice or be downgraded.

## 7. Anti-tautology rules (honesty engineering)

1. Parameters come from literature values, never tuned to produce a desired winner.
2. Task-contingency is a first-class result: where homogeneous teams win, report it.
3. Every figure shows variance across seeds (error bars), not single runs.
4. The blog's claims carry evidence grades (🟢 simulated-robust / 🟡 suggestive / 🔴 assumed).
5. Framing: this is a **wind tunnel**, not proof. It makes org-design hypotheses *falsifiable in silico* — the cheapest place to be wrong — before anyone tests them with expensive LLM agents.

## 8. The formula (v1 hypotheses — experiments will refine)

- **Cell size:** n* = 5–7. Federate; never grow one cell past ~9.
- **Discovery cell:** ~1/6 each Framer, Builder, Analyst, Specialist, Healer, Herald (+Coordinator as 7th or dual-hatted).
- **Production cell:** ~50% Builders/Specialists, 1 Coordinator, 1 Analyst, 1 Healer.
- **Span:** 1 coordinator per 5–7 producers; player-coach below 5.
- **Specialist density:** ~1 per 5–10 generalists (test 1:5/1:10/1:15).
- **Invariants:** attributable workstreams, error-reporting rewarded, written role contracts, rank-and-prune cadence, no duplicate dominants without a Healer/Analyst counterweight.

## 9. Out of scope for v1 (future work)

LLM-backed validation of the winning forms; market-of-microenterprises tournament (4×5 competing cells); casualty/resilience injection (dropout tests, redundancy ≥2); principal-misalignment ablation ("Worse Together"); scaling past n=150 (Dunbar layers for agent orgs).
