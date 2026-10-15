# Workstream 07 — Self-Learning, Adaptation and Retention

**Objectives served:** demonstrate transfer and retention; learn from experience without unlimited or
unbounded learning; keep procedures and lessons separate from facts and hypotheses; fail conservatively
under unfamiliar conditions.

**The central finding of this workstream** (`inspected`, across `reflexion`, `self-refine`, `textgrad`,
`opro`, `voyager`, `expel`, `ace`, `dspy`, `a-mem`): every one of them demonstrates improvement **on the
task it was built for**. **None** of the bundled material demonstrates *retention over unrelated sessions*,
*transfer to a different document class*, or *regression prevention* — the three properties objective 7
actually asks for. That is a gap in the field, not a gap in the search, and it means those three properties
must be **constructed locally** (roadmap Phase 6) rather than adopted.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 7.1 | **External-memory adaptation** (procedures, lessons, prompts) separated from **parameter updates** (fine-tuning, RL) | Only the first is compatible with a frozen evaluation and an unknown resource budget |
| 7.2 | A lesson enters `lessons` **only** with independent review: human, frozen key, or verifiable external signal | Model self-critique is not supervision |
| 7.3 | Self-reflection may **propose**, never **accept** | The single most common way a system talks itself into a regression |
| 7.4 | **Regression suite**: the frozen evaluation re-run after every change | "Learning" that breaks previously working behaviour is not learning |
| 7.5 | **Retention probe**: re-ask previously answered items after N unrelated sessions | Detects forgetting disguised as improvement |
| 7.6 | **Transfer set**: a third document class, never used in tuning | Detects source-specific overfitting |
| 7.7 | Procedures are **declarative recipes** with preconditions, steps, validation and a recorded scope | A procedure that fires with unmet preconditions is a bug with confidence |
| 7.8 | **Bounded** learning: an explicit cap on how much may change per cycle, and a rollback path | "Unlimited learning" is an explicit non-goal |
| 7.9 | Every adaptation records what evidence produced it, and can be reverted individually | Auditable learning, not drift |

**Not a goal.** A system that improves on its own without an external signal. That is the thing this
workstream is designed to refuse.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: skill-library + itemised-playbook growth, gated by external review

* **Procedures** follow the Voyager skill-library pattern (MIT, code bundled): a skill is a named, reusable
  recipe stored with the conditions under which it was shown to work. Voyager's published result — 3.3× more
  unique items and skills that transfer to a **new** world — is the reason the pattern is interesting. It is
  also a Minecraft result, and therefore an **analogy, not evidence** for document reading.
* **Playbook growth** follows ACE's itemised, append-only model (Apache-2.0): add or revise individual items
  rather than rewriting a whole context. Append-only growth is auditable and revertible, which whole-context
  rewriting is not.
* **Acceptance** follows §7.2: an external signal, a frozen key, or a human. Reflexion-style verbal
  self-reflection (MIT, code bundled) and Self-Refine's iterative refinement (Apache-2.0) are allowed to
  *propose* items into `hypotheses`; promotion to `lessons` requires the gate.
* **Bounds** follow §7.8: a cap on items changed per cycle, a diff, and a one-command revert.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **PEFT / LoRA** | **Rejected for this project** | Adapter training needs a GPU and substantial RAM (Q1 unanswered). More fundamentally: weights changing underneath a frozen evaluation destroys the comparability that Phase 1 exists to create, and contamination becomes much harder to rule out |
| **Unsloth** | **Rejected** | GPU (CUDA) required; its large memory-reduction claims are **reported** by the vendor and not reproduced here |
| **bitsandbytes / quantisation for inference** | Catalogued, not a learning mechanism | Reducing inference cost is workstream 13's business, not adaptation |
| **Tree of Thoughts** | **Rejected** | Search multiplies LLM calls per question and produces more confident wrong answers when no evidence gate exists |
| **DSPy optimisers** | Catalogued for its **signature and metric vocabulary** | The library is light; the optimisers make many calls, and optimisation must never touch held-out sources. Borrow the typed-signature idea for workstream 04's contracts |
| **OPRO** (LLMs as optimizers) | Pattern noted, not adopted | Iterative LLM calls to optimise a prompt; same leakage risk, and the gains are on the authors' tasks |
| **TextGrad** | Pattern noted, not adopted | "Textual gradients" are many LLM calls; without an external signal it is self-critique with extra steps. Dormant since 2025-07 |
| **ExpeL** | Reference only | Experiential learning from a task pool; **upstream has no licence file**, so only what the licence permitted was kept, and the slug did not resolve via the API on 2026-10-14 |
| **A-MEM** | Pattern noted, not adopted | LLM-driven linking between memories is consolidation, which workstream 06 rejects |
| **mem0** as a learning layer | Not adopted | Extraction needs a vector store plus an LLM per write; consolidation rewrites records |
| **smolagents** | Catalogued | Very light agent loop (Apache-2.0), useful if an agentic reading loop is ever needed — but an agent loop is not a learning mechanism, and it enlarges the tool surface that workstream 14 has to contain |
| **LMOps / promptbench** (Microsoft, MIT) | Catalogued | Prompt-optimisation and benchmarking utilities; overlapping with DSPy, and every optimiser carries the same leakage constraint |
| **Google LLM Tuning Playbook** (CC BY 4.0) | **Adopted as guidance** | The only fully redistributable long-form technical report in the collection (~120 KB of text bundled). Its evaluation-first discipline matches this workstream's requirements directly |

### 2.3 Why the evidence base is weaker than it looks

Reported gains in this category are almost all measured **in environments with ground-truth feedback**:

* Reflexion — 91% pass@1 on HumanEval versus GPT-4's 80% (arXiv:2303.11366v4, **verified** metadata).
  HumanEval has a test suite. The reflection is graded by execution, not by the model.
* Self-Refine — ~20% average absolute improvement (arXiv:2303.17651v2, **verified**), on GPT-3.5/4-era
  models, on tasks with checkable outputs.
* Voyager — skills validated by environment execution in Minecraft.
* Self-Rewarding LMs (arXiv:2401.10020v3, **verified**) — the model is its own judge, which is exactly the
  configuration §7.2 forbids for `lessons`.

Document interpretation has **no execution oracle**. A wrong reading of a specification does not throw an
exception. That is why the gate must be a human, a frozen key, or a verifiable external signal — and why
"the model said it improved" is not admissible here.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `tuning-playbook` (CC BY 4.0) | [full playbook text](../../resources/documentation/tuning-playbook/) · [licence](../../resources/licenses/tuning-playbook/) |
| `voyager` (MIT) | [documentation](../../resources/documentation/voyager/) · [code examples](../../resources/code-examples/voyager/) · [licence](../../resources/licenses/voyager/) — dormant since 2024-04 |
| `ace` (Apache-2.0) | [documentation](../../resources/documentation/ace/) · [licence](../../resources/licenses/ace/) |
| `reflexion` (MIT) | [documentation](../../resources/documentation/reflexion/) · [code examples](../../resources/code-examples/reflexion/) · [licence](../../resources/licenses/reflexion/) — dormant since 2025-01 |
| `self-refine` (Apache-2.0) | [documentation](../../resources/documentation/self-refine/) · [licence](../../resources/licenses/self-refine/) — dormant since 2024-10 |
| `textgrad` (MIT) | [documentation](../../resources/documentation/textgrad/) · [code examples](../../resources/code-examples/textgrad/) · [licence](../../resources/licenses/textgrad/) — dormant since 2025-07 |
| `opro` (Apache-2.0) | [documentation](../../resources/documentation/opro/) · [code examples](../../resources/code-examples/opro/) · [licence](../../resources/licenses/opro/) — dormant since 2024-12 |
| `dspy` (MIT) | [documentation](../../resources/documentation/dspy/) — signatures, modules, metrics, evaluation, optimisation · [licence](../../resources/licenses/dspy/) |
| `expel` | [documentation](../../resources/documentation/expel/) · [licence](../../resources/licenses/expel/) — **no upstream licence file at `LeapLabTHU/ExpeL`; treat as reference only** |
| `a-mem` (MIT) | [documentation](../../resources/documentation/a-mem/) · [licence](../../resources/licenses/a-mem/) |
| `lmops` (MIT) | [documentation](../../resources/documentation/lmops/) · [licence](../../resources/licenses/lmops/) |
| `smolagents` (Apache-2.0) | [documentation](../../resources/documentation/smolagents/) · [licence](../../resources/licenses/smolagents/) |
| `mem0` (Apache-2.0) | [documentation](../../resources/documentation/mem0/) · [licence](../../resources/licenses/mem0/) |
| `peft` (Apache-2.0) | [documentation](../../resources/documentation/peft/) · [licence](../../resources/licenses/peft/) — **rejected** as a learning mechanism |
| `unsloth` (Apache-2.0) | [documentation](../../resources/documentation/unsloth/) · [licence](../../resources/licenses/unsloth/) — **rejected** |
| `tot` (MIT) | [documentation](../../resources/documentation/tot/) · [code examples](../../resources/code-examples/tot/) · [licence](../../resources/licenses/tot/) — **rejected** |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) — Voyager, Reflexion, Self-Refine, Self-Rewarding LMs, Generative Agents, ExpeL |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| Google LLM Tuning Playbook | https://github.com/google-research/tuning_playbook (dormant since 2024-06) |
| Voyager | https://github.com/MineDojo/Voyager · arXiv:2305.16291v2 (**verified**) |
| ACE | https://github.com/ace-agent/ace (**slug corrected from `ShengranHu/ACE`**) |
| Reflexion | https://github.com/noahshinn/reflexion · arXiv:2303.11366v4 (**verified**) |
| Self-Refine | https://github.com/madaan/self-refine · arXiv:2303.17651v2 (**verified**) |
| TextGrad | https://github.com/zou-group/textgrad |
| OPRO | https://github.com/google-deepmind/opro |
| DSPy | https://github.com/stanfordnlp/dspy |
| ExpeL | https://github.com/LeapLabTHU/ExpeL (**did not resolve via the API on 2026-10-14**) |
| A-MEM | https://github.com/agiresearch/A-mem |
| LMOps | https://github.com/microsoft/LMOps |
| smolagents | https://github.com/huggingface/smolagents |
| mem0 | https://github.com/mem0ai/mem0 |
| PEFT | https://github.com/huggingface/peft |
| Unsloth | https://github.com/unslothai/unsloth |
| Tree of Thoughts | https://github.com/princeton-nlp/tree-of-thought-llm |
| Self-Rewarding LMs | arXiv:2401.10020v3 (**verified**) — no bundled code |

## 5. Adoption steps

1. **Do not start here.** Phases 0–4 of the [roadmap](../../IMPLEMENTATION_ROADMAP.md) come first: without a
   measured budget, a frozen evaluation and trustworthy stores, any "learning" is unverifiable drift.
2. **Define the procedure schema** (workstream 06, §2.1): name, preconditions, ordered steps, validation,
   `scope_shown_to_work`, `evaluation_id`.
3. **Add the precondition check**: a procedure whose preconditions are unmet **refuses to run** and records
   the refusal. This is also the strategy-suitability gate workstream 10 needs.
4. **Add the proposal path**: self-reflection writes candidate items into `hypotheses` with `origin`,
   never into `lessons` or `procedures`.
5. **Add the acceptance gate** with `review_kind ∈ {human, frozen_key, external_signal}` and a reference.
   No reference, no insertion.
6. **Bound each cycle**: cap items changed, produce a diff, and make the whole cycle revertible in one
   command.
7. **Wire the three probes**: regression (the frozen suite), retention (re-ask after N sessions), transfer
   (a third document class). All three run after every cycle, and all three have pre-declared thresholds.
8. **Record the denominator** for every improvement claim, and the number of configurations compared.
9. **Only if** external-memory adaptation demonstrably plateaus *and* Q1 shows the hardware permits it,
   revisit fine-tuning — as a new decision with its own contract, not as a default.

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| Proposal via self-reflection | 2–3× LLM calls per trial (Self-Refine's own characterisation) | Cost per cycle, bounded by §7.8's cap |
| TextGrad-style "gradients" | Many LLM calls | Rejected partly on cost |
| Tree of Thoughts | Search multiplies calls per question | Rejected |
| DSPy / OPRO optimisation | Many calls per optimisation run | Must never touch held-out sources |
| ACE-style itemised growth | Light storage; LLM-call heavy to generate items | Append-only storage cost is trivial |
| PEFT / LoRA training | GPU + substantial RAM | Rejected; Q1 unanswered |
| Unsloth | CUDA GPU required | Rejected |
| Regression + retention + transfer probes | Three extra evaluation runs per cycle | The real cost of learning honestly — and the reason to bound cycles |
| smolagents | Very light | The agent loop is Python; the cost is in the model calls and the tool surface |

## 7. Qualification requirements

1. **Regression**: the frozen suite shows no degradation beyond a pre-declared tolerance after every
   learning cycle.
2. **Retention**: 20 previously answered items re-asked after 5 unrelated sessions show no decay beyond
   tolerance.
3. **Transfer**: a third document class, never used in tuning, shows no collapse.
4. Every accepted lesson names its `review_kind` and reference; a lesson without one cannot exist in the
   store (verified by a test that attempts it and must fail).
5. Every procedure records `scope_shown_to_work`, and fires only when its preconditions hold; a planted
   unmet-precondition case produces a recorded refusal, not a wrong action.
6. Every learning cycle is revertible individually, and the revert is demonstrated.
7. The number of items changed per cycle is at or below the declared cap.
8. Improvement claims report the attempted denominator and the number of configurations compared, with a
   correction applied when more than one configuration was compared.
9. No adaptation ever writes to `facts`, and no adaptation ever touches a trading, risk, approval, holding
   or open-position parameter.
10. The claim "the system learned" is supported by 1–3, **not** by a self-reported improvement.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Fine-tuning / LoRA / PEFT as the learning mechanism | Resource fit unknown (Q1); weights changing under a frozen evaluation destroys comparability; contamination risk. Revisit only on evidence and hardware |
| Unsloth | CUDA GPU required; vendor memory-reduction claims not reproduced |
| RL or reward-model training | No oracle, no budget, no authorisation |
| Tree of Thoughts / multi-agent debate | Cost multiplication without an evidence gate; agreement between models is not independent evidence |
| Self-Rewarding-style self-judgement | Directly violates §7.2 |
| LLM-driven consolidation of lessons (A-MEM, mem0, MemoryBank decay) | Rewriting or decaying records is what an auditable store must not do |
| Unbounded learning | An explicit non-goal; §7.8 caps every cycle |
| Claiming transfer from Voyager's Minecraft result | Different environment; analogy at most |
| Claiming learning from a public benchmark score | Benchmarks are contamination magnets and say nothing about unfamiliar trading documents — see [BENCHMARK_NOTES.md](../../resources/benchmark-descriptions/BENCHMARK_NOTES.md) |
| Optimising against held-out sources | The most common way an evaluation is silently destroyed; prohibited by [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §7 |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| Who or what performs independent review (a human? a frozen key? an external signal?) | Requirement 7.2 — the whole workstream | Ask the user; without an answer, learning cannot be demonstrated, only asserted |
| Retention and transfer thresholds | §7 items 2 and 3 | Pre-declare before the first cycle; inventing them afterwards invalidates the result |
| A third document class for transfer | §7 item 3 | Depends on Q4 (rights) and on the unknown document classes |
| Whether SAM-X has any existing adaptation mechanism | Step 1's inventory | Ask; inspect |
| ExpeL's upstream slug and licence | Citing or bundling more of it | Re-check upstream; metadata-only until a licence appears |
| The negative literature on self-correction without external feedback | §2.3's supporting citation | Its identifier was **not re-verified this session**; the design rule does not depend on it |
| Whether any published gain in this category replicates on document interpretation | The entire premise | Nobody has shown it; that is the gap. A bounded local experiment is the only way to find out |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
