# RESEARCH REPORT

Findings from building this collection on **2026-10-14**, organised by workstream. Each section states
what was found, what evidence supports it, and what remains unknown. Detail lives in the workstream
READMEs; this report is the cross-cutting narrative and the place where **negative results** and
**licensing discoveries** are collected.

Evidence labels: **measured** · **verified** · **inspected** · **estimate** · **reported** · **proposed** ·
**unknown**.

---

## 0. Method, scope and access limits

**Method.** (1) Shortlisted ~150 upstream projects across the 14 workstreams from prior knowledge of the
field. (2) Resolved each through the GitHub REST API, recording licence, last push, star count, archived
flag, default branch and HEAD commit SHA. (3) Inventoried each repository's full file tree at that commit
so that specific files — not whole repositories — could be selected. (4) Downloaded selected files through
the GitHub contents API at the pinned commit, recording blob SHA, byte size and SHA-256. (5) Snapshotted
PyPI registry metadata for 126 package names (124 resolved). (6) Read every root licence file that GitHub's
detector could not classify, and overrode the detector where the text disagreed. (7) Verified research-paper
metadata against the arXiv API. (8) Authored analysis, templates, diagrams, plans and this report.

**Access limits (measured 2026-10-14).** Sandbox `bash` egress reached only `github.com`,
`codeload.github.com`, `api.github.com`, `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`.
`arxiv.org`, `export.arxiv.org`, `huggingface.co`, `openreview.net`, `aclanthology.org`,
`proceedings.mlr.press`, `docs.python.org`, `sqlite.org`, `duckdb.org` and `llm.datasette.io` all failed at
the network layer from `bash`. A separate read-only page-fetch path reached general web **text** (used for
arXiv metadata verification) but cannot save binaries.

**Consequences, stated plainly.**

* No paper PDFs are bundled. Two independent reasons: the binary route was unreachable, **and** the arXiv
  non-exclusive distribution licence does not grant third-party redistribution. arXiv PDFs sitting inside
  permissively-licensed repositories (found in `docling-project/docling` and `Unstructured-IO/unstructured`
  test fixtures) inherit the *paper's* licence, not the repository's, so they were deliberately not copied.
* No model weights, no datasets, no whole repositories.
* Coverage is **broad but not exhaustive**. No claim of complete internet coverage is made, and no browsing
  result is fabricated: every bundled file has a retrieval URL, a commit SHA and a digest.

**Scale of the result.** 871 files, 20.40 MB, from 144 repositories, all pinned to a commit. 169 catalog
rows: 42 `trial-ready`, 112 `needs-more-evidence`, 15 `rejected`. 8 metadata-only resources. 1 bundled PDF.
155 upstream licence texts. 31 papers with metadata verified against the arXiv API.

---

## 1. Cross-cutting findings

### F1 — The binding constraint is provenance discipline, not retrieval technology *(verified by inspection)*

Every component that promises "memory" or "retrieval" solves the easy half. The half SAM-X needs — *which
store may be written by whom, and what makes a claim a fact* — is almost never enforced by the tools.
`mem0`, `cognee`, `MemOS`, `graphiti`, `letta` all provide storage and consolidation; none of them
prevents a model-written summary from being returned as if it were a source-linked fact. That is an
architectural decision SAM-X must make itself. It is the reason Rank 3 in
[TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) is a schema-and-write-authority change rather than a
dependency.

### F2 — "Indexing works" and "reading works" are unrelated claims *(verified)*

Reported position R4 (147 pages indexed across two documents) is a navigation achievement. RULER
(arXiv:2404.06654v3, metadata verified via the arXiv API) reports models scoring near-perfectly on vanilla
needle-in-a-haystack while dropping sharply as length and task complexity grow; of models claiming ≥32K
context, only about half held up at 32K. Reported R5 (13/32 exact fields, 0/4 fully correct cases) is
consistent with that pattern. **Implication:** the collection prioritises task generators that test
multi-hop tracing, aggregation and position sensitivity over retrieval-success probes.

### F3 — Citation presence is a weak signal *(verified paper metadata)*

ALCE (arXiv:2305.14627v2, EMNLP 2023) reports that even the best systems lacked complete citation support
about half the time on ELI5. Combined with the assignment's own warning — *a matching quote or valid
citation identifier does not necessarily support an answer* — this makes the **evidence gate**
(quote-presence → entailment → abstain) a mandatory component, not a nice-to-have. It is Rank 5.

### F4 — Self-critique is not supervision *(verified pattern, one paper id not re-verified)*

Reflexion's published gains come from environments with ground-truth feedback signals. Voyager's skill
library is validated by environment execution. The relevant negative literature (LLMs cannot reliably
self-correct reasoning without external feedback) was **not re-verified in this session** — its arXiv
identifier is recorded in [resources/papers/PAPER_INDEX.md](resources/papers/PAPER_INDEX.md) as
*unverified*. Regardless of that citation, the design rule adopted here is independent of it: a lesson
enters the `lessons` store only with an external signal (execution result, frozen key, or human review).
Model-generated reflections may *propose*.

### F5 — Licensing is a first-class research finding, and four discoveries change adoption decisions *(verified by reading bundled licence texts)*

| Discovery | Consequence |
|---|---|
| **Alibi Detect is Business Source License 1.1**, not Apache-2.0: non-production use only until each version's change date (4 years), then Apache-2.0 | A formerly-obvious drift-detection choice is now restricted for production. `river` (BSD-3) becomes the recommended path |
| **PyMuPDF is AGPL-3.0 or Artifex commercial** | The fastest, most capable PDF library in the shortlist carries copyleft that reaches a networked service. `pypdf` (BSD-3) + `pdfminer.six` (MIT) are the recommended text path |
| **Marker/Surya: Apache-2.0 code, modified OpenRAIL-M weights** | "Open source" was true of the code and not of the models. Weights carry use restrictions — a policy question for a trading application |
| **vectorbt: Commons Clause over Apache-2.0**; **MinerU: Apache-2.0 plus additional terms**; **LiteLLM: MIT except `enterprise/`** | Redistribution is allowed but selling is not (vectorbt); additional terms must be read (MinerU); one directory is out of bounds (LiteLLM) |

Plus one removal: **`yixuantt/MultiHop-RAG` has no licence file at all**, so two files downloaded in an
early pass were deleted during the audit and replaced with a metadata-only record
(`resources/documentation/_metadata-only/multihop-rag.md`). Absence of a licence means all rights
reserved — a fact that is easy to miss when a repository is popular and its README inviting.

### F6 — Upstream disappearance and ownership change are real supply-chain risks *(verified)*

* `twopirllc/pandas-ta` returned HTTP 404 through the GitHub API on 2026-10-14; only community forks
  resolve (`xgboosted/pandas-ta-classic`, MIT, actively pushed). A widely used indicator library's
  canonical slug is gone.
* Ownership/org changes observed during the check window: `iterative/dvc` → `treeverse/dvc`;
  `great-expectations/great_expectations` → `fivetran/great_expectations`; `VikParuchuri/marker` →
  `datalab-to/marker`; `explodinggradients/ragas` → `vibrantlabsai/ragas`; `robertmartin8/PyPortfolioOpt`
  → `PyPortfolio/PyPortfolioOpt`; `hsiehjackson/RULER` → `NVIDIA/RULER`; `pymupdf/RAG` →
  `pymupdf/pymupdf4llm`.
* `AutoGPTQ` and `AutoAWQ` are **archived** upstream (`archived=true`; last pushes 2025-04-11 and
  2025-05-11).
* `MemoryBank-SiliconFriend` (2023-05-24), `noahshinn/reflexion` (2025-01-14), `parthsarthi03/raptor`
  (2024-09-03), `OpenBMB/InfiniteBench` (2024-09-25), `THUDM/LongBench` (2025-01-15),
  `vectara/vectara-answer` (2025-05-08), `google-research/tuning_playbook` (2024-06-18) are dormant.

**Implication:** every catalog row pins a commit SHA and records `checked_date`, `upstream_last_pushed` and
`upstream_archived`. Dormant is not disqualifying for *reference code* (RAPTOR, RULER generators) but is
disqualifying for a *dependency in a maintained system* without a vendoring plan.

### F7 — Most "learning" systems are untested on the property SAM-X cares about *(inspected)*

Across `reflexion`, `self-refine`, `textgrad`, `opro`, `voyager`, `expel`, `ace`, `dspy`: all demonstrate
improvement on the tasks they were built for. None of the bundled material demonstrates **retention over
unrelated sessions**, **transfer to a different document class**, or **regression prevention** — the three
properties objective 7 asks for. Those must be constructed locally (Phase 6 of the roadmap). This is a gap
in the field, not a gap in the search.

### F8 — Resource-footprint reality check *(estimate, from inspected documentation)*

Server-class components were rejected on footprint: Milvus (etcd + MinIO + Pulsar), Weaviate and Qdrant
(server daemons), Vespa (JVM), Airflow (scheduler + webserver + metadata DB), Temporal (server + DB),
Dagster (daemon + webserver), RAGFlow (multi-container Compose stack), gVisor (container runtime), E2B
(remote paid sandboxes). Against a reported laptop with limited spare RAM, the embedded/in-process set —
SQLite + FTS5 + `sqlite-vec` + `diskcache` + DuckDB with `memory_limit` + Polars streaming + `river`
(constant memory by design) — is the only tier that fits without measurement heroics. All footprint
statements here are **estimates from documentation**, not measurements on the target machine; Phase 0
converts them into numbers.

---

## 2. Workstream findings

Full detail, adoption steps and unresolved gaps: see each workstream README.

### 01 — Low-RAM computing → [workstreams/01-low-ram/](workstreams/01-low-ram/README.md)

* **Strongest approach:** SQLite-anchored spine with an *enforced* resident ceiling (`diskcache` spill),
  exact token budgets (`tiktoken`), and independent measurement (`psutil` RSS **and** PSS).
* **Key distinction, documented throughout:** application RAM ≠ system RAM ≠ VRAM ≠ disk. `mmap`-backed
  indexes (Faiss `OnDiskInvertedLists`, USearch) move bytes out of process RSS into the OS page cache —
  which still counts against a machine with little spare RAM. Reporting only process RSS would hide the
  real pressure.
* **Hidden allocations found in inspected docs:** Dask worker processes each re-import and can re-load
  models; joblib/loky workers multiply model RAM; DuckDB's `memory_limit` is advisory for some operators;
  Transformers' `device_map="auto"` can silently spill to disk and stall; llama.cpp KV-cache size grows
  with context length independently of weight size.
* **Startup overhead and process lifetimes:** Ollama's `keep_alive` (docs bundled) is the concrete lever —
  a resident daemon has an idle cost, per-call CLI invocation has a start cost. Both must be measured, not
  assumed; the experiment is written in the catalog row.
* **Concurrency limits:** SQLite is single-writer; `sqlitedict` assumes one writer; two readers on one file
  need WAL and a tested race path (Phase 7 exit criterion).
* **Rejected:** Dask as the *primary* mechanism (heavy; sequential document walk does not need it),
  memory-profiler as a dependency (unmaintained since 2022-10-19).

### 02 — Historical data and storage → [workstreams/02-data-storage/](workstreams/02-data-storage/README.md)

* **Strongest approach:** directory-per-generation + manifest (schema, provenance, source, retrieval
  timestamp, hash) + atomic publish (temp → verify hash → rename) + rollback by repointing. This is 80% of
  what Delta Lake provides, without a native dependency. `delta-rs` is catalogued as the upgrade path if
  concurrent readers and time travel become real needs.
* **Observations vs estimates** must be separate typed columns; `pandera` (MIT) is the enforcement
  mechanism recommended, with Great Expectations recorded as the overlapping alternative (and its upstream
  org move to Fivetran noted).
* **Missing timestamps do not prove market closures.** Recorded as a rule, with the required alternative:
  a gap record carrying a *reason* (`closure`, `no-trade`, `vendor-gap`, `unknown`) — `unknown` being the
  honest default.
* **Data-source risk, verified:** `yfinance` is an unofficial client (Apache-2.0 code, no data licence, no
  SLA); back-adjusted prices can silently rewrite history, which is fatal for reproducible backtests. The
  catalog experiment (fetch the same symbol/day twice, 7 days apart, diff the series) is designed to
  produce that evidence locally.
* **Continuity risk, verified:** `twopirllc/pandas-ta` unresolvable; fork `pandas-ta-classic` catalogued
  with the caveat that library defaults are never document parameters.
* **Rejected:** Zarr as the primary format (v2/v3 transition is a live migration risk), DVC as a dependency
  (a sha256 manifest is a few lines).

### 03 — Whole-document reading → [workstreams/03-document-reading/](workstreams/03-document-reading/README.md)

* **Recommended text path:** `pypdf` (BSD-3) for page maps/outlines/metadata + `pdfminer.six` (MIT) for
  layout-aware extraction, with **disagreement between the two treated as an extraction-error signal**, not
  resolved by preference. `markitdown` (MIT) as the single normalisation step *only if* page provenance
  survives conversion — that is the pre-declared rejection criterion in its catalog row.
* **Tables:** `camelot` (MIT) with human cell-by-cell verification, because a missed table row means an
  invented or dropped parameter.
* **Licence-gated alternatives documented, not adopted:** PyMuPDF (AGPL/commercial), MinerU (Apache +
  additional terms), Marker/Surya (Apache code + OpenRAIL-M weights), Docling (MIT code, weights need
  approval).
* **Scans and diagrams:** the first fix is *detection* — an image-only page is a distinct state from an
  empty page. OCR (tesseract, Apache-2.0) is deferred until the coverage report shows image-only pages that
  matter.
* **Central rule:** extraction and indexing do not establish understanding. Coverage is reported as
  pages-extracted / image-only / failed / hash-mismatched, alongside every score.

### 04 — Semantic interpretation → [workstreams/04-semantic-interpretation/](workstreams/04-semantic-interpretation/README.md)

* The eight confusions are implemented as a **typed extraction contract** with four allowed states per
  field: `specified`, `partially_specified` (what is known recorded), `absent_from_source`, `ambiguous`.
* **Useful partial information is preserved without inventing the rest** — that is the whole point of the
  fourth state. A library default may be recorded as a hypothesis and never as a parameter.
* **Invented-parameter count is a hard-zero acceptance criterion** in
  [EVALUATION_PLAN.md](EVALUATION_PLAN.md) §5: one invention fails the run.
* **Different scope/version ≠ contradiction** is handled by the temporal-validity columns from Rank 3: two
  facts from two document versions can both be true with non-overlapping validity intervals.
* Benchmark evidence (LongBench, ∞Bench, NovelQA, RULER, FILM/IN2, "Lost in the Middle", "Same Task, More
  Tokens") is catalogued with the explicit caveat that these are **public-benchmark** results on other
  models and other document classes; two of the arXiv identifiers commonly cited in this area could not be
  confirmed and are flagged rather than asserted (HELMET; and 2105.07538 resolved to a *different* paper
  than expected — a VAR anomaly-detection paper, which turned out to be relevant to workstream 10).

### 05 — Retrieval and evidence → [workstreams/05-retrieval-evidence/](workstreams/05-retrieval-evidence/README.md)

* **Lexical first** (SQLite FTS5 / `rank_bm25`), dense second, graph only if a documented failure demands
  it. Justification is recorded as an experiment, not an opinion.
* **Hierarchical retrieval** via the RAPTOR tree pattern (full MIT implementation bundled) for
  *location only*; summaries live in `hypotheses`.
* **Freshness** is a retrieval filter, not a post-hoc warning: a stale source is excluded or flagged at
  query time using validity intervals.
* **Entailment** is the gate. Citation-completeness metrics from ALCE/ARES/RAGTruth/TRUE are catalogued;
  `long-form-factuality`'s decomposition approach (composite licence, scoped in the manifest) is the
  bundled reference, with the caveat that its SAFE rater is a hosted model judging a model.
* **Rejected on resource fit:** Vespa, RAGFlow, Milvus, Weaviate, Qdrant-server. **Recorded as
  alternatives, not additions:** LlamaIndex / LangChain / Haystack / txtai — at most one, and the
  recommendation is to borrow their schemas instead.

### 06 — Memory → [workstreams/06-memory/](workstreams/06-memory/README.md)

* Four stores with write authority + temporal validity in SQL (Rank 3). Bundled reference code:
  `graphiti` nodes/edges (bi-temporal), `letta` (paging architecture), `a-mem`, `memorybank`, `cognee`
  chunk-ownership, `MemOS` vocabulary, and the memory-survey evaluation dimensions (arXiv:2404.13501v1,
  verified).
* **Retrieval failure must be distinguishable from non-existence.** This is a schema requirement (a query
  log with outcomes), not a nicety.
* **Saving bytes is not learning and not zero forgetting.** Retention probes and transfer sets are the
  only accepted evidence.
* **Contradiction handling:** flag, never merge. Deletion is replaced by interval closure so history stays
  auditable.
* **Prompt-injection is a memory-poisoning vector**, verified by paper metadata: PoisonedRAG
  (arXiv:2402.07867v3, USENIX Security 2025) reports ~90% attack success injecting five texts into a
  corpus of millions. Therefore memory writes require provenance and may never alter risk, holding or
  approval parameters.

### 07 — Self-learning → [workstreams/07-self-learning/](workstreams/07-self-learning/README.md)

* **External-memory adaptation** (procedures, lessons, prompts) is separated from **parameter updates**
  (fine-tuning, RL). PEFT/Unsloth are catalogued and **rejected** for this project: laptop resource fit,
  plus the reproducibility/contamination problem of weights changing underneath a frozen benchmark.
* **Curricula** are represented as ordered, scoped procedures with preconditions — a procedure that fires
  with an unmet precondition must refuse.
* **Regression prevention** is the frozen Phase 1 suite re-run after every change; **retention** is the
  re-ask probe; **transfer** is a third document class. All three are exit criteria in Phase 6.
* ACE's itemised, append-only playbook growth (Apache-2.0) is adopted as a pattern because it avoids
  whole-context rewrites; its published gains are the authors' and are not reproduced here.

### 08 — Independent evaluation → [workstreams/08-independent-evaluation/](workstreams/08-independent-evaluation/README.md)

* The full protocol is [EVALUATION_PLAN.md](EVALUATION_PLAN.md). Tooling: Inspect AI (MIT) concepts or a
  150-line equivalent; HF Evaluate for metric definitions; DeepEval/RAGAS/promptfoo for assertion
  vocabulary; HELM for report shape; lm-evaluation-harness for its **decontamination** practice (its
  benchmarks are not run).
* **New sources** are mandatory: the two already-indexed documents are contaminated by prior exposure and
  may be used only for mechanical/coverage tests.
* **Immutability**: write-once run directories, new `run_id` per re-run, overwrite attempts fail loudly.
* **Failures preserved** as a first-class artefact, with reasons.

### 09 — Research and backtesting → [workstreams/09-research-backtesting/](workstreams/09-research-backtesting/README.md)

* **Reproducibility**: one config artefact pinning every decision — Qlib's `workflow_config_*.yaml`
  benchmark files (13 bundled, MIT) are the model.
* **Costs/slippage/timing/stop-first**: `zipline-reloaded`'s `slippage.py`, `commission.py`, `controls.py`
  (Apache-2.0, bundled) and Freqtrade's `stoploss.md` (GPL-3.0, bundled) are the inspectable references.
  Stop-first handling on a bar where both stop and target are touched is called out as a semantic decision
  that must be written down and tested, because engines differ.
* **Look-ahead prevention**: truncation-equivalence test (decisions at ≤ T bit-identical with and without
  post-T data) plus completed-bar-only resampling. Freqtrade ships a lookahead-analysis doc; the concept is
  re-implemented rather than the GPL code copied.
* **Multiple testing**: MIT-licensed `ml4t` scripts bundled (`07_multiple_testing.py`,
  `06_ic_inference.py`, `05_signal_evaluation.py`, `03_label_methods.py`,
  `04_maximum_favorable_adverse_excursion.py`). Rule adopted: **no strategy is promoted on a naive Sharpe
  alone**; the trial count and an adjusted metric are reported together.
* **Separation of test kinds**: synthetic engineering tests ≠ observed-market research ≠ live-performance
  evidence. The collection contains no live-performance evidence and does not claim any.
* **Licensing findings**: vectorbt (Commons Clause), backtesting.py (AGPL-3.0), Backtrader (GPL-3.0),
  Freqtrade (GPL-3.0), mlfinlab (proprietary, rejected, dormant since 2023). The López de Prado books are
  metadata-only; their MIT-licensed companion code is bundled instead.

### 10 — Unfamiliar market conditions → [workstreams/10-unfamiliar-conditions/](workstreams/10-unfamiliar-conditions/README.md)

* **Recommended:** `river` (BSD-3) drift detectors (ADWIN/DDM/KSWIN/HDDM) for **constant-memory**
  monitoring; `ruptures` (BSD-2) change points with a **fixed, recorded** penalty; `MAPIE` (BSD-3)
  conformal intervals whose nominal-vs-realised coverage gap is itself the unfamiliarity signal;
  `hmmlearn` (BSD-3) if latent states are wanted, with the state labels recorded as hypotheses.
* **The goal is recognising unsupported situations, not claiming reliable performance everywhere.** A
  strategy-suitability gate refuses to run a procedure outside the scope recorded for it.
* **Licensing finding:** Alibi Detect is BSL 1.1 (non-production until change date) — recorded as the
  reason `river` is preferred.
* **Verified paper lead:** arXiv:2105.07538v1 (Maeng, Eckley, Fearnhead) — collective anomaly detection in
  high-dimensional VAR models with Type-I error control. Relevant because most ad-hoc drift detectors have
  no false-alarm guarantee. PDF not bundled (access + licence).
* **Unknowns:** threshold selection, false-alarm budget, and whether any of it transfers between symbols
  and regimes. All are experiment parameters, not defaults.

### 11 — Risk and execution reliability → [workstreams/11-risk-execution/](workstreams/11-risk-execution/README.md)

* **Research only.** No order was placed, no credential configured, no venue contacted. CCXT's Manual
  (522 KB, MIT, bundled) is used as a *factual map* of per-venue capabilities: client order ids
  (idempotency), partial-fill reporting, error taxonomy, rate limits.
* **Order idempotency**: deterministic key = hash(intent + parameters + window), stored before acting;
  retries replay the recorded outcome. Vendor design references are metadata-only (their docs are not
  redistributable and were unreachable for download).
* **Reconciliation**: an explicit `unknown` outcome state that **refuses to act** is required; a timeout
  must never be resolved by assumption.
* **Stale-data refusal**: data older than a declared horizon blocks the dependent step.
* **Risk representation**: exposure limits, sizing, stop/target and holding rules as typed objects with
  unit tests plus a pre-trade veto gate (`zipline/finance/controls.py` pattern, bundled). NautilusTrader's
  RiskEngine docs (LGPL-3.0) are bundled as the strongest open design reference; the platform is not
  adopted (it would replace existing components).

### 12 — Operations and monitoring → [workstreams/12-operations-monitoring/](workstreams/12-operations-monitoring/README.md)

* **An ambiguous timeout must not automatically cause duplicate work** — implemented as idempotency keys
  plus a state check before retry, with `tenacity` (Apache-2.0) expressing the policy declaratively so it
  is auditable.
* **Checkpoints** as artefact targets (Luigi pattern, Apache-2.0): a step is complete iff its output exists
  with a recorded hash; resume by existence.
* **Process ownership** via a SQLite run log (run_id, task, state, attempt, timestamps, checkpoint path,
  outcome); **cancellation** and **bounded retries** recorded per attempt.
* **Telemetry**: `prometheus_client` metric shapes written to a local file/SQLite rather than running a
  Prometheus server; `rich` for terminal dashboards; alerts on declared thresholds only, each actionable.
* **Rejected:** Airflow (scheduler + webserver + metadata DB), Temporal (server), Dagster (daemon) —
  footprint, plus overlap with a ~100-line run log.

### 13 — Local models and optional APIs → [workstreams/13-models-apis/](workstreams/13-models-apis/README.md)

* **Blocked on hardware questions Q1–Q3.** No model choice, no RAM figure and no quantisation level is
  committed anywhere in this collection.
* **Bundled and ready:** the complete *Google LLM Tuning Playbook* (CC BY 4.0, 120 KB of text — the only
  fully redistributable long-form technical report in the collection), llama.cpp performance/KV-cache/MLX/
  Vulkan docs, Ollama `faq`/`modelfile`/`gpu`/`api`/`import`/`troubleshooting` docs, Transformers
  `model_memory_anatomy` + quantisation + `perf_infer_cpu` docs, PEFT/LoRA guides, lmdeploy KV-cache
  quantisation docs, bitsandbytes docs, and the typed API surfaces of the OpenAI/Anthropic/Google SDKs.
* **Terms verification is mandatory and not done here:** pricing/quota pages are metadata-only (they change
  often, are not redistributable, and were unreachable for download). Rule recorded: never assume a free
  tier is unlimited or permanent; never propose quota evasion or account rotation.
* **Weights licensing**: Apache-2.0 / Llama community licence / OpenRAIL-M / custom — must be read on each
  model card at adoption time. HF was unreachable for download, so no card is bundled.
* **Rejected:** vLLM (GPU-first), lmdeploy as an engine, AutoGPTQ and AutoAWQ (**archived upstream**),
  Unsloth/PEFT (fine-tuning category), E2B (paid remote sandboxes).

### 14 — Security and isolation → [workstreams/14-security-isolation/](workstreams/14-security-isolation/README.md)

* **Bundled in full:** OWASP Top 10 for LLM Applications **2025** — the 10.7 MB official PDF plus all
  eleven vulnerability markdown files (CC BY-SA 4.0, licence verified). Three entries map directly onto
  SAM-X: LLM01 prompt injection, LLM08 vector/embedding weaknesses, LLM10 unbounded consumption (the RAM
  budget *is* a security control).
* **Verified threat evidence:** indirect prompt injection (arXiv:2302.12173v2), AgentDojo
  (arXiv:2406.13352v3), InjecAgent (arXiv:2403.02691v3, ACL 2024 Findings — ReAct-prompted GPT-4 vulnerable
  24% of the time), PoisonedRAG (arXiv:2402.07867v3, USENIX Security 2025).
* **Controls, all labelled *proposed* until demonstrated:** sandboxed parsing (`nsjail` config + schema
  bundled; OS rlimits as the portable fallback), a source/sink inventory for dynamic execution (`bandit`
  finds sinks, `semgrep` taint rules find paths), pinned hash-locked dependencies with `pip-audit` advisory
  checks, secret scanning (`gitleaks` rules bundled, `detect-secrets`, and a `git grep` over all revisions
  of this repository — zero findings, recorded in [RESEARCH_LOG.md](RESEARCH_LOG.md)), and a fixed reviewed
  tool set with **no generated-code execution**.
* **Structural containment over detection:** the reading/research path has no tool that can place an order
  or alter a risk parameter. This is asserted as a design requirement and must be verified by code
  inspection — it is not demonstrated by anything in this collection.
* **Recorded trap:** TruffleHog (AGPL-3.0) verifies findings by making network calls with the discovered
  credential. Never run that against credentials you do not own.

---

## 3. Negative results and things that did not work

1. **Nine shortlisted repository slugs did not resolve** (HTTP 404 via the GitHub API on 2026-10-14):
   `grantjenks/free-diskcache` (correct slug `python-diskcache`), `polars-dev/polars` (`pola-rs/polars`),
   `twopirllc/pandas-ta`, `NovelQA/novelqa`, `gregkamradt/needle-in-a-haystack` (`gkamradt/...`),
   `ShengranHu/ACE` (`ace-agent/ace`), `patrickchao/self-adapting-llms`, `stanfordfordlp/helm`
   (`stanford-crfm/helm`), `centre-borelli/ruptures` (`deepcharles/ruptures`), `M4LC0N/crepes`. Four were
   my own slug errors and were corrected; the rest are genuine upstream changes or removals. `crepes` could
   not be resolved on GitHub at all and is catalogued from PyPI registry metadata only.
2. **Two arXiv identifiers I expected to be correct were wrong.** `2409.12181` is not HELMET; `2105.07538`
   is not the conformal-prediction introduction (it is a VAR anomaly-detection paper). Both are recorded as
   verified findings and the affected entries are flagged. Several other identifiers are explicitly marked
   *not verified this session* rather than asserted.
3. **One collection had to be undone.** `yixuantt/MultiHop-RAG` has no licence; three downloaded files were
   deleted and replaced with a metadata-only record. This is the licence audit working as intended.
4. **Paper PDFs could not be bundled at all** despite being the most obviously useful artefact class — for
   two independent reasons (network egress, and arXiv's licence not granting redistribution). Worked around
   by bundling the two fully redistributable long-form documents that do exist in scope (Google's CC BY 4.0
   tuning playbook, OWASP's CC BY-SA 4.0 Top 10) plus verified metadata for 31 papers.
5. **Vendor documentation sites were unreachable for download**, so several components are catalogued from
   registry metadata plus repository docs only (`pyarrow`, `zarr`, `sentence-transformers`, `crepes`).
   Their `evidence_status` says so.
6. **Nothing was executed.** No RAM figure, latency figure, accuracy figure or compatibility claim in this
   collection is a measurement. Every number attributed to an upstream project is either quoted from its
   own documentation (and labelled) or explicitly marked as not reproduced.

## 4. What would most change these conclusions

| If | Then |
|---|---|
| Measured spare RAM is very small (Q1/Q2) | Rank 1 and Rank 5 still hold (they are storage work). Rank 2's 128K-token runs become infeasible; local generative reading is off the table and the design must work with retrieval + abstention only |
| The two indexed documents cannot be used for evaluation (Q4) | Phase 1 cannot start until another held-out corpus exists — this is the most likely schedule blocker |
| R5's key was not frozen before outputs (Q6) | 13/32 is not a baseline; Phase 1 must establish one, and every comparison to R5 in this collection becomes void |
| SAM-X already executes model-generated code (Q9) | Workstream 14 becomes Phase 1 and the rest waits |
| A hosted API is already authorised and in use (Q8) | Workstream 13 shifts from "measure local fit" to "budget, queue, defer, and audit egress", and terms must be re-verified on that date |
