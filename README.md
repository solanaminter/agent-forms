# Agent Forms

**What composition of agent roles and personalities maximizes organizational
performance — and can we write it down as a formula?**

Enterprises behave like super-organisms: a company or a country functions as one
giant intelligence composed of specialized sub-agents (people). This project
asks whether organizational wisdom — how villages, firms, and labs actually
divide labor — transfers to teams of AI agents, and tests the answer
empirically in a cheap, seeded, fully local simulation: a **wind tunnel** for
org-design hypotheses, not proof.

Measured two ways:
- **Discovery** (scientific-discovery analog): finding novel, high-quality
  solutions in a rugged space.
- **Revenue** (production analog): net value produced per unit of compute.

With two failure modes to avoid explicitly: **too many cooks** (coordination
overhead swamping productive work) and **the 80/20 idleness trap** (most agents
contributing little while a few carry the load).

## The village → agent role map

| Village archetype      | Agent role   | Behavioral policy                                    |
|------------------------|--------------|------------------------------------------------------|
| Problem-sizers         | Framer       | Scopes the problem, proposes high-variance directions |
| Blue-collar            | Builder      | Core work: converts proposals into tested outputs    |
| White-collar (analyst) | Analyst      | Evaluates, kills bad candidates, measures            |
| Tradescraft experts    | Specialist   | Deep narrow skill; hill-climbs within a subdomain    |
| Healers                | Healer       | Repairs cohesion, surfaces errors, preserves diversity |
| Propagandists          | Herald       | External links: imports outside info, sets demand    |
| Village chief          | Coordinator  | Allocates budget/attention, owns the mission         |

A balanced "village cell" = n=6, full role coverage, no duplicate dominants.
Each agent also gets four traits (diligence, creativity, sociability,
conformity) drawn around role means with noise — roles are behavioral priors,
not straitjackets.

## The v1 formula (hypotheses under test — see `experiments/RESULTS.md` for what survived)

- **Cell size:** n* = 5–7. Federate; never grow one cell past ~9.
- **Discovery cell:** ~1/6 each Framer, Builder, Analyst, Specialist, Healer, Herald.
- **Production cell:** ~50% Builders/Specialists, 1 Coordinator, 1 Analyst, 1 Healer.
- **Span:** 1 coordinator per 5–7 producers; player-coach below 5.
- **Invariants:** attributable workstreams, error-reporting rewarded, written
  role contracts, rank-and-prune cadence, no duplicate dominants without a
  Healer/Analyst counterweight.

## How to run

```bash
pip install -r requirements.txt   # numpy, matplotlib only
cd experiments
python3 run_experiments.py
```

No network, no API calls, no cost. Seeded RNG everywhere (≥20 seeds per
condition). Runtime is minutes. Results land in `experiments/results/*.csv`;
one PNG figure per experiment (error bars = std across seeds) in
`experiments/figures/`; the quantitative write-up in `experiments/RESULTS.md`.

## Repository layout

```
research/                 # literature briefs + SYNTHESIS.md (the design doc)
experiments/
  orgsim/                 # simulation package
    agents.py             # Agent: role, traits, skills
    tasks.py              # T1 discovery (rugged landscape), T2 production (pipeline)
    org.py                # team assembly, loafing, coordination cost, protocols,
                          # orchestrator selection, rank-and-prune
    metrics.py            # contribution shares, concentration (80/20), summaries
  run_experiments.py      # E1..E9 + E2 sensitivity analyses
  results/                # tidy CSVs, one row per (condition, seed)
  figures/                # one PNG per experiment, error bars across seeds
  RESULTS.md              # quantitative outcomes + evidence grades
```

## Literature grounding

Every simulation parameter is set from the research briefs and cites its source
in a code comment — e.g. `# Ringelmann 1913 via org-science-brief §5`. Key ones:

- **Social loafing:** per-capita effort 100/93/85/49% for n=1/2/3/8 (Ringelmann
  1913); attributable workstreams halve the penalty (Karau & Williams 1993).
- **Coordination cost:** per-round cost = c × edges; all-to-all edges =
  n(n−1)/2 (Graicunas 1933); star-via-coordinator = n−1 plus latency/distortion.
- **Diversity:** homogeneous heuristics → correlated errors, shared local optima
  (Hong & Page 2004, under its stated conditions).
- **Turn-taking:** free-for-all lets 1–2 high-sociability agents dominate ~80%
  of the floor (Project Aristotle); protocol + Healer surfaces errors
  (Edmondson 1999).
- **Orchestrator selection:** promote on coordination traits, never raw task
  skill — top-seller promotion hurt subordinate performance ~7.5% per rank
  (Benson, Li & Shue 2018); best bosses add >10% (Lazear, Shaw & Stanton 2015).
- **Small teams disrupt:** disruption declines with each added member (Wu,
  Evans & Wang 2019, *Nature*, 65M artifacts).
- **Rank-and-prune:** DyLAN (Liu et al. 2023) deactivates low-contribution
  agents at inference time; contribution concentration is *measured*
  (Price's-law check), never assumed.
- **Written contracts:** Morning Star's CLOU peer contracts vs. drift.

Parameters labeled `ASSUMED` in code are explicit guesses (magnitudes the
literature doesn't pin down); E2's sensitivity analyses (loafing ×0.5/×1.5,
coordination cost ×0.5/×2) exist so conclusions can't depend on them quietly.

## Evidence grades

- 🟢 **robust** — holds across seeds and the sensitivity analyses.
- 🟡 **suggestive** — consistent direction, but sensitive to assumed parameters.
- 🔴 **assumed** — built into the model mechanics; not evidence.

## Honest limitations

- This is a wind tunnel, not proof: it makes org-design hypotheses *falsifiable
  in silico* — the cheapest place to be wrong — before anyone tests them with
  expensive LLM agents.
- Agent behaviors are parametric policies, not real LLM agents; several
  magnitudes (marked `ASSUMED`) are guesses the literature doesn't pin down.
- Anti-tautology rule enforced: parameters come from literature values, never
  tuned to produce a desired winner. Where results contradict a hypothesis,
  that is reported as a finding (see `experiments/RESULTS.md`).
