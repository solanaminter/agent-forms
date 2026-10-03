# Agent Forms — Experiment Results (v1)

**Date:** 2026-10-02. **Method:** `experiments/run_experiments.py`, seeded RNG,
20 seeds per condition, no network/API calls. Total runtime 153.6 s.
Figures in `experiments/figures/` (error bars = std across seeds); tidy CSVs in
`experiments/results/`.

**Evidence grades:** 🟢 robust (clear separation, survives sensitivity checks) /
🟡 suggestive (directional, sensitive to assumed parameters or weak separation) /
🔴 assumed (built into model mechanics). Per the anti-tautology rule, results
that contradict a hypothesis are reported as findings, not buried.

---

## E1 — Role-mix sweep (n=6): balanced vs all-Builder vs all-Framer vs random vs no-roles

| condition   | T1 best_frac (discovery) | T2 revenue/compute (production) |
|-------------|--------------------------|---------------------------------|
| balanced    | **0.960 ± 0.083**        | 0.711 ± 0.095                   |
| random-mix  | 0.965 ± 0.068            | 0.556 ± 0.422                   |
| all-framer  | 0.870 ± 0.113            | −0.084 ± 0.042                  |
| no-roles    | 0.818 ± 0.207            | −0.435 ± 0.020                  |
| all-builder | 0.751 ± 0.222            | **2.249 ± 0.208**               |

- **T1 hypothesis** (balanced wins on discovery): **HELD** 🟢 — balanced and
  random-mix tie at the top and clearly beat homogeneous/no-role teams.
  all-Builder collapses (0.751): correlated heuristics get stuck in one local
  optimum (Hong & Page mechanism working as modeled).
- **T2 hypothesis** (builder-heavy wins on production): **HELD** 🟢 —
  all-Builder wins by ~3×. The no-roles and all-Framer teams go *negative*
  (defects escape, no demand lift).
- **Finding:** there is no golden mix — the winner is **task-contingent**, as
  the Bedwell review predicts. Note random-mix ≈ balanced on T1: *coverage of
  distinct heuristics* may matter more than exact 1/6 proportions.

## E2 — Size sweep (n=2..14, balanced proportions, T2 revenue per compute)

Peak at **n=2** (1.65), declining thereafter: n=4: 1.10, n=6: 0.67, n=8: 0.66,
n=10: 0.53, n=14: 0.18. Small secondary bump at n=8 (role-cycle composition
effect, not robust).

- **Hypothesis** (peaks at 5–7, degrades past ~9): **CONTRADICTED on location —
  this is a finding, not a bug** 🟢. The peak stays at n=2 under *all four*
  sensitivity variants (loafing ×0.5/×1.5, coordination cost ×0.5/×2), so the
  rejection is robust, not a parameter accident. The "degrades past ~9" half
  holds in every variant.
- **Interpretation:** per-compute efficiency is dominated from n=2 by Ringelmann
  loafing + Graicunas n² coordination cost; the multiplicative value of
  overhead roles (quality, defect-catch, demand) never compensates *per unit
  compute*. The literature's 5–7 guidance is about *mission effectiveness*
  (total throughput, disruption), not per-compute efficiency — the v1 formula
  should scope the n*=5–7 claim accordingly.

## E3 — Coordinator ratio (overhead : producers = 1:4, 1:7, 1:12; T2)

| ratio | revenue/compute |
|-------|-----------------|
| 1:4   | 1.715 ± 0.134   |
| 1:7   | 1.808 ± 0.095   |
| 1:12  | **1.980 ± 0.155** |

- **Hypothesis** (optimum ~1:5–1:7; past 1:10 cost exceeds benefit):
  **CONTRADICTED** 🟡 — leaner wins monotonically in this model; analyst
  defect-catch and coordinator boss-effect don't cover their compute/loafing/
  coordination cost at these scales. Downgraded to 🟡 because the 1:7 vs 1:12
  gap is ~1 std and depends on assumed defect-cost and demand-lift scales.
  The EM-playbook 1:5–1:7 band is not reproduced here.

## E4 — Split don't grow (2×5 federation vs 1×10, decomposable T1, equal compute)

| condition      | novelty (top-20) | best_frac |
|----------------|------------------|-----------|
| federation 2×5 | **0.015 ± 0.003** | 0.931 ± 0.183 |
| single 1×10    | 0.011 ± 0.002    | 0.967 ± 0.066 |

- **Hypothesis** (federation wins on novelty at equal compute): **HELD** 🟢 —
  +36% novelty, separated by >1 std (Wu/Evans/Wang: small teams disrupt).
- **Nuance:** the single team finds a slightly better *best* value but with
  much higher variance across seeds for the federation — splitting buys
  exploration breadth at the cost of best-case reliability.

## E5 — Turn-taking protocol vs free-for-all (n=6, T2)

| condition    | errors surfaced | defects escaped | net revenue |
|--------------|-----------------|-----------------|-------------|
| turn-taking  | **54.5 ± 6.3**  | **1.6 ± 1.0**   | 60.9 ± 10.7 |
| free-for-all | 13.3 ± 3.5      | 2.9 ± 2.1       | 43.0 ± 9.6  |

- **Hypothesis** (protocol surfaces more errors, fewer escaped defects):
  **HELD, strongly** 🟢 — 4.1× more errors surfaced (Edmondson mechanism),
  ~45% fewer escaped defects, higher net revenue. The single most robust
  process-level result in the battery.

## E6 — Orchestrator selection (n=8: promote-by-coordination-trait vs top-task-scorer)

| condition      | net revenue      |
|----------------|------------------|
| trait-selected | **212.8 ± 32.9** |
| top-scorer     | 165.0 ± 17.5     |

- **Hypothesis** (trait-selected ≥10% better team output): **HELD** 🟡 —
  **+29.0%**. Direction is robust; graded 🟡 because the magnitude flows from
  the literature-parameterized mechanics themselves (Benson-Li-Shue negative
  correlation + Lazear-Shaw-Stanton ±10% boss band + the lost production of the
  promoted star). The honest claim: the *mechanism* replicates the field
  finding's direction with room to spare.

## E7 — Rank-and-prune (mid-run deactivation of bottom-2, DyLAN analog)

| condition         | revenue/compute | top-√n contrib. share |
|-------------------|-----------------|-----------------------|
| prune bottom-2    | **1.265 ± 0.185** | 0.64 ± 0.02         |
| no prune          | 1.014 ± 0.137   | 0.61 ± 0.04           |

- **Hypothesis** (pruning idlers improves efficiency): **HELD** 🟢 — +24.8%
  revenue per compute.
- **80/20 measurement (not assumed):** the top √8 ≈ 3 contributors (37.5% of
  agents) produce ~61–64% of attributable contribution — a heavy tail,
  somewhat steeper than Price's-law folklore (√n doing 50%). Pruning does not
  destroy the tail; it trims it.

## E8 — Written contracts vs implicit drift (T1, n=6 and n=10)

| condition      | best_frac      |
|----------------|----------------|
| n=6 contracts  | 0.937 ± 0.129  |
| n=6 drift      | 0.890 ± 0.144  |
| n=10 contracts | 0.961 ± 0.106  |
| n=10 drift     | 0.908 ± 0.152  |

- **Hypothesis** (contracts reduce drift/duplication; gap widens with n):
  **direction held, "widens with n" NOT supported** 🟡 — the gap is 0.047 at
  n=6 and 0.053 at n=10, i.e. essentially flat, and within noise. Contracts
  help a little; the Morning Star CLOU effect does not scale up in this model.

## E9 — Personality mix (mixed vs uniform traits, roles fixed, T1)

| condition      | best_frac      |
|----------------|---------------|
| mixed traits   | **0.992 ± 0.019** |
| uniform traits | 0.943 ± 0.110 |

- **Hypothesis** (mixed wins on T1 — complementarity, Hong-Page conditions):
  **HELD** 🟢. Bonus finding: uniform-trait teams have **5.8× the variance**
  (0.110 vs 0.019) — trait homogeneity doesn't just lower the mean, it makes
  outcomes brittle.

---

## Cross-cutting notes

- **What survived:** task-contingency of role mix (E1), turn-taking (E5),
  trait-based orchestrator selection (E6), rank-and-prune (E7), trait mix (E9),
  federation novelty (E4).
- **What didn't:** the 5–7 efficiency peak (E2 — robustly rejected, peak at
  n=2 in all sensitivity variants), the 1:5–1:7 overhead optimum (E3 —
  monotonic lean-is-better), contracts gap widening with n (E8 — flat).
- **Wind-tunnel caveats:** agent behaviors are parametric policies, not LLM
  agents; magnitudes marked `ASSUMED` in code are explicit guesses; T1/T2 are
  stylized analogs of discovery and production. The value here is falsifiable
  hypotheses at ~zero cost, not proof.
