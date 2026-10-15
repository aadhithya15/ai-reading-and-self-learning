# EVALUATION REPORT — <experiment id>

> Written **after** the run, from stored artefacts only. If a number in this report cannot be traced to a
> stored raw output, it does not belong here.
>
> This report is generated from a frozen [experiment-contract.md](experiment-contract.md). Where the run
> deviated from the contract, the deviation is recorded in §10 — deviations are findings, not footnotes.
>
> Evidence labels: **measured** · **verified** · **inspected** · **estimate** · **reported** · **proposed** ·
> **unknown**. Every number in §5 carries one.

---

## 1. Verdict

| Field | Value |
|---|---|
| Experiment id | `<EXP-YYYYMMDD-nn>` |
| Candidate id / hash | `<...>` |
| Run id | `<...>` — a re-run gets a **new** id; existing runs are never overwritten |
| Date of run | `<YYYY-MM-DD>` |
| Date of report | `<YYYY-MM-DD>` |
| **Verdict** | `ACCEPT` \| `REJECT` \| `INCONCLUSIVE` |
| Verdict against | The pre-declared criteria in the contract, §8 — quoted verbatim below |
| Decided by | `<name/agent>` — and whether that is the same party that owns the candidate |
| One-sentence finding | `<...>` |

**Pre-declared acceptance criteria (copied from the contract, unedited):**

1. `<...>`

**Pre-declared rejection criteria (copied from the contract, unedited):**

1. `<...>`

**Which criteria were met / missed:**

| Criterion | Met? | Evidence |
|---|---|---|
| `<...>` | yes / no | `<artefact path + record id>` |

## 2. Freeze verification

Confirm the freeze held. If any hash differs from the contract, the run is invalid and the verdict is
`INCONCLUSIVE`.

| Artefact | Hash in contract | Hash at run time | Match |
|---|---|---|---|
| Contract | `<...>` | `<...>` | yes / no |
| Candidate + config | `<...>` | `<...>` | yes / no |
| Item file | `<...>` | `<...>` | yes / no |
| Key file | `<...>` | `<...>` | yes / no |
| Scorer | `<...>` | `<...>` | yes / no |

## 3. What was run

| Field | Value |
|---|---|
| Machine | `<CPU, total RAM, swap, free disk, OS>` — measured, not assumed |
| Runtime | `<language + version, key dependency versions>` |
| Baseline actually run | `<id/hash>` or `not re-run — prior recorded outputs re-scored` |
| Items attempted / total | `<n>` / `<N>` — **the attempted denominator** |
| Items per set | TRAIN `<n>` · VALID `<n>` · TEST `<n>` · TRANSFER `<n>` · NEGATIVE `<n>` |
| Wall time total | `<s>` |
| Cost total | `<currency + amount, or "none">` |
| Sampler | `<instrument, version, interval, process separation>` |

## 4. Coverage and data quality

Report this **before** the scores, because a coverage gap changes what a score means.

| Field | Value |
|---|---|
| Source pages total | `<n>` |
| Pages extracted | `<n>` |
| Image-only pages | `<n>` |
| Extraction failures | `<n>` — listed in `<artefact>` |
| Hash mismatches vs source of record | `<n>` |
| Items affected by a coverage gap | `<n>` — reported separately from the headline numbers |

## 5. Results

Every row: value, denominator, interval, evidence label.

### 5.1 Correctness

| Metric | Baseline | Candidate | Δ | n | 95% CI or exact test | Label |
|---|---|---|---|---|---|---|
| Exact-field match rate | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | measured |
| Fully-correct-case rate | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | measured |
| Accuracy over **attempted** items | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | measured |
| Accuracy over **all** items | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | measured |

### 5.2 Meaning

| Metric | Value | Instrument | Label |
|---|---|---|---|
| Judge score on answer adequacy | `<...>` | `<judge model + version + prompt hash + temperature>` | reported (model-judged — **not** independent) |
| Human review outcome | `<...>` | `<reviewer, date>` | verified / not done |

A model judging a model is not independent supervision and is never the sole acceptance gate.

### 5.3 Evidence

| Metric | Value | n | Label |
|---|---|---|---|
| Quote-presence (cited string literally on the cited page) | `<...>` | `<...>` | measured |
| Entailment (cited passage supports the claim) | `<...>` | `<...>` | measured |
| Answers whose evidence was a summary rather than a source passage | `<...>` — target 0 | `<...>` | measured |
| Citation completeness | `<...>` | `<...>` | measured |

### 5.4 Abstention and invention

| Metric | Value | n | Label |
|---|---|---|---|
| Abstention rate | `<...>` | `<...>` | measured |
| Correct abstentions (unanswerable items) | `<...>` | `<...>` | measured |
| Incorrect abstentions (answerable items) | `<...>` | `<...>` | measured |
| **Invented-parameter count** | `<...>` — target **0**; one invention fails the run | `<...>` | measured |
| `absent_from_source` correctly identified | `<...>` | `<...>` | measured |
| `partially_specified` correctly identified, with the partial information preserved | `<...>` | `<...>` | measured |
| `ambiguous` distinguished from `absent_from_source` | `<...>` | `<...>` | measured |

### 5.5 The eight confusions (workstream 04)

| Confusion | Correct | Incorrect | n |
|---|---|---|---|
| Dataset description treated as a trading rule | `<...>` | `<...>` | `<...>` |
| Sampling frequency treated as an execution timeframe | `<...>` | `<...>` | `<...>` |
| Benchmark date treated as a holding period | `<...>` | `<...>` | `<...>` |
| Action vocabulary treated as a signal | `<...>` | `<...>` | `<...>` |
| Indicator name treated as a parameter setting | `<...>` | `<...>` | `<...>` |
| Partial constraint treated as a complete specification | `<...>` | `<...>` | `<...>` |
| Unsupported interpretation treated as genuine absence | `<...>` | `<...>` | `<...>` |
| Different scope/version treated as a contradiction | `<...>` | `<...>` | `<...>` |

### 5.6 Negative cases (contract §6)

| # | Case | Expected | Observed | Pass |
|---|---|---|---|---|
| N1 | `<...>` | `<...>` | `<...>` | yes / no |

### 5.7 Resources

| Metric | Baseline | Candidate | Ceiling | Label |
|---|---|---|---|---|
| Peak RSS | `<MB>` | `<MB>` | `<MB>` | measured |
| Peak PSS | `<MB>` | `<MB>` | `<MB>` | measured |
| Minimum available system memory | `<MB>` | `<MB>` | `<MB>` | measured |
| Spill / eviction events | `<n>` | `<n>` | — | measured |
| Wall time p50 / p95 | `<s>` | `<s>` | `<s>` | measured |
| Cold start | `<s>` | `<s>` | `<s>` | measured |
| Tokens in / out | `<n>` | `<n>` | `<n>` | measured |
| Cost | `<...>` | `<...>` | `<...>` | measured |
| On-disk footprint | `<MB>` | `<MB>` | `<MB>` | measured |

### 5.8 Reliability

| Metric | Value | Label |
|---|---|---|
| Crashes | `<n>` | measured |
| Timeouts | `<n>` | measured |
| Retries (and whether any retry produced a duplicate effect) | `<n>` | measured |
| Items with no recorded output | `<n>` — **must be 0** | measured |

## 6. Regression, retention, transfer

| Test | Result | Threshold | Pass | n |
|---|---|---|---|---|
| Regression vs the frozen suite | `<...>` | `<...>` | yes / no | `<...>` |
| Retention (re-asked after `<n>` unrelated sessions) | `<...>` | `<...>` | yes / no | `<...>` |
| Transfer (different source class, never tuned on) | `<...>` | `<...>` | yes / no | `<...>` |

## 7. Contamination and leakage

| Check | Result |
|---|---|
| Keys stored outside the candidate's read scope | yes / no |
| Any TEST item or TEST-derived text found in a prompt, few-shot example, cache or tuning trace | `<none found / list>` |
| Candidate training cutoff vs item and source dates | `<per-item flags; n flagged contamination-risk>` |
| Scores for `contamination-risk` items reported separately | yes / no |
| Tuning indexes rebuilt from TRAIN sources only | yes / no |
| Cache invalidated for this candidate id and prompt hash | yes / no |
| Configurations compared | `<n>` — correction applied: `<method or "none, because n=1">` |
| Held-out sources committed to the repository | **must be no** |

## 8. Which kind of test is each result

Never conflate these. State it per result.

| Result | Kind |
|---|---|
| `<...>` | mechanical \| synthetic fixture \| source-based qualification \| deployment proof |

**No result in this collection is a deployment proof.** Deployment proof requires authorised operation on
live data over elapsed time.

## 9. What was NOT tested

Mandatory section. An unstated gap becomes an assumed capability.

* `<...>`
* `<...>`
* Not tested on any document class other than `<...>`
* Not tested at any scale other than `<...>`
* Not tested under `<resource pressure / concurrency / network failure / hostile input>`
* Not tested over time — no retention beyond `<n>` sessions

## 10. Deviations from the contract

| Deviation | Why | Effect on the verdict |
|---|---|---|
| `<...>` | `<...>` | `<...>` |

If the key, an item or the scorer changed after freeze, the verdict is `INCONCLUSIVE` regardless of scores.

## 11. Failures, preserved

Every failure case, verbatim, with the reason. Not a summary — the actual records, or a pointer to the
stored records plus a count.

| Item id | Input (truncated) | Raw output (truncated) | Expected | Why it failed |
|---|---|---|---|---|
| `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Failure count: `<n>` of `<N>`. Full records: `<artefact path>`.

## 12. Artefact index

| Artefact | Path | Hash |
|---|---|---|
| Contract | `<...>` | `<...>` |
| Items | `<...>` | `<...>` |
| Key file (**hash only — the key is not stored here**) | n/a | `<...>` |
| Raw outputs | `<...>` | `<...>` |
| Evidence records | `<...>` | `<...>` |
| Resource trace | `<...>` | `<...>` |
| Scores | `<...>` | `<...>` |
| Failures | `<...>` | `<...>` |

Storage is write-once. A re-run creates a new run id.

## 13. Conclusion and next step

| Field | Value |
|---|---|
| Plain-language finding | `<what a non-specialist should take away>` |
| What this licenses you to claim | `<...>` |
| What this does **not** license you to claim | `<...>` |
| Recommended next experiment | `<id or description>` |
| Catalog rows to update | `<component ids — update evidence_status, classification, checked_date>` |

Do not claim perfect reading, unlimited learning, universal market handling, guaranteed RAM savings or
trading profits. If the results tempt you to, re-read §9.
