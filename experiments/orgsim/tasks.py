"""Task environments.

T1 -- Discovery (rugged landscape search; scientific-discovery analog).
    Synthetic rugged function: sum of Gaussians + noise, many local optima.
    Agents propose candidates per role policy; Builders test (evaluate);
    Analysts kill dominated/duplicated candidates; Specialists hill-climb
    within a subdomain; Framers jump; Heralds import external candidates;
    Healers reintroduce diverse discarded candidates and share negative
    results; Coordinator allocates the evaluation budget.

T2 -- Production / revenue (pipeline analog).
    Builders produce units; Specialists multiply quality on their subtask;
    Analysts catch defects; Herald outreach sets the demand multiplier;
    Coordinator overhead is subtracted. Revenue = units*quality*demand
    - coordination cost - defect cost.

No LLM calls; everything is numpy, seeded.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence
import numpy as np

from .agents import Agent
from .org import (loafing, comm_edges, comm_shares, gate_prob,
                  coordinator_effectiveness, COORD_COST_C,
                  STAR_DISTORTION)

# Within-role proposal-noise correlation. Hong & Page (2004, PNAS):# homogeneous-heuristic teams have CORRELATED errors (all stuck in the same
# local optimum); diverse heuristics give independent errors so selection
# across proposals works. rho magnitude is ASSUMED; the mechanism direction
# (correlated vs independent) is the literature claim.
NOISE_RHO = 0.8

# Healer: low effective conformity -- re-surfaces discarded alternatives
# (SYNTHESIS.md sec 3).
HEALER_CONFORMITY_FACTOR = 0.7  # ASSUMED magnitude

# Revenue scale: one quality-adjusted unit sold at demand=1 is worth this.
# ASSUMED -- sets the absolute revenue level so typical teams are profitable;
# relative comparisons (the experimental contrasts) do not depend on it, but
# the E2 peak LOCATION is scale-sensitive, so E2 carries sensitivity analyses.
UNIT_VALUE = 3.0
SURFACED_ERROR_COST = 0.05    # cheap fix once reported. ASSUMED.
UNSURFACED_ERROR_COST = 0.30  # hidden errors cost 6x surfaced ones. ASSUMED.
CAUGHT_DEFECT_COST = 0.15     # rework. ASSUMED.
ESCAPED_DEFECT_COST = 1.5     # escaped defects destroy value. ASSUMED.


class Landscape:
    """Rugged synthetic function: sum of Gaussians + eval noise."""

    def __init__(self, seed: int, n_gauss: int = 12, dim: int = 2):
        rng = np.random.default_rng(seed)
        self.dim = dim
        self.mus = rng.uniform(0.0, 1.0, size=(n_gauss, dim))
        self.amps = rng.uniform(0.4, 1.0, size=n_gauss)
        self.amps[rng.integers(n_gauss)] = rng.uniform(1.3, 1.6)  # clear global opt
        self.sigmas = rng.uniform(0.03, 0.12, size=n_gauss)
        self._opt: Optional[float] = None

    def value(self, x: np.ndarray) -> np.ndarray:
        x = np.atleast_2d(x)
        d2 = ((x[:, None, :] - self.mus[None, :, :]) ** 2).sum(-1)
        return (self.amps[None, :] * np.exp(-d2 / (2 * self.sigmas[None, :] ** 2))).sum(1)

    def grid_optimum(self, res: int = 120) -> float:
        if self._opt is None:
            g = np.linspace(0, 1, res)
            mesh = np.stack(np.meshgrid(*([g] * self.dim)), -1).reshape(-1, self.dim)
            self._opt = float(self.value(mesh).max())
        return self._opt


# ---------------------------------------------------------------------------
# T1 -- Discovery
# ---------------------------------------------------------------------------

def _propose(role: str, a: Agent, best_x: np.ndarray, quad_best: np.ndarray,
             shared_noise: np.ndarray, rng: np.random.Generator,
             domain_half: Optional[int], conformity_eff: float) -> np.ndarray:
    """One candidate point from an agent's role policy + correlated noise."""
    ind = rng.normal(size=2)
    corr = NOISE_RHO * shared_noise + np.sqrt(1 - NOISE_RHO ** 2) * ind
    if role == "Framer":
        # High-variance novel directions (Plant analog).
        jump = rng.uniform(0, 1, size=2)
        x = conformity_eff * best_x + (1 - conformity_eff) * jump
        x = x + 0.02 * corr
    elif role == "Builder":
        x = best_x + 0.04 * (1 + a.creativity) * corr  # local refinement
    elif role == "Analyst":
        x = best_x + 0.05 * corr
    elif role == "Specialist":
        x = quad_best + 0.02 * corr  # deep narrow hill-climb in subdomain
    elif role == "Healer":
        x = best_x + 0.08 * corr
    elif role == "Herald":
        # External link: imports outside information, far from consensus.
        x = rng.uniform(0, 1, size=2) + 0.01 * corr
    elif role == "Coordinator":
        x = best_x + 0.03 * corr
    else:  # Generic (no-roles control)
        x = best_x + 0.06 * corr
    # Drift (E8): implicit contracts let agents slide off-role toward generic.
    if a.drift > 0:
        generic = best_x + 0.09 * rng.normal(size=2)
        x = (1 - a.drift) * x + a.drift * generic
    x = np.clip(x, 0.0, 1.0)
    if domain_half is not None:  # E4 decomposable task: search one half
        x[0] = np.clip(x[0], 0.0 if domain_half == 0 else 0.5,
                       0.5 if domain_half == 0 else 1.0)
    return x


def run_t1(team: Sequence[Agent], seed: int, rounds: int = 40, budget: int = 12,
           protocol: str = "turn-taking", contracts: bool = True,
           domain_half: Optional[int] = None,
           eval_noise: float = 0.003, loaf_strength: float = 1.0) -> Dict:
    """Run the discovery task. Returns metric dict."""
    rng = np.random.default_rng(seed)
    land = Landscape(seed ^ 0x9E37)
    opt = land.grid_optimum()

    best_x = np.array([0.5, 0.5])
    best_v = float(land.value(best_x)[0])
    quad_best = np.tile(best_x, (4, 1)).copy()
    evaluated: List[np.ndarray] = [best_x.copy()]
    eval_vals: List[float] = [best_v]
    discards: List[np.ndarray] = []     # dominated candidates (Healer pool)
    neg_regions: List[np.ndarray] = []  # Healer-shared negative results
    novelties: List[float] = []         # novelty of every evaluated candidate
    top_nov: List[float] = []           # (novelty, value) tracked below
    top_records: List[tuple] = []
    has_coord = any(a.active and a.role == "Coordinator" for a in team)
    healer_present = any(a.active and a.role == "Healer" for a in team)

    for r in range(rounds):
        active = [a for a in team if a.active]
        n = len(active)
        if n == 0:
            break
        loaf = loafing(n, strength=loaf_strength, attributable=True)
        shares = comm_shares(active, protocol)
        conf_eff = np.mean([a.conformity for a in active])
        if healer_present:
            conf_eff *= HEALER_CONFORMITY_FACTOR
        shared = {role: rng.normal(size=2) for role in {a.role for a in active}}

        if not contracts:
            # Implicit contracts: role adherence decays (Morning Star CLOU
            # contrast -- written role contracts vs drift; drift rate ASSUMED).
            for a in active:
                a.drift = min(0.6, a.drift + 0.04)

        proposals: List[tuple] = []  # (agent, x)
        for a in active:
            effort = a.diligence * loaf
            k = 1 + int(2 * effort)
            for _ in range(k):
                if a.role == "Healer" and r % 3 == 0 and discards:
                    # Reintroduce the discarded candidate farthest from best
                    # (diversity preservation).
                    d = np.array([np.linalg.norm(d - best_x) for d in discards])
                    x = discards[int(np.argmax(d))].copy()
                else:
                    x = _propose(a.role, a, best_x, quad_best[a.quadrant],
                                 shared[a.role], rng, domain_half, conf_eff)
                # Healer-shared negative results: avoid known-bad regions.
                for _try in range(3):
                    if any(np.linalg.norm(x - z) < 0.06 for z in neg_regions):
                        x = np.clip(best_x + 0.10 * rng.normal(size=2), 0, 1)
                    else:
                        break
                # Communication gate: low-share agents' ideas may never surface
                # (Project Aristotle: 1-2 dominate ~80% under free-for-all).
                if rng.random() < gate_prob(a, shares, n):
                    proposals.append((a, x))

        # Analyst kill step: remove near-duplicate candidates before spending
        # eval budget (gated by the analyst's own floor time).
        analysts = [a for a in active if a.role == "Analyst"]
        kept = []
        for a, x in proposals:
            dup = any(np.linalg.norm(x - e) < 0.005 for e in evaluated)
            if dup and analysts and rng.random() < np.mean(
                    [gate_prob(an, shares, n) for an in analysts]):
                a.contribution += 0.0  # budget saved, no direct credit
                for an in analysts:
                    an.contribution += 0.005
                continue
            kept.append((a, x))

        # Budget allocation: Coordinator prioritizes by recent contribution;
        # otherwise round-robin shuffle.
        if has_coord:
            kept.sort(key=lambda t: t[0].contribution + rng.random() * 0.01,
                      reverse=True)
        else:
            rng.shuffle(kept)
        kept = kept[:budget]

        prev_best = best_v
        for a, x in kept:
            nov = min(np.linalg.norm(x - e) for e in evaluated)
            novelties.append(nov)
            v = float(land.value(x)[0] + rng.normal(0, eval_noise))
            evaluated.append(x.copy())
            eval_vals.append(v)
            top_records.append((nov, v))
            if v > best_v:
                credit = (v - prev_best) * (1.0 + nov)
                a.contribution += credit
                best_v, best_x = v, x.copy()
                qb = quad_best[a.quadrant]
                if land.value(x[None, :])[0] > land.value(qb[None, :])[0]:
                    quad_best[a.quadrant] = x.copy()
            elif v < best_v - 0.25:
                discards.append(x.copy())
                if a.role == "Healer" and len(neg_regions) < 12:
                    # Healers share negative results (Edmondson 1999 analog:
                    # reported errors become learnable).
                    neg_regions.append(x.copy())
                    a.contribution += 0.01

    top_records.sort(key=lambda t: t[1], reverse=True)
    top20 = top_records[:20]
    novelty_top20 = float(np.mean([t[0] for t in top20])) if top20 else 0.0
    novelty_best = max(0.0, float(np.linalg.norm(best_x - 0.5)) - 0.2)
    shares = [a.contribution for a in team]
    return {
        "best_value": best_v,
        "best_frac": best_v / opt,
        "novelty_best": novelty_best,
        "novelty_top20": novelty_top20,
        "evals_used": len(evaluated),
        "contrib_shares": shares,
        "n": len([a for a in team if a.active]),
    }


# ---------------------------------------------------------------------------
# T2 -- Production / revenue
# ---------------------------------------------------------------------------

def run_t2(team: Sequence[Agent], seed: int, rounds: int = 30,
           protocol: str = "turn-taking",
           coord_cost_c: float = COORD_COST_C,
           prune_at: Optional[int] = None, prune_k: int = 0,
           loaf_strength: float = 1.0) -> Dict:
    """Run the production task. Returns metric dict."""
    rng = np.random.default_rng(seed)
    coord = next((a for a in team if a.active and a.role == "Coordinator"), None)
    topology = "star" if coord is not None else "all-to-all"
    # Star topology: decision latency + manager mis-aggregation distortion
    # (SYNTHESIS.md sec 4 item 2). Magnitudes ASSUMED.
    distortion = 1.0
    if coord is not None:
        distortion = 1.0 - STAR_DISTORTION * (1.0 - coord.coord_skill)

    revenue = 0.0
    compute = 0.0
    units_total = 0.0
    defects_escaped = 0
    errors_surfaced = 0
    errors_total = 0

    for r in range(rounds):
        active = [a for a in team if a.active]
        n = len(active)
        if n == 0:
            break
        if prune_at is not None and r == prune_at:
            from .org import prune_bottom_k
            prune_bottom_k(team, prune_k)
            active = [a for a in team if a.active]
            n = len(active)
        loaf = loafing(n, strength=loaf_strength, attributable=True)
        shares = comm_shares(active, protocol)

        # Coordinator boss effect: +/-10% band on subordinate output
        # (Lazear, Shaw & Stanton 2015).
        eff = coordinator_effectiveness(coord, topology) if coord else 1.0

        # --- production ---
        prod_value = 0.0
        for a in active:
            effort = a.diligence * loaf
            if a.role == "Builder":
                u = a.task_skill * effort
            elif a.role == "Specialist":
                u = 0.6 * a.task_skill * effort  # narrow subtask, less volume
            elif a.role == "Framer":
                u = 0.3 * a.task_skill * effort
            else:
                u = 0.0
            prod_value += u
            a.contribution += u  # base attributable output
        units = prod_value * eff
        units_total += units

        # --- quality: Specialists multiply quality on their subtask ---
        n_spec = sum(1 for a in active if a.role == "Specialist")
        quality = min(0.97, 0.85 + 0.04 * n_spec) * distortion  # base ASSUMED

        # --- defects: Analysts catch them; uncaught destroy revenue ---
        defects = rng.binomial(max(0, int(round(units * 10))), (1 - quality) / 10)
        analysts = [a for a in active if a.role == "Analyst"]
        if analysts:
            gate = np.mean([gate_prob(an, shares, n) for an in analysts])
            p_catch = (1 - 0.5 ** len(analysts)) * gate  # diminishing, gated
            caught = rng.binomial(defects, p_catch)
            for an in analysts:
                an.contribution += caught * 1.5 / len(analysts)  # loss avoided
        else:
            caught = 0
        escaped = defects - caught
        defects_escaped += escaped

        # --- errors: witnessed at random; surfacing needs floor time ---
        # Edmondson (1999): psychologically-safe teams REPORT more errors and
        # perform better. Protocol (+Healer) = safety analog.
        healers = [a for a in active if a.role == "Healer"]
        n_err = rng.poisson(0.4 * n)
        errors_total += n_err
        for _ in range(n_err):
            witness = active[rng.integers(n)]
            p_surface = 0.30 * gate_prob(witness, shares, n)
            if protocol == "turn-taking" and healers:
                p_surface = min(0.95, p_surface + 0.45)  # Healer-enforced
            if rng.random() < p_surface:
                errors_surfaced += 1
                revenue -= SURFACED_ERROR_COST  # cheap fix once surfaced
                witness.contribution += 0.5 / max(1, n)  # reporting rewarded
                for h in healers:
                    h.contribution += 0.5 / max(1, len(healers) * n)
            else:
                revenue -= UNSURFACED_ERROR_COST

        # --- demand: Herald outreach sets the multiplier (gated by floor) ---
        heralds = [a for a in active if a.role == "Herald"]
        demand = 1.0
        if heralds:
            gate = np.mean([gate_prob(h, shares, n) for h in heralds])
            lift = 0.25 * np.mean([h.diligence * loaf for h in heralds]) * gate
            demand = 1.0 + lift  # lift scale ASSUMED
            base = units * quality
            for h in heralds:
                h.contribution += (demand - 1.0) * base / len(heralds)

        # Coordinator contribution: the boss-effect lift, made attributable.
        if coord:
            coord.contribution += (eff - 1.0) * prod_value

        revenue += units * quality * demand * UNIT_VALUE
        revenue -= caught * CAUGHT_DEFECT_COST
        revenue -= escaped * ESCAPED_DEFECT_COST
        revenue -= coordination_cost(n, topology, coord_cost_c)
        compute += n * 0.5            # 1 agent-round = 0.5 compute units. ASSUMED.

    shares = [a.contribution for a in team]
    return {
        "net_revenue": revenue,
        "revenue_per_compute": revenue / max(compute, 1e-9),
        "units": units_total,
        "defects_escaped": defects_escaped,
        "errors_surfaced": errors_surfaced,
        "errors_total": errors_total,
        "compute": compute,
        "contrib_shares": shares,
        "n_final": len([a for a in team if a.active]),
    }


def coordination_cost(n: int, topology: str, c: float) -> float:
    return c * comm_edges(n, topology)
