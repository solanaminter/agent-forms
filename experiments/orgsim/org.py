"""Team assembly, social loafing, coordination cost, communication protocols,
orchestrator selection, and rank-and-prune. Every literature-derived
parameter carries a citation comment.
"""
from __future__ import annotations

from typing import Dict, List, Sequence
import numpy as np

from .agents import Agent, ROLES, make_agent

# ---------------------------------------------------------------------------
# Social loafing -- Ringelmann (1913), rope-pulling, via org-science-brief sec 5:
# per-capita effort 100% alone, 93% in pairs, 85% in trios, ~49% in groups of 8.
# ---------------------------------------------------------------------------
LOAF_POINTS = ((1, 1.00), (2, 0.93), (3, 0.85), (8, 0.49))


def loafing(n: int, strength: float = 1.0, attributable: bool = True) -> float:
    """Per-capita effort multiplier for a group of size n.

    strength: sensitivity knob (E2: x0.5 / x1.5 on the penalty).
    attributable: when every agent has a logged, attributable workstream the
        loafing penalty is halved (Karau & Williams 1993 meta-analysis:
        identifiability strongly reduces loafing; org-science-brief sec 5).
    """
    xs = [p[0] for p in LOAF_POINTS]
    ys = [p[1] for p in LOAF_POINTS]
    if n <= 8:
        L = float(np.interp(n, xs, ys))
    else:
        # Linear extrapolation past the observed range; floor is ASSUMED
        # (Ringelmann measured up to 8; we sweep to 14 in E2).
        slope = (0.49 - 0.85) / (8 - 3)
        L = max(0.30, 0.49 + slope * (n - 8))
    penalty = 1.0 - L
    if attributable:
        penalty *= 0.5  # Karau & Williams (1993)
    penalty *= strength
    return max(0.05, 1.0 - penalty)


# ---------------------------------------------------------------------------
# Coordination cost -- per-round cost = c * E, E = active communication edges.
# All-to-all: E = n(n-1)/2. Hierarchy (star via Coordinator): E = n-1, but adds
# decision latency and distortion (SYNTHESIS.md sec 4, item 2; Graicunas 1933).
# ---------------------------------------------------------------------------
COORD_COST_C = 0.05  # revenue units per edge per round. ASSUMED scale;
# E2 sensitivity re-runs at x0.5 / x2, so conclusions must not depend on it.
STAR_LATENCY_PENALTY = 0.98   # decision latency under star topology. ASSUMED.
STAR_DISTORTION = 0.05        # manager mis-aggregation shrinks with coord_skill. ASSUMED.


def comm_edges(n: int, topology: str) -> int:
    if topology == "star":
        return n - 1
    return n * (n - 1) // 2  # all-to-all (Graicunas 1933 relationship load)


def coordination_cost(n: int, topology: str, c: float = COORD_COST_C) -> float:
    return c * comm_edges(n, topology)


# ---------------------------------------------------------------------------
# Communication protocol -- turn-taking vs free-for-all.
# Free-for-all: high-sociability agents consume the communication budget;
# in weak teams 1-2 people dominate ~80% of discussion (Project Aristotle,
# Rozovsky et al.; org-science-brief sec 4). Protocol: equal turns
# (Edmondson 1999: psychologically-safe teams surface errors).
# ---------------------------------------------------------------------------
def comm_shares(team: Sequence[Agent], protocol: str) -> Dict[int, float]:
    active = [a for a in team if a.active]
    n = len(active)
    if protocol == "turn-taking":
        return {a.id: 1.0 / n for a in active}
    # free-for-all: top-2 by sociability split 80%, rest share 20%.
    ranked = sorted(active, key=lambda a: a.sociability, reverse=True)
    shares: Dict[int, float] = {}
    top = ranked[:2]
    rest = ranked[2:]
    w_top = [a.sociability for a in top]
    tot = sum(w_top) or 1.0
    for a, w in zip(top, w_top):
        shares[a.id] = 0.80 * w / tot
    for a in rest:
        shares[a.id] = 0.20 / max(1, len(rest))
    return shares


def gate_prob(agent: Agent, shares: Dict[int, float], n: int) -> float:
    """Probability an agent's information is actually considered this round."""
    return min(1.0, shares.get(agent.id, 0.0) * n)


# ---------------------------------------------------------------------------
# Team assembly
# ---------------------------------------------------------------------------
def assemble(roles: Sequence[str], rng: np.random.Generator,
             trait_mode: str = "role") -> List[Agent]:
    team = [make_agent(r, rng, agent_id=i, trait_mode=trait_mode)
            for i, r in enumerate(roles)]
    # Specialists get round-robin subdomain quadrants (T1 hill-climbing).
    q = 0
    for a in team:
        if a.role == "Specialist":
            a.quadrant = q % 4
            q += 1
    return team


BALANCED_6 = ["Framer", "Builder", "Analyst", "Specialist", "Healer", "Herald"]
# The "village cell": n=6, full role coverage, no duplicate dominants
# (SYNTHESIS.md sec 2).


def balanced_roles(n: int) -> List[str]:
    """Proportional fill of the village cell for the E2 size sweep."""
    cyc = BALANCED_6
    return [cyc[i % len(cyc)] for i in range(n)]


# ---------------------------------------------------------------------------
# Orchestrator selection (E6).
# promote-by-coordination-trait vs promote-top-task-scorer.
# Benson, Li & Shue (2018): promoting top sellers *hurt* subordinate
# performance ~7.5% per sales rank. Lazear, Shaw & Stanton (2015): best
# bosses raise subordinate output >10%.
# ---------------------------------------------------------------------------
def select_coordinator(team: List[Agent], mode: str) -> Agent:
    candidates = [a for a in team if a.active]
    if mode == "trait":
        # Choose on coordination trait; task skill of the pick is whatever it
        # is (independently sampled -- the Benson-Li-Shue world).
        return max(candidates, key=lambda a: a.coord_skill)
    if mode == "top-scorer":
        # Peter-Principle policy: the best individual producer is pulled off
        # task work into coordination (keeps their own low coord_skill).
        return max(candidates, key=lambda a: a.task_skill)
    raise ValueError(mode)


def coordinator_effectiveness(coord: Agent, topology: str) -> float:
    """Multiplier on subordinate output from the coordinator (boss effect).

    Lazear, Shaw & Stanton (2015): best bosses raise subordinate output >10%
    vs worst bosses. We map coord_skill in [0,1] to a +/-10% band: 0.9 -> 1.08,
    0.3 -> 0.94. Band edges ASSUMED; the >10% spread is the literature value.
    """
    eff = 1.0 + 0.2 * (coord.coord_skill - 0.5)
    if topology == "star":
        eff *= STAR_LATENCY_PENALTY  # decision latency. ASSUMED.
    return eff


# ---------------------------------------------------------------------------
# Rank-and-prune (E7) -- DyLAN analog (Liu et al. 2023, ICLR 2024): rank agents
# by measured contribution and deactivate low contributors at inference time.
# ---------------------------------------------------------------------------
def prune_bottom_k(team: List[Agent], k: int) -> List[Agent]:
    active = sorted([a for a in team if a.active],
                    key=lambda a: a.contribution)
    pruned = []
    for a in active[:k]:
        a.active = False
        pruned.append(a)
    return pruned
