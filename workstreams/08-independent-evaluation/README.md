# Workstream 08 — Independent, Reproducible Evaluation

**Objectives served:** demonstrate transfer and retention; recognise unsupported claims; never overfit to
benchmarks; make every claim traceable.

**The full protocol lives in [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md).** This README covers the
tooling, the evidence about the tools, and what each one is and is not for. If you read one file about
evaluation, read that one.

**Reported context this workstream exists for:** one frozen reader qualification scored **13/32 exact field
judgments** and **0/4 fully correct cases**; the candidate was rejected (R3 — **reported**). That number is
only a baseline if the items and key were frozen before the candidate produced outputs, the scorer still
exists, and the evaluator was independent. **Nobody knows whether those conditions held** — that is question
Q6, and Phase 1 of the roadmap exists to resolve it by re-scoring the recorded outputs under the frozen
protocol.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 8.1 | Candidate, items, keys, scorer and config **frozen by hash before any output exists** | Otherwise every future number is incomparable |
| 8.2 | Evaluator **separate** from candidate: separate process, config and credentials | A model judging a model is not independent supervision |
| 8.3 | **Immutable, append-only logs**; a re-run gets a new run id | Overwriting is how failures disappear |
| 8.4 | **Layered scoring**: deterministic → entailment → model judge, cheapest and most objective first | A judge is the most expensive and least reliable layer |
| 8.5 | **Abstention scored**, and the **attempted denominator** published next to every rate | Otherwise the system optimises into guessing, or into abstaining to inflate accuracy |
| 8.6 | **Failures preserved verbatim**, with reasons | A rejected candidate is a result; a lost failure is a wasted experiment |
| 8.7 | **Negative cases** pre-declared: missing info, partial constraints, exceptions, contradictions, stale sources, unanswerable queries, hostile content, resource exhaustion | Objective 4 cannot be measured without them |
| 8.8 | **Regression, retention and transfer** suites, all frozen | Objective 7 |
| 8.9 | **Contamination checked per item**, not assumed | Public benchmarks and 2023–24 datasets are in training corpora |
| 8.10 | **Held-out sources and keys never committed** to this repository | Publishing a key destroys it |
| 8.11 | Resource measurement **out-of-process** | A candidate must not self-report its own footprint |
| 8.12 | Test kinds never conflated: mechanical / synthetic fixture / source-based qualification / deployment proof | A passing mechanical test is not a qualification |

**Not a goal.** A high score. The goal is a number that a second operator can regenerate bit-for-bit and
that survives being disagreed with.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: a frozen protocol, with the lightest runner that can enforce it

Two acceptable runners, in order of preference:

1. **Hand-rolled, ~150 lines**: JSONL items → candidate → JSONL outputs → scorer → write-once results
   directory. Zero dependencies, fully auditable, and every requirement in §1 is expressible.
2. **Inspect AI** (MIT, UK AI Safety Institute): adopt if its concepts map cleanly onto the existing
   environment. Its bundled documentation covers eval sets, solvers, scorers, an append-only `.eval` log
   format, a log viewer, explicit error and limit handling, parallelism, caching and datasets. The **limit
   machinery** (`docs/_token_limits.md`, `_cost_limits.md`, `_turn_limits.md`, `_setting_max_samples.md`) is
   the specific reason it is worth considering: it makes a resource-bounded evaluation *expressible* rather
   than merely hoped for.

Scoring layers, in order:

| Layer | Instrument | What it decides |
|---|---|---|
| Deterministic | Exact-field match with a **written, frozen normalisation rule**; quote-presence | Correctness, and whether a citation is fabricated |
| Entailment | Small local NLI model, or rules | Whether the cited passage actually **supports** the claim |
| Model judge | Recorded judge model, prompt, version, temperature | Meaning and adequacy only — **never** the acceptance gate |

Metric *definitions* come from Hugging Face Evaluate (Apache-2.0) — in particular `exact_match`, whose
normalisation options are exactly where scores silently change. Assertion *vocabulary* comes from promptfoo
(MIT). Report *shape* comes from HELM (Apache-2.0): metrics × scenarios × models shown together, including
efficiency, rather than one accuracy number. **Decontamination practice** comes from
lm-evaluation-harness (MIT).

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **Ragas**, **DeepEval**, **TruLens** | **Metric vocabulary only** | All three are LLM-judged and therefore not independent supervision. Neither Ragas nor DeepEval was run during this build. TruLens adds an optional dashboard/server |
| **HELM scenarios** | **Not run** | Full runs are cluster-scale; scenarios say nothing about unfamiliar trading documents; contamination risk. The reporting format is adopted |
| **lm-evaluation-harness tasks** | **Not run** | Model inference dominates cost; same objections. Its **decontamination** documentation is adopted |
| **LongBench / ∞Bench / NovelQA / AgentBench / NIAH** | **Harnesses and scorers adopted; data not run** | LongBench's average English length is 6 711 words (**verified** metadata) — it does not test a 147-page scale. See [BENCHMARK_NOTES.md](../../resources/benchmark-descriptions/BENCHMARK_NOTES.md) |
| **RULER generators** | **Adopted as the item source** | Apache-2.0 code that *generates* tasks locally from any haystack: NIAH variants, variable tracking (multi-hop), QA, common-words and frequent-words extraction. Re-seedable, auditable, leakage-resistant, no dataset download |
| **HELMET** | Harness code adopted; **paper identifier unverified** | arXiv `2409.12181` was queried and resolved to a *different* paper, so the commonly cited HELMET identifier is **not confirmed** (MO-08). Its MIT-licensed `data.py`, `eval.py`, `arguments.py`, `model_utils.py` are bundled |
| **MultiHop-RAG** | **Rejected** | No upstream licence file → no redistribution right. Three files downloaded in an early pass were deleted during the audit; RULER's generators provide the same multi-hop construct lawfully |
| **`long-form-factuality` (SAFE)** | Decomposition adopted | Splitting a long answer into individually checkable claims is exactly right. Its SAFE rater is a **hosted model judging a model**; composite licence, scoped in the manifest |
| **`vectara-answer` / HHEM** | Concept noted | Answer-support scoring is useful; a Streamlit app plus an optional local evaluator model is not a lightweight dependency, and it is model-judged |
| **Google Uncertainty Baselines** | Reference only | TensorFlow/JAX research-grade implementations; heavy, and aimed at model uncertainty rather than document interpretation |
| **`garak`** | Adopt for the **adversarial probe set**, not for scoring | Apache-2.0 LLM vulnerability scanner; probes a target model with many payloads. Belongs to workstream 14's threat testing, and needs approval to run against any model |
| **MAPIE** | Adopted for **interval reporting** | BSD-3, sklearn-compatible conformal prediction. Gives the pre-declared thresholds a defensible interval instead of a guess. Its cost is repeated fits |
| **Qlib** | Adopted for **reproducibility of the research workflow** | MIT; its 13 bundled `workflow_config_*.yaml` files are the clearest example of pinning every research decision in one artefact. Its data server and workflow engine are sized for research clusters |
| **`ml4t`** | Adopted for **statistical honesty** | MIT scripts bundled for multiple testing, IC inference, signal evaluation, labelling and MFE/MAE. The multiple-testing discipline applies to evaluations as much as to backtests |
| **`pandera`** | Adopted for **item and output schema validation** | MIT, in-process; a malformed item file should fail loudly before a run, not silently during scoring |
| **DVC** | Not adopted | Ownership changed during the check window; a sha256 manifest covers the need |
| **`memory_profiler`** | Not adopted | Unmaintained since 2022-10-19; `psutil` sampling out-of-process is the requirement (8.11) |
| **DSPy metrics** | Vocabulary noted | Its metric abstraction is a clean way to express layered scoring; its optimisers must never touch held-out sources |

### 2.3 Why "independent" is harder than it sounds

For a one-person project the roles in [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §2 (item author,
candidate owner, scorer, reviewer, resource monitor) collapse onto one human or one agent. That does not
make independence impossible, but it does mean it must be **separated in time and recorded as such**: author
and freeze items on day 1; run the candidate on day 2 without re-reading the key; score on day 3. The
limitation is stated in the report rather than hidden. An AI evaluating another AI is better than
self-evaluation and worse than qualified human review — both facts are recorded, and neither is called
certification.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `inspect_ai` (MIT) | [documentation](../../resources/documentation/inspect_ai/) — README, `AGENTS.md`, `SECURITY.md`, `CHANGELOG.md`, `_cost_limits.md`, `_token_limits.md`, `_turn_limits.md`, `_setting_max_samples.md`, `_tools-annotations-required.md` · [licence](../../resources/licenses/inspect_ai/) |
| `ruler` (Apache-2.0) | [documentation](../../resources/documentation/ruler/) · [task and model configs](../../resources/configurations/ruler/) · [licence](../../resources/licenses/ruler/) — generator scripts live under [code examples](../../resources/code-examples/) |
| `hf-evaluate` (Apache-2.0) | [documentation](../../resources/documentation/hf-evaluate/) — including `considerations.md` on metric misuse · [licence](../../resources/licenses/hf-evaluate/) |
| `promptfoo` (MIT) | [documentation](../../resources/documentation/promptfoo/) · [licence](../../resources/licenses/promptfoo/) |
| `helm` (Apache-2.0) | [documentation](../../resources/documentation/helm/) · [licence](../../resources/licenses/helm/) (**slug corrected from `stanfordfordlp/helm` to `stanford-crfm/helm`**) |
| `lm-eval-harness` (MIT) | [documentation](../../resources/documentation/lm-eval-harness/) — including the decontamination notes · [licence](../../resources/licenses/lm-eval-harness/) |
| `helmet` (MIT) | [benchmark description](../../resources/benchmark-descriptions/helmet/) · [harness code](../../resources/code-examples/helmet/) · [changelog](../../resources/documentation/helmet/) · [licence](../../resources/licenses/helmet/) |
| `longbench` (MIT) | [benchmark description](../../resources/benchmark-descriptions/longbench/) · [harness code](../../resources/code-examples/longbench/) · [licence](../../resources/licenses/longbench/) |
| `infinitebench` (MIT) | [benchmark description](../../resources/benchmark-descriptions/infinitebench/) · [scorers](../../resources/code-examples/infinitebench/) · [licence](../../resources/licenses/infinitebench/) |
| `agentbench` (Apache-2.0) | [benchmark description](../../resources/benchmark-descriptions/agentbench/) · [documentation](../../resources/documentation/agentbench/) — including `docs/Config_en.md` · [licence](../../resources/licenses/agentbench/) |
| `niah` (MIT) | [benchmark description](../../resources/benchmark-descriptions/niah/) · [code](../../resources/code-examples/niah/) · [licence](../../resources/licenses/niah/) |
| `long-form-factuality` | [documentation](../../resources/documentation/long-form-factuality/) · [scoped licence](../../resources/licenses/long-form-factuality/) |
| `mapie` (BSD-3) | [documentation](../../resources/documentation/mapie/) · [licence](../../resources/licenses/mapie/) |
| `ml4t` (MIT) | [code examples](../../resources/code-examples/ml4t/) · [documentation](../../resources/documentation/ml4t/) · [licence](../../resources/licenses/ml4t/) |
| `qlib` (MIT) | [workflow configs](../../resources/configurations/qlib/) · [documentation](../../resources/documentation/qlib/) |
| `pandera` (MIT) | [documentation](../../resources/documentation/pandera/) · [licence](../../resources/licenses/pandera/) |
| `ragas`, `deepeval`, `trulens` | [RAGAS](../../resources/documentation/ragas/) · [DeepEval](../../resources/documentation/deepeval/) · [TruLens](../../resources/documentation/trulens/) — metric vocabulary only |
| `vectara-answer`, `uncertainty-baselines` | [Vectara Answer](../../resources/documentation/vectara-answer/) · [Uncertainty Baselines](../../resources/documentation/uncertainty-baselines/) |
| `garak` (Apache-2.0) | [documentation](../../resources/documentation/garak/) · [code examples](../../resources/code-examples/garak/) · [licence](../../resources/licenses/garak/) |
| `tuning-playbook` (CC BY 4.0) | [full text](../../resources/documentation/tuning-playbook/) — its evaluation-first chapters are the closest thing to a redistributable textbook here |
| `novelqa`, `multihop-rag`, `nuster-survey` | **Not bundled** — metadata-only rows. MultiHop-RAG: no upstream licence. See [_metadata-only record](../../resources/documentation/_metadata-only/multihop-rag.md) |
| Templates | [experiment-contract.md](../../templates/experiment-contract.md) · [evaluation-report.md](../../templates/evaluation-report.md) · [component-assessment.md](../../templates/component-assessment.md) · [source-provenance.json](../../templates/source-provenance.json) |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) — RULER, LongBench, ∞Bench, NovelQA, ALCE, ARES, RAGTruth, FILM/IN2, Lost in the Middle, Same Task More Tokens |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| Inspect AI | https://github.com/UKGovernmentBEIS/inspect_ai · https://inspect.aisi.org.uk/ |
| RULER | https://github.com/NVIDIA/RULER · arXiv:2404.06654v3 (**verified**) |
| HF Evaluate | https://github.com/huggingface/evaluate |
| promptfoo | https://github.com/promptfoo/promptfoo · https://promptfoo.dev/ (**unreachable for download from the build sandbox**) |
| HELM | https://github.com/stanford-crfm/helm |
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness |
| HELMET | https://github.com/princeton-nlp/HELMET — **paper identifier unverified (MO-08)** |
| LongBench | https://github.com/THUDM/LongBench · arXiv:2308.14508v2 (**verified**) |
| ∞Bench | https://github.com/OpenBMB/InfiniteBench · arXiv:2402.13718v3 (**verified**) |
| AgentBench | https://github.com/THUDM/AgentBench |
| NovelQA | https://github.com/NovelQA/novelqa · arXiv:2403.12766v3 (**verified**) — corpus not redistributable |
| Long-form factuality | https://github.com/google-deepmind/long-form-factuality |
| MAPIE | https://github.com/scikit-learn-contrib/MAPIE |
| ml4t | https://github.com/stefan-jansen/machine-learning-for-trading |
| Qlib | https://github.com/microsoft/qlib |
| garak | https://github.com/NVIDIA/garak |
| Tuning Playbook | https://github.com/google-research/tuning_playbook |
| ALCE / ARES / RAGTruth | arXiv:2305.14627v2 · arXiv:2311.09476v2 · arXiv:2401.00396v2 (all **verified**) |

## 5. Adoption steps

1. **Write the contract before anything else**, using
   [experiment-contract.md](../../templates/experiment-contract.md). Freeze candidate, items, key hash,
   scorer and budget.
2. **Re-score the recorded R3 outputs** under the frozen protocol **without re-running the candidate**. If
   13/32 is not reproduced, the difference is the most informative finding available and must be known
   before any improvement is claimed.
3. **Prepare the held-out source set** per [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §3: at least one
   document class the candidate has never seen, rights confirmed (Q4), provenance recorded with
   [source-provenance.json](../../templates/source-provenance.json), keys stored outside the repository.
4. **Generate mechanical items locally** with the bundled RULER generators over text the project owns the
   rights to. Fresh seed → fresh items → nothing that could have been in a training corpus.
5. **Implement layered scoring**: deterministic exact-field match with a written normalisation rule;
   quote-presence; entailment; optional judge with everything recorded.
6. **Add abstention scoring and the attempted denominator** from the first run.
7. **Add the negative-case suite** (8.7) and the regression/retention/transfer suites (8.8).
8. **Add out-of-process resource sampling** (8.11) and write the trace into the run directory.
9. **Make the run directory write-once**; a re-run creates a new run id and an overwrite attempt fails
   loudly.
10. **Run the leakage checklist** ([EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §7) before every reported
    evaluation.
11. **Report** with [evaluation-report.md](../../templates/evaluation-report.md), including §8 (test kind
    per result) and §9 (what was **not** tested).

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| Hand-rolled runner | Negligible | The candidate's inference dominates everything |
| Inspect AI | Python framework; parallelism configurable | RAM depends on the model backend, not the framework |
| RULER generators | Light scripts | The **evaluated model** dominates; 128K-token runs may be infeasible on the reported machine (Q1–Q3) |
| Deterministic scoring | Negligible | String and field comparison |
| Entailment scoring | One small local NLI model, or rules | Weights are an approval gate |
| Model-judge scoring | API cost or local VRAM, per item | Bounded by never being the acceptance gate |
| HELM / lm-eval full runs | **Cluster-scale** | The reason their scenarios are not run |
| ∞Bench / LongBench data runs | 100K+ token contexts are RAM- and time-heavy | Data not downloaded in any case |
| MAPIE conformal intervals | Repeated fits | Cheap at evaluation scale; declare the coverage level up front |
| Immutable logs and traces | Disk, growing per run | Rotate the resource traces, never the failures |

## 7. Qualification requirements

An evaluation setup is qualified when **all** of the following hold:

1. A clean re-run reproduces **every** score bit-for-bit from the recorded candidate id, item hash, key
   hash, scorer version and config hash.
2. The log is append-only: an attempted overwrite fails loudly and is recorded.
3. Every failure case is retrievable by item id, verbatim.
4. Evaluator and candidate are separate processes with separate configs (and separate credentials if
   hosted), verified by inspection.
5. No held-out item, and no text derived from a held-out source, appears in any prompt, few-shot example,
   cache or tuning trace — checked, not assumed.
6. Every item records the candidate model's training cutoff versus the item's creation date and the
   source's publication date; `contamination-risk` items are reported separately.
7. Abstention is scored, and the attempted denominator is published next to every rate.
8. Resource figures come from an out-of-process sampler, with the sampler's version and interval recorded.
9. Each result is labelled with its test kind (mechanical / synthetic fixture / source-based qualification /
   deployment proof). **No result here is a deployment proof.**
10. The number of configurations compared is recorded, and a correction is applied when it exceeds one.
11. The verdict is decided against criteria that were written **before** the run.
12. Held-out sources and keys are not present anywhere in this repository — verified by
    `scripts/validate_catalog.py`'s secret scan and by inspection.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Running public leaderboards as qualification | Scale mismatch, contamination risk, cluster-scale cost, and they say nothing about unfamiliar trading documents |
| MultiHop-RAG | No upstream licence; files deleted during the audit |
| NovelQA corpus | Copyrighted novels; metadata-only |
| arXiv paper PDFs as evaluation material | Not redistributable, and not downloadable from the sandbox |
| LLM-as-judge as the acceptance gate | Not independent supervision; also the most expensive layer |
| Ragas / DeepEval / TruLens scores as acceptance criteria | Model-judged; vocabulary adopted, scores not |
| Self-reported resource usage | Requirement 8.11 |
| Re-running a candidate after seeing failures and reporting the better number | That is a new candidate; the run id and the contract enforce it |
| Overwriting a run directory | Requirement 8.3 |
| Publishing keys or protected questions | Requirement 8.10 — only templates and hashes are published |
| Reporting accuracy without the attempted denominator | Requirement 8.5 |
| Treating a passing mechanical test as a qualification | Requirement 8.12 |
| Claiming that an AI evaluation is human-independent certification | It is better than self-evaluation and worse than qualified human review; both facts are recorded |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| Whether R3's items and key were frozen before outputs (Q6) | Whether 13/32 is a baseline at all | Ask. If not, Phase 1 must build a new baseline and every comparison to R3 is void |
| Whether R3's scorer and raw outputs still exist | Step 2 | Ask; if lost, the outputs cannot be re-scored and a new run is required |
| Rights over any candidate held-out document (Q4) | Step 3 — the whole held-out set | Question for the user; this is the most likely schedule blocker |
| The document classes to evaluate against | Item authoring | Unknown; ask (also workstreams 03 and 04 §9) |
| Whether Inspect AI fits the existing Python environment | Runner choice | A dependency/version check — requires install authorisation this engagement did not have |
| No entailment model chosen | The second scoring layer | Approve weights, or ship the rule-based gate first and label it |
| Acceptance thresholds for every metric | §5 step 1 | Must come from the project's own risk tolerance; inventing them here would itself be an invented parameter |
| HELMET's arXiv identifier (MO-08) | Citing the paper | Re-derive from the repository README; re-query arXiv in batches of ≤ 6 ids |
| Who performs independent review, in a one-person project | Requirement 8.2 | Temporal separation plus a recorded statement of the limitation |
| Nothing here was executed | All of it | Requires authorisation this engagement did not have |
