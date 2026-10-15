# BENCHMARK NOTES

Why public benchmarks are **not** qualification evidence for SAM-X — and what they *are* good for.

This file exists because the collection bundles benchmark **harnesses, scorers, configs and descriptions**
without bundling benchmark **data**, and because a reader who does not know why will reasonably conclude
that something was missed. Nothing was missed. The distinction is deliberate and is recorded here.

---

## 1. The position in one paragraph

Public long-context and RAG benchmarks measure whether a **model** performs on **their** tasks, on **their**
corpora, at **their** lengths. SAM-X needs to know whether a **candidate reader** performs on **its**
document classes, at **its** scale (147 pages across two documents, reported), with **its** failure
requirements (no invented parameters, correct abstention, evidence that entails). Those are different
questions, and answering the first does not answer the second. Public benchmarks are therefore used here for
three things only: **design lessons**, **scorer and harness code**, and **reporting shape**. They are never
used as an acceptance gate.

## 2. What is bundled, and what is not

| Bundled | Not bundled | Why not |
|---|---|---|
| Harness and runner code (MIT/Apache-2.0): LongBench `pred.py`/`result.py`, ∞Bench `compute_scores.py`/`prompt.py`, HELMET `data.py`/`eval.py`/`arguments.py`/`model_utils.py`, RULER generators and configs, NIAH scripts, AgentBench configs | Benchmark **datasets** | Hosted on Hugging Face, which was unreachable for download from the build sandbox; and a 2023–24 public dataset is a contamination magnet |
| Benchmark **descriptions**: the five upstream READMEs under this directory | Paper PDFs | arXiv's non-exclusive licence does not grant redistribution — see [PAPER_INDEX.md](../papers/PAPER_INDEX.md) |
| MultiHop-RAG: **nothing** | MultiHop-RAG code and data | **No licence file exists upstream**, so there is no redistribution right. Three files downloaded in an early pass were deleted during the licence audit; see [_metadata-only/multihop-rag.md](../documentation/_metadata-only/multihop-rag.md) |
| NovelQA: **nothing** | NovelQA corpus | >200K-token **copyrighted novels** — copying them is out of scope |
| NIAH haystack text: **nothing** | The Paul Graham essays used as the haystack | Copyrighted essays, and unnecessary: the RULER generators can build a haystack from any text the project owns |

Bundled benchmark descriptions in this directory: [agentbench](agentbench/README.md) ·
[helmet](helmet/README.md) · [infinitebench](infinitebench/README.md) · [longbench](longbench/README.md) ·
[niah](niah/README.md). Each is listed in [ASSET_MANIFEST.json](../../ASSET_MANIFEST.json) with its upstream
commit and SHA-256.

## 3. Per-benchmark assessment

| Benchmark | Licence | Scale (from verified metadata or bundled description) | Relevance to SAM-X | Verdict |
|---|---|---|---|---|
| **RULER** (NVIDIA) | Apache-2.0 | Configurable token lengths (8K/32K/128K); task generators: NIAH variants, variable tracking (multi-hop), QA, common-words and frequent-words extraction | **High** — the generators are the recommended item source. Its headline finding is the most load-bearing in the collection: near-perfect vanilla NIAH coexists with sharp drops at 32K, and only about half of models claiming ≥32K held up | **Adopt the generators.** Do not adopt its model leaderboard as evidence about SAM-X |
| **LongBench** (THUDM) | MIT (harness) | 21 datasets; **average 6 711 English words** | **Low for scale** — 6 711 words is roughly 20–25 pages, nowhere near 147 pages. Its useful finding: retrieval helps weak long-context models and lags strong ones | Harness and configs adopted as reference; **data not run** |
| **∞Bench / InfiniteBench** (OpenBMB) | MIT (harness) | 100K+ token tasks | **Medium** — the right order of magnitude, but the tasks are general (novels, code, dialogue), not specifications | Scorers adopted; data not downloaded |
| **HELMET** (princeton-nlp) | MIT (code) | Long-context application-centric suite | **Medium** — its emphasis on *application* tasks rather than synthetic recall is the right instinct | Harness code adopted. **Its arXiv identifier is unverified**: `2409.12181` resolved to a different paper (MO-08) |
| **NIAH** (gkamradt) | MIT (code; GitHub's detector says NOASSERTION) | Single-fact retrieval at varying depth and length | **Low alone** — RULER shows passing NIAH is close to meaningless by itself | Code adopted as a generator reference; **haystack essays not collected** |
| **AgentBench** (THUDM) | Apache-2.0 | Multi-environment agent benchmark, some Dockerised | **Low** — agent capability across environments, not document interpretation | Configs adopted for their environment-isolation patterns; environments not run |
| **MultiHop-RAG** | **None** | Multi-hop queries over a news corpus | Would have been **high** — multi-hop retrieval is exactly the construct needed | **Not bundled: no licence.** RULER's `variable_tracking.py` + `qa.py` produce the same construct lawfully |
| **NovelQA** | Corpus copyrighted | >200K-token novels | **Medium** for scale, **low** for redistribution | Metadata-only |
| **ALCE / ARES / RAGTruth / TRUE** | Mixed; papers metadata-only | Citation and faithfulness evaluation | **High as concepts** — ALCE's finding that even good systems lacked complete citation support ~50% of the time on ELI5 is why the evidence gate is mandatory | Concepts and metric definitions adopted; nothing run |

## 4. The four reasons a public benchmark cannot qualify SAM-X

1. **Scale mismatch.** LongBench averages 6 711 English words. SAM-X's reported corpus is 147 pages across
   two documents. A benchmark whose average item is a fraction of one document cannot measure navigation
   across a document.
2. **Contamination.** These benchmarks are 2023–2024 vintage and their corpora are plausibly inside the
   training data of any current model. A high score may be recall, not reading.
   [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §7 requires a per-item contamination check: candidate
   training cutoff versus item creation date versus source publication date.
3. **Domain mismatch.** Novels, news, dialogue, code and Wikipedia are not broker specifications, vendor
   manuals or regulatory filings. The failure modes SAM-X must avoid — confusing a dataset description with a
   trading rule, a sampling frequency with an execution timeframe, an indicator name with a parameter
   setting — do not appear in these corpora at all.
4. **Wrong unit of analysis.** Benchmarks score **models**. SAM-X is qualifying a **system**: retrieval plus
   memory stores plus an evidence gate plus abstention policy plus a resource budget. A model score cannot
   detect an invented parameter, a summary cited as evidence, or a memory ceiling breach.

## 5. What benchmarks *are* good for here

| Use | Example |
|---|---|
| **Item generation** | RULER's Apache-2.0 generators, pointed at text the project owns the rights to, with a fresh seed. Re-seedable, auditable, and cannot have been in a training corpus |
| **Scorer code** | ∞Bench's `compute_scores.py`, LongBench's `result.py`, HELMET's `eval.py` — objective, deterministic scoring implementations to read and adapt |
| **Reporting shape** | HELM's metrics × scenarios × models matrix, including efficiency, rather than a single accuracy number |
| **Decontamination practice** | lm-evaluation-harness's decontamination documentation — the *practice* is adopted even though its tasks are not run |
| **Design lessons** | RULER (position and complexity matter), Lost in the Middle (position sweep), Same Task More Tokens (length as an independent variable), ALCE (citation presence is weak), LongBench (retrieval helps weak models more) |
| **Metric vocabulary** | Ragas, DeepEval, promptfoo, HF Evaluate — names and definitions for assertion types. **LLM-judged metrics are never an acceptance gate** |

## 6. The substitute that is lawful and scale-appropriate

Because the datasets cannot be bundled and would be contaminated anyway, the recommended evaluation source is
**locally generated items over project-owned text**:

1. Take text the project holds the rights to use (question Q4 in
   [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md)) — explicitly **not** the two documents already indexed,
   which are contaminated by prior exposure.
2. Run the bundled RULER generators with a recorded seed at the token lengths the machine can actually
   sustain (Q1–Q3 decide).
3. Add hand-authored field-extraction items with expected value, page and exact supporting quote.
4. Add negative items **by construction**: delete a parameter (expect `absent_from_source`), split a
   constraint across two pages (expect both cited), add an exception clause (expect it reported), publish a
   superseded document version (expect the current one used and the stale one flagged), include a quote that
   does not entail the claim (expect rejection).
5. Freeze items and keys by hash before any output exists, and keep the keys outside this repository.

Full protocol: [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md). Contract template:
[templates/experiment-contract.md](../../templates/experiment-contract.md). Report template:
[templates/evaluation-report.md](../../templates/evaluation-report.md).

## 7. What must never be claimed from a benchmark result

* That SAM-X can read unfamiliar documents.
* That a candidate is better than the rejected one (reported R3: 13/32 exact fields, 0/4 fully correct).
* That a context length is supported.
* That citations are faithful.
* That memory, transfer or retention works.
* That any strategy is profitable, or that any market condition is handled.

A benchmark score supports one claim: that a model, on that benchmark, on that date, scored that number.
Everything else requires the source-based qualification in
[EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) — and even that is not deployment proof.
