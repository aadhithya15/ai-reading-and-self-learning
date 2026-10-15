# Workstream 04 — Semantic Interpretation of Unfamiliar Documents

**Objectives served:** interpret documents never seen before rather than recall benchmark answers;
recognise exceptions, partial constraints, unsupported claims, missing information and real contradictions;
**never invent setup parameters**; demonstrate transfer.

**Reported context:** the one frozen reader qualification scored **13/32 exact field judgments** and **0/4
fully correct cases**, and the candidate was rejected (R3 — reported). Reliable summaries and
unfamiliar-source interpretation are unfinished (R4). This workstream is where that number has to move, and
where the *reason* it is low has to be diagnosed rather than assumed.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 4.1 | A **typed extraction contract** per document class: field name, type, unit, allowed states, source-quote requirement | An untyped extraction is a guess with formatting |
| 4.2 | Four allowed states per field: `specified`, `partially_specified`, `absent_from_source`, `ambiguous` | "Useful partial information must be preserved without inventing the rest" |
| 4.3 | **Invented-parameter count = 0** as a hard acceptance criterion | One invented parameter can invalidate a whole research result |
| 4.4 | A library default may be recorded as a **hypothesis**, never as a parameter | Defaults are the most common source of invented values |
| 4.5 | Exceptions and carve-outs reported **with** the rule they qualify | A rule without its exception is a different rule |
| 4.6 | Genuine contradictions distinguished from scope/version differences | Two true facts with non-overlapping validity are not a contradiction |
| 4.7 | Unsupported interpretation distinguished from genuine absence | Two different outcomes, both testable, requiring different responses |
| 4.8 | Every extracted value carries its **exact quote, page and document version** | Traceability is what makes the rest auditable |
| 4.9 | Interpretation quality measured **separately from** extraction coverage | A missing page that causes a wrong answer is a data problem, not a comprehension problem |

### 1.1 The eight confusions

These are the specific, testable failure modes this workstream exists to prevent. Each becomes an item kind
in the evaluation set (see [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §4).

| # | Confusion | Correct behaviour |
|---|---|---|
| C1 | A **dataset description** read as a **trading rule** | "This dataset contains daily bars" is not "trade daily" |
| C2 | A **sampling frequency** read as an **execution timeframe** | Data granularity ≠ order frequency |
| C3 | A **benchmark date or backtest window** read as a **holding period** | The evaluation window is not a position duration |
| C4 | An **action vocabulary** read as a **signal** | "The agent may buy, sell or hold" is not "buy now" |
| C5 | An **indicator name** read as a **parameter setting** | "uses RSI" does not specify RSI(14) |
| C6 | A **partial constraint** read as a **complete specification** | "at least 20 bars" does not mean "exactly 20 bars" |
| C7 | An **unsupported interpretation** conflated with **genuine absence** | "The source does not say" and "I inferred X" are different answers |
| C8 | A **scope or version difference** read as a **contradiction** | Two documents can both be right about different things |

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: typed contract + four states + evidence-bound output

Define, per document class, a schema (pydantic or an equivalent typed structure) in which every field
declares its type, unit and allowed states, and in which a `specified` value **cannot be constructed
without** an accompanying quote, page and document version. Make `partially_specified` a first-class output
that carries what *is* known. Make `absent_from_source` and `ambiguous` distinct.

This is deliberately boring. It is also the only approach in the shortlist that makes requirement 4.3
*structurally* true rather than behaviourally hoped for.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| Prompt-only discipline ("never invent parameters") | **Necessary but insufficient** | A prompt cannot be audited. A type can |
| Post-hoc validation of free-text answers | Adopt **in addition** | Quote-presence and entailment checks (workstream 05) catch inventions the contract missed |
| LLM-as-judge for interpretation quality | **Last layer only** | A model judging a model is not independent supervision; used for meaning, never as the acceptance gate |
| Public long-context benchmarks as evidence | **Rejected as qualification** | LongBench's average English length is 6 711 words (**verified** metadata) — it does not test a 147-page scale at all. See [BENCHMARK_NOTES.md](../../resources/benchmark-descriptions/BENCHMARK_NOTES.md) |
| Fine-tuning a model to interpret better | **Rejected** | Laptop resource fit unknown (Q1); weights changing under a frozen evaluation destroys comparability; contamination becomes harder to rule out |
| Tree-of-Thoughts / multi-agent debate | **Rejected** | Multiplies token cost and RAM per question, and produces more confident wrong answers when no evidence gate exists |
| `vectara-answer` / HHEM hallucination evaluator | Catalogued | A useful *concept* (score answer-support), but it is a Streamlit app plus an optional local evaluator model, and it is model-judged |
| `long-form-factuality` (SAFE / LongFact) | Adopt the **decomposition idea** | Composite licence (Apache-2.0 per directory + MIT for `factscore`), scoped in the manifest. Its decomposition of a long answer into individually checkable claims is exactly right; its SAFE rater is a hosted model judging a model |
| `inspect_ai` | Adopt as the **runner** | MIT; token/cost/turn limits and explicit error handling are documented in the bundled files — the limit machinery is what makes a resource-bounded interpretation test expressible |

### 2.3 What the benchmark literature actually contributes

The bundled and catalogued benchmark evidence is used for **design lessons**, not for qualification:

* **RULER** (arXiv:2404.06654v3, **verified** metadata; Apache-2.0 generators bundled) — near-perfect
  vanilla needle-in-a-haystack scores coexist with sharp degradation as length and task complexity grow; of
  models claiming ≥32K context, only about half held up at 32K. *Lesson: test multi-hop, aggregation and
  position, not retrieval success.*
* **Lost in the Middle** (arXiv:2307.03172v3, **verified**) — evidence position changes accuracy.
  *Lesson: sweep the position of the evidence and report the curve.*
* **Same Task, More Tokens** (arXiv:2402.14848v2, ACL 2024, **verified**) — performance degrades with
  context length even at fixed task difficulty. *Lesson: length is an independent variable, not a nuisance.*
* **FILM / IN2 training** (arXiv:2404.16811v2, **verified**) — 4K–32K synthetic QA training repairs
  lost-in-the-middle on Mistral-7B. *Lesson: synthetic item generation is a legitimate tool — and a warning
  that a model's behaviour may already have been shaped by synthetic data.*
* **LongBench** (arXiv:2308.14508v2, **verified**) — retrieval helps weak long-context models and lags
  strong ones; average English length 6 711 words. *Lesson: scale mismatch with SAM-X's 147 pages.*
* **NovelQA** (arXiv:2403.12766v3, ICLR 2025, **verified**) — >200K-token copyrighted novels.
  *Lesson: long-narrative QA is a real construct; the corpus is not redistributable, so it is metadata-only.*
* **∞Bench** (arXiv:2402.13718v3, **verified**) — 100K+ token tasks; harness and scorers bundled (MIT).

Two identifiers commonly cited in this area were checked and found **wrong**: `2409.12181` is *not* HELMET,
and `2105.07538` is *not* the conformal-prediction introduction (it is a VAR anomaly-detection paper,
relevant to workstream 10). HELMET's arXiv identifier remains **unverified** and is recorded as such (MO-08);
its MIT-licensed repository code is bundled instead.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `inspect_ai` (MIT) | [documentation](../../resources/documentation/inspect_ai/) — including `docs/_cost_limits.md`, `_token_limits.md`, `_turn_limits.md`, `_setting_max_samples.md`, `AGENTS.md`, `SECURITY.md`, `CHANGELOG.md` · [licence](../../resources/licenses/inspect_ai/) |
| `ruler` (Apache-2.0) | [documentation](../../resources/documentation/ruler/) · [task configs](../../resources/configurations/ruler/) — `synthetic.yaml`, `config_tasks.sh`, `config_models.sh` · [licence](../../resources/licenses/ruler/) |
| `tiktoken` (MIT) | [registry metadata](../../resources/documentation/_pypi-metadata/) — exact token counts for every assembled context |
| `camelot` (MIT) | [documentation](../../resources/documentation/camelot/) — table extraction, shared with workstream 03 |
| `helmet` (MIT) | [benchmark description](../../resources/benchmark-descriptions/helmet/) · [harness code](../../resources/code-examples/helmet/) — `data.py`, `eval.py`, `arguments.py`, `model_utils.py` · [changelog](../../resources/documentation/helmet/) · [licence](../../resources/licenses/helmet/) |
| `longbench` (MIT) | [benchmark description](../../resources/benchmark-descriptions/longbench/) · [harness code](../../resources/code-examples/longbench/) — `pred.py`, `result.py` · [requirements](../../resources/documentation/longbench/) · [licence](../../resources/licenses/longbench/) |
| `infinitebench` (MIT) | [benchmark description](../../resources/benchmark-descriptions/infinitebench/) · [scorers](../../resources/code-examples/infinitebench/) — `src/compute_scores.py`, `src/prompt.py`, `src/args.py` · [licence](../../resources/licenses/infinitebench/) |
| `niah` (MIT) | [benchmark description](../../resources/benchmark-descriptions/niah/) · [code](../../resources/code-examples/niah/) · [licence](../../resources/licenses/niah/) — **its Paul Graham essay haystack was deliberately NOT collected** (copyright, and unnecessary) |
| `long-form-factuality` | [documentation](../../resources/documentation/long-form-factuality/) — `eval/README.md`, `longfact/README.md`, `requirements.txt` · [scoped licence](../../resources/licenses/long-form-factuality/) |
| `vectara-answer` (Apache-2.0) | [documentation](../../resources/documentation/vectara-answer/) · [licence](../../resources/licenses/vectara-answer/) — dormant since 2025-05 |
| `docling` (MIT) | [documentation](../../resources/documentation/docling/) — `docs/concepts/docling_document.md` is a useful typed-document model · [licence](../../resources/licenses/docling/) |
| `novelqa` | **Not bundled** — metadata-only catalog row; long-narrative QA over copyrighted novels |
| `multihop-rag` | **Not bundled** — no upstream licence file exists. See [_metadata-only record](../../resources/documentation/_metadata-only/multihop-rag.md) |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) — metadata-only, identifiers labelled verified or unverified |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| Inspect AI | https://github.com/UKGovernmentBEIS/inspect_ai · https://inspect.aisi.org.uk/ |
| RULER | https://github.com/NVIDIA/RULER (**moved from `hsiehjackson/RULER`**) |
| tiktoken | https://github.com/openai/tiktoken |
| HELMET | https://github.com/princeton-nlp/HELMET — **paper identifier unverified (MO-08)** |
| LongBench | https://github.com/THUDM/LongBench · arXiv:2308.14508v2 (**verified**) |
| ∞Bench | https://github.com/OpenBMB/InfiniteBench · arXiv:2402.13718v3 (**verified**) |
| Needle-in-a-Haystack | https://github.com/gkamradt/needle-in-a-haystack (**corrected from `gregkamradt/`**) |
| Long-form factuality / SAFE | https://github.com/google-deepmind/long-form-factuality |
| Vectara Answer | https://github.com/vectara/vectara-answer |
| NovelQA | https://github.com/NovelQA/novelqa (**slug did not resolve via the API on 2026-10-14**) |
| MultiHop-RAG | https://github.com/yixuantt/MultiHop-Rag · arXiv:2401.15391v1 (**verified**) — **no licence; nothing bundled** |

## 5. Adoption steps

1. **Diagnose R3 before trying to beat it.** Re-score the recorded 13/32 outputs under the frozen protocol
   ([roadmap](../../IMPLEMENTATION_ROADMAP.md) Phase 1) and classify each failure against C1–C8 and the four
   field states. If the failures cluster in one confusion, that is the whole project for a while.
2. **Write the typed contract** for the actual document class (unknown today — see §9). One field at a time:
   name, type, unit, allowed states, quote requirement.
3. **Make `specified` unconstructable without evidence.** The type system, not a prompt, enforces 4.3.
4. **Implement the four states**, including `partially_specified` carrying what *is* known, and
   `absent_from_source` distinct from `ambiguous`.
5. **Add the eight confusion items** to the evaluation set as their own category, with expected behaviours
   pre-declared.
6. **Bind every value to quote + page + document version**, and check quote-presence deterministically
   (workstream 05).
7. **Sweep evidence position and context length** using the bundled RULER generators over text the project
   owns the rights to. Report the curve, not a point.
8. **Score abstention and the attempted denominator** from day one, so the metric cannot be gamed later.
9. **Build the transfer set** — a different document class, never tuned on — before claiming any
   interpretation capability (R4 says transfer is unfinished; this is how it becomes finished or refuted).

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| Typed contract + validation | Negligible | Pure CPU, proportional to fields |
| Quote-presence checks | Negligible | String search against stored page text |
| Entailment checks | One small local NLI model, or rule-based | Weights are an approval gate; rules are the fallback |
| RULER item generation | Light — generators are scripts | The **evaluated model** dominates cost, not the generator |
| 32K-token contexts | Model-dependent, potentially large | llama.cpp KV cache grows with context length independently of weight size |
| 128K-token contexts | Likely infeasible on the reported machine | Q1–Q3 decide; the experiment must declare the lengths it will actually run |
| Model-judged scoring | API cost or local VRAM | Never the sole acceptance gate, so its cost is bounded by design |
| Inspect AI parallelism | Configurable | `docs/_setting_max_samples.md` and the limit docs are bundled precisely so this can be capped |

## 7. Qualification requirements

1. **Invented-parameter count = 0.** One invention fails the run regardless of every other score.
2. Every `specified` value resolves to a quote that is literally present on the cited page of the cited
   document version.
3. `absent_from_source` correctly identified on items where the information is genuinely absent, at a
   pre-declared rate.
4. `partially_specified` correctly identified **and** the partial information preserved, not discarded and
   not completed.
5. `ambiguous` distinguished from `absent_from_source` at a pre-declared rate.
6. Each of C1–C8 measured separately, with its own denominator and interval.
7. Position-sensitivity and length-sensitivity curves reported, not single points.
8. Abstention scored, and the attempted denominator reported next to every rate.
9. **Transfer**: a previously unexposed document class scored separately, with no collapse.
10. **Retention**: previously answered items re-asked after unrelated sessions, with no decay beyond
    tolerance.
11. Contamination checked per item: model training cutoff versus item creation date versus source
    publication date.

A score on a public benchmark does not satisfy any of these. See
[BENCHMARK_NOTES.md](../../resources/benchmark-descriptions/BENCHMARK_NOTES.md).

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Prompt-only "do not invent parameters" | Unauditable; requirement 4.3 must be structural |
| Public leaderboards (HELM scenarios, lm-evaluation-harness tasks, LongBench/∞Bench/NovelQA data) as qualification | Scale mismatch, contamination risk, scarce RAM, and they say nothing about unfamiliar trading documents. Harnesses, scorers and report shapes adopted; scenarios not run |
| Vanilla needle-in-a-haystack as a qualification | RULER (**verified**) shows near-perfect NIAH coexisting with sharp degradation on complex tasks |
| MultiHop-RAG | No upstream licence file → no redistribution right; three downloaded files were deleted during the audit. RULER's `variable_tracking.py` + `qa.py` produce the same multi-hop construct lawfully |
| Fine-tuning or RL as the interpretation mechanism | Resource fit unknown; destroys evaluation comparability; contamination risk. Learning is pursued through external memory (workstream 07) |
| Tree-of-Thoughts, multi-agent debate | Cost and RAM multiplication without an evidence gate; agreement between models is not independent evidence |
| LLM-as-judge as the acceptance gate | Not independent supervision |
| Claiming interpretation capability from extraction coverage | Requirement 4.9 exists to prevent it |
| Asserting HELMET's commonly cited arXiv identifier | Checked and **disproved**; recorded as unverified (MO-08) rather than repeated |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **The document classes are unknown** | The typed contract cannot be written | Ask the user; inspect the two indexed documents once rights are confirmed (Q4) |
| Whether R3's items and key were frozen before outputs (Q6) | Whether 13/32 is a usable baseline at all | Ask; if not, Phase 1 must build a new baseline and every comparison to R3 is void |
| Whether R3's scorer still exists | Re-scoring the recorded outputs | Ask; if lost, the outputs must be re-scored from scratch under the new protocol |
| HELMET's arXiv identifier | Citing the paper | Re-derive from the repository README; re-query the arXiv API in batches of ≤ 6 ids |
| 46 further arXiv identifiers used as leads | Citing them | Same; until then they are labelled *not re-verified this session* |
| No entailment model chosen | Requirement 4.7's automated check | Needs a weights-download approval, or a rule-based gate first |
| Whether summaries are currently cited as evidence (Q7) | How urgent the fact/hypothesis split is | Ask; inspect the existing answer path |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
| No result in this workstream is evidence about trading performance | Any claim of profitability | Nothing in this collection is, and none should be read as one |
