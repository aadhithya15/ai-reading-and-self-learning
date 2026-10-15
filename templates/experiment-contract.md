# EXPERIMENT CONTRACT — <short name>

> **Fill this in and commit it BEFORE the experiment runs.** An experiment whose contract was written
> afterwards is not an experiment; it is a story.
>
> Rules this template enforces:
> * the candidate, the items, the keys and the scorer are **frozen by hash before any output exists**;
> * acceptance and rejection criteria are **pre-declared**, so a bad result cannot be re-argued;
> * the **unchanged baseline** is named, so "improvement" means something;
> * **negative cases** are pre-declared, so abstention is scored rather than guessed at;
> * measurements are separated from estimates, and unknowns are marked unknown;
> * failures are preserved, not summarised away.
>
> Delete every `<...>` placeholder. If you cannot fill a field, write `UNKNOWN — <what is needed to find
> out>`. Never invent a value: an invented parameter in a contract is as damaging as an invented parameter
> in an answer.

---

## 0. Identification

| Field | Value |
|---|---|
| Contract id | `<EXP-YYYYMMDD-nn>` |
| Title | `<one line>` |
| Author / agent | `<name or agent id>` |
| Date written | `<YYYY-MM-DD>` — must be **before** the first run |
| Workstream(s) | `<e.g. 03-document-reading, 08-independent-evaluation>` |
| Catalog rows involved | `<component ids from RESOURCE_CATALOG.csv>` |
| Related recommendation | `<e.g. TOP_RECOMMENDATIONS.md Rank 1>` |
| Roadmap phase | `<e.g. Phase 3>` |
| Status | `draft` \| `frozen` \| `running` \| `reported` \| `abandoned` |

## 1. Hypothesis

State it so that it can be **false**.

> `<One or two sentences. Name the mechanism, the measurable outcome and the direction.
>  Example: "Adding a reopen-and-verify step reduces unsupported answers by at least X without pushing
>  p95 latency past Y, because the failure mode is answering from summary context rather than from the
>  source passage.">`

What would convince you the hypothesis is **wrong**? `<...>`

## 2. Unchanged baseline

| Field | Value |
|---|---|
| Baseline name / version | `<exact identifier of what runs today, unchanged>` |
| Baseline commit or config hash | `<sha>` |
| Why this is the right comparison | `<...>` |
| Known baseline numbers (with source and date) | `<measured / reported / unknown>` |

The baseline is **not modified** during this experiment. If it must change, that is a new contract.

## 3. Candidate

| Field | Value |
|---|---|
| Candidate id / version | `<...>` |
| Commit or build hash | `<sha>` |
| Prompt / config hash | `<sha256 of the exact prompt and config files>` |
| Retrieval configuration | `<index type, chunking, top-k, reranker, filters>` |
| Model(s) | `<name, version, provider, training cutoff date if known>` |
| What changed versus baseline | `<the single variable, ideally>` |
| Dependencies and versions | `<name==version, ...>` |

## 4. Comparability of access, context and compute

Everything that differs between baseline and candidate must be listed. Anything not listed is assumed
identical, and an unlisted difference invalidates the comparison.

| Dimension | Baseline | Candidate | Identical? |
|---|---|---|---|
| Input documents / sources | `<...>` | `<...>` | yes / no — `<difference>` |
| Context available per query | `<tokens>` | `<tokens>` | yes / no |
| Retrieval depth (top-k) | `<...>` | `<...>` | yes / no |
| Machine (CPU, RAM, swap, disk) | `<...>` | `<...>` | yes / no |
| Runtime / interpreter versions | `<...>` | `<...>` | yes / no |
| Concurrency | `<...>` | `<...>` | yes / no |
| Network access | `<none / which hosts>` | `<none / which hosts>` | yes / no |
| Random seeds | `<...>` | `<...>` | yes / no |
| Cost budget | `<...>` | `<...>` | yes / no |

## 5. Evaluation sources and leakage control

| Field | Value |
|---|---|
| TRAIN sources | `<ids>` — used for tuning only |
| VALIDATION sources | `<ids>` — every look logged |
| **TEST / held-out sources** | `<ids>` — opened once |
| TRANSFER sources | `<ids>` — different class, never tuned on |
| Item count per set | TRAIN `<n>` · VALID `<n>` · TEST `<n>` · TRANSFER `<n>` · NEGATIVE `<n>` |
| Item file hash | `<sha256>` |
| **Key file hash** | `<sha256>` — the key itself is stored `<location outside the candidate's read scope>` |
| Who authored the items and keys | `<person/agent>` — and their relationship to the candidate owner |
| Were keys frozen before outputs? | yes / no — **if no, stop and fix this first** |
| Contamination check | For each item: candidate model training cutoff `<date>` vs item creation `<date>` vs source publication `<date>`. Items at risk are flagged `contamination-risk` and reported separately |
| Rights to use these sources | `<confirmed / NOT confirmed — see PROJECT_CONTEXT.md Q4>` |
| Provenance record | `<path to a filled templates/source-provenance.json per source>` |

Sources previously exposed to the candidate (including anything it has already indexed) are **not**
held-out and may not support a capability claim.

## 6. Pre-declared negative cases

Each must have an **expected behaviour**, usually abstention with a label.

| # | Case | Expected behaviour |
|---|---|---|
| N1 | Required information absent from the source | Report `absent_from_source`; do not guess; do not substitute a library default |
| N2 | Constraint is only partially specified | Report `partially_specified` with what *is* known; do not complete it |
| N3 | An exception or carve-out qualifies a general rule | Report the rule **and** the exception |
| N4 | Two sources genuinely contradict | Report the contradiction; do not merge or silently pick one |
| N5 | Two sources differ only in scope or version | Report both with their validity intervals; **not** a contradiction |
| N6 | Source is stale / superseded | Use the current source; flag the stale one |
| N7 | Query has no answer in the corpus | Abstain; do not produce a plausible answer |
| N8 | A quote exists but does **not** entail the claim | Reject the claim; abstain |
| N9 | Retrieval fails although the fact exists | Report retrieval failure — distinguishable from "does not exist" |
| N10 | Resource exhaustion mid-run (memory ceiling, timeout, quota) | Fail conservatively; record the state; no partial answer presented as complete |
| N11 | Hostile content in the document (embedded instruction, path traversal, resource bomb) | Treat as data; no tool invocation; no write outside the sandbox |
| N12 | `<domain-specific case>` | `<...>` |

## 7. Measurements

Separate **measured** from **estimated**. Anything estimated says so in the value column.

| Metric | Instrument | Baseline target | Candidate acceptance threshold | Measured / estimated |
|---|---|---|---|---|
| Exact-field correctness | `<scorer>` | `<n>` | `<n>` | |
| Fully-correct-case rate | `<scorer>` | `<n>` | `<n>` | |
| Quote-presence (citation literally on cited page) | `<scorer>` | `<n>` | 100% | |
| Entailment (cited passage supports the claim) | `<scorer/model>` | `<n>` | `<n>` | |
| Unsupported-answer rate | `<scorer>` | `<n>` | `<n>` | |
| Abstention rate, and correctness of abstention | `<scorer>` | `<n>` | `<n>` | |
| **Attempted denominator** | count | — | reported next to every rate | |
| Invented-parameter count | `<scorer>` | 0 | **0 (hard)** | |
| Confusion-classification accuracy (eight confusions) | `<scorer>` | `<n>` | `<n>` | |
| Peak RSS / peak PSS / minimum available memory | `psutil`, independent sampler | `<MB>` | `≤ <MB>` | |
| Wall time p50 / p95 | timer | `<s>` | `≤ <s>` | |
| Tokens in / out, and cost | `<counter>` | `<n>` | `≤ <n>` | |
| Cold-start time, index build time | timer | `<s>` | `≤ <s>` | |
| On-disk footprint | `du` | `<MB>` | `≤ <MB>` | |
| Crash / timeout / retry count | run log | `<n>` | `≤ <n>` | |

Sampling interval, sampler process and sampler version: `<...>`. The candidate does not self-report its
own resource use.

## 8. Acceptance, rejection and inconclusive criteria

**ACCEPT if all hold** (pre-declared, no post-hoc additions):

1. `<...>`
2. `<...>`
3. `<...>`

**REJECT if any hold:**

1. Any invented parameter.
2. Any cited quote not present on the cited page.
3. Any answer whose evidence is a summary (a hypothesis) rather than a source passage.
4. Peak resource use above the declared ceiling without a recorded spill/degradation event.
5. A failure case missing from the log.
6. The key, an item or the scorer changed after freeze.
7. Accuracy improved while the attempted denominator shrank.
8. `<...>`

**INCONCLUSIVE** (a legitimate outcome, recorded as such): too few items for the observed effect size;
environment drift between runs; a dependency changed mid-run; `<...>`.

Statistical handling: `<CI method or exact test>`; number of configurations compared `<n>`; correction
applied `<Bonferroni / Holm / none — and why>`.

## 9. Regression, retention and transfer

| Test | What it uses | Threshold |
|---|---|---|
| Regression | The frozen suite from the previous accepted candidate | no degradation beyond `<tolerance>` |
| Retention | Re-ask `<n>` previously answered items after `<n>` unrelated sessions | no decay beyond `<tolerance>` |
| Transfer | The TRANSFER source set, never tuned on | score `≥ <threshold>` |

## 10. Artefacts to preserve

All of these, in a write-once location, per [EVALUATION_PLAN.md](../EVALUATION_PLAN.md) §6:

* [ ] this contract, hashed, with the freeze timestamp
* [ ] candidate and config hashes
* [ ] item file (without keys) and the key file **hash**
* [ ] raw outputs, one record per item, including abstentions and failures
* [ ] per-claim evidence records (cited page, quote, quote-presence result, entailment result)
* [ ] independent resource trace
* [ ] scores with denominators, intervals and comparison counts
* [ ] the completed [evaluation-report.md](evaluation-report.md)
* [ ] **every failure case, verbatim, with the reason it failed**

Re-running creates a new run id. Overwriting an existing run is a protocol violation.

## 11. Authorisation and safety

| Question | Answer |
|---|---|
| Does this experiment install a dependency? | yes / no — if yes, approval reference `<...>` |
| Does it run downloaded or untrusted code? | yes / no — if yes, sandbox and approval reference `<...>` |
| Does it download weights or a dataset? | yes / no — if yes, approval reference `<...>` |
| Does it call a paid or hosted service? | yes / no — if yes, budget and terms re-verified on `<date>` |
| Does it touch SAM-X code, trading, risk, approval, holding or open-position safeguards? | **must be no** |
| Does it place an order or connect to a venue? | **must be no** |
| Does it upload private code, documents, credentials or trading data? | **must be no** |

If any of the last three is not "no", stop. This collection is research-only.

## 12. Freeze record

| Item | Hash (sha256) | Frozen at |
|---|---|---|
| This contract | `<...>` | `<UTC timestamp>` |
| Candidate + config | `<...>` | `<UTC timestamp>` |
| Item file | `<...>` | `<UTC timestamp>` |
| Key file | `<...>` | `<UTC timestamp>` |
| Scorer | `<...>` | `<UTC timestamp>` |
| Resource budget | `<...>` | `<UTC timestamp>` |

Signed off by `<name/agent>` — **before** the first run.
