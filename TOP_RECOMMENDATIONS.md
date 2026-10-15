# TOP RECOMMENDATIONS

Five opportunities, ranked by **usefulness → evidence → resource fit → integration burden → risk**.

Ranking rule applied throughout: *prefer the smallest compatible change that makes a failure impossible
or visible, over the largest change that makes a success more likely.* Where a simpler alternative would
have been sufficient, it is recommended instead and the complex option is explicitly rejected — see
[REJECTED_OPTIONS.md](REJECTED_OPTIONS.md).

Every recommendation below shares three properties:

* **Permissively licensed or licence-verified** primary material is already bundled, pinned to a commit.
* **No model weights, no datasets, no servers, no paid services** are required to start.
* **Nothing was executed** during this build; each carries a bounded experiment that can reject it.

Evidence labels: **measured** · **verified** · **inspected** · **estimate** · **reported** · **proposed** ·
**unknown** (defined in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §5 and [START_HERE.md](START_HERE.md) §5).

---

## Rank 1 — Bounded-memory SQLite reading spine

**Workstreams:** [01](workstreams/01-low-ram/README.md) · [02](workstreams/02-data-storage/README.md) ·
[03](workstreams/03-document-reading/README.md) · [05](workstreams/05-retrieval-evidence/README.md)

**Components:** `diskcache` (Apache-2.0) · `sqlitedict` (Apache-2.0) · SQLite FTS5 (stdlib) ·
`sqlite-vec` (MIT/Apache-2.0) · `tiktoken` (MIT) · `psutil` (BSD-3) · `tenacity` (Apache-2.0)

### What it is

One SQLite file per document generation holding: the page map (page → byte range → heading path →
hash), extracted text per page, an FTS5 lexical index, optionally `sqlite-vec` embeddings, and a
`diskcache` spill tier for hot page objects. A `psutil`-measured budget enforces a resident ceiling and
`diskcache` evicts to disk when the ceiling is reached. Token counting via `tiktoken` makes every context
budget an exact number instead of a guess.

### The SAM-X problem it addresses

Reported position R4 says a disk-backed prototype already indexed 147 pages across two documents. This
recommendation is the **minimal generalisation of what already exists**: same storage engine, same
in-process model, plus the three things a reader needs and an index does not provide — a heading/page map
for navigation, an exact token budget, and an enforced resident-memory ceiling with defined spill
behaviour.

### Why the simpler alternatives are insufficient

| Simpler alternative | Why it is not enough |
|---|---|
| Keep everything in RAM dicts | Contradicts the reported RAM constraint; no defined behaviour when the ceiling is hit |
| Raw `sqlite3` only, hand-rolled | Fine, and it is the stated **fallback** — but you would re-implement eviction, sharding and atomic commits that `diskcache`/`sqlitedict` already provide under permissive licences |
| A vector database (Chroma/Qdrant/LanceDB) | Adds a process or a native format for a corpus of two documents; `sqlite-vec` is inside the same file and the same query language |
| DuckDB as the primary store | Excellent for analytical scans over bar history (workstream 02) but wrong shape for page-level random access with a hard memory ceiling; recommended *alongside*, not instead |

### Evidence status

* Licence texts read and bundled for every component (`resources/licenses/`). **verified**
* `diskcache` core/fanout/persistent implementation inspected (82 KB + 22 KB + 34 KB of Python). **inspected**
* `sqlite-vec` README and three examples inspected; version 0.1.9 at check date, dual MIT/Apache-2.0. **inspected**
* `psutil` docs inspected; actively pushed 2026-10-14. **inspected**
* RAM/latency behaviour on the actual machine: **unknown** — that is what the experiment measures.

### Bounded experiment (accept/reject)

* **Hypothesis.** A page-map + FTS5 + diskcache spine can answer "locate then reopen" queries over the
  147 already-indexed pages with peak resident memory under a declared ceiling, with no measurable
  accuracy loss against an all-in-RAM baseline.
* **Unchanged baseline.** The existing disk-backed prototype as-is, plus an all-in-RAM variant of the same
  logic. Both run on the same machine, same document set, same query order.
* **Comparable access/context/compute.** Identical inputs, identical query list, identical machine,
  identical Python; the only difference is the storage/spill layer. Any difference is stated in the report.
* **Evaluation sources.** The two already-indexed documents are **not** held-out (the system has seen
  them). A previously unexposed third document of the same class must be prepared per
  [EVALUATION_PLAN.md](EVALUATION_PLAN.md) §3 before any capability claim.
* **Frozen before outputs.** Query list, expected page ids, token budget, memory ceiling, and the
  scoring script — all committed before the first run.
* **Measurements.** Peak RSS and PSS (psutil), p50/p95 query latency, FTS5 vs `sqlite-vec` recall@5,
  cold-start time, on-disk size, and — critically — whether every returned answer resolves to a stored
  page whose text hash matches the source of record.
* **Pre-declared acceptance.** Peak RSS ≤ the declared ceiling on every run; 100% of returned answers
  resolve to a verifiable page; recall@5 ≥ the in-RAM baseline minus a declared tolerance; no query
  silently returns an unverified passage.
* **Pre-declared rejection.** Any run exceeds the ceiling without a recorded spill event; any answer
  cannot be resolved to a page; recall drops beyond tolerance; or the spill path makes p95 latency
  unusable (declared threshold).
* **Negative cases.** Corrupt/truncated page text; a page whose hash changed since indexing; a query whose
  answer spans a page boundary; a query for a page that was never extracted (scan, image-only); budget
  exhaustion mid-query; concurrent second reader on the same file.
* **Preserve.** The resource trace, every query/output pair, the FTS5 query strings, and all failures.

### Integration difficulty and fallback

**Low.** Pure Python plus one optional SQLite extension. No server, no network, no weights.
**Fallback:** raw `sqlite3` + a hand-written LRU with a disk spill (~150 lines). **Conservative
default:** run with `sqlite-vec` disabled and FTS5 only — lexical retrieval must be measured first anyway
(see Rank 5).

---

## Rank 2 — Locally regenerable long-context qualification harness (RULER-based) with a reopen-and-verify contract

**Workstreams:** [03](workstreams/03-document-reading/README.md) ·
[04](workstreams/04-semantic-interpretation/README.md) · [08](workstreams/08-independent-evaluation/README.md)

**Components:** `ruler` (Apache-2.0, generator code bundled) · `niah` (MIT, code only) ·
`longbench` harness configs (MIT) · `infinitebench` scorers (MIT) · `inspect_ai` (MIT) as the runner

### What it is

Build SAM-X's reader qualification from **code that generates tasks locally**, instead of downloading a
dataset. Bundled: `niah.py`, `variable_tracking.py`, `qa.py`, `common_words_extraction.py`,
`freq_words_extraction.py`, `constants.py`, `prepare.py`, `tokenizer.py`, `eval/evaluate.py`,
`synthetic.yaml` — all from `NVIDIA/RULER` at a pinned commit. Point the generators at text SAM-X already
has the rights to, add the reopen-and-verify contract, and you have a re-generable, auditable,
leakage-resistant qualification set.

### The SAM-X problem it addresses

R5 reports a rejected candidate at 13/32 exact field judgments and 0/4 fully correct cases. That is a
result, but with a 32-item denominator and no re-generable item source it cannot be compared to the next
candidate, and it cannot be extended without touching the original key. A generator-based harness makes
items **cheap to re-create, easy to hold out, and impossible to leak** (a fresh seed produces fresh
items).

### Why the simpler alternatives are insufficient

| Simpler alternative | Why it is not enough |
|---|---|
| Vanilla needle-in-a-haystack | **Verified evidence against it:** RULER (arXiv:2404.06654v3) reports near-perfect vanilla NIAH scores coexisting with large drops as length and task complexity grow; of models claiming ≥32K context, only about half held up at 32K. Passing NIAH is close to meaningless alone |
| Download LongBench / ∞Bench data | Data is Hugging Face-hosted (unreachable for download from the build sandbox) and a 2023–24 vintage benchmark is a contamination magnet. The **harness** configs are bundled; the data is not needed if items are generated locally |
| MultiHop-RAG | **No upstream licence file exists** → no redistribution right. Removed during the licence audit; see `resources/documentation/_metadata-only/multihop-rag.md`. RULER's `variable_tracking.py` + `qa.py` produce the same multi-hop construct lawfully |
| Write probes by hand | Reasonable for 10 items, but position/length sweeps need dozens; hand-written items are also harder to hold out from a future candidate |

### Evidence status

* Generator code read and bundled at a pinned commit. **inspected**
* RULER paper metadata verified via the arXiv API on 2026-10-14 (v3, COLM 2024). **verified**
* Licence: Apache-2.0. **verified**
* Whether the generators produce useful items **for SAM-X's document class**: **unknown** — that is the
  experiment. Synthetic tasks are engineering tests, never market-document comprehension.

### Bounded experiment

* **Hypothesis.** A frozen reader candidate's accuracy degrades predictably with context length and with
  the position of the evidence, and requiring reopen-and-verify removes unsupported answers at an
  acceptable latency cost.
* **Unchanged baseline.** The same candidate answering from summary context only, with no reopen step.
* **Comparable access/context/compute.** Identical model, identical tokenizer, identical token lengths
  (8k / 32k / 128k), identical machine; the only variable is the reopen-and-verify step.
* **Evaluation sources.** Haystack text from documents SAM-X owns the rights to, **not** from the two
  already-indexed documents (those are contaminated by prior exposure). Keys frozen before outputs.
* **Measurements.** Accuracy by task type and by evidence position; evidence completeness (is the cited
  passage actually on the cited page?); abstention rate; **attempted denominator** (accuracy over
  attempted items, reported alongside accuracy over all items); peak RSS; wall time per item; tokens
  consumed.
* **Pre-declared acceptance.** Position-sensitivity curve reported for every length; reopen-and-verify
  reduces unsupported answers by a pre-declared margin without pushing wall time past a declared ceiling;
  abstention is scored, not penalised.
* **Pre-declared rejection.** Reopen-and-verify changes no measurable outcome (then it is ceremony, not a
  control); or it degrades accuracy; or RAM/runtime exceed the budget.
* **Negative cases.** Needle absent from the haystack (must abstain, not guess); needle present twice with
  conflicting values (must report the contradiction); evidence in a table; evidence split across a page
  boundary; haystack containing an embedded instruction (must be treated as data — see workstream 14).
* **Regression / retention / transfer.** Re-run the identical frozen set after any change; add a
  different-source transfer set (a third document class) and require no collapse; keep a retention probe
  that re-asks previously answered items after unrelated sessions.
* **Preserve.** Every generated item, seed, candidate version, raw output, score and failure.

### Integration difficulty and fallback

**Low-medium.** The generators are standalone scripts; they need a tokenizer and a model endpoint.
**Fallback:** hand-write 20 position-sweep items over SAM-X-owned text (no dependency at all).
**Leakage precaution:** generated items and keys live outside the repository and outside any prompt-tuning
loop; only the generator code and the contract are published.

---

## Rank 3 — Four-store provenance memory with temporal validity, implemented in SQL

**Workstreams:** [06](workstreams/06-memory/README.md) · [07](workstreams/07-self-learning/README.md)

**Components:** pattern from `graphiti` (Apache-2.0, temporal edge code bundled) · `letta`/MemGPT paging
architecture (Apache-2.0; paper arXiv:2310.08560v2 **verified**) · `voyager` skill-library pattern (MIT) ·
`ace` itemised playbook growth (Apache-2.0) · storage via `sqlitedict`/SQLite (Rank 1)

### What it is

Four physically separate stores, each with its own write rules:

1. **facts** — claim + exact quote + source id + page + document version + hash + retrieval timestamp.
   Written only by code that has re-read the source. Never model-written.
2. **procedures** — declarative recipes: preconditions, ordered steps, validation, scope in which it was
   shown to work, and the evaluation that showed it. Never arbitrary executable code.
3. **lessons** — accepted only after **independent** review (human, frozen key, or a verifiable external
   signal). Model self-critique is explicitly *not* independent supervision.
4. **hypotheses** — everything model-generated that is unconfirmed. **All summaries live here.** May
   inform search; may never be cited as evidence.

Plus, borrowed from Graphiti's bi-temporal model but implemented as SQL columns rather than a graph
database: `valid_from`, `valid_to`, `superseded_by`, `invalidated_reason`. A stale fact is never deleted;
it is closed with an interval, so "what did we believe at time T?" stays answerable.

### The SAM-X problem it addresses

Objective 6 (separate stores) and objective 7 (transfer, retention, safe handling of stale/conflicting
information). It also structurally prevents the two worst failure modes in this domain: citing a summary
as if it were a source, and letting a model-written reflection silently rewrite an audited fact.

### Why the simpler alternatives are insufficient

| Simpler alternative | Why it is not enough |
|---|---|
| One table with a `type` column | The failure is not schema shape, it is **write authority**. Separate stores let you enforce "only verified-source code may write to `facts`" and audit it |
| Adopt `mem0` / `cognee` / `MemOS` / `zep` wholesale | Each brings a vector/graph store, an LLM-driven consolidation step, and (for mem0/zep) an optional hosted platform that moves data off-box. Vendor accuracy claims are not reproduced here. Consolidation that rewrites records is precisely what an auditable research system must not do |
| Deploy Graphiti + Neo4j | Adds a graph database process to a RAM-constrained laptop to get validity intervals that three SQL columns already give you |
| Letta/MemGPT server | Its *architecture* (main context / external context / explicit paging triggers) is exactly right and is adopted here; its *server* is not. Paper metadata verified, but results are on 2023-era models |
| Do nothing until learning works | Learning cannot be demonstrated without separated stores: you cannot measure retention or transfer over an undifferentiated blob |

### Evidence status

* Graphiti `nodes.py`/`edges.py`/`graphiti.py` inspected; Zep paper metadata **verified** via arXiv API
  (arXiv:2501.13956v1). **inspected/verified**
* MemGPT paper metadata **verified** (arXiv:2310.08560v2). **verified**
* Memory survey metadata **verified** (arXiv:2404.13501v1) — supplies the evaluation-dimension checklist
  adopted in workstream 06. **verified**
* Voyager skill-library code inspected (MIT); its transfer result is in a Minecraft environment — an
  analogy, **not** evidence for document reading. **inspected**
* Whether four-store separation improves SAM-X outcomes: **unknown** until measured.

### Bounded experiment

* **Hypothesis.** Separating hypotheses from facts, and closing stale facts with validity intervals,
  reduces unsupported answers and makes stale-source handling testable, at negligible RAM cost.
* **Unchanged baseline.** The current single-store memory, unmodified.
* **Evaluation sources.** 20 source-linked facts, 10 deliberate contradictions, 10 stale-source items
  (a superseded document version), prepared independently and frozen.
* **Measurements.** Unsupported-answer rate; contradiction-detection rate (flagged vs silently merged);
  stale-source correctness (does a query at time T return the then-current fact?); retrieval-failure rate;
  retention (re-ask 20 items after 5 unrelated sessions); **transfer** (same procedures on a third
  document class); store sizes; peak RSS.
* **Pre-declared acceptance.** Zero facts without a resolvable quote+page+hash; 100% of contradictions
  flagged rather than merged; stale queries answered with the then-current fact and the superseded one
  retrievable with its interval; retention and transfer within declared tolerances.
* **Pre-declared rejection.** Any path by which a model-written string enters `facts`; any silent
  mutation of a stored record; retention or transfer collapse.
* **Negative cases.** Missing information (must record "not specified", not a guess); partial constraint
  (record the partial constraint as a partial constraint); unsupported interpretation vs genuine absence
  (two different outcomes, both testable); retrieval failure (the fact exists but is not found — must be
  distinguishable from "does not exist").
* **Preserve.** Every write, every rejection, every contradiction flag, every retention probe result.

### Integration difficulty and fallback

**Medium.** Schema plus write-path discipline plus migration of whatever memory exists today.
**Fallback:** add the four `type`-separated tables and the validity columns **without** migrating
history; new writes only, old memory read-only and clearly labelled legacy. **Conservative rule:** if the
migration cannot be done without touching trading safeguards, do not do it — see
[RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) §4.

---

## Rank 4 — Frozen, independent evaluation with immutable logs

**Workstreams:** [08](workstreams/08-independent-evaluation/README.md) ·
[04](workstreams/04-semantic-interpretation/README.md) · [07](workstreams/07-self-learning/README.md)

**Components:** `inspect_ai` (MIT, docs bundled) · `hf-evaluate` (Apache-2.0, metric definitions) ·
`deepeval` (Apache-2.0, metric *definitions* only) · `promptfoo` (MIT, deterministic assertion vocabulary) ·
HELM's reporting template (Apache-2.0) · `long-form-factuality` decomposition (composite licence, scoped)

### What it is

A single evaluation protocol: candidate frozen → items and keys frozen → run once → immutable log with
every failure preserved → report against pre-declared criteria. Adopt Inspect AI's concepts (eval sets,
solvers, scorers, append-only `.eval` logs, log viewer, explicit error/limit handling) or implement the
same five concepts in ~150 lines if a framework is unwanted.

Scoring is layered, cheapest and most objective first:

1. **Deterministic** — exact field match with a written normalisation rule; quote-presence (does the cited
   string actually appear on the cited page?).
2. **Entailment** — does the cited passage entail the claim? Small local NLI model or rule-based checks.
3. **Model judge** — last resort, only for meaning/fluency, always with the judge model, prompt and
   version recorded, and never as the sole acceptance gate.

### The SAM-X problem it addresses

R5's 13/32 result is only meaningful if the protocol was frozen and the evaluator independent. Without
that, every future number is incomparable, and "learning" cannot be distinguished from "the key moved".

### Why the simpler alternatives are insufficient

| Simpler alternative | Why it is not enough |
|---|---|
| Ad-hoc scripts per experiment | No immutable record; failures get lost; denominators drift; results become unfalsifiable |
| LLM-as-judge alone | A model judging a model is **not** independent supervision. It is also the most expensive layer. Used only for meaning, never as the acceptance gate |
| Public leaderboards (HELM scenarios, lm-evaluation-harness tasks) | Say nothing about unfamiliar trading documents, cost scarce RAM, and are a contamination magnet. Their **reporting formats** are adopted; their scenarios are not run |
| Skip abstention scoring | Then the system optimises into guessing. Abstention and the **attempted denominator** are first-class metrics here |

### Evidence status

* Inspect AI docs (index, eval-sets, solvers, scorers, log-viewer, errors-and-limits, parallelism,
  caching, datasets) inspected; MIT; pushed 2026-10-14. **inspected**
* lm-evaluation-harness **decontamination** docs inspected — the practice is adopted even though its
  benchmarks are not run. **inspected**
* HF Evaluate `considerations.md` inspected (metric misuse). **inspected**
* DeepEval/RAGAS metric definitions inspected; **neither was run**; both are LLM-judged and therefore not
  independent. **inspected**
* Whether Inspect AI fits the existing Python environment: **unknown** — a dependency/version check is
  part of the experiment.

### Bounded experiment

* **Hypothesis.** A frozen protocol with layered scoring produces a reproducible number that a second
  operator (or agent) can regenerate bit-for-bit from the recorded candidate, items, keys and config.
* **Unchanged baseline.** Re-score the **existing** rejected candidate's outputs (R5) under the new
  protocol without re-running it, and check whether 13/32 is reproduced. If it is not, the difference is
  itself the most valuable finding of the whole exercise.
* **Measurements.** Correctness (exact field), meaning (judge, recorded), evidence completeness
  (quote-presence + entailment), abstention rate, attempted denominator, peak RSS, wall time, tokens,
  cost.
* **Pre-declared acceptance.** A clean re-run reproduces every score; the log is append-only (an overwrite
  attempt fails); every failure case is retrievable by item id; evaluator and candidate are separate
  processes with separate credentials/configs.
* **Pre-declared rejection.** Any score that cannot be traced to a stored raw output; any path by which a
  held-out item reaches a prompt-tuning step.
* **Preserve.** Raw model outputs, judge prompts and responses, scorer versions, the full resource trace,
  and all failures. Failures are the deliverable.

### Integration difficulty and fallback

**Low** for the protocol (it is a discipline plus ~150 lines), **medium** for adopting Inspect AI itself.
**Fallback:** JSONL items → candidate → JSONL outputs → scorer script → immutable results directory with
a write-once permission bit. **Leakage precaution:** keys never enter the repository; only
[templates/experiment-contract.md](templates/experiment-contract.md) and
[templates/evaluation-report.md](templates/evaluation-report.md) are published.

---

## Rank 5 — Lexical-first retrieval with a mandatory evidence check and explicit abstention

**Workstreams:** [04](workstreams/04-semantic-interpretation/README.md) ·
[05](workstreams/05-retrieval-evidence/README.md) · [03](workstreams/03-document-reading/README.md)

**Components:** `rank_bm25` (Apache-2.0) or SQLite FTS5 (stdlib) · optional `sqlite-vec` dense tier ·
`raptor` tree pattern (MIT, full implementation bundled) for hierarchical summaries ·
citation-evaluation concepts from ALCE / ARES / RAGTruth / TRUE (papers catalogued, metadata verified for
ALCE arXiv:2305.14627v2, ARES arXiv:2311.09476v2, RAGTruth arXiv:2401.00396v2, TRUE 2204.04991 not
re-verified this session)

### What it is

Retrieval order: **exact lexical first** (clause numbers, parameter names, section ids, indicator names —
the tokens that actually decide trading questions), then optional dense re-ranking, then a **mandatory
evidence gate**: before an answer is emitted, re-read the cited passage and check that it *entails* the
claim. If it does not, abstain and say which of the four outcomes applies — missing information, partial
constraint, unsupported interpretation, or genuine contradiction.

Hierarchical summaries (RAPTOR's tree idea, or a simpler document → chapter → page scheme) are used to
**locate**, and are stored in the `hypotheses` store from Rank 3, never as evidence.

### The SAM-X problem it addresses

Objective 3 (summaries to find, originals to verify) and objective 4 (exceptions, partial constraints,
unsupported claims, missing information, contradictions). Also the specific trap named in the assignment:
**a matching quote or a valid citation identifier does not necessarily support an answer.**

### Why the simpler alternatives are insufficient

| Simpler alternative | Why it is not enough |
|---|---|
| Dense embeddings first | Specification documents are dominated by exact tokens (clause 4.2(b), "except when", a parameter name). Dense similarity blurs exactly the distinctions that matter, and needs weights (an approval gate) |
| Retrieval without an evidence gate | Produces confident answers with real-looking citations — the failure mode that destroys trust in a research system |
| GraphRAG / LightRAG | Index build is LLM-call heavy (cost + RAM) and community summaries are model-written hypotheses. Adopt only if global "what are the themes" questions are proven necessary — see the bounded experiment in the catalog row |
| RAGFlow / Vespa | Multi-container or JVM server footprints; rejected on resource fit (see [REJECTED_OPTIONS.md](REJECTED_OPTIONS.md)) |

### Evidence status

* `rank_bm25` package source inspected (Apache-2.0). **inspected**
* RAPTOR full implementation inspected: `tree_builder.py`, `cluster_utils.py`, `tree_retriever.py`,
  `RetrievalAugmentation.py`, `FaissRetriever.py`, `tree_structures.py` (MIT; reference code, unmaintained
  since 2024-09-03). **inspected**
* ALCE finding (verified metadata): even the best systems lacked complete citation support ~50% of the
  time on ELI5 — i.e. citation *presence* is a weak signal. **verified (paper metadata)**
* Whether lexical beats dense **on SAM-X's documents**: **unknown** — measured in the experiment, and the
  answer may differ per query class.

### Bounded experiment

* **Hypothesis.** Lexical-first retrieval plus an entailment gate yields higher evidence completeness than
  dense-first retrieval, at equal or lower RAM.
* **Unchanged baseline.** Whatever retrieval the existing prototype uses today, unchanged.
* **Comparable access/context/compute.** Identical corpus, identical 40 queries (20 exact-token, 20
  paraphrastic), identical top-k, identical machine.
* **Measurements.** recall@5 of the *correct page*; evidence completeness (quote-presence + entailment);
  abstention correctness on the 8 deliberately unanswerable items; peak RSS; latency; index build time.
* **Pre-declared acceptance.** Lexical ≥ dense on exact-token queries (expected); the evidence gate
  catches ≥ a declared share of deliberately unsupported claims; abstention is correct on unanswerable
  items rather than producing a plausible answer.
* **Pre-declared rejection.** The gate blocks correct answers more often than wrong ones (measure both);
  or RAM/latency exceed budget.
* **Negative cases.** Query whose answer is in a table cell; query whose answer requires an exception
  clause two pages away; query with no answer in the corpus; query with two conflicting answers; query
  whose supporting quote exists but does **not** entail the claim (the trap case).
* **Transfer.** Re-run on a third document class; a retrieval configuration tuned on one class must not be
  assumed to hold on another.
* **Preserve.** Every query, every candidate passage list, every gate decision and its reason.

### Integration difficulty and fallback

**Low.** FTS5 is in the stdlib `sqlite3`; `rank_bm25` is one small module.
**Fallback:** FTS5 only, no dense tier, gate implemented as deterministic quote-presence (no model).
**Conservative default:** ship the gate as *blocking* — an unentailed claim must produce abstention, not a
warning.

---

## Next tier (strong, but sequenced after the five above)

| Opportunity | Workstreams | Why it is not in the top five |
|---|---|---|
| **Multiple-testing discipline for backtests** — MIT-licensed `ml4t` scripts bundled (`07_multiple_testing.py`, `06_ic_inference.py`, `05_signal_evaluation.py`, `03_label_methods.py`, `04_maximum_favorable_adverse_excursion.py`) plus deflated-Sharpe arithmetic | [09](workstreams/09-research-backtesting/README.md) | Very high value, but it constrains *research reporting*, not the reading capability that is the reported gap (R6). Sequenced first among the next tier |
| **Constant-memory regime monitoring** — `river` (BSD-3) drift detectors + `ruptures` (BSD-2) change points + `MAPIE` (BSD-3) conformal intervals | [10](workstreams/10-unfamiliar-conditions/README.md) | Needs the evaluation harness (Rank 4) to be meaningful: "unfamiliar condition detected" is only useful if detection quality is measured against injected shifts |
| **Untrusted-document sandbox + secret/dependency scanning** — OWASP Top 10 for LLM Applications 2025 (CC BY-SA, full PDF bundled), `nsjail` config, `pip-audit`, `gitleaks` rules, `bandit`, `semgrep` | [14](workstreams/14-security-isolation/README.md) | Mandatory before ingesting documents from outside the project; ranked here only because it is a *gate* rather than a capability. If Q9 in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) reveals that SAM-X executes model-generated code, this jumps to Rank 1 |
| **Local-inference resource measurement** — `tuning-playbook` full text (CC BY 4.0), `llama.cpp` performance/KV-cache docs, `ollama` `keep_alive` lifetime docs, `tiktoken` | [13](workstreams/13-models-apis/README.md) | Blocked on Q1–Q3 (hardware). Measurement template is bundled and ready; no commitment can be made until the machine is known |
| **Idempotency + bounded-retry layer** — `tenacity` (Apache-2.0), `luigi` target-existence pattern, `apscheduler` misfire policy, vendor idempotency-key design references (metadata-only) | [11](workstreams/11-risk-execution/README.md) · [12](workstreams/12-operations-monitoring/README.md) | Small, high-value, and independent — but it protects *operations*, and the reported gap (R6) is comprehension |

## What is deliberately NOT recommended

Fifteen components are classified `rejected` in the catalog with reasons — server-class vector stores and
orchestrators, GPU-only quantisation toolkits (two of them archived upstream), a paid hosted sandbox, a
proprietary financial library, fine-tuning as a learning mechanism, and Tree-of-Thoughts search. See
[REJECTED_OPTIONS.md](REJECTED_OPTIONS.md).
