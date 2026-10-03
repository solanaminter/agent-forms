"""Agent model for orgsim.

An Agent is a role + four traits + two skills. Roles are behavioral *priors*,
not straitjackets: traits are drawn around role means with noise
(SYNTHESIS.md section 3). Trait knobs move outcomes (Big5-Scaler agent work;
Toronto 2026 complementarity finding -- see research/org-science-brief.md).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import numpy as np

ROLES = ("Framer", "Builder", "Analyst", "Specialist", "Healer", "Herald", "Coordinator")

# Role -> mean trait values.
#   diligence  (effort level; Specialists/Builders high, Framers lower)
#   creativity (proposal variance; Framers high, Analysts low)
#   sociability(communication propensity; Heralds/Coordinators high)
#   conformity (herding tendency; low conformity preserves dissent)
# Basis: SYNTHESIS.md section 3 (village -> agent role map; Belbin clusters).
ROLE_TRAIT_MEANS: Dict[str, Dict[str, float]] = {
    "Framer":      {"diligence": 0.50, "creativity": 0.90, "sociability": 0.50, "conformity": 0.30},
    "Builder":     {"diligence": 0.85, "creativity": 0.45, "sociability": 0.50, "conformity": 0.60},
    "Analyst":     {"diligence": 0.75, "creativity": 0.30, "sociability": 0.50, "conformity": 0.60},
    "Specialist":  {"diligence": 0.85, "creativity": 0.40, "sociability": 0.35, "conformity": 0.50},
    "Healer":      {"diligence": 0.70, "creativity": 0.50, "sociability": 0.85, "conformity": 0.40},
    "Herald":      {"diligence": 0.70, "creativity": 0.70, "sociability": 0.90, "conformity": 0.60},
    "Coordinator": {"diligence": 0.80, "creativity": 0.50, "sociability": 0.90, "conformity": 0.50},
}
# Roles are priors, not straitjackets (SYNTHESIS.md section 3). Noise sd assumed.
TRAIT_NOISE = 0.10

# Mean task skill per role (production/discovery competence).
ROLE_TASK_SKILL = {
    "Framer": 0.60, "Builder": 0.85, "Analyst": 0.75, "Specialist": 0.90,
    "Healer": 0.60, "Herald": 0.65, "Coordinator": 0.60, "Generic": 0.65,
}
# Coordination trait per role. Sampled INDEPENDENTLY of task skill:
# Benson, Li & Shue (2018, QJE) -- sales skill and managerial skill are
# negatively correlated; promoting top sellers hurt subordinate performance
# ~7.5% per sales rank. So high task_skill must NOT imply high coord_skill.
ROLE_COORD_SKILL = {
    "Framer": 0.40, "Builder": 0.35, "Analyst": 0.55, "Specialist": 0.35,
    "Healer": 0.80, "Herald": 0.75, "Coordinator": 0.85, "Generic": 0.50,
}
SKILL_NOISE = 0.12  # assumed


@dataclass
class Agent:
    id: int
    role: str
    diligence: float
    creativity: float
    sociability: float
    conformity: float
    task_skill: float
    coord_skill: float
    contribution: float = 0.0   # accumulated attributable contribution (E7 pruning)
    drift: float = 0.0          # role-adherence loss under implicit contracts (E8)
    active: bool = True
    quadrant: int = 0           # Specialist's assigned subdomain in T1


def make_agent(role: str, rng: np.random.Generator, agent_id: int = 0,
               trait_mode: str = "role") -> Agent:
    """Build one agent.

    trait_mode: "role" (role means + noise), "uniform" (E9 control: every agent
    gets population-mean traits, roles fixed), "generic" (E1 no-roles control).
    """
    if trait_mode == "uniform":
        # E9: kill trait variance, keep role policies.
        means = {t: float(np.mean([m[t] for m in ROLE_TRAIT_MEANS.values()]))
                 for t in ("diligence", "creativity", "sociability", "conformity")}
    elif trait_mode == "generic":
        means = {"diligence": 0.60, "creativity": 0.60,
                 "sociability": 0.60, "conformity": 0.60}
    else:
        # Unknown role strings (e.g. "Generic") fall back to neutral traits.
        means = ROLE_TRAIT_MEANS.get(role, {"diligence": 0.60, "creativity": 0.60,
                                            "sociability": 0.60, "conformity": 0.60})
    tr = {t: float(np.clip(rng.normal(means[t], TRAIT_NOISE), 0.05, 0.99))
          for t in means}
    task_skill = float(np.clip(
        rng.normal(ROLE_TASK_SKILL.get(role, 0.65), SKILL_NOISE), 0.05, 0.99))
    # Independent draw: managerial trait uncorrelated with task skill
    # (Benson, Li & Shue 2018).
    coord_skill = float(np.clip(
        rng.normal(ROLE_COORD_SKILL.get(role, 0.50), SKILL_NOISE), 0.05, 0.99))
    return Agent(id=agent_id, role=role, task_skill=task_skill,
                 coord_skill=coord_skill, **tr)
