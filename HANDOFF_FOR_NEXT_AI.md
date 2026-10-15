# HANDOFF FOR THE NEXT AI

You are picking this up with **no chat history**. This file is written for exactly that situation: it tells
you what this is, what is known versus assumed, where to start, and what you must not do.

Read this first. Then [START_HERE.md](START_HERE.md). Everything else is reachable from those two.

---

## 1. What this repository is

A **research and resource collection** — not a system, not a library, not a SAM-X fork. It exists to help
upgrade an existing project called **SAM-X** into a resource-efficient trading *research* bot that can
interpret unfamiliar documents rather than recite memorised benchmark answers.

**SAM-X itself is not in this repository and was not modified.** No line of SAM-X code was read, run,
changed or committed. No service was activated. No dependency was installed. No downloaded asset was
executed. No trade was placed. Nothing here is trading advice, and no result here is evidence that any
strategy makes money.

The full objective list (11 objectives) and the explicit non-goals are in
[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §1–§2. Read them before proposing anything, because several
plausible-sounding improvements are explicitly out of scope: perfect understanding, unlimited learning,
benchmark overfitting, and guaranteed profits are all non-goals, not aspirations.

## 2. Standing constraints that still apply to you

These came from the user and were not relaxed at any point:

* **Do not modify SAM-X** or activate its services. Do not place trades.
* **Do not install dependencies or run downloaded/untrusted code.** Every bundled asset is untrusted until
  you have verified its hash and read it.
* **Do not download model weights or large datasets** without explicit approval.
* **Do not change** source-separation, protected-holdout, trading, risk, approval, holding-rule or
  open-position safeguards.
* **Do not upload** private code, documents, credentials, account information or trading data.
* **Do not start paid services**, bypass licensing, permissions, resource guards or API limits, or propose
  quota evasion / account rotation.
* **Never ask the user to paste a password, token or 2FA code into chat.** (A GitHub PAT *was* pasted into
  chat during the original build; it was not used or stored, and the user was told to revoke it. If you see
  a credential in chat, do not use it, do not write it to a file, and tell the user to rotate it.)
* **Do not promise** perfect reading, unlimited learning, universal market handling, guaranteed RAM savings
  or trading profits.
* Publicly accessible ≠ redistributable. Check and record the licence before bundling anything. If rights
  are unclear, create a **metadata-only** entry instead. Never bypass a paywall. Never copy an entire
  copyrighted book or transcript.
* Validation scripts you write must stay narrowly scoped to **structure, links, existence and hashes** —
  never execution of collected assets.

## 3. Reported context versus verified findings

**This distinction is the most important thing in this file.** Getting it wrong produces confident nonsense.

### 3.1 Reported by the user — never verified by anyone

Label these `reported` in anything you write. Do not upgrade them to facts.

| # | Reported position |
|---|---|
| R1 | Spare laptop RAM is limited. **No number was ever given.** |
| R2 | A disk-backed navigation prototype indexed **147 pages across 2 documents**. Indexing ≠ comprehension. |
| R3 | One frozen reader qualification scored **13/32 exact field judgments** and **0/4 fully correct cases**; the candidate was rejected. |
| R4 | Reliable summaries, unfamiliar-source interpretation and demonstrated transfer are **unfinished**. |
| R5 | The user prefers **reusing compatible existing components** over new infrastructure. |

Nobody has seen SAM-X's code, its machine, its data or its evaluation key. The 13/32 figure has no
verifiable protocol behind it — see Q6 below.

### 3.2 Verified during the build (2026-10-14)

Label these `verified`. They are reproducible from this repository.

* **871 files, 20.40 MB**, from **144 upstream repositories**, each pinned to a commit SHA, each with a
  recorded SHA-256. Largest single file 10.72 MB. One bundled PDF.
* **169 catalog rows**: 42 `trial-ready`, 112 `needs-more-evidence`, 15 `rejected`. Priorities: 27 P1,
  59 P2, 83 P3. All 871 asset paths attributed exactly once.
* **Licence audit complete**: 0 assets `review-required`, 0 `not-permitted`. 155 upstream licence texts
  bundled. Three files were downloaded and then **deleted** because upstream (`yixuantt/MultiHop-RAG`) has
  no licence at all.
* **31 papers** had their metadata verified against the arXiv API on 2026-10-14. Two identifiers I assumed
  were **wrong** (`2409.12181` is not HELMET; `2105.07538` is a VAR anomaly-detection paper, not a
  conformal-prediction introduction). 46 further identifiers remain **unverified** and are labelled as
  such.
* **Alibi Detect is Business Source License 1.1** (non-production until each version's change date), not
  Apache-2.0. **PyMuPDF is AGPL-3.0 or Artifex commercial.** **Marker/Surya weights are modified
  OpenRAIL-M** while their code is Apache-2.0. **vectorbt carries a Commons Clause.** **MinerU has
  additional terms.** **LiteLLM is MIT except `enterprise/`.**
* **`twopirllc/pandas-ta` no longer resolves** (HTTP 404); `AutoGPTQ` and `AutoAWQ` are **archived**;
  `iterative/dvc` → `treeverse/dvc` and `great-expectations/great_expectations` →
  `fivetran/great_expectations` moved **during the single check window**.
* The build sandbox reached only `github.com`, `codeload.github.com`, `api.github.com`, `pypi.org`,
  `files.pythonhosted.org`, `registry.npmjs.org`. arxiv.org, huggingface.co, openreview.net,
  aclanthology.org, docs.python.org and several vendor doc sites were **unreachable**.
* The build sandbox had 3 939 MB RAM, 0 swap, 2 CPUs, ~20 GB free disk. **That is not the user's machine.**

### 3.3 Inferred, proposed, estimated, unknown

* `inferred` — conclusions drawn from verified evidence plus reasoning (e.g. "LongBench's average English
  length of 6 711 words means it does not test a 147-page scale" — the word count is verified, the
  implication is inferred).
* `proposed` — designs in this collection that nobody has built or tested. **Almost everything in the
  recommendations is `proposed`.**
* `estimate` — any resource figure taken from documentation. **No RAM, latency or accuracy number in this
  collection is a measurement.**
* `unknown` — the honest default. Used liberally, on purpose.

## 4. What the collection contains

```
README.md                     entry point and navigation
START_HERE.md                 read-order, evidence-label scheme, safety rules
PROJECT_CONTEXT.md            objectives, non-goals, reported-vs-verified, Q1–Q10, glossary, storage decisions
RESOURCE_CATALOG.csv          169 rows × 23 columns — one row per unique component, with the 15-point assessment
ASSET_MANIFEST.json           871 assets — URL, retrieval date, path, size, SHA-256, blob SHA, commit,
                              licence, status (manifest_version 1.2; the two blob-SHA
                              fields are explained in §13)
ATTRIBUTION.md                consolidated attribution and notices
RESEARCH_REPORT.md            findings by workstream, cross-cutting findings F1–F8, negative results
TOP_RECOMMENDATIONS.md        the five ranked opportunities, each with a bounded accept/reject experiment
IMPLEMENTATION_ROADMAP.md     Phases 0–9 with exit criteria, non-goals and authorisations
EVALUATION_PLAN.md            the independent qualification protocol, metrics, leakage checklist
RISKS_AND_UNKNOWNS.md         30+ risks with severity and mitigation; Q1–Q10 restated with what each blocks
REJECTED_OPTIONS.md           what was rejected, why, and what would change the decision
RESEARCH_LOG.md               dated log: searches, access limits, decisions D1–D15, failures not to retry
HANDOFF_FOR_NEXT_AI.md        this file

workstreams/01-low-ram … 14-security-isolation/     14 READMEs, each with the required nine sections
resources/papers/PAPER_INDEX.md                     31 verified + 46 unverified identifiers, labelled
resources/benchmark-descriptions/BENCHMARK_NOTES.md why public benchmarks are not qualification evidence
resources/diagrams/*.svg                            architecture and data-flow diagrams
resources/documentation/      599 files — official docs and reference material from pinned commits
resources/code-examples/       86 files — inspectable reference implementations
resources/configurations/      26 files — real config templates (Qlib workflows, hummingbot, nsjail, …)
resources/licenses/           155 files — verbatim upstream licence texts + INDEX.md
resources/documentation/_metadata-only/             records for material deliberately not bundled
templates/                    experiment-contract, component-assessment, evaluation-report, source-provenance
scripts/validate_catalog.py   offline structural validation (never executes an asset)
scripts/verify_asset_hashes.py offline SHA-256 re-verification against the manifest
```

Counts by category: documentation 599 · licenses 155 · code-examples 86 · configurations 26 ·
benchmark-descriptions 5 · papers 0 PDFs (metadata-only) · 124 PyPI registry snapshots + 747 GitHub files ·
8 metadata-only resources (MO-01…MO-08).

## 5. Where to start

**In this order.**

1. [START_HERE.md](START_HERE.md) — five minutes, gives you the evidence-label scheme and the safety rules.
2. [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4 — the ten open questions. **If you can answer any of them,
   answer them before doing anything else.** Q9 in particular reorders the entire roadmap.
3. [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) — the five ranked opportunities with their bounded
   experiments.
4. [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — Phases 0–9, and the "what would change this
   roadmap" table at the end.
5. The workstream README for whatever you are actually working on.

**Most useful single assets**, if you only look at five:

| Asset | Path | Why |
|---|---|---|
| RULER task generators | `resources/code-examples/ruler/` (`niah.py`, `variable_tracking.py`, `qa.py`, `common_words_extraction.py`, `freq_words_extraction.py`, `constants.py`, `prepare.py`, `tokenizer.py`, `eval/evaluate.py`) | Apache-2.0 code that **generates** long-context evaluation items locally from any haystack. Solves the "no dataset download, no contamination, re-seedable" problem in one move |
| Google LLM Tuning Playbook | `resources/documentation/tuning_playbook/` (CC BY 4.0, ~120 KB of text) | The only fully redistributable long-form technical report in the collection; directly relevant to workstream 13 |
| OWASP Top 10 for LLM Applications 2025 | `resources/documentation/owasp-llm-top10/` (CC BY-SA 4.0, PDF + 11 markdown files) | The security baseline for workstream 14; LLM01, LLM08 and LLM10 map straight onto SAM-X |
| ML4T multiple-testing scripts | `resources/code-examples/ml4t/07_defining_the_learning_task/` (MIT) | The concrete arithmetic for "no strategy promoted on a naive Sharpe alone" |
| Graphiti temporal edges | `resources/code-examples/graphiti/` (Apache-2.0) | The bi-temporal validity pattern (`valid_from`/`valid_to`/`superseded_by`) implemented in SQL, without a graph database |

## 6. Verified / inferred / proposed / unknown — the summary you asked for

| Status | What falls in it |
|---|---|
| **Verified** | Every bundled file exists at its recorded path with its recorded SHA-256 and size. Every licence classification was read from bundled text. 144 upstream commits are pinned. 31 paper identifiers are confirmed. The repository's own Git history contains no secrets. |
| **Inferred** | Which components fit the reported resource constraint; that LongBench cannot test a 147-page scale; that lexical retrieval should be measured before dense; that four-store separation is what makes retention and transfer measurable at all. |
| **Proposed** | All five recommendations' designs. All nine roadmap phases. The four-store schema. The evidence gate. The evaluation protocol. Every control in workstream 14. **None of it is built or tested.** |
| **Unknown** | The machine (Q1–Q3). Document rights and held-out availability (Q4). The existing prototype's interface (Q5). Whether R5's key was frozen (Q6). Whether summaries are currently cited as evidence (Q7). Hosted-API authorisation and terms (Q8). Whether SAM-X executes generated code (Q9). Whether safeguards are code-enforced (Q10). Every RAM, latency and accuracy figure for every component on the target machine. |

## 7. Components that are alternatives — do NOT install together

These overlap. Installing more than one from a group adds footprint and conflicting abstractions without
adding capability.

| Group | Members | Pick |
|---|---|---|
| **Embedded key-value / disk spill** | `diskcache`, `sqlitedict`, `shelve` (stdlib) | `diskcache` (or `sqlitedict` if you want dict semantics over SQLite). Not both |
| **Vector search** | `sqlite-vec`, `USearch`, `faiss` (in-process), Chroma, LanceDB, Qdrant-server, Weaviate, Milvus, Vespa | `sqlite-vec` first — same file, same query language as everything else. Server-class members are **rejected on resource fit** |
| **Lexical search** | SQLite **FTS5** (stdlib), `rank_bm25`, Whoosh | FTS5. Add `rank_bm25` only for a comparison measurement |
| **PDF text extraction** | `pypdf` + `pdfminer.six`, PyMuPDF, MinerU, Marker, Surya, Docling, `markitdown` | `pypdf` + `pdfminer.six` (permissive). PyMuPDF is AGPL/commercial; Marker/Surya weights are OpenRAIL-M; Docling weights need approval. **Do not mix extractors silently** — treat disagreement as an extraction-error signal |
| **Analytical store** | DuckDB, Polars, pandas | DuckDB for scans with `memory_limit`; Polars streaming for transforms; pandas only where an existing dependency requires it. All three can coexist, but pick one as the primary |
| **Data versioning** | manifest + atomic rename (recommended), Delta Lake / `delta-rs`, DVC, Zarr | The manifest. DVC's ownership changed mid-check; Zarr has a live v2/v3 migration |
| **Data quality** | `pandera`, Great Expectations | `pandera` (MIT). GX's upstream org moved to Fivetran |
| **RAG / agent framework** | LlamaIndex, LangChain, LangGraph, Haystack, txtai | **None.** Borrow their schemas. At most one, ever |
| **Memory layer** | four-store SQL (recommended), `mem0`, `cognee`, `MemOS`, `A-MEM`, Letta server, Graphiti + Neo4j, Zep server | The four-store SQL design. All the others consolidate or rewrite records, which an auditable system must not do |
| **Hierarchical retrieval** | RAPTOR pattern (recommended), GraphRAG, LightRAG | RAPTOR's *pattern* (its dependency is unmaintained). GraphRAG/LightRAG index builds are LLM-call heavy and produce model-written community summaries |
| **Drift / regime detection** | `river` (BSD-3), Alibi Detect (**BSL 1.1 — non-production**), `ruptures`, `MAPIE`, `hmmlearn` | `river` for constant-memory detection; `ruptures` for change points; `MAPIE` for conformal intervals. Alibi Detect only in non-production and only after reading the BSL change date |
| **Backtesting engine** | `zipline-reloaded` (Apache-2.0), NautilusTrader (LGPL), Freqtrade (GPL), Backtrader (GPL), backtesting.py (AGPL), vectorbt (Commons Clause), Qlib (MIT) | **Read their semantics; do not vendor** the copyleft ones. `zipline-reloaded`'s `slippage.py` / `commission.py` / `controls.py` and Qlib's workflow configs are the permissive references |
| **Evaluation runner** | hand-rolled ~150 lines, Inspect AI (MIT), lm-evaluation-harness, HELM | Hand-rolled or Inspect AI. HELM/lm-eval contribute **report shape and decontamination practice**, not scenarios |
| **LLM-judged metrics** | Ragas, DeepEval, promptfoo | **Metric vocabulary only.** An LLM judging an LLM is not independent supervision and is never an acceptance gate |
| **Local inference** | llama.cpp, Ollama, vLLM (GPU), lmdeploy (GPU), Transformers on CPU | llama.cpp or Ollama. vLLM/lmdeploy are GPU-first. **Blocked on Q1–Q3 — choose nothing until the machine is known** |
| **Quantisation** | llama.cpp built-in, Ollama formats, bitsandbytes, AutoGPTQ (**archived**), AutoAWQ (**archived**) | llama.cpp / Ollama. Both leading toolkits are archived upstream |
| **Secret scanning** | `gitleaks` (rules bundled), `detect-secrets`, TruffleHog (**AGPL, verifies by default → live network calls with found credentials**) | `gitleaks` or `detect-secrets`. **Never** run TruffleHog in verify mode against credentials you do not own |
| **Sandboxing** | `nsjail` (config bundled), OS rlimits/cgroups, gVisor (needs kernel support), E2B (**paid, remote**) | `nsjail` on Linux, rlimits as the portable fallback |
| **Orchestration** | run log in SQLite + Luigi target-existence pattern (recommended), Airflow, Temporal, Dagster, Prefect | The run log. All three servers are rejected on footprint |
| **Metrics** | `prometheus_client` shapes written to a local file/SQLite, Prometheus server + Grafana (AGPL) | The former |

## 8. Ready for bounded trials now

`trial-ready` in the catalog (42 rows). The ones with the lowest risk and clearest experiment:

* **Phase 0 resource trace** — `psutil` sampling over one existing job. Cannot break anything, produces the
  numbers every other decision needs.
* **Phase 1 re-scoring** — deterministic exact-match + quote-presence scoring of the *already recorded* R5
  outputs under the frozen protocol. Tests the protocol, not the model.
* **Phase 3 spine** — SQLite page map + FTS5 + `diskcache` + `tiktoken` budget over the 147 already-indexed
  pages, measuring peak RSS and whether every answer resolves to a hash-verified page.
* **RULER generators** — produce a fresh item set from text the project owns the rights to. No network, no
  dataset, no weights.
* **Secret and dependency audit** — `gitleaks` rules + `pip-audit` against the project's own repository
  (needs approval to scan the SAM-X codebase).

Each has a pre-declared accept/reject criterion in its catalog row or in
[TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md). Write the experiment contract
([templates/experiment-contract.md](templates/experiment-contract.md)) **before** running anything.

## 9. Needs more evidence before any trial

112 rows. The common reasons, so you do not have to rediscover them:

* **No footprint measurement on the target machine** — this is most of them, and Q1–Q3 unblock it.
* **Weights required** (Marker, Surya, Docling, sentence-transformers, any embedding or NLI model) — an
  approval gate, plus a licence read on the model card at adoption time.
* **Upstream dormant or archived** — fine for reference code, not fine for a live dependency without a
  vendoring plan.
* **Vendor claims not independently reproduced** — mem0's accuracy numbers, Zep's DMR results, any
  README speedup. Treat as leads.
* **Licence needs a decision, not just a reading** — PyMuPDF (AGPL vs commercial), vectorbt (Commons
  Clause), Alibi Detect (BSL change date), MinerU (additional terms), LiteLLM (`enterprise/`).

## 10. Needs explicit authorisation from the user

* Downloading **any** model weights or dataset.
* Installing **any** dependency, or running **any** downloaded code.
* Starting **any** paid or hosted service; and re-verifying its terms on that date (pricing pages are
  metadata-only here because they change and are not redistributable).
* Scanning the **SAM-X codebase** with any tool.
* Building or downloading a **sandbox binary** (`nsjail`) — treat it as untrusted until hash-verified.
* Using the two indexed documents, or any third document, as **evaluation sources** — this is a rights
  question (Q4), not a technical one.
* Anything touching trading, risk, approval, holding-rule or open-position safeguards. **This engagement
  never had that authorisation and you should assume you do not either.**

## 11. Dependencies and recommended sequence

Phase order, with hard dependencies (full detail and exit criteria in
[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)):

```
0  Measure the machine and the existing system        ← blocks everything
1  Freeze the evaluation protocol; re-score R5        ← needs 0
2  Four-store memory + temporal validity (SQL)        ← needs 0
3  Bounded-memory reading spine + reopen-and-verify   ← needs 0, benefits from 2
4  Lexical-first retrieval + evidence gate            ← needs 2 and 3
5  Typed interpretation contract (eight confusions)   ← needs 1
6  Learning, retention, transfer, regression          ← needs 1, 2, 4
7  Idempotency, checkpoints, run log, telemetry       ← independent, start any time
8  Immutable data generations + backtest hygiene      ← needs 0 and 7
9  Regime monitoring, risk objects, security hardening ← needs 7; jumps to first if Q9 = yes
```

Hard dependencies: **0 → 1** (nothing is comparable without measurement and a frozen protocol),
**2 → 4** (the evidence gate needs the fact/hypothesis split), **1 → 6** (learning claims need a frozen
regression suite).

**The first three experiments**, if you do nothing else:

1. `psutil` resource trace over one existing SAM-X job → the real memory ceiling.
2. Re-score the recorded R5 outputs under the frozen protocol → find out whether 13/32 is a baseline at all.
3. Reopen-and-verify over the 147 indexed pages → measure whether every answer resolves to a hash-verified
   page, and what peak RSS the spine needs.

All three are bounded (≤ 1 day), reversible, and produce a number that can **reject** a hypothesis.

## 12. Evaluation leakage precautions

Non-negotiable. Full checklist in [EVALUATION_PLAN.md](EVALUATION_PLAN.md) §7.

* **Keys and held-out sources never enter this repository.** Only templates and hashes are published.
* The two already-indexed documents are **contaminated by prior exposure** (reported R2). They may be used
  for mechanical and coverage tests. They may **not** support a capability claim.
* Prompt tuning, few-shot selection, threshold setting and retrieval-config tuning happen on TRAIN sources
  only. Every look at VALIDATION is logged — it is a slow leak.
* TEST is opened **once** per candidate generation. A new candidate needs fresh items or a fresh source.
* Record the candidate model's **training cutoff** against every item's creation date and every source's
  publication date. Flag `contamination-risk` items and report them separately.
* Public benchmarks (LongBench, ∞Bench, NovelQA, HELM scenarios, lm-eval tasks) are **not** qualification
  evidence for unfamiliar trading documents. Their harnesses, scorers, report shapes and decontamination
  practices are adopted; their scenarios are not run. See
  [resources/benchmark-descriptions/BENCHMARK_NOTES.md](resources/benchmark-descriptions/BENCHMARK_NOTES.md).
* Cache keys must include candidate id and prompt hash, or you are scoring yesterday's answer.
* Report the **attempted denominator** next to every rate. Accuracy that improves while the denominator
  shrinks is abstention being used to game the metric — that is a pre-declared rejection criterion.
* Record the number of configurations compared and apply a correction. The multiple-testing discipline that
  workstream 09 demands of backtests applies equally to evaluations.

## 13. How to find and verify bundled assets

**Find.** Three indexes, each answering a different question:

* *"Which component should I use?"* → [RESOURCE_CATALOG.csv](RESOURCE_CATALOG.csv). One row per unique
  component: id, name, workstreams, type, official URL, local paths, pinned commit, licence,
  redistribution status, checked date, evidence status, hardware needs, costs/privacy, integration role,
  priority, classification, and the full 15-point assessment.
* *"Where did this file come from and is it intact?"* → [ASSET_MANIFEST.json](ASSET_MANIFEST.json). Per
  asset: id, related component ids, original URL, retrieval date, local path, size, SHA-256, local and
  upstream Git blob SHAs, upstream commit, licence, attribution, status (`downloaded` / `inspected` /
  `tested` / `metadata-only`), and any access, integrity or verification limitation.
* *"What am I allowed to do with it?"* → [resources/licenses/INDEX.md](resources/licenses/INDEX.md) (144
  components with bundled licence text, the redistribution-status vocabulary, and an explicit
  "deliberately NOT collected" list) and [ATTRIBUTION.md](ATTRIBUTION.md).

**Verify.** Both scripts are offline and read-only. Neither executes, imports or parses a collected asset.

```bash
python3 scripts/validate_catalog.py       # structure, vocabularies, cross-checks, links, existence, secret scan
python3 scripts/verify_asset_hashes.py    # recompute SHA-256, size and Git blob SHA for all 871 assets
```

`validate_catalog.py` exits 0 (clean), 1 (errors) or 2 (usage/IO problem). Every `component_id` in the
manifest resolves to a catalog row: PyPI distribution names were normalised to their catalog ids at build
time (for example `apache-airflow` → `airflow`, `marker-pdf` → `marker`, `evaluate` → `hf-evaluate`), so a
new warning of that kind means a genuinely new, unassessed component appeared.

**Two warnings are expected and correct**, both in bundled upstream files, both reviewed and explained in
the `BUNDLED_CREDENTIAL_LOOKALIKES` table inside the validator:

* `resources/documentation/trufflehog/README.md` quotes an example AWS access key id in its sample scanner
  output. That key is a canary token published by `trufflesecurity/test_keys`, not a live credential and not
  this project's.
* `resources/configurations/gitleaks/config__gitleaks.toml` is gitleaks' own published configuration; its
  `[allowlist]` carries 16 Google-API-key-shaped strings that gitleaks allowlists so its own examples and
  test fixtures are not reported. They are upstream's, were **not** tested or used, and the file is kept
  byte-identical to its recorded SHA-256 because editing a bundled asset would misrepresent it.

The rule that table enforces is the important part: a credential-shaped string in a file **authored here**
is always an error, and one in a **bundled upstream** file is an error unless someone has read it and
written down why it is acceptable. A third warning would mean something new and unreviewed appeared.

**The two blob-SHA fields.** `local_git_blob_sha` hashes **the bundled bytes** and is recomputed by
`verify_asset_hashes.py`; it matches this repository's published tree for all 871 assets.
`upstream_git_blob_sha` is the object SHA GitHub reports for `upstream_path` at `upstream_commit` —
provenance, and deliberately **not** compared against our copy. For **7** assets the upstream path is a
symlink, so GitHub reports the link's SHA while serving the resolved target's bytes and the two values
differ **by design**; those records set `upstream_path_is_symlink: true`, name the target and explain
themselves, and the validator fails if an unexplained difference ever appears. **124** package-registry
metadata records have `upstream_git_blob_sha: null` with a recorded reason: there is no upstream Git object
to point at. When in doubt, verify with `sha256`.

**Before you trust any asset further:**

1. Confirm its SHA-256 matches the manifest (`verify_asset_hashes.py`, which also recomputes
   `local_git_blob_sha`). If it is flagged `upstream_path_is_symlink`, do not expect
   `upstream_git_blob_sha` to match anything you compute from the bundled bytes.
2. Read its bundled licence text under `resources/licenses/` — do not rely on a detector or a README badge.
   GitHub's detector returned `NOASSERTION` for several repositories that do have licences.
3. Check `checked_date`, `upstream_last_pushed` and `upstream_archived` in its catalog row. Ownership
   changed for two well-known projects **during the single day** this was built.
4. Read the file. Do not run it.

## 14. Known gaps you will hit

* **No paper PDFs.** By licence and by network. 31 papers are metadata-only with verified identifiers;
  46 more identifiers are labelled *not re-verified this session* — re-query the arXiv API in batches of
  ≤ 6 ids if you need them, and do not assert an identifier you have not confirmed.
* **No Hugging Face model or dataset cards** — host unreachable. Any weights decision needs a card read at
  adoption time.
* **No vendor ToS or pricing pages** — unreachable and not redistributable. Never assume a free tier is
  unlimited or permanent.
* **Nothing measured.** There is no RAM figure, latency figure or accuracy figure for any component on any
  real machine in this collection. Every such number is an `estimate` from documentation.
* **SAM-X is a black box.** Ten questions in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4 stand between this
  collection and a concrete adoption plan. Ask them; do not guess answers.
* **The document classes SAM-X must read are not stated anywhere.** Broker specifications? Research reports?
  Regulatory filings? Vendor manuals? The entire evaluation design depends on this. It is the first thing to
  establish after Q1–Q3.

## 15. Housekeeping

* Work happens on the session branch; the repository's `main` carried one commit (`10bb5f6`, "Fresh start",
  `README.md` only) before this collection.
* A recoverable snapshot of the pre-collection state exists as branch `archive/pre-samx-collection` and tag
  `archive/fresh-start-pre-collection`, both at `10bb5f6`. It is deliberately **not** linked from the main
  navigation, to keep the old state separate from the new collection.
* No prior deliverables were deleted, because none existed. Nothing user-authored was discarded.
* Git history was never rewritten, force-pushed or erased. Repository visibility was never changed.
* Bundle size 20.40 MB / repository ~24 MB. No GitHub Releases, no Git LFS — both checked against
  GitHub's published limits and found unnecessary. Revisit if the bundle passes ~100 MB
  ([PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §8).
* If you add an asset: add its manifest entry, add or update its catalog row, link it from the relevant
  workstream README, and re-run both scripts. If you add a file under `resources/` without a manifest entry,
  the orphan check will warn.
