# SAM-X — Master Research and Resource Collection

**Purpose.** A single, self-contained, source-backed research collection for upgrading **SAM-X** into a
resource-efficient trading-research bot that can *interpret unfamiliar documents* rather than recite
benchmark answers, *navigate long documents with bounded memory*, *verify answers by reopening the
original passages*, and *learn safely* — separating source-linked facts from reusable procedures,
reviewed lessons and unverified hypotheses.

**This repository is the entry point.** It is designed to be handed to another AI or another engineer
as a bare URL, with no accompanying conversation. Start at **[START_HERE.md](START_HERE.md)**.

Collection built **2026-10-14** (UTC). Everything here is either (a) a licence-checked copy of a public
artefact, with its exact upstream commit recorded, or (b) original analysis written for this collection.
Nothing was executed, installed or traded.

---

## 1. What is in here, in numbers

| Thing | Count | Where |
|---|---|---|
| Unique assessed components (catalog rows) | **169** | [RESOURCE_CATALOG.csv](RESOURCE_CATALOG.csv) |
| Bundled asset files | **871** | `resources/` + [ASSET_MANIFEST.json](ASSET_MANIFEST.json) |
| Total bundled size | **20.40 MB** (20,398,632 bytes) | largest single file 10.7 MB |
| Bundled PDFs | **1** (OWASP Top 10 for LLM Applications 2025, CC BY-SA 4.0) | `resources/documentation/owasp-llm-top10/` |
| Bundled documentation files (`.md`/`.rst`/`.txt`/`.mdx`) | **599** | `resources/documentation/` |
| Bundled code examples (`.py`/`.cs`/`.sh`) | **86** | `resources/code-examples/` |
| Bundled configuration examples (`.yaml`/`.json`/`.toml`/`.yml`) | **26** | `resources/configurations/` |
| Bundled benchmark descriptions/harnesses | **5** | `resources/benchmark-descriptions/` |
| Bundled upstream licence texts | **155** | `resources/licenses/` (+ [INDEX](resources/licenses/INDEX.md)) |
| Package-registry metadata snapshots (PyPI JSON API) | **124** | `resources/documentation/_pypi-metadata/` |
| Upstream repositories pinned by commit SHA | **144** | `ASSET_MANIFEST.json` → `upstream_commit` |
| Metadata-only resources (lawfully cannot be bundled) | **8** | `ASSET_MANIFEST.json` → `metadata_only_resources` |
| Research papers catalogued with verified metadata | **31** | [resources/papers/PAPER_INDEX.md](resources/papers/PAPER_INDEX.md) |
| Workstreams covered | **14 / 14** | [workstreams/](workstreams/) |
| Recommendations classified `trial-ready` | **42** | catalog column `classification` |
| Recommendations classified `needs-more-evidence` | **112** | catalog column `classification` |
| Recommendations classified `rejected` | **15** | catalog column `classification` |

**Honesty note on those numbers.** "Bundled" means the bytes are in this repository at the recorded path
with a recorded SHA-256. It does **not** mean the component was installed, run, benchmarked or found
suitable. No collected code was executed during this build — see
[RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) §1 and the `evidence_status` column of every catalog row.

## 2. Navigation

**Read first**

| File | What it gives you |
|---|---|
| [START_HERE.md](START_HERE.md) | 10-minute and 60-minute reading paths; what to do first; what not to do |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Objectives, constraints, **reported vs verified** facts, open questions |
| [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) | Everything the next agent needs, including leakage precautions |

**Decisions**

| File | What it gives you |
|---|---|
| [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) | The five strongest opportunities, ranked, with qualification experiments |
| [RESEARCH_REPORT.md](RESEARCH_REPORT.md) | Full findings across all 14 workstreams |
| [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) | Sequenced phases, each with an exit criterion |
| [EVALUATION_PLAN.md](EVALUATION_PLAN.md) | Independent qualification design: freeze, holdouts, metrics, gates |
| [REJECTED_OPTIONS.md](REJECTED_OPTIONS.md) | What was rejected and **why** — prevents re-litigating settled questions |
| [RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) | Unknowns, blockers, unverified claims, licensing hazards |
| [RESEARCH_LOG.md](RESEARCH_LOG.md) | Dated log of searches, access limits, decisions, and the licence audit |

**Machinery**

| Path | What it is |
|---|---|
| [RESOURCE_CATALOG.csv](RESOURCE_CATALOG.csv) | 169 rows × 23 columns: one row per unique component |
| [ASSET_MANIFEST.json](ASSET_MANIFEST.json) | 871 assets: URL, retrieval date, commit, size, SHA-256, licence, limits |
| [ATTRIBUTION.md](ATTRIBUTION.md) | Third-party notices by licence family, and what was deliberately not collected |
| [workstreams/](workstreams/) | 14 directories, one README each: requirements, approaches, adoption steps, gaps |
| [resources/](resources/) | `papers/ documentation/ code-examples/ configurations/ benchmark-descriptions/ diagrams/ licenses/` |
| [resources/diagrams/](resources/diagrams/README.md) | 4 original SVGs: the reading pipeline, the four memory stores, the evidence gate and abstention, the frozen evaluation protocol |
| [templates/](templates/) | Experiment contract, component assessment, evaluation report, source provenance |
| [scripts/](scripts/) | `validate_catalog.py`, `verify_asset_hashes.py` — structure/links/existence/hashes only |

Shared assets are stored **once** under `resources/` and referenced from the workstream READMEs; there are
no duplicated PDFs and no unexplained folders.

## 3. The objective, in one paragraph

SAM-X must read documents it has never seen, find the relevant chapter and page with bounded memory,
quote the original passage to support every claim, notice when a document only *partially* specifies
something (and refuse to invent the rest), keep four clearly separated kinds of memory, prove that what
it learned transfers to a different source, and run reproducible historical research — all on a laptop
with limited spare RAM, without touching live trading policy, and without placing orders.
We are explicitly **not** seeking perfect understanding, unlimited learning, benchmark overfitting, or
guaranteed trading profits.

## 4. Safety boundaries observed while building this

* SAM-X itself was **not** modified, started, or connected to anything. No service was activated.
* No trade was placed; no exchange or broker credentials were configured or used.
* No dependency was installed and **no collected code was executed**. Files were read for licence and
  content inspection only. The two scripts in `scripts/` were authored here and validate structure — they
  never import, run or network-fetch anything they check.
* No model weights, datasets or unrelated repositories were downloaded.
* No private code, documents, credentials, account data or trading data was uploaded. The conversation
  that produced this collection is not in this repository.
* Source, holdout, risk, approval, holding-rule and open-position safeguards were not touched.
* No paywall or access control was bypassed. Where an artefact could not lawfully be bundled, it is a
  metadata-only entry with its official link and the reason.
* A credential that was pasted into the originating chat was **not** used, **not** stored and **not**
  committed; it should be revoked by its owner. Publication used the sandbox's own GitHub connection.

## 5. Verify it yourself

```bash
python3 scripts/validate_catalog.py      # CSV/JSON structure, links, existence, counts, secret scan
python3 scripts/verify_asset_hashes.py   # recompute SHA-256 for all 871 bundled assets
```

Both are read-only and offline. `verify_asset_hashes.py` compares against the digests recorded at
download time; a mismatch means the file changed since collection and must be investigated before use.

## 6. Repository history and the previous deliverable

The repository contained exactly one committed file when this build started: a placeholder `README.md`
from commit `10bb5f6` ("Fresh start"), which itself announced that the SAM-X collection would live here.
There were no other prior deliverables, no uncommitted changes and no third-party contributions to
preserve. That state is recoverable:

* archive branch: `archive/pre-samx-collection`
* archive tag: `archive/fresh-start-pre-collection`

Both point at `10bb5f611486450400069b076d425d6a9b3940b1`. They are deliberately **not** linked from this
README's navigation, per the requirement to keep the old archive separate from the new collection.
No history was rewritten, no force-push was performed, and repository visibility was not changed.

## 7. Licence of this collection

* Third-party material is redistributed under its own licences — see [ATTRIBUTION.md](ATTRIBUTION.md)
  and `resources/licenses/INDEX.md`. Every bundled file's licence and redistribution decision is recorded
  in `ASSET_MANIFEST.json`.
* Original material written for this collection (all analysis, cataloguing, templates, plans, diagrams in
  `resources/diagrams/`) is provided as-is, without warranty, for the SAM-X project's internal research
  use. It is not affiliated with, reviewed by, or endorsed by any upstream project mentioned.

## 8. What this collection does not promise

No perfect reading. No unlimited learning. No handling of every market condition. No guaranteed RAM
savings. No trading profits. No claim that any component here is installed, compatible or proven — every
such statement in this repository is labelled as measurement, estimate, proposal or unknown.
