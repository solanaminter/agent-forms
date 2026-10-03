#!/usr/bin/env python3
"""Run experiments E1..E9 (+ E2 sensitivity) from research/SYNTHESIS.md section 6.

Seeded RNG everywhere; >=20 seeds per condition. Writes tidy CSVs to
experiments/results/ and one PNG figure per experiment (error bars = std
across seeds) to experiments/figures/.

No network, no API calls. Runtime target: minutes, not hours.
"""
import csv
import math
import os
import time

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from orgsim import (
    assemble, balanced_roles, BALANCED_6, ROLES,
    run_t1, run_t2, select_coordinator, topk_share, gini, COORD_COST_C,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIG = os.path.join(HERE, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

SEEDS = list(range(20))  # >=20 seeds per condition (SYNTHESIS.md sec 6)

plt.rcParams.update({"figure.dpi": 110, "font.size": 10,
                     "axes.titlesize": 11, "axes.labelsize": 10})


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def team_rng(exp_tag: int, cond_idx: int, seed: int) -> np.random.Generator:
    return np.random.default_rng([exp_tag, cond_idx, seed])


def run_condition(exp_tag, cond_idx, roles_fn, task, task_kw, trait_mode="role"):
    rows = []
    for s in SEEDS:
        rng = team_rng(exp_tag, cond_idx, s)
        roles = roles_fn(rng)
        team = assemble(roles, rng, trait_mode=trait_mode)
        out = task(team, seed=1000 * exp_tag + 100 * cond_idx + s, **task_kw)
        out = dict(out)
        out["seed"] = s
        # contribution concentration (measured, not assumed -- Price's law)
        shares = out.pop("contrib_shares", None)
        if shares is not None:
            k = math.ceil(math.sqrt(max(1, len(shares))))
            out["conc_top_sqrt"] = topk_share(shares, k)
            out["contrib_gini"] = gini(shares)
        rows.append(out)
    return rows


def save_csv(exp_id, cond_labels, all_rows):
    path = os.path.join(RES, f"{exp_id}.csv")
    keys = ["experiment", "condition", "seed"]
    metric_keys = [k for k in all_rows[0][0].keys() if k != "seed"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys + metric_keys)
        w.writeheader()
        for label, rows in zip(cond_labels, all_rows):
            for r in rows:
                w.writerow({"experiment": exp_id, "condition": label,
                            "seed": r["seed"],
                            **{k: r[k] for k in metric_keys}})
    return path


def summarize_conds(cond_labels, all_rows, metrics):
    """{condition: {metric: (mean, std)}}"""
    summ = {}
    for label, rows in zip(cond_labels, all_rows):
        summ[label] = {}
        for m in metrics:
            vals = [r[m] for r in rows]
            summ[label][m] = (float(np.mean(vals)),
                              float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0)
    return summ


def bar_fig(path, title, ylabel, labels, means, stds, xlabel=""):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = np.arange(len(labels))
    ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, wrap=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def line_fig(path, title, xlabel, ylabel, series):
    """series: list of (label, xs, means, stds)."""
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for label, xs, means, stds in series:
        ax.errorbar(xs, means, yerr=stds, marker="o", capsize=3, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, wrap=True)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


# --------------------------------------------------------------------------
# E1 -- Role-mix sweep (n=6): balanced village vs all-Builder vs all-Framer
#       vs random mix vs no-roles. T1 + T2.
# Hypothesis: balanced wins on T1 (discovery); Builder-heavy wins on T2
# (production) -- task-contingent, no golden mix (Bedwell review).
# --------------------------------------------------------------------------
def exp_e1():
    conds = [
        ("balanced", lambda rng: list(BALANCED_6), "role"),
        ("all-builder", lambda rng: ["Builder"] * 6, "role"),
        ("all-framer", lambda rng: ["Framer"] * 6, "role"),
        ("random-mix", lambda rng: [ROLES[i] for i in rng.integers(0, len(ROLES), 6)], "role"),
        ("no-roles", lambda rng: ["Generic"] * 6, "generic"),
    ]
    labels = [c[0] for c in conds]
    t1_rows, t2_rows = [], []
    for i, (_, fn, tm) in enumerate(conds):
        t1_rows.append(run_condition(1, i, fn, run_t1, {"rounds": 40, "budget": 12}, tm))
        t2_rows.append(run_condition(1, i + 10, fn, run_t2, {"rounds": 30}, tm))
    save_csv("e1_rolemix_t1", labels, t1_rows)
    save_csv("e1_rolemix_t2", labels, t2_rows)
    s1 = summarize_conds(labels, t1_rows, ["best_frac", "novelty_top20"])
    s2 = summarize_conds(labels, t2_rows, ["revenue_per_compute", "net_revenue"])

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    x = np.arange(len(labels))
    for ax, summ, metric, yl in [
            (axes[0], s1, "best_frac", "best value / grid optimum (T1)"),
            (axes[1], s2, "revenue_per_compute", "net revenue / compute (T2)")]:
        means = [summ[l][metric][0] for l in labels]
        stds = [summ[l][metric][1] for l in labels]
        ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15, ha="right")
        ax.set_ylabel(yl)
    axes[0].set_title("E1a: discovery quality by role mix\nH: balanced village wins on T1", wrap=True)
    axes[1].set_title("E1b: production efficiency by role mix\nH: builder-heavy wins on T2 (task-contingent)", wrap=True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e1_rolemix.png"))
    plt.close(fig)
    return ("e1", s1, s2)


# --------------------------------------------------------------------------
# E2 -- Size sweep n=2..14, balanced proportions, T2 throughput per unit cost.
# Hypothesis: peaks at 5-7, degrades past ~9 (Putnam & Myers; Ringelmann).
# Sensitivity: loafing strength x0.5/x1.5, coordination cost c x0.5/x2.
# --------------------------------------------------------------------------
def exp_e2():
    sizes = list(range(2, 15))
    variants = [
        ("baseline", {"loaf_strength": 1.0, "coord_cost_c": COORD_COST_C}),
        ("loafing x0.5", {"loaf_strength": 0.5, "coord_cost_c": COORD_COST_C}),
        ("loafing x1.5", {"loaf_strength": 1.5, "coord_cost_c": COORD_COST_C}),
        ("coord-cost x0.5", {"loaf_strength": 1.0, "coord_cost_c": COORD_COST_C * 0.5}),
        ("coord-cost x2", {"loaf_strength": 1.0, "coord_cost_c": COORD_COST_C * 2.0}),
    ]
    series, all_csv_rows, csv_labels = [], [], []
    for v_idx, (vlabel, kw) in enumerate(variants):
        means, stds = [], []
        for n in sizes:
            rows = run_condition(2, v_idx * 100 + n,
                                 lambda rng, n=n: balanced_roles(n),
                                 run_t2, {"rounds": 30, **kw})
            vals = [r["revenue_per_compute"] for r in rows]
            means.append(float(np.mean(vals)))
            stds.append(float(np.std(vals, ddof=1)))
            if v_idx == 0:
                all_csv_rows.append(rows)
                csv_labels.append(f"n={n}")
        series.append((vlabel, sizes, means, stds))
    save_csv("e2_size", csv_labels, all_csv_rows)
    # sensitivity csv (long form)
    sens_rows, sens_labels = [], []
    for v_idx, (vlabel, kw) in enumerate(variants):
        for n in sizes:
            rows = run_condition(2, 500 + v_idx * 100 + n,
                                 lambda rng, n=n: balanced_roles(n),
                                 run_t2, {"rounds": 30, **kw})
            sens_rows.append(rows)
            sens_labels.append(f"{vlabel}|n={n}")
    save_csv("e2_sensitivity", sens_labels, sens_rows)

    line_fig(os.path.join(FIG, "e2_size.png"),
             "E2: throughput per unit cost vs team size\nH: peaks at n=5-7, degrades past ~9 (Putnam & Myers; Ringelmann 1913)",
             "team size n", "revenue per unit compute (T2)",
             [series[0]])
    line_fig(os.path.join(FIG, "e2_sensitivity.png"),
             "E2 sensitivity: size sweep under loafing x0.5/x1.5 and coord-cost x0.5/x2\n"
             "Conclusions must be robust to parameter choice or be downgraded",
             "team size n", "revenue per unit compute (T2)", series)
    base = {f"n={n}": (m, s) for n, m, s in
            zip(sizes, series[0][2], series[0][3])}
    return ("e2", base, series)


# --------------------------------------------------------------------------
# E3 -- Coordinator ratio: overhead (Coord+Analyst) : producers at
#       1:4, 1:7, 1:12. Hypothesis: optimum ~1:5-1:7; past 1:10 cost exceeds
#       benefit (EM playbook; Grove leverage).
# --------------------------------------------------------------------------
def exp_e3():
    producers = ["Builder"] * 10 + ["Specialist"] * 2
    conds = [
        ("1:4", producers + ["Coordinator", "Analyst", "Analyst"]),
        ("1:7", producers + ["Coordinator", "Analyst"]),
        ("1:12", producers + ["Coordinator"]),
    ]
    labels = [c[0] for c in conds]
    all_rows = [run_condition(3, i, lambda rng, roles=c[1]: list(roles),
                             run_t2, {"rounds": 30})
                for i, c in enumerate(conds)]
    save_csv("e3_ratio", labels, all_rows)
    s = summarize_conds(labels, all_rows, ["revenue_per_compute", "net_revenue",
                                           "defects_escaped"])
    bar_fig(os.path.join(FIG, "e3_ratio.png"),
            "E3: production efficiency vs overhead ratio (Coord+Analyst : producers)\n"
            "H: optimum ~1:5-1:7; past 1:10 cost exceeds benefit",
            "net revenue / compute (T2)",
            labels,
            [s[l]["revenue_per_compute"][0] for l in labels],
            [s[l]["revenue_per_compute"][1] for l in labels],
            xlabel="overhead : producer ratio")
    return ("e3", s)


# --------------------------------------------------------------------------
# E4 -- Split don't grow: 2x5-cell federation vs 1x10 team on decomposable T1.
# Hypothesis: federation wins on novelty at equal compute
# (Wu, Evans & Wang 2019; Buurtzorg split rule).
# --------------------------------------------------------------------------
def exp_e4():
    fed_rows, single_rows = [], []
    for s in SEEDS:
        # federation: two 5-cells, one per domain half, half budget each
        cell_roles = ["Framer", "Builder", "Analyst", "Specialist", "Healer"]
        halves = []
        for h in (0, 1):
            rng = team_rng(4, h, s)
            team = assemble(cell_roles, rng)
            halves.append(run_t1(team, seed=4000 + h * 100 + s, rounds=40,
                                 budget=6, domain_half=h))
        fed_rows.append({
            "seed": s,
            "best_frac": max(h["best_frac"] for h in halves),
            "novelty_top20": float(np.mean([h["novelty_top20"] for h in halves])),
            "evals_used": sum(h["evals_used"] for h in halves),
        })
        rng = team_rng(4, 2, s)
        team = assemble(balanced_roles(10), rng)
        out = run_t1(team, seed=4200 + s, rounds=40, budget=12)
        out["seed"] = s
        single_rows.append({k: out[k] for k in
                            ("seed", "best_frac", "novelty_top20", "evals_used")})
    labels = ["federation 2x5", "single 1x10"]
    save_csv("e4_federation", labels, [fed_rows, single_rows])
    s = summarize_conds(labels, [fed_rows, single_rows],
                        ["best_frac", "novelty_top20"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    x = np.arange(2)
    for ax, metric, yl in [(axes[0], "novelty_top20", "mean novelty of top-20 candidates"),
                           (axes[1], "best_frac", "best value / grid optimum")]:
        means = [s[l][metric][0] for l in labels]
        stds = [s[l][metric][1] for l in labels]
        ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel(yl)
    axes[0].set_title("E4: novelty -- federation vs single team\nH: federation wins (Wu/Evans/Wang 2019)", wrap=True)
    axes[1].set_title("E4: discovery quality (equal compute)", wrap=True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e4_federation.png"))
    plt.close(fig)
    return ("e4", s)


# --------------------------------------------------------------------------
# E5 -- Turn-taking protocol vs free-for-all (n=6, T2).
# Hypothesis: protocol surfaces more errors, fewer escaped defects
# (Edmondson 1999; Project Aristotle).
# --------------------------------------------------------------------------
def exp_e5():
    conds = ["turn-taking", "free-for-all"]
    all_rows = [run_condition(5, i, lambda rng: list(BALANCED_6),
                             run_t2, {"rounds": 30, "protocol": p})
                for i, p in enumerate(conds)]
    save_csv("e5_turntaking", conds, all_rows)
    s = summarize_conds(conds, all_rows,
                        ["errors_surfaced", "defects_escaped", "net_revenue"])
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
    x = np.arange(2)
    for ax, metric, yl, ttl in [
            (axes[0], "errors_surfaced", "errors surfaced (count)",
             "errors surfaced\nH: protocol > free-for-all"),
            (axes[1], "defects_escaped", "defects escaped (count)",
             "defects escaped\nH: protocol < free-for-all"),
            (axes[2], "net_revenue", "net revenue (T2)",
             "net revenue")]:
        means = [s[l][metric][0] for l in conds]
        stds = [s[l][metric][1] for l in conds]
        ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(conds, rotation=12, ha="right")
        ax.set_ylabel(yl)
        ax.set_title(ttl, wrap=True)
    fig.suptitle("E5: turn-taking protocol vs free-for-all (Edmondson 1999; Project Aristotle)",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e5_turntaking.png"))
    plt.close(fig)
    return ("e5", s)


# --------------------------------------------------------------------------
# E6 -- Orchestrator selection (n=8): promote-by-coordination-trait vs
#       promote-top-task-scorer. Hypothesis: trait-selected >=10% better team
#       output (Benson, Li & Shue 2018; Lazear, Shaw & Stanton 2015).
# --------------------------------------------------------------------------
def exp_e6():
    # Build 8 agents; the coordinator is picked by mode, then stops producing
    # and coordinates (keeping their own traits -- the Benson-Li-Shue world).
    # NOTE: build_team returns an assembled team (not role names), so E6 runs
    # its own seed loop instead of run_condition.
    def build_team(rng, mode):
        team = assemble(["Builder"] * 5 + ["Specialist"] * 2 + ["Generic"], rng)
        coord = select_coordinator(team, mode)
        coord.role = "Coordinator"
        return team

    conds = ["trait-selected", "top-scorer"]
    modes = ["trait", "top-scorer"]
    all_rows = []
    for i, m in enumerate(modes):
        rows = []
        for s in SEEDS:
            rng = team_rng(6, i, s)
            team = build_team(rng, m)
            out = run_t2(team, seed=6000 + i * 100 + s, rounds=30)
            out["seed"] = s
            shares = out.pop("contrib_shares")
            k = math.ceil(math.sqrt(len(shares)))
            out["conc_top_sqrt"] = topk_share(shares, k)
            out["contrib_gini"] = gini(shares)
            rows.append(out)
        all_rows.append(rows)
    save_csv("e6_orchestrator", conds, all_rows)
    s = summarize_conds(conds, all_rows, ["net_revenue", "revenue_per_compute"])
    bar_fig(os.path.join(FIG, "e6_orchestrator.png"),
            "E6: team output by orchestrator selection rule\n"
            "H: trait-selected >=10% better (Benson, Li & Shue 2018; Lazear et al. 2015)",
            "net revenue (T2)",
            conds,
            [s[l]["net_revenue"][0] for l in conds],
            [s[l]["net_revenue"][1] for l in conds])
    return ("e6", s)


# --------------------------------------------------------------------------
# E7 -- Rank-and-prune: mid-run deactivation of bottom-2 contributors
#       (DyLAN analog, Liu et al. 2023) vs no prune. Instrument contribution
#       concentration (80/20 measurement).
# Hypothesis: pruning idlers improves efficiency; concentration is measurable.
# --------------------------------------------------------------------------
def exp_e7():
    roles = ["Builder"] * 3 + ["Specialist", "Analyst", "Healer", "Herald", "Framer"]
    conds = ["prune bottom-2 @mid", "no prune"]
    all_rows = [
        run_condition(7, 0, lambda rng: list(roles), run_t2,
                      {"rounds": 30, "prune_at": 15, "prune_k": 2}),
        run_condition(7, 1, lambda rng: list(roles), run_t2, {"rounds": 30}),
    ]
    save_csv("e7_prune", conds, all_rows)
    s = summarize_conds(conds, all_rows,
                        ["revenue_per_compute", "net_revenue", "conc_top_sqrt",
                         "contrib_gini", "n_final"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    x = np.arange(2)
    for ax, metric, yl, ttl in [
            (axes[0], "revenue_per_compute", "net revenue / compute",
             "E7: efficiency -- prune vs no prune\nH: pruning idlers improves efficiency"),
            (axes[1], "conc_top_sqrt", "share of top-sqrt(n) contributors",
             "E7: contribution concentration (measured,\nnot assumed -- Price's-law check)")]:
        means = [s[l][metric][0] for l in conds]
        stds = [s[l][metric][1] for l in conds]
        ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(conds, rotation=12, ha="right")
        ax.set_ylabel(yl)
        ax.set_title(ttl, wrap=True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e7_prune.png"))
    plt.close(fig)
    return ("e7", s)


# --------------------------------------------------------------------------
# E8 -- Written contracts (adherence enforced) vs implicit (drift allowed),
#       at n=6 and n=10, T1. Hypothesis: contracts reduce duplication/drift;
#       gap widens with n (Morning Star CLOU).
# --------------------------------------------------------------------------
def exp_e8():
    labels, all_rows = [], []
    for j, n in enumerate([6, 10]):
        for i, contracts in enumerate([True, False]):
            label = f"n={n} " + ("contracts" if contracts else "drift")
            labels.append(label)
            all_rows.append(run_condition(
                8, j * 10 + i, lambda rng, n=n: balanced_roles(n),
                run_t1, {"rounds": 40, "budget": 12, "contracts": contracts}))
    save_csv("e8_contracts", labels, all_rows)
    s = summarize_conds(labels, all_rows, ["best_frac", "evals_used"])
    bar_fig(os.path.join(FIG, "e8_contracts.png"),
            "E8: discovery quality -- written role contracts vs implicit drift\n"
            "H: contracts reduce drift/duplication; gap widens with n (Morning Star CLOU)",
            "best value / grid optimum (T1)",
            labels,
            [s[l]["best_frac"][0] for l in labels],
            [s[l]["best_frac"][1] for l in labels])
    return ("e8", s)


# --------------------------------------------------------------------------
# E9 -- Personality mix: mixed traits vs uniform traits, roles fixed, T1.
# Hypothesis: mixed wins on T1 (complementarity; Hong-Page conditions).
# --------------------------------------------------------------------------
def exp_e9():
    conds = [("mixed traits", "role"), ("uniform traits", "uniform")]
    labels = [c[0] for c in conds]
    all_rows = [run_condition(9, i, lambda rng: list(BALANCED_6),
                             run_t1, {"rounds": 40, "budget": 12}, tm)
                for i, (_, tm) in enumerate(conds)]
    save_csv("e9_traits", labels, all_rows)
    s = summarize_conds(labels, all_rows, ["best_frac", "novelty_top20"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    x = np.arange(2)
    for ax, metric, yl in [(axes[0], "best_frac", "best value / grid optimum"),
                           (axes[1], "novelty_top20", "mean novelty of top-20")]:
        means = [s[l][metric][0] for l in labels]
        stds = [s[l][metric][1] for l in labels]
        ax.bar(x, means, yerr=stds, capsize=4, color="#4C78A8", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=12, ha="right")
        ax.set_ylabel(yl)
    axes[0].set_title("E9: discovery quality -- mixed vs uniform traits\nH: mixed wins (Hong & Page 2004 conditions)", wrap=True)
    axes[1].set_title("E9: novelty", wrap=True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e9_traits.png"))
    plt.close(fig)
    return ("e9", s)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    results = {}
    for fn in [exp_e1, exp_e2, exp_e3, exp_e4, exp_e5, exp_e6, exp_e7, exp_e8, exp_e9]:
        name = fn.__name__
        print(f"running {name} ...", flush=True)
        t1 = time.time()
        out = fn()
        results[out[0]] = out[1:]
        print(f"  done in {time.time() - t1:.1f}s", flush=True)

    print("\n==== SUMMARY (mean +/- std across 20 seeds) ====")
    e1, e1t2 = results["e1"][0], results["e1"][1]
    for l in ["balanced", "all-builder", "all-framer", "random-mix", "no-roles"]:
        m, s = e1[l]["best_frac"]
        m2, s2 = e1t2[l]["revenue_per_compute"]
        print(f"E1 {l:12s} T1 best_frac {m:.3f}+/-{s:.3f} | T2 rpc {m2:.3f}+/-{s2:.3f}")
    e2 = results["e2"][0]
    peak = max(e2, key=lambda k: e2[k][0])
    print(f"E2 peak revenue/compute at {peak}: "
          + ", ".join(f"{k}={e2[k][0]:.3f}" for k in ["n=4", "n=5", "n=6", "n=7", "n=8", "n=9", "n=10"]))
    e3 = results["e3"][0]
    for l in ["1:4", "1:7", "1:12"]:
        m, s = e3[l]["revenue_per_compute"]
        print(f"E3 {l:5s} rpc {m:.3f}+/-{s:.3f}")
    e4 = results["e4"][0]
    for l in ["federation 2x5", "single 1x10"]:
        m, s = e4[l]["novelty_top20"]
        m2, s2 = e4[l]["best_frac"]
        print(f"E4 {l:15s} novelty {m:.3f}+/-{s:.3f} | best_frac {m2:.3f}+/-{s2:.3f}")
    e5 = results["e5"][0]
    for l in ["turn-taking", "free-for-all"]:
        a, b = e5[l]["errors_surfaced"], e5[l]["defects_escaped"]
        print(f"E5 {l:13s} errors_surfaced {a[0]:.1f}+/-{a[1]:.1f} | defects_escaped {b[0]:.1f}+/-{b[1]:.1f}")
    e6 = results["e6"][0]
    for l in ["trait-selected", "top-scorer"]:
        m, s = e6[l]["net_revenue"]
        print(f"E6 {l:15s} net_revenue {m:.2f}+/-{s:.2f}")
    e7 = results["e7"][0]
    for l in ["prune bottom-2 @mid", "no prune"]:
        m, s = e7[l]["revenue_per_compute"]
        c, cs = e7[l]["conc_top_sqrt"]
        print(f"E7 {l:18s} rpc {m:.3f}+/-{s:.3f} | conc_top_sqrt {c:.2f}+/-{cs:.2f}")
    e8 = results["e8"][0]
    for l in ["n=6 contracts", "n=6 drift", "n=10 contracts", "n=10 drift"]:
        m, s = e8[l]["best_frac"]
        print(f"E8 {l:14s} best_frac {m:.3f}+/-{s:.3f}")
    e9 = results["e9"][0]
    for l in ["mixed traits", "uniform traits"]:
        m, s = e9[l]["best_frac"]
        print(f"E9 {l:15s} best_frac {m:.3f}+/-{s:.3f}")
    print(f"\nTOTAL runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
