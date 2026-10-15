# RISKS AND UNKNOWNS

Everything that could make this collection misleading, and everything this collection does not know.

Two categories, kept separate on purpose:

* **§1 Risks** — things that could go wrong or be misread, with mitigation and owner.
* **§2 Unresolved information requirements** — specific facts needed before certain decisions can be made.
  These are questions for the user, not guesses to be filled in.

Severity scale: **High** = could produce a wrong trading-relevant decision or a licence violation.
**Medium** = could waste significant effort or produce an unfalsifiable claim. **Low** = housekeeping.

---

## 1. Risks

### R-A. Evidence and interpretation

| # | Risk | Sev | Why it matters | Mitigation | Status |
|---|---|---|---|---|---|
| A1 | **A bundled component is read as an endorsement** — "it is in the collection, so it must work" | High | 112 of 169 rows are `needs-more-evidence`. None was executed | Classification column; every row carries `evidence_status`; [START_HERE.md](START_HERE.md) §5 forbids reading inclusion as endorsement | Mitigated by design |
| A2 | **Upstream claims are treated as reproduced results** | High | Many READMEs report speedups and accuracy gains measured by their authors on other tasks | Catalog rows separate `findings_from_source` from anything SAM-X could claim; [EVALUATION_PLAN.md](EVALUATION_PLAN.md) §8 separates test kinds | Mitigated by design |
| A3 | **A summary is cited as evidence** | High | This is objective 3's failure mode. No bundled tool prevents it | Rank 3 four-store split; summaries are `hypotheses`; the evidence gate blocks any answer whose evidence is a hypothesis | Proposed — must be implemented and tested |
| A4 | **A matching quote or valid citation id is taken as support** | High | Explicitly named in the objective; ALCE (arXiv:2305.14627v2, verified) shows ~50% incomplete citation support even in good systems | Quote-presence **and** entailment both scored; abstention is a first-class outcome | Proposed |
| A5 | **Inventing a setup parameter to complete a table** | High | One invented parameter can invalidate a whole research result | `invented-parameter` count is a hard-zero acceptance criterion; four field states including `absent_from_source` | Proposed |
| A6 | **Reported context is silently upgraded into verified fact** | Medium | R1–R7 are user-reported; nobody has seen the code, the machine or the evaluation key | Labels enforced everywhere; Q1–Q10 in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4 keep them open | Mitigated by design |
| A7 | **Small denominators produce confident conclusions** | Medium | 13/32 has a wide interval | CIs or exact tests required for headline numbers; comparison counts recorded and corrected | Proposed |
| A8 | **Contamination is assumed away** | Medium | Public benchmarks and 2023–24 datasets are in training corpora | Every item records model training cutoff vs item/source dates; `contamination-risk` items reported separately | Proposed |

### R-B. Resources and operations

| # | Risk | Sev | Why it matters | Mitigation | Status |
|---|---|---|---|---|---|
| B1 | **No component's footprint was measured on the target machine** | High | Every "fits in low RAM" statement here is an estimate from documentation | Phase 0 resource trace is blocking; `RESOURCE_BUDGET.md` must exist before adoption | Open — needs the user's machine |
| B2 | **The build sandbox is not the target machine** | Medium | 3 939 MB RAM / 0 swap / 2 CPUs / ~20 GB free here tells you nothing about the laptop | Stated explicitly in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4 Q1–Q3 | Open |
| B3 | **`mmap`-backed indexes reduce process RSS but not machine pressure** | Medium | Reporting only RSS would hide the real constraint | Both RSS and PSS plus available memory are measured; the distinction is documented in workstream 01 | Proposed |
| B4 | **Server-class components get installed "just to try"** | Medium | Milvus/Weaviate/Qdrant-server/Vespa/Airflow/Temporal/RAGFlow would not fit | 15 rows classified `rejected` on resource fit with reasons; [REJECTED_OPTIONS.md](REJECTED_OPTIONS.md) | Mitigated by design |
| B5 | **Disk-cache spill makes latency unusable** | Medium | A reader that is correct but too slow will be bypassed | p95 latency is an acceptance criterion with a pre-declared ceiling | Proposed |
| B6 | **Repository growth** | Low | 24 MB now; GitHub file/repo limits and LFS policy were checked before upload | Single largest file 10.72 MB (OWASP PDF); no archives; LFS not used; a ~100 MB revisit threshold is recorded in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §8 | Mitigated |

### R-C. Licensing and rights

| # | Risk | Sev | Why it matters | Mitigation | Status |
|---|---|---|---|---|---|
| C1 | **AGPL/copyleft code reaches a networked service** | High | PyMuPDF (AGPL or commercial), backtesting.py (AGPL), TruffleHog (AGPL), NautilusTrader (LGPL), Freqtrade/Backtrader (GPL) | Copyleft components are catalogued as **reference semantics only**, never vendored; `resources/licenses/INDEX.md` lists every one | Mitigated by design |
| C2 | **A weight licence differs from the code licence** | High | Marker/Surya: Apache-2.0 code, **modified OpenRAIL-M weights**; Docling weights separate | Recorded per component; no weights bundled; weights adoption is an approval gate | Mitigated by design |
| C3 | **A material with no licence is copied** | High | Already happened once — `yixuantt/MultiHop-RAG`; three files were downloaded then deleted | Licence audit ran over all 871 assets; 0 `review-required`, 0 `not-permitted` remain; MO-01 records the case | **Resolved** |
| C4 | **arXiv PDFs are redistributed** | Medium | arXiv's non-exclusive licence does not grant third-party redistribution; PDFs inside permissive repos inherit the paper's licence | Zero paper PDFs bundled; 31 papers are metadata-only with verified identifiers | Mitigated |
| C5 | **Commons Clause / BSL / additional terms are missed** | Medium | vectorbt (Commons Clause: no selling), Alibi Detect (BSL 1.1: non-production until change date), MinerU (Apache + additional terms), LiteLLM (MIT except `enterprise/`) | All four recorded in catalog rows and in the licences index | Mitigated |
| C6 | **Attribution notices are dropped** | Medium | CC BY 4.0 (tuning playbook), CC BY-SA 4.0 (OWASP), MIT/BSD notice requirements | [ATTRIBUTION.md](ATTRIBUTION.md) at the repo root; 155 upstream licence texts bundled verbatim; manifest records attribution per asset | Mitigated |
| C7 | **Held-out evaluation sources get committed** | Medium | Would destroy the evaluation's value | Keys and held-out sources stay outside the repo; only provenance templates and hashes are published | Proposed |

### R-D. Security

| # | Risk | Sev | Why it matters | Mitigation | Status |
|---|---|---|---|---|---|
| D1 | **A downloaded document contains an embedded instruction that gets executed** | High | Verified literature: Greshake et al. arXiv:2302.12173v2; InjecAgent arXiv:2403.02691v3 (ACL 2024 Findings, ReAct-GPT-4 vulnerable 24%); AgentDojo arXiv:2406.13352v3 | Untrusted-document parsing in a sandbox with no network and enforced limits; parsed text is data, never instructions; the reading path has no order-placing or risk-altering tool | Proposed — must be demonstrated |
| D2 | **Retrieval corpus poisoning** | High | PoisonedRAG arXiv:2402.07867v3 (USENIX Security 2025): five injected texts → ~90% attack success over a corpus of millions; the paper reports evaluated defenses as insufficient | Provenance on every memory write; writes may never alter risk/holding/approval parameters; source allowlist | Proposed |
| D3 | **A hostile document exhausts resources during parsing** | Medium | A decompression bomb or a pathological layout can OOM a small machine | rlimits/cgroups in the sandbox; parse timeout; page-size and file-size caps before extraction | Proposed |
| D4 | **A secret is committed** | Medium | The user pasted a GitHub PAT into chat during this engagement | A credential-pattern scan ran over all new files and over every revision of this repository's history: zero findings. **The exposed PAT must still be revoked by its owner — it was exposed in chat, which is outside this repository** | Repo clean; token revocation is the user's action |
| D5 | **A scanner makes live network calls with discovered credentials** | Medium | TruffleHog verifies by default — running it against credentials you do not own is a real incident | Recorded as a trap in the catalog row and in workstream 14; `gitleaks` (rules bundled) and `detect-secrets` are the offline recommendations | Mitigated by documentation |
| D6 | **Downloaded repository scripts get executed** | High | Standing constraint: every downloaded asset is untrusted | Nothing was executed during this build; the validation scripts are read-only and offline; workstream 14 requires hash-locked pinned dependencies before any install | Mitigated |
| D7 | **Supply-chain drift under a pinned name** | Medium | Verified during the check window: `iterative/dvc` → `treeverse/dvc`; `great-expectations/great_expectings` → `fivetran/great_expectations`; `twopirllc/pandas-ta` 404 | Every row pins a commit SHA; `upstream_last_pushed` and `upstream_archived` recorded; re-verify at adoption time | Mitigated by design |

### R-E. Scope and claims

| # | Risk | Sev | Why it matters | Mitigation | Status |
|---|---|---|---|---|---|
| E1 | **The collection is read as a guarantee of capability** | High | It is a resource collection, not a working system | No promise of perfect reading, unlimited learning, universal market handling, guaranteed RAM savings or trading profits appears anywhere; [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §2 lists the explicit non-goals | Mitigated |
| E2 | **Something in the collection gets treated as trading advice or a strategy** | High | Backtesting references are semantics sources | Every workstream 09/10/11 row states research-only; no strategy, signal or parameter set is recommended | Mitigated |
| E3 | **SAM-X is assumed to have been changed** | Medium | It was not, and must not be | Confirmed in [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) and in the final report; this repository contains no SAM-X code | Mitigated |
| E4 | **Work is duplicated because the collection is hard to navigate** | Low | 871 files across 169 components | `RESOURCE_CATALOG.csv` + `ASSET_MANIFEST.json` + per-workstream READMEs + `scripts/validate_catalog.py` | Mitigated |

---

## 2. Unresolved information requirements

These are **questions**, not gaps to be filled by assumption. Until answered, the dependent decisions stay
open. Full text in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4; the blocking ones are repeated here with
what each blocks.

| # | Question | Blocks | Why it cannot be guessed |
|---|---|---|---|
| **Q1** | What is the actual machine — CPU, total RAM, RAM already committed, swap, free disk, disk throughput, OS? | Every resource-fit decision; workstreams 01, 13 | "Limited spare RAM" is a description, not a number. A 4 GB and a 24 GB machine admit completely different designs |
| **Q2** | What is the peak RSS of one existing end-to-end SAM-X job, measured? | The declared memory ceiling for the reader | Nothing in this collection measured SAM-X |
| **Q3** | How much disk is free, and what is its sustained read throughput? | Whether the disk-backed spill tier is viable at all | A spill tier on a slow disk can make p95 latency unusable (risk B5) |
| **Q4** | What rights does the project hold over the two indexed documents, and can a third, previously unexposed document of the same class be obtained for evaluation? | Phase 1 (the whole evaluation plan); every capability claim | Rights and availability are facts about the user's situation. If the answer is no, held-out evaluation cannot start |
| **Q5** | What is the existing disk-backed prototype's storage schema and interface? Does it record a page map and per-page hashes? | Phase 3 (extend vs replace) | Reuse is preferred (reported position R7) but cannot be planned against an unknown interface |
| **Q6** | For the rejected reader qualification (13/32, 0/4): were the items and key frozen **before** the candidate produced outputs? Who authored them? Is the scorer still available? | Whether R5 is a usable baseline | If the key moved, the number is uninterpretable and Phase 1 must build a new baseline |
| **Q7** | Does the existing system summarise, and if so are summaries ever returned as evidence or stored as facts? | Whether risk A3 is live today | This determines whether Phase 2 is urgent or merely prudent |
| **Q8** | Is any hosted model API already authorised, and under what budget and data-handling terms? | Workstream 13 (local vs hosted); egress and privacy controls | Starting a paid service is outside this engagement's authorisation; terms must be read on the adoption date, not quoted from memory |
| **Q9** | Does SAM-X execute model-generated or downloaded code anywhere? | **The entire phase order** — if yes, workstream 14 becomes Phase 1 | This is the single highest-leverage unknown in the collection |
| **Q10** | Are the trading/risk/approval/holding-rule/open-position safeguards enforced in code, in configuration, or by convention? | Whether Phase 2's schema change can be done safely, and what "do not touch safeguards" concretely means | A convention is not a control; the answer changes how much care Phase 2 needs |

### Additional unknowns that cannot be resolved from outside

* Whether any bundled component is **already present** in SAM-X's environment, and at what version —
  compatibility cannot be asserted without an inventory (reported position R7 asks for reuse; reuse
  requires knowing what exists).
* Whether the existing system has a **test suite** and a CI, which determines how much of Phase 1 can be
  automated.
* The **document classes** SAM-X must actually read (broker specifications? research reports? regulatory
  filings? vendor manuals?). The whole evaluation design depends on this, and it is not stated anywhere in
  the reported context.
* Whether outputs are consumed by **humans or by downstream code**. If downstream code parses them, the
  typed-contract work in Phase 5 becomes the highest-value item rather than Phase 3.

### What was checked and could not be checked

| Area | Checked | Could not be checked |
|---|---|---|
| Licences | All 871 bundled assets; 155 upstream licence texts read; 0 review-required, 0 not-permitted | Vendor ToS/pricing pages (unreachable, and not redistributable); HF model/dataset cards (host unreachable) |
| Existence and integrity | SHA-256 + size recorded for every asset; `scripts/verify_asset_hashes.py` re-checks offline | Nothing beyond existence: no asset was executed, imported or parsed |
| Upstream liveness | `pushed_at`, `archived`, star count, HEAD SHA for 137 repositories | Future liveness; the reason behind the `dvc` and `great_expectations` org moves |
| Paper metadata | 31 papers verified against the arXiv API on 2026-10-14 | Paper full texts (no binary download route, and no redistribution right); 46 additional identifiers remain unverified and are labelled as such |
| SAM-X | Nothing | Everything — no access was available or sought |
| Internet coverage | Broad across GitHub, PyPI, npm registry, arXiv metadata, and official repository docs | Not exhaustive, and not claimed to be. No browsing result was fabricated |
