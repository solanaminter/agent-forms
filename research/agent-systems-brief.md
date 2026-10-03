# Multi-Agent Systems & Role Composition — Literature Brief
*For the "agent forms" project (designing multi-agent AI teams using organizational wisdom). Compiled 2026-10-02.*
*Evidence tags: **[EVIDENCE]** = peer-reviewed paper or measured result; **[ENGINEERING]** = first-party engineering report with numbers; **[SECONDARY]** = cited via secondary survey/community doc — verify before relying on exact numbers; **[DISCOURSE]** = essays/industry writing, not measured claims.*

---

## 1. Role-based multi-agent frameworks

### MetaGPT — "Code = SOP(Team)" **[EVIDENCE]**
- **Paper:** Hong, S. et al. (2023/2024). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework.* ICLR 2024. https://arxiv.org/abs/2308.00352
- **Claim:** Simulates a software company: fixed roles — **Product Manager → Architect → Project Manager → Engineer → QA Engineer** — passing structured artifacts (PRD, design doc, task list, code) through encoded Standardized Operating Procedures (SOPs). Structured artifact handoffs suppress cascading hallucinations of free-chat chains.
- **Key numbers:** 85.9% Pass@1 on HumanEval (vs GPT-4's 67.0%); 87.7% on MBPP; 2× token efficiency vs ChatDev (124.3 vs 248.9 tokens/line). **[SECONDARY]** — these figures come from community summaries of the paper; confirm from the paper itself.
- **Composition pattern:** fixed, small (5 roles), sequential pipeline, heterogeneity by *role*, not by model.

### ChatDev — "virtual software company" via chat chains **[EVIDENCE]**
- **Paper:** Qian, C. et al. (2023). *Communicative Agents for Software Development.* ACL 2024. https://aclanthology.org/2024.acl-long.810/ (arXiv:2307.07924)
- **Claim:** Roles mirror a real company org chart — **CEO, CPO, CTO, Programmer, Reviewer, Tester** (+ Art Designer) — organized into four waterfall phases (Designing, Coding, Testing, Documenting). The core unit is a *chat chain*: exactly two agents (Instructor + Assistant) hold a bounded dialogue per subtask. The value comes from **paired propose/validate dialogue, not from a large simultaneous committee**.
- **Key numbers:** over 70 requirements, avg 17.04 files/program, ~409 s, ~$0.30/program; reviewer–programmer dialogue caught ~20 vulnerability types, tester–programmer dialogue >10 bugs **[SECONDARY via survey]**. A follow-on study reported ChatDev identified ~10/20 vulnerability types through multi-turn dialogue. Note: ChatDev **2.0 (DevAll, 2025)** moved to a general orchestration platform with map/tree parallelism, backed by MacNet (multi-agent network scaling, NeurIPS 2025) and Puppeteer (dynamic orchestration).

### AutoGen — conversable agents, no prescribed org **[EVIDENCE]**
- **Paper:** Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* COLM 2024. https://arxiv.org/abs/2308.08155
- **Claim:** Two abstractions: (1) **ConversableAgent** (backed by LLM/human/tool; subclasses `AssistantAgent` solver and `UserProxyAgent` for human + code execution); (2) **conversation programming** — the workflow *is* the conversation, with static or dynamic interaction patterns. Deliberately prescribes no fixed role set: roles = configured capability subsets. Dynamic group chat uses a `GroupChatManager` that repeatedly selects a speaker; a pilot on 12 complex tasks found role-play speaker selection beat task-based selection on success rate with fewer LLM calls **[SECONDARY]**.
- **Composition pattern:** programmable, any size, any topology; roles are emergent from config, not canonical.

### CrewAI — role/goal/backstory + three orchestration modes **[ENGINEERING/DOCS]**
- **Source:** CrewAI docs & community; flagship patterns from https://www.analyticsinsight.net/artificial-intelligence/crewai-explained-how-role-based-ai-agents-work
- **Claim:** Every agent is defined by **role + goal + backstory** (behavioral instructions, not true specialization). Crews run in one of three processes:
  - **Sequential** — assembly line; strict dependencies; one agent's output feeds the next.
  - **Hierarchical** — a manager agent dynamically delegates to worker agents, validates outputs, reroutes. Best for complex/iterative work requiring quality control.
  - **Consensual (experimental)** — agents negotiate/vote on execution paths.
- **Relevant evidence:** a TDS case study documents manager–worker failure modes (delegation breakdowns), i.e., hierarchy adds a failure surface when delegation is vague.

### CAMEL — inception-prompted role-play (minimal pair) **[EVIDENCE]**
- **Paper:** Li, G. et al. (2023). *CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society.* https://arxiv.org/abs/2303.17760
- **Claim:** The minimal viable agent organization is **two agents** (assistant + user) role-playing via "inception prompting" with minimal human supervision. Shows role-play alone unlocks cooperative task-solving.

---

## 2. Agent societies & collective behavior

### AgentVerse — dynamic expert recruitment + emergent behaviors **[EVIDENCE]**
- **Paper:** Chen, W. et al. (2023). *AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors.* ICLR 2024. https://arxiv.org/abs/2308.10848
- **Claim:** Four-stage loop: **(1) Expert Recruitment** (a "recruiter" agent auto-generates expert role descriptions per task — an HR-manager analogue; composition re-adjusts after each round), **(2) Collaborative Decision-Making** (horizontal/democratic or vertical/solver+reviewers), **(3) Action Execution**, **(4) Evaluation**. Dynamic groups beat single agents and static groups across reasoning, coding, tool-use tasks. **Three emergent social behaviors observed without being programmed: volunteering, conformity, and destructive behavior** — directly relevant to free-riding/conformity/idle-agent failure modes.

### DyLAN — feed-forward agent network + inference-time team optimization **[EVIDENCE]**
- **Paper:** Liu, Z. et al. (2023). *Dynamic LLM-Agent Network: An LLM-Agent Collaboration Framework.* ICLR 2024 (under review). https://arxiv.org/abs/2310.02170
- **Claim:** Models multi-round collaboration as a feed-forward network (agents = nodes at time steps, messages = edges). Uses an **LLM-empowered ranker to rank agents and deactivate low-performing ones** at inference time — explicit pruning of unproductive agents — plus **Byzantine-consensus early stopping** (stop when a layer reaches consensus). Also proposes automatic agent team optimization: agents rate predecessors' solutions; aggregate ratings select top-k contributors.
- **Relevance:** the closest published analogue to "fire the underperformers / cut idle agents": DyLAN *measures contribution and deactivates low-contribution nodes*, validating an internal performance-rating mechanism.

### Generative Agents (Smallville) — the persona + memory substrate **[EVIDENCE]**
- **Paper:** Park, J.S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* UIST 2023 (Best Paper). https://arxiv.org/abs/2304.03442
- **Claim:** 25 agents in a sandbox town, each with a **memory stream + reflection + planning** architecture, seeded only with natural-language persona descriptions. Emergent social behavior (information diffusion, relationship formation, coordination — e.g., organizing a Valentine's Day party) arose from believable individuals; ablations showed each architectural component necessary. Human evaluators rated agents more believable than crowdworker-authored alternatives.
- **Relevance:** establishes that **persona initialization is a first-class design lever** — "no objective; the 'direction' is the persona + the event stream."

### AgentSociety — population-scale agent society (10k+ agents) **[EVIDENCE]**
- **Paper:** Piao, J. et al. (2025). *AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents Advances Understanding of Human Behaviors and Society.* https://arxiv.org/abs/2502.08691
- **Claim:** 10,000+ LLM agents (GPT-4-based, with memory, goals, decision-making, social tracking), ~5M interactions, in a realistic urban/social/economic environment (MQTT messaging, distributed engine). Reproduced outcomes of five real-world social experiments: polarization, inflammatory information spread, UBI policy effects, hurricane shocks, urban sustainability.
- **Relevance:** proof that large-scale agent "organizations" can be simulated and *empirically validated against real human data* — the right substrate for testing org-form hypotheses.

### SOTopia — social intelligence as a measurable team outcome **[EVIDENCE]**
- **Paper:** Zhou, X. et al. (2023/2024). *SOTopia: Interactive Evaluation for Social Intelligence in Language Agents.* ICLR 2024. https://arxiv.org/abs/2310.11667
- **Claim:** 90 scenarios × 40 characters (with personalities, occupations, secrets, goals) as a task space; agents coordinate/compete/negotiate. **SOTOPIA-Eval**: 7 dimensions — Goal Completion [0–10], Believability, Knowledge, Secret [-10–0], Relationship [-5–5], Social Rules [-10–0], Financial/Material Benefits [-5–5] — with GPT-4 judges correlating well with human ratings. Even GPT-4 falls short of humans on SOTOPIA-hard; agents are highly influenced by partners and leak secrets.
- **Relevance:** an off-the-shelf multi-dimensional **evaluation protocol for agent social performance** — usable as an outcome measure for "agent form" experiments.

### MultiAgentBench — topology systematically compared **[EVIDENCE]**
- **Paper:** Zhu, K. et al. (2025). *MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents.* ACL 2025. https://aclanthology.org/2025.acl-long.421/
- **Claim:** Benchmarks collaboration/competition under different coordination structures; shows **star, chain, tree, and graph topologies substantially change collective performance** — communication structure is a first-order design variable. **[SECONDARY via survey README]**.

---

## 3. Scaling & composition findings

### "More Agents Is All You Need" — Agent Forest (sampling-and-voting scaling law) **[EVIDENCE]**
- **Paper:** Li, J. et al. (2024). *More Agents Is All You Need.* https://arxiv.org/abs/2402.05120 (Tencent)
- **Claim:** Simple sampling-and-voting over N instantiated agents yields performance that **scales monotonically with N** (tested up to N≈40 on GSM8K, MATH, MMLU) — no complex collaboration machinery needed. Gains are task-difficulty dependent: (1) gains rise then fall with inherent difficulty, (2) gains grow with number of reasoning steps, (3) gains grow with prior probability of a correct answer. Hierarchical LLM deployment (different models at different levels) improved 35%→47% **[SECONDARY]**.
- **Caveat:** this is *parallel independent sampling + voting*, not collaborative organizations — the "headcount" scales but there is no org structure. Also the 2026 follow-up "Rethinking Mixture-of-Agents" (TMLR) found Self-MoA outperforming 3-layer Mixed-MoA with half the forward passes — raw width is not always optimal.

### Mixture-of-Agents (MoA) — proposer/aggregator layers **[EVIDENCE]**
- **Paper:** Wang, J. et al. (2024). *Mixture-of-Agents Enhances Large Language Model Capabilities.* https://arxiv.org/abs/2406.04692 (Together AI, ICLR 2025)
- **Claim:** Layered architecture: N proposers generate diverse responses; an **aggregator** synthesizes them; stack 2–3 layers. Two functional roles — proposer and aggregator — with **model specialization**: WizardLM excels as proposer but poor as aggregator; GPT-4o/Qwen/LLaMA-3 versatile at both **[from paper text]**. Open-model MoA reached 65.1% LC win rate on AlpacaEval 2.0 vs GPT-4o's 57.5%. Scores increase monotonically with n (more proposers), and **multiple different LLMs as proposers consistently beat the same LLM sampled n times** (diversity > redundancy).
- **Relevance:** first quantitative evidence for **functional role specialization in agent teams** and for *diversity over headcount*.

### Multi-agent debate (Du et al.) — critique-and-revise improves factuality/reasoning **[EVIDENCE]**
- **Paper:** Du, Y. et al. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.* ICML 2024. https://arxiv.org/abs/2305.14325
- **Claim:** 3 identical-model agents independently answer, then debate over 2 rounds seeing each other's answers; converge to a common answer. Arithmetic 67%→82%; GSM8K 77%→85%; MMLU 64%→71%; biographies factuality 66%→74% **[SECONDARY via community summary — verify]**. More agents and more rounds help; but **convergence ≠ correctness** (confident wrong consensus possible); expensive (~9 calls/question).
- **Follow-ups:** ReConcile (Chen et al., 2023, https://arxiv.org/abs/2309.13007): round-table with **confidence-weighted voting across diverse LLM families**, up to +11.4% — **model diversity is the primary driver** **[SECONDARY]**. Liang et al. (2024, EMNLP, https://arxiv.org/abs/2305.19118) identifies **Degeneration-of-Thought**: single agents can't self-correct once confident; multi-agent debate overcomes it — i.e., dissent is load-bearing. Wu et al. (2025, https://arxiv.org/abs/2511.07784) controlled study: **intrinsic reasoning strength and group diversity dominate**; structural knobs (order, confidence visibility) give limited gains; **majority pressure suppresses independent correction**. Choi et al. (2025, https://arxiv.org/abs/2508.17536, NeurIPS spotlight): **majority voting alone accounts for most multi-agent gains**; multi-round debate adds only marginal benefit in some settings.

### Anthropic's multi-agent research system — orchestrator-worker in production **[ENGINEERING]**
- **Source:** Anthropic Engineering blog, "How we built our multi-agent research system" (June 13, 2025). https://www.anthropic.com/engineering/multi-agent-research-system
- **Claim:** Lead agent plans, spawns 3–5 parallel subagents with isolated contexts, synthesizes; separate CitationAgent. **Outperformed single-agent Claude Opus 4 by 90.2%** on internal research eval. **Token usage alone explained 80% of performance variance** on BrowseComp; multi-agent uses **~15× the tokens** of chat. Scoping rule: simple fact-finding = 1 agent (3–10 calls); comparisons = 2–4 subagents; complex research = 10+ subagents. **Explicit caveats:** poor fit where agents need shared context or many interdependencies — *"most coding tasks involve fewer truly parallelizable tasks than research."* Failure modes named: agents **"spawning 50 subagents for simple queries"** (role/team proliferation) and **"distracting each other with excessive updates"** (coordination tax).
- **Counterpoint:** Cognition (Walden Yan, "Don't Build Multi-Agents," June 12, 2025) argues parallel subagents make conflicting implicit decisions (worked example: Flappy Bird split across two subagents produced incompatible halves); principles: share full traces, keep writing single-threaded. The two converge on: **fan out for reading; keep writing single-threaded.**

---

## 4. Communication topology & coordination overhead

- **Sparse debate topologies:** Li et al. (Findings of EMNLP 2024) — "Sparse Communication Topology": sparsifying the debate graph cuts tokens 30–60% with minimal accuracy loss; overly dense topologies become burdensome; **performance does not consistently improve with increased edge density** (also MacNet, Qian et al. 2025: MLP-like/complete/random/star/tree graphs tested). **[SECONDARY via survey]**
- **AgentPrune** (Zhang et al., 2025): formally defines **Communication Redundancy** in MAS; learns a graph mask to prune removable edges with comparable performance — most multi-agent edges are redundant. **[SECONDARY]**
- **Towards a Science of Scaling Agent Systems** (Kim, Liu et al., 2025/2026, Google DeepMind/MIT, https://arxiv.org/abs/2512.08296) — the keystone quantitative study **[SECONDARY via community summaries — verify numbers in paper]**: 180 configurations × 5 architectures × 3 model families × 4 benchmarks; mixed-effects model (R² = 0.524); three dominant effects: (1) **tool-coordination trade-off**, (2) **capability saturation beyond ~45% single-agent baseline** (above it, multi-agent overhead dominates → diminishing/negative returns), (3) **topology-dependent error amplification**: independent "bag of agents" amplifies errors **17.2×**, centralized orchestrator contains it to **4.4×**. Centralized coordination: +80.8% on parallelizable tasks (financial reasoning); **all multi-agent variants degrade 39–70% on sequential constraint-satisfaction tasks**. Architecture-task alignment determines success, not agent count; the model predicts the optimal architecture for 87% of held-out configurations (cross-validated).
- **Topology taxonomy:** independent (no communication), centralized (orchestrator), decentralized (peer-to-peer), hybrid (hierarchy + lateral) — plus learned/dynamic variants: GPTSwarm (Zhuge et al., 2024), G-Designer (Zhang et al., 2025), GTD graph-diffusion topology generation (2025) reporting 94.14% on GSM8K with sparse generated topologies vs 87.45% vanilla CoT **[SECONDARY via paper text]**, TalkHier (Wang et al., 2025): hierarchical activation of agent teams.
- **Scale anecdote:** SWARM+ (2026) coordinates ~1,000 agents at 98.5% completion by keeping **group size ≤10 at every hierarchy level** **[SECONDARY, single community source — weak evidence]**.

---

## 5. "Agent organizations" / companies-as-agents discourse

- **McKinsey, "The agentic organization: Contours of the next paradigm for the AI era" (Sep 2025)** — frames the "agentic organization" as the largest org paradigm shift since the industrial/digital revolutions: humans + virtual/physical AI agents working side by side at near-zero marginal cost. Based on early-adopter experience; a management-consulting framing, not measured science. **[DISCOURSE]** (PDF: http://kingsley.idehen.net/DAV/home/kidehen/Public/PDFs/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era.pdf)
- **The "virtual company" framing is native to the agent literature itself:** MetaGPT ("simulate a software company"), ChatDev ("virtual software company" with CEO/CTO/CPO), CAMEL ("mind exploration of LLM society"). The field already borrows org charts as architectures — but almost entirely for *software engineering* teams.
- **Anthropic, "Building Effective Agents" (Dec 2024)** https://www.anthropic.com/engineering/building-effective-agents — catalogs five composable patterns (prompt chaining, routing, parallelization, **orchestrator-workers**, evaluator-optimizer); first principle: simplicity; add agentic complexity only when it demonstrably pays. **[ENGINEERING]**
- **Gap:** I found no 2024–2026 paper that *measures* alternative org forms (percentages of roles like village craftspeople/healers/propagandists, span-of-control experiments, middle-management ablations) against outcomes like revenue or scientific discovery. The org-as-agent literature is almost all either (a) software-company mimicry or (b) social-simulation description. **Your proposed experiment — parametrized role-mix + topology × outcome metrics — is a genuine gap.**

---

## 6. Failure modes observed ("too many cooks" analogues)

| Failure mode | Source |
|---|---|
| **Conformity / stance homogenization** (agents copy each other, suppressing correction) | AgentVerse (emergent behavior) **[EVIDENCE]**; Wu et al. 2025: "majority pressure suppresses independent correction" **[EVIDENCE]** |
| **Destructive behavior** emerging unprompted in tool-use games | AgentVerse **[EVIDENCE]** |
| **Free-riding by another name**: idle/low-contribution agents; fixed by ranking + deactivation | DyLAN's inference-time agent selection + Byzantine early stopping **[EVIDENCE]** |
| **Role/team proliferation**: "spawning 50 subagents for simple queries"; "distracting each other with excessive updates" | Anthropic engineering **[ENGINEERING]** |
| **Capability saturation**: single-agent >~45% accuracy ⇒ multi-agent adds overhead, diminishing or negative returns | Science-of-Scaling study **[SECONDARY]** |
| **Error amplification via topology**: 17.2× for independent agents vs 4.4× centralized | Science-of-Scaling study **[SECONDARY]** |
| **Converging confidently on wrong answers** | Du et al. debate **[EVIDENCE]**; Wu et al. 2025 **[EVIDENCE]** |
| **Multi-agent collapse under misaligned principals** (different users, shared resources): single coordinator fulfills ~2× as many requests; teams "completely collapse in two environments" | "Worse Together" / **MAMUBench** (Paliskara, Namchittai, Lampinen, 2026) **[SECONDARY via smartchunks write-up — verify paper]** |
| **Degeneration-of-Thought**: confident single agents can't self-correct; needs external dissent | Liang et al., EMNLP 2024 **[EVIDENCE]** |
| **Sequential tasks degrade under decomposition** (39–70% worse for all multi-agent variants) | Science-of-Scaling study **[SECONDARY]** |

---

## 7. Personality / prompt-initialization effects on team outcomes

- **Big5-Scaler (2025)** https://arxiv.org/abs/2508.06149 — prompt-based Big Five conditioning with explicit numeric trait values (0–100) at inference time, no fine-tuning; reliably elicits personality-consistent behavior (trait scores >4.0/5, PersonaCLR ~0.8). Gives a **quantitative personality knob** for experiments. **[EVIDENCE, single paper]**
- **"Not Birds of a Feather"** (Wang, Chiu, Wei, Hou, Xiu, Univ. of Toronto, 2026) https://arxiv.org/pdf/2607.19785v2 — a host agent choosing among six Big-Five-differentiated candidates (capability equalized, 375 trials): selection is strongly personality-dependent; neutral hosts match personalities to task types (open→creative, conscientious→most else); hosts with their own personalities choose **complements, not similar partners** — opposite of human homophily. **[EVIDENCE, preprint]**
- **"Agents with Feelings?"** (2026) https://arxiv.org/html/2607.05659 — systematic study of personality+emotion profiles in LLM *software* teams: shared-profile vs mixed-profile teams across 4 LLMs; mixed personality profiles affect team performance **[SECONDARY via abstract]**.
- **Aral & Ju (MIT, human–AI pairing study, 1,200+ participants)** — Big Five-prompted AI collaborators: best text/image ad quality from extraverted-human×extraverted-AI, conscientious×conscientious, open-human×conscientious-AI pairings; some pairings significantly *reduced* quality (e.g., extraverted human × conscientious AI). **[SECONDARY via press write-up — find the paper]**
- **Diversity-of-thought as a mechanism:** MoA shows diverse-model proposers beat same-model sampling; ReConcile shows diversity is the primary driver; SOTopia shows agents are highly influenced by conversational partners. Together: **persona/role diversity is well-evidenced as beneficial; specific trait→outcome mappings are still speculative.**

---

## 8. Design patterns worth testing (from the literature)

1. **Static SOP pipeline** (MetaGPT pattern): 5 fixed roles, sequential, structured artifact handoffs. Baseline for "company org chart." Test: vary role count (3 vs 5 vs 8) and measure error cascade vs verification gain.
2. **Dyadic chat chains** (ChatDev pattern): exactly 2 agents per subtask (Instructor+Assistant). Test the hypothesis that pairwise dialogue beats committee discussion at equal token budgets.
3. **Dynamic recruiter team** (AgentVerse pattern): an HR-analogue recruiter generates role descriptions per task, re-staffs after evaluation rounds. Test: recruiter-chosen mix vs fixed mix vs random mix.
4. **Rank-and-prune** (DyLAN pattern): agents rate each other's contributions; deactivate bottom-k; Byzantine-consensus early stop. Test as the "cut idle middle management" intervention — measure contribution distribution (does an 80/20 split emerge?).
5. **MoA proposer/aggregator layers**: homogeneous proposers (2–6) + one aggregator, 2 layers. Test: diverse-model proposers vs diverse-persona proposers vs same-model sampling.
6. **Debate with dissent preservation** (Du + Wu 2025 + ReConcile): 3 agents, 2 rounds, confidence-weighted voting across diverse models; test majority-vote fast path vs full debate (Choi 2025 says voting captures most gains).
7. **Orchestrator-worker** (Anthropic pattern): lead plans, 3–5 isolated-context subagents, synthesis pass. Test on breadth-first vs tightly-coupled tasks to replicate the 45%-saturation boundary.
8. **Topology sweep** (MultiAgentBench pattern): same task × star/chain/tree/graph/centralized/decentralized; measure error amplification and coordination tokens.
9. **Personality-mix experiments** (Big5-Scaler + Not-Birds-of-a-Feather): fix roles, vary trait profiles (all-conscientious vs mixed OCEAN); test recruiter-selected complementarity vs homophily.
10. **Principal-alignment ablation** ("Worse Together" pattern): same team, aligned vs misaligned goals over a shared resource pool; measures the organizational-wisdom claim that *shared objectives* are the precondition for any org form.

### Evidence quality flags
- **Well-evidenced:** role assignment beats no-role (AgentVerse); structured handoffs beat free chat (MetaGPT); diversity > headcount (MoA, ReConcile); debate improves reasoning with diminishing returns (Du + follow-ups); coordination overhead grows superlinearly and centralized topologies contain errors (scaling-science study); topology changes outcomes (MultiAgentBench); persona prompts steer behavior measurably (Big5-Scaler); orchestrator-worker wins big on breadth-first research but not on tightly-coupled coding (Anthropic).
- **Speculative / thin:** exact "ideal percentage breakdown" of roles (no paper tests this); SWARM+ 1,000-agent claim (single community source); the 45% saturation threshold and 17.2×/4.4× error figures (one recent paper, verify); "Worse Together"/MAMUBench details (press write-up only); Aral & Ju trait-pairing effects (press write-up only); any claim mapping Big Five mixes to revenue or scientific discovery (not studied).
- **Genuine gap (your project's opening):** no published work parametrizes *role mix percentages* and *management-layer depth* against outcome metrics. The closest instruments are DyLAN (contribution ranking), AgentSociety (population-scale simulation), and SOTOPIA-Eval (multi-dimensional outcome scoring).
