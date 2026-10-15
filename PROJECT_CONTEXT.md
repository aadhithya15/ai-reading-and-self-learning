# PROJECT CONTEXT

This document separates **what was reported to us** from **what was verified during this build**, states
the constraints that shaped every recommendation, and lists the questions that must be answered before
any hardware-specific or spend-specific commitment is made.

Read this before [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md). Recommendations here are conditional
on §4.

---

## 1. Objective

Upgrade SAM-X into a **resource-efficient trading research bot** that can:

1. Interpret unfamiliar documents rather than reproduce memorised benchmark answers.
2. Navigate documents, chapters and pages with **bounded memory**.
3. Use summaries to *locate* information, then **reopen the original passage to verify** an answer.
4. Recognise exceptions, partial constraints, unsupported claims, missing information and genuine
   contradictions.
5. **Avoid inventing setup parameters.**
6. Maintain separate stores for source-linked **facts**, reusable **procedures**, independently reviewed
   **lessons**, and unverified **hypotheses**.
7. Demonstrate **learning transfer** to different sources, plus retention and safe handling of stale or
   conflicting information.
8. Conduct **reproducible** historical research and backtesting.
9. Handle unfamiliar conditions, uncertainty, resource shortages and failures **conservatively**.
10. Preserve source separation, protected holdouts, trading, risk, approvals, holding rules and
    open-position safeguards.

### Explicit non-goals

Perfect understanding · unlimited learning · benchmark overfitting · guaranteed trading profits ·
replacing the whole system · adding overlapping infrastructure where a compatible existing component
would do.

### The design stance that follows from the objective

Everything in this collection is chosen to make SAM-X **fail loudly and abstain** rather than fail
silently and confabulate. Three consequences appear repeatedly:

* **Evidence before infrastructure.** A lexical baseline (BM25 / SQLite FTS5) must be measured before any
  vector, graph or hybrid retrieval is justified.
* **Separation before capability.** Four memory stores with provenance are a prerequisite for trusting any
  "learning" claim, because saving bytes is not learning and self-critique is not supervision.
* **Measurement before optimisation.** RAM and runtime are first-class metrics alongside correctness.
  A method that improves accuracy by 3 points while exceeding the memory budget is a rejection, not a win.

## 2. Reported current position (NOT independently verified)

The following was **reported by the project owner**. Nothing in this section was confirmed during the
build, because SAM-X itself was out of scope: it was not read, run, modified or connected to anything.

| # | Reported | Status | Why it matters |
|---|---|---|---|
| R1 | Existing Python system with local inference, document processing, historical research, data collection and trading safeguards | **reported** | Sets the "reuse over replace" mandate and the Python-centric component shortlist |
| R2 | Limited spare laptop RAM; exact hardware and headroom unconfirmed | **reported — must be measured** | Every resource-fit conclusion is conditional on this. See §4 Q1–Q3 |
| R3 | Several low-RAM research tools and prototypes exist; some routes are opt-in rather than deployed | **reported** | Overlap risk: new components must be justified against what already exists |
| R4 | A disk-backed navigation prototype indexed 147 pages across two existing documents | **reported** | The only concrete scale figure available. Indexing is not comprehension — see §3 |
| R5 | One frozen reader qualification scored 13/32 exact field judgments and 0/4 fully correct cases; that candidate was rejected | **reported** | The baseline to beat. Its denominator (32 judgments / 4 cases) is small; see §4 Q6 |
| R6 | Reliable summaries, unfamiliar-source interpretation and demonstrated learning transfer remain unfinished | **reported** | These three are the actual gaps; the rest is supporting work |
| R7 | Reuse of compatible existing components is preferred | **reported** | Used as a hard filter in [REJECTED_OPTIONS.md](REJECTED_OPTIONS.md) |

**Consequence:** no claim in this repository depends on R1–R7 being true. Where a recommendation would
change if a reported fact is wrong, that dependency is stated explicitly.

## 3. What WAS verified during this build

Verification was limited to public sources reachable from the build environment. It says nothing about
SAM-X internals.

| Finding | Evidence |
|---|---|
| 144 upstream repositories were resolvable and pinned to a specific commit SHA | `ASSET_MANIFEST.json` → `upstream_commit` per repository, `upstream_git_blob_sha` per file |
| 871 files were downloaded with SHA-256 recorded at download time | `ASSET_MANIFEST.json`; re-checkable with `scripts/verify_asset_hashes.py` |
| 9 upstream repositories in the shortlist could not be resolved (HTTP 404 through the GitHub API on 2026-10-14) | [RESEARCH_LOG.md](RESEARCH_LOG.md) §3 |
| `twopirllc/pandas-ta` is unresolvable; only community forks exist | GitHub API 404 + search; row `pandas-ta-classic` in the catalog |
| `yixuantt/MultiHop-RAG` has **no licence file** → no redistribution right | repository root listing via API; two files downloaded in an early pass were deleted |
| Alibi Detect moved to **Business Source License 1.1** (non-production use only until a per-version change date) | licence text read in full, bundled at `resources/licenses/alibi-detect/` |
| vectorbt is **Commons Clause over Apache-2.0** (redistribution allowed, selling not) | licence text read in full, bundled |
| PyMuPDF is **AGPL-3.0 or Artifex commercial** (dual licensed) | PyPI metadata snapshot, bundled |
| Marker and Surya are **Apache-2.0 code + modified OpenRAIL-M weights** | both licence texts bundled; no weights downloaded |
| MinerU is Apache-2.0 **plus additional terms** | licence text bundled |
| LiteLLM is MIT **except the `enterprise/` directory** | licence text bundled; nothing from `enterprise/` collected |
| `AutoGPTQ` and `AutoAWQ` are **archived** upstream | GitHub API `archived=true`, last pushes 2025-04-11 / 2025-05-11 |
| `google-research/tuning_playbook` is **CC BY 4.0** and its full text is redistributable | licence read; 120 KB of text bundled |
| OWASP Top 10 for LLM Applications is **CC BY-SA 4.0**, including the 2025 PDF | licence read; PDF + 11 markdown files bundled |
| arXiv:2409.12181 is **not** the HELMET paper (it is Lu et al., "A Controlled Study on Long Context Extension and Generalization in LLMs") | arXiv API query, 2026-10-14 |
| RULER's published finding: models near-perfect on vanilla needle-in-a-haystack drop sharply with length and task complexity; of models claiming ≥32K context only about half held up at 32K | arXiv:2404.06654v3 metadata verified via API |
| PoisonedRAG reports ~90% attack success injecting 5 texts into a corpus of millions | arXiv:2402.07867v3 metadata verified; USENIX Security 2025 |

**Interpretation of R4 in light of the above.** A 147-page index across two documents is a *navigation*
achievement. RULER (verified) shows that retrieval-style success on synthetic long-context probes
coexists with large failures on tasks requiring aggregation and multi-hop tracing. So R4 should be read
as "the plumbing exists", never as "the reading works". The reported R5 result (13/32 exact fields, 0/4
fully correct cases) is consistent with that reading.

## 4. Open questions that block commitments

These could not be answered from inside the build. They are ordered by how much they change the plan.

| # | Question | Why it blocks | How to answer |
|---|---|---|---|
| **Q1** | What is the actual machine? CPU model, core count, total RAM, RAM already committed, GPU present (and VRAM), OS, Python version | Determines whether local inference is viable at all; whether MLX (Apple-only), llama.cpp CPU, or a hosted API is the right path; whether an OCR/layout model can be loaded | `uname -a`, `nproc`, `free -m` (or `sysctl hw.memsize`), `python3 -V`, and a 5-minute idle-RAM baseline with nothing else running |
| **Q2** | What is the measured **spare** RAM during a normal SAM-X run, not the idle figure | "Limited spare RAM" is not a budget. Every recommendation in workstream 01 needs a number and a safety margin | Instrument with psutil for one full existing job; record peak RSS and available memory (see the experiment in catalog row `psutil`) |
| **Q3** | Is disk space and disk speed adequate for a disk-backed index and cache | Disk-backed navigation trades RAM for I/O; a slow disk can make it worse than a smaller in-RAM index | Measure free space, and sequential/random read throughput on the intended volume |
| **Q4** | What are the two already-indexed documents, and what are the rights to store/quote them | Determines whether they can be used as evaluation sources at all, and whether a held-out set must come from elsewhere | Owner confirms document class, licence and confidentiality |
| **Q5** | What exactly does the existing disk-backed navigation prototype store, and what is its interface | Decides reuse vs replacement — the central "prefer compatible components" constraint | Owner points at the module; a 30-minute read is enough |
| **Q6** | What were the 32 field judgments and 4 cases in the rejected qualification? Was the key frozen before outputs? Was the evaluator independent? | 13/32 on a 32-item denominator has a wide confidence interval; and if the protocol was not frozen, the number is not comparable to the next candidate | Owner supplies the frozen item set, key and outputs — or accepts that the baseline must be re-established under [EVALUATION_PLAN.md](EVALUATION_PLAN.md) |
| **Q7** | What is the current summarisation path, and is a summary ever used as evidence | If summaries are cited as evidence, that is the highest-priority defect: summaries are hypotheses, not facts | Owner identifies the code path |
| **Q8** | Is any hosted API already authorised, with what budget and what data-egress approval | Determines whether requirement 13 work is "design the deferral path" or "already spending" | Owner confirms; pricing/terms must then be re-verified on official pages on that date |
| **Q9** | Does SAM-X currently execute any model-generated or downloaded code | If yes, workstream 14 moves from P2 to P1 immediately | Code inspection for `eval`/`exec`/`subprocess`/`pickle.load` reachable from untrusted input |
| **Q10** | Are the trading safeguards (risk limits, approvals, holding rules, open positions) enforced in code or by convention | Requirement 10/11 assume they are preserved; the collection must not weaken them | Owner confirms where they live; nothing in this collection may alter them |

Until Q1–Q3 are answered, treat every RAM figure in this collection as a **template with a blank**, not a
recommendation. No hardware-specific commitment is made anywhere in this repository.

## 5. Constraints that shaped the collection

| Constraint | Effect on the collection |
|---|---|
| Limited spare laptop RAM (reported) | Server-class options rejected on resource fit: Milvus, Weaviate, Qdrant server, Vespa, Airflow, Temporal, RAGFlow, Zep server, gVisor, E2B. Embedded/in-process options preferred: SQLite + `sqlite-vec`, `diskcache`, DuckDB with `memory_limit`, Polars streaming, River (constant memory by design) |
| Reuse over replacement | Frameworks (LlamaIndex, LangChain, Haystack, DSPy) are catalogued as **pattern sources** with narrow adoption experiments, not as wholesale replacements |
| Python-centric existing system | Python-first shortlist; C#/Go/Rust-only tools are documented as references (LEAN, Gitleaks, nsjail) with the integration cost stated |
| Research-only mandate | No live-trading component was configured. CCXT/Freqtrade/Hummingbot/ib_async are catalogued for their *documentation of execution reality*, with an explicit no-orders boundary |
| No weights/datasets without approval | Model-dependent components (Docling, MinerU, Marker, Surya, docTR, deepdoctection, bitsandbytes, HHEM) are gated behind an approval step, and the gate is written into their experiment |
| Licensing | AGPL/BSL/Commons-Clause/OpenRAIL-M findings are recorded as decision points, not silently accepted. One component set was **removed** during the licence audit (MultiHop-RAG) |
| Single repository, no splitting | Everything is here; larger bundles were avoided rather than moved to Releases/LFS (see §6) |

## 6. Storage decisions

Checked against GitHub's published limits before uploading (see [RESEARCH_LOG.md](RESEARCH_LOG.md) §5):

* **Small permitted assets are in the repository directly** — all 871 files, 20.40 MB total.
* **GitHub Releases were not used.** No single bundle justified it; the largest file is 10.7 MB, well
  inside normal repository limits, and splitting assets away from the manifest would break the
  "discoverable from the master README" requirement.
* **Git LFS was not used.** It adds quota, bandwidth and access implications (LFS objects require
  authentication for some access paths and count against separate storage/bandwidth quotas) for no
  benefit at 20 MB. If this collection grows beyond roughly 100 MB, LFS or Releases should be revisited —
  that threshold is recorded so the decision is not re-litigated from scratch.
* **Nothing was split into other repositories.**
* Assets are stored **once** and referenced from many workstream READMEs. No duplicate PDFs. Every
  directory has a purpose documented in the relevant workstream README or in
  `resources/licenses/INDEX.md`.
* Whole repositories, archives, weights and datasets were deliberately not downloaded.

## 7. Glossary used consistently across this collection

| Term | Definition used here |
|---|---|
| **Fact** | A claim that resolves to a specific passage in a specific source at a specific version, with the quote recorded. Facts are never model-written. |
| **Procedure** | A reusable, declarative recipe: preconditions, ordered steps, validation, and the scope in which it was shown to work. Not arbitrary generated code. |
| **Lesson** | A generalisation accepted only after **independent** review (human, frozen key, or a verifiable external signal). Model self-critique does not qualify. |
| **Hypothesis** | Anything model-generated that has not been independently confirmed — including every summary. Hypotheses may inform search; they may never be cited as evidence. |
| **Bounded memory** | A declared, enforced ceiling on resident bytes for a component, measured (not estimated), with a defined spill/evict behaviour when the ceiling is reached. |
| **Reopen-and-verify** | Before an answer is emitted, the cited original passage is re-read from the source of record and the claim is checked against it. A summary match is not verification. |
| **Abstention** | A first-class output: "the document does not specify this", "the source is stale", "confidence is below the declared floor", "resource budget exhausted". Abstention is scored, not penalised. |
| **Held-out source** | A document the candidate has never seen, whose items and keys were frozen before any output, and which is excluded from every prompt-tuning and optimisation loop. |
| **Generation** | An immutable, hash-identified snapshot of historical data. Publication is atomic; readers see either the old or the new generation, never a partial one. |
| **Attempted denominator** | The count of items the system actually attempted, reported alongside accuracy, so that abstention cannot be hidden by shrinking the denominator. |

## 8. Where to go next

* [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) — the five strongest opportunities.
* [EVALUATION_PLAN.md](EVALUATION_PLAN.md) — how to prove any of them without fooling yourself.
* [RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) — what would invalidate them.
* [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) — the operational handoff.
