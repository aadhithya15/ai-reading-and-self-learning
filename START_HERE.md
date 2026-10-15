# START HERE

You have been given one repository URL and no conversation. This page tells you what the collection is,
how to read it efficiently, what is already known, and what to do first.

**If you read nothing else, read §1, §2 and §6.** Everything else is reference.

---

## 1. What this repository is

A research and resource collection built on **2026-10-14** to support upgrading **SAM-X** — an existing
Python system that does local inference, document processing, historical research, data collection and
trading-safeguard enforcement — into a **resource-efficient trading research bot** that can read and
interpret *unfamiliar* documents.

It is **not**:

* a report you can skim and act on without checking the evidence labels;
* a list of links (871 actual files are bundled, each with a recorded upstream commit and SHA-256);
* an installation guide (nothing here was installed, run, benchmarked or proven);
* a claim that SAM-X's problems are solved.

It **is**:

* 169 assessed components across 14 workstreams, each with the SAM-X problem it addresses, what was
  inspected, its licence and redistribution status, its resource needs, its limitations, a conservative
  fallback, and one bounded experiment that could accept or reject it;
* the licence-checked primary material needed to evaluate them offline;
* an evaluation design that keeps held-out sources out of every optimisation loop;
* an honest list of what is unknown, blocked or unverified.

## 2. Ten-minute path

1. [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — objectives, constraints, and the crucial split between
   **reported** context and **verified** findings. §4 lists the questions that must be answered before any
   hardware-specific commitment.
2. [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) — the five strongest opportunities and why simpler
   alternatives were considered insufficient (or sufficient) in each case.
3. [RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) §1–§3 — what could invalidate the recommendations.
4. [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) — the operational handoff: what is ready for a bounded
   trial, what needs evidence, what needs authorisation.

## 3. Sixty-minute path

Add, in this order:

5. [RESEARCH_REPORT.md](RESEARCH_REPORT.md) — findings for all 14 workstreams, with the negative results
   and the licensing discoveries that change what may be adopted.
6. [EVALUATION_PLAN.md](EVALUATION_PLAN.md) — how a candidate is frozen, how held-out sources are
   prepared, what is measured (correctness, meaning, evidence, abstention, attempted denominators, RAM,
   runtime), and what pre-declared criteria accept or reject it.
7. [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — the sequence, with an exit criterion per phase.
8. The workstream READMEs relevant to the first phase. Every workstream README follows the same shape:
   requirements and purpose → strongest approaches and alternatives → bundled assets (relative links) →
   official upstream references → adoption steps → resource implications → qualification requirements →
   rejected approaches → unresolved gaps.

| Workstream | Directory | One-line framing |
|---|---|---|
| 01 Low-RAM computing | [workstreams/01-low-ram/](workstreams/01-low-ram/README.md) | Turn "limited spare RAM" into a measured, enforced budget |
| 02 Historical data & storage | [workstreams/02-data-storage/](workstreams/02-data-storage/README.md) | Immutable generations, provenance, observations ≠ estimates |
| 03 Whole-document reading | [workstreams/03-document-reading/](workstreams/03-document-reading/README.md) | Coverage, page maps, tables, exceptions — indexing ≠ understanding |
| 04 Semantic interpretation | [workstreams/04-semantic-interpretation/](workstreams/04-semantic-interpretation/README.md) | The eight confusions that produce invented parameters |
| 05 Retrieval & evidence | [workstreams/05-retrieval-evidence/](workstreams/05-retrieval-evidence/README.md) | A matching quote or valid citation id does not support an answer |
| 06 Memory | [workstreams/06-memory/](workstreams/06-memory/README.md) | Four stores, provenance, invalidation; saving bytes ≠ learning |
| 07 Self-learning | [workstreams/07-self-learning/](workstreams/07-self-learning/README.md) | Checked mistakes, transfer, retention; self-critique ≠ supervision |
| 08 Independent evaluation | [workstreams/08-independent-evaluation/](workstreams/08-independent-evaluation/README.md) | Frozen candidates/questions/keys, leakage prevention, preserved failures |
| 09 Research & backtesting | [workstreams/09-research-backtesting/](workstreams/09-research-backtesting/README.md) | Reproducibility, look-ahead, multiple testing, overfitting |
| 10 Unfamiliar conditions | [workstreams/10-unfamiliar-conditions/](workstreams/10-unfamiliar-conditions/README.md) | Recognise unsupported situations; do not claim universal performance |
| 11 Risk & execution reliability | [workstreams/11-risk-execution/](workstreams/11-risk-execution/README.md) | Exposure, sizing, idempotency, reconciliation, stale-data refusal |
| 12 Operations & monitoring | [workstreams/12-operations-monitoring/](workstreams/12-operations-monitoring/README.md) | Ownership, checkpoints, bounded retries; a timeout must not duplicate work |
| 13 Local models & optional APIs | [workstreams/13-models-apis/](workstreams/13-models-apis/README.md) | Resource fit, licensing, costs, quotas, graceful deferral |
| 14 Security & isolation | [workstreams/14-security-isolation/](workstreams/14-security-isolation/README.md) | Documents are an attack surface; proposed ≠ demonstrated |

## 4. Where the actual material is

```
resources/
  papers/                  PAPER_INDEX.md — 31 verified + 46 recorded-but-unverified identifiers
  documentation/           599 files: upstream docs, READMEs, guides + 124 PyPI metadata snapshots
                           _metadata-only/  records for artefacts that may not be bundled
  code-examples/           86 files: inspectable implementations (RULER generators, RAPTOR tree,
                           zipline risk controls, ML4T multiple-testing, graphiti temporal edges…)
  configurations/          26 files: real config examples (Qlib workflow YAMLs, freqtrade configs,
                           RULER synthetic.yaml, gitleaks rules, nsjail sandbox.cfg…)
  benchmark-descriptions/   5 bundled descriptions (LongBench/HELMET/NIAH/∞Bench/AgentBench)
                           + BENCHMARK_NOTES.md (why public benchmarks are not qualification evidence)
  diagrams/                4 original SVGs + README: bounded-memory reading pipeline, four-store
                           memory, evidence gate and abstention, frozen evaluation protocol
  licenses/                155 upstream licence texts + INDEX.md
```

Every file is listed in [ASSET_MANIFEST.json](ASSET_MANIFEST.json) with: `asset_id`, related
`component_ids`, `original_url`, `retrieval_api_url`, `retrieval_date`, `local_path`, `file_size_bytes`,
`sha256`, `upstream_repo`, `upstream_path`, `upstream_commit`, `git_blob_sha`, licence fields,
`redistribution_status`, `verification_limits` and `access_limits`.

## 5. How to trust (or not trust) any statement here

Each catalog row carries an `evidence_status` field. The vocabulary used across the collection:

| Label | Meaning |
|---|---|
| **measured** | A number produced by an observation recorded in this repository |
| **verified** | Confirmed against a primary source during this build (official API, licence text, repository inventory) |
| **inspected** | The artefact was read (docs/code/licence) but not run |
| **estimate** | Reasoned expectation, not a measurement. Always labelled as such |
| **reported** | Asserted by the project owner or an upstream author; not independently confirmed |
| **proposed** | A design that has not been implemented or demonstrated |
| **unknown** | Not determined. Treated as unknown, never as favourable |

Popular repositories, star counts and README claims are treated as **leads**, never as reliability
evidence. Published benchmark gains are never presented as SAM-X gains.

## 6. What to do first (concrete, in order)

1. **Answer the hardware questions** in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4. Every resource-fit
   recommendation is conditional on them, and none of them were answerable from inside this build.
2. **Run the two validators** (`scripts/validate_catalog.py`, `scripts/verify_asset_hashes.py`) so you are
   working from an intact collection.
3. **Freeze an evaluation** before changing any code: build the held-out source set and answer keys
   described in [EVALUATION_PLAN.md](EVALUATION_PLAN.md) §3–§5, using
   [templates/experiment-contract.md](templates/experiment-contract.md). The prior reported qualification
   result (13/32 exact field judgements, 0/4 fully correct cases, candidate rejected) is only
   interpretable against a frozen, leakage-controlled protocol.
4. **Pick ONE recommendation** from [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) and run its bounded
   experiment with the pre-declared acceptance/rejection criteria. Do not adopt three things at once.
5. Record the outcome in a [templates/evaluation-report.md](templates/evaluation-report.md), preserving
   failures. A rejected candidate is a result, not a setback.

## 7. What you must NOT do

* Do not modify SAM-X's live trading policy, risk limits, approval flow, holding rules or open-position
  safeguards as a side-effect of a research experiment.
* Do not place orders, connect to an exchange or broker, or start a paid service.
* Do not execute anything under `resources/`. It is untrusted-by-default reference material: read it,
  copy patterns from it deliberately, and never `pip install -e` or run it in place.
* Do not download model weights or large datasets without explicit approval — several catalog entries
  require them, and that requirement is recorded as a gate, not as a task to complete silently.
* Do not treat bundled documentation snapshots as current. Each has a `retrieval_date` and an
  `upstream_commit`; re-verify before relying on anything time-sensitive (pricing, quotas, terms).
* Do not publish held-out questions or answer keys. Templates exist so the protocol can be shared while
  the keys stay private.
* Do not assume a "free" hosted tier is unlimited or permanent, and never propose quota evasion or
  account rotation.

## 8. Scope and access limits of the build itself

Recorded in full in [RESEARCH_LOG.md](RESEARCH_LOG.md) §1–§2 and in `ASSET_MANIFEST.json` →
`global_access_limitations`. Summary: the build sandbox could download binaries only from
`github.com`, `codeload.github.com`, `api.github.com`, `pypi.org`, `files.pythonhosted.org` and
`registry.npmjs.org`. `arxiv.org`, `huggingface.co`, `openreview.net`, `aclanthology.org`,
`proceedings.mlr.press` and vendor documentation sites were reachable for **reading text only**. That is
why no paper PDFs, model weights or HF dataset archives are bundled, and why 8 resources are
metadata-only entries with official links. Coverage is broad but **not exhaustive**, and no browsing
result is fabricated: every bundled file has a retrieval URL, a commit SHA and a digest.
