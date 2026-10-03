"""orgsim — a "wind tunnel" for organizational hypotheses about agent teams.

Implements the design in research/SYNTHESIS.md: literature-derived parameters
(cited in code comments), two task environments (T1 discovery, T2 production),
and team-assembly / coordination / selection mechanics. No network, no API
calls, seeded RNG throughout.
"""

from .agents import ROLES, Agent, make_agent
from .org import (
    loafing,
    comm_edges,
    comm_shares,
    assemble,
    balanced_roles,
    BALANCED_6,
    select_coordinator,
    prune_bottom_k,
    COORD_COST_C,
)
from .tasks import Landscape, run_t1, run_t2
from .metrics import topk_share, gini, summarize

__all__ = [
    "ROLES", "Agent", "make_agent",
    "loafing", "comm_edges", "comm_shares", "assemble",
    "balanced_roles", "BALANCED_6",
    "select_coordinator", "prune_bottom_k", "COORD_COST_C",
    "Landscape", "run_t1", "run_t2",
    "topk_share", "gini", "summarize",
]
