# EVALUATION PLAN

How a SAM-X reader candidate is qualified — independently, reproducibly, and without fooling ourselves.

This plan exists because the reported baseline (**R5**: one frozen reader qualification scored 13/32 exact
field judgments and 0/4 fully correct cases; candidate rejected) is only meaningful if the protocol behind
it was frozen and the evaluator was independent. If it was not, the number is a data point about the past,
not a baseline for the future. Phase 1 of the
[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) resolves that question by re-scoring the existing
outputs under this protocol.

**Nothing in this plan is published with its keys.** Protected questions and hidden answer keys stay
outside the repository; the shareable artefacts are
[templates/experiment-contract.md](templates/experiment-contract.md),
[templates/evaluation-report.md](templates/evaluation-report.md) and
[templates/source-provenance.json](templates/source-provenance.json).

---

## 1. Principles

1. **Freeze before you run.** Candidate version, item set, answer key, scorer version, prompt/config and
   resource budget are all committed (by hash) before the first output exists. Anything changed afterwards
   is a new candidate, not a fix.
2. **Separate the evaluator from the candidate.** Different process, different config, different
   credentials if hosted, no shared mutable state. The evaluator must not be able to read the candidate's
   internal prompt-tuning artefacts, and the candidate must not be able to read the key.
3. **Never expose held-out sources to any optimisation loop.** Prompt tuning, few-shot example selection,
   threshold setting, retrieval-config tuning and human iteration all happen on TRAIN/VALIDATION sources
   only. TEST sources are opened once.
4. **Score abstention, and publish the attempted denominator.** Accuracy over attempted items and accuracy
   over all items are both reported. A system that answers 40% of items correctly on 50% of them is not a
   system with 40% accuracy.
5. **Preserve failures.** Raw outputs, judge prompts/responses, scorer versions, resource traces and every
   failure case are retained. A rejected candidate is a result.
6. **Measure meaning, evidence and resources, not just correctness.** A correct answer with no supporting
   evidence is a lucky guess; a correct answer that exceeds the memory budget is not deployable.
7. **Distinguish test kinds.** Mechanical tests, synthetic fixtures, source-based qualification and
   deployment proof are four different things and are never reported as one another. Independent AI
   evaluation is **not** human-independent certification.
8. **Contamination is a first-class check**, not an assumption: for every item, record whether the
   candidate model could have seen the source or the item before.

## 2. Roles and separation

| Role | Responsibility | May not |
|---|---|---|
| **Item author** | Writes items and keys from sources they hold the rights to use | Tune the candidate |
| **Candidate owner** | Freezes the candidate, runs it, records outputs | Read the key; edit items; edit the scorer |
| **Scorer** | Deterministic + entailment + (optional) judge scoring; produces the report | Change the key after seeing outputs |
| **Reviewer** | Independent review for `lessons` acceptance; signs off the report | Be the same agent/person as the candidate owner for the acceptance decision |
| **Resource monitor** | Records RAM/runtime from an independent sampler | Be the candidate process itself |

For a one-person project these roles collapse onto one human — in which case **separate them in time**
(author and freeze items on day 1; run the candidate on day 2 without re-reading the key; score on day 3)
and record that the separation was temporal, not personal. That limitation is stated in the report rather
than hidden.

## 3. Evaluation sources

| Set | Purpose | Rules |
|---|---|---|
| **TRAIN** | Prompt/config iteration, few-shot selection, retrieval tuning | May be seen repeatedly. Never used for reported numbers |
| **VALIDATION** | Choosing between configurations | May be seen repeatedly, but every look is logged (it is a slow leak) |
| **TEST / held-out** | The reported number | Opened **once** per candidate. Fresh items or a fresh source for each new candidate generation |
| **TRANSFER** | Different source class, different vendor, different document genre | Never used for tuning; proves generalisation |
| **ADVERSARIAL / negative** | Missing info, partial constraints, exceptions, contradictions, stale sources, unanswerable queries, embedded instructions, resource exhaustion | Must be pre-declared; each has an expected behaviour, usually abstention |

Requirements for a source to be usable at all:

* **Rights confirmed** — the project may store, index and quote it (question Q4 in
  [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4).
* **Provenance recorded** using [templates/source-provenance.json](templates/source-provenance.json):
  origin, retrieval date, hash, version, licence, confidentiality, known extraction problems.
* **Not previously exposed** to the candidate. The two already-indexed documents (reported R4) are
  **contaminated by prior exposure** and may be used for mechanical/coverage tests, but not for capability
  claims.
* **Extraction status known**: pages extracted, image-only, failed, hash-mismatched. Coverage is reported
  alongside scores, because a missing page that produces a wrong answer is a data problem, not a
  comprehension problem.

### How to build items without leaking them

1. Generate mechanically where possible: `NVIDIA/RULER`'s bundled generators
   (`resources/code-examples/ruler/`) create NIAH variants, variable-tracking (multi-hop), aggregation and
   word-extraction tasks from **any** haystack text, with a seed. A fresh seed yields fresh items that
   cannot have been in any training corpus. Apache-2.0; no dataset download.
2. Author field-extraction items by hand from the held-out source: each item names the field, the expected
   value, the page, and the exact supporting quote.
3. Author negative items by construction: delete a parameter from a synthetic specification (→ expected:
   `absent_from_source`), split a constraint across two pages (→ expected: both cited), add an exception
   clause (→ expected: exception reported), publish a superseded version of a document (→ expected: the
   current one used, the stale one flagged).
4. Store keys in a location the candidate process cannot read; publish only hashes of the key files.

## 4. What is measured

| Dimension | Metric | Layer | Notes |
|---|---|---|---|
| **Correctness** | exact-field match rate | deterministic | Normalisation rules written down and frozen (case, whitespace, units, number format). Use HF Evaluate's `exact_match` definition or a local equivalent with the rules recorded — a subtly different normaliser silently changes scores |
| **Correctness (composite)** | fully-correct-case rate | deterministic | A case is correct only if *all* its fields are correct. R5's "0/4 fully correct cases" is this metric |
| **Meaning** | judge score on answer adequacy | model judge | Optional; judge model, prompt, version and temperature recorded. Never the sole acceptance gate |
| **Evidence** | quote-presence rate | deterministic | Does the cited string literally appear on the cited page? Cheap, objective, catches fabricated citations |
| **Evidence** | entailment rate | entailment | Does the cited passage actually support the claim? A valid citation id + a real quote can still fail this — the trap named in the objective |
| **Evidence** | citation completeness | deterministic | All required sources cited; no uncited claims |
| **Abstention** | abstention rate, and correctness of abstention | deterministic | Abstaining on an unanswerable item is correct; abstaining on an answerable item is a miss. Both counted |
| **Denominator honesty** | attempted / total | deterministic | Reported next to every rate |
| **Interpretation** | confusion-classification accuracy | deterministic | On items designed for the eight confusions in workstream 04: did it treat a dataset description as a trading rule? A sampling frequency as an execution timeframe? An indicator name as a parameter setting? |
| **Invention** | invented-parameter count | deterministic | Any parameter value in an output with no source quote is an invention. **Target: zero.** One invention fails the run regardless of other scores |
| **Resources** | peak RSS, peak PSS, available-memory minimum | measured | Independent sampler (psutil), not self-reported |
| **Resources** | wall time p50/p95, tokens in/out, cost | measured | Per item and per run |
| **Reliability** | crash/timeout rate, spill events, retry counts | measured | A candidate that needs 3 retries to answer is a different candidate |
| **Retention** | re-ask score after N unrelated sessions | deterministic | Detects forgetting disguised as learning |
| **Transfer** | score on the TRANSFER set | deterministic | Detects source-specific overfitting |
| **Regression** | delta against the frozen regression suite | deterministic | Detects "improvements" that break previously working behaviour |

## 5. Pre-declared acceptance and rejection criteria

Written into [templates/experiment-contract.md](templates/experiment-contract.md) **before** the run, and
versioned. Example shape (numbers are placeholders — the project must set them from its own risk
tolerance; inventing them here would itself be an invented parameter):

**Accept if all hold**

* invented-parameter count = 0
* quote-presence = 100% of cited claims
* entailment rate ≥ `E_min` on answerable items
* fully-correct-case rate ≥ `C_min`, and strictly greater than the frozen baseline
* abstention correct on ≥ `A_min` of unanswerable/negative items
* peak RSS ≤ declared ceiling on every run; spill events logged
* p95 wall time ≤ declared ceiling
* regression delta within tolerance; retention delta within tolerance; transfer score ≥ `T_min`

**Reject if any hold**

* any invented parameter
* any cited quote not present on the cited page
* any answer whose evidence is a summary (a hypothesis) rather than a source passage
* peak RSS exceeds the ceiling without a logged spill
* a failure case is missing from the log
* the key, an item, or the scorer changed after freeze
* accuracy improved while the attempted denominator shrank (abstention used to game the rate)

**Inconclusive** (a legitimate outcome, recorded as such): too few items for the observed effect size;
environment drift between runs; a dependency version changed mid-run.

### Statistical honesty

With small denominators, differences are not findings. Report a confidence interval or an exact test for
every headline number, and state the item count next to the rate. A 13/32 result has a wide interval; a
claim that a new candidate is "better" on 32 items needs a test, not an impression. Where multiple
configurations are compared, record the number of comparisons and apply a correction — the same
multiple-testing discipline that workstream 09 demands of backtests applies to evaluations.

## 6. Immutability and artefacts

For each run, store in a write-once directory (or with the write-once bit set):

```
runs/<candidate_id>/<run_id>/
  contract.md            # the frozen experiment contract, hashed
  candidate.json         # model, version, prompt hash, config hash, retrieval config, commit
  items.jsonl            # item ids + inputs (no keys)
  keys.sha256            # hash of the key file only — the key itself lives elsewhere
  outputs.jsonl          # raw candidate outputs, one per item, including failures and abstentions
  evidence.jsonl         # per claim: cited page, quote, quote-presence result, entailment result
  resources.jsonl        # independent sampler trace (timestamp, rss, pss, available)
  scores.json            # all metrics, denominators, CIs, comparison count
  report.md              # from templates/evaluation-report.md
  failures/              # every failure case, verbatim, with the reason it failed
```

Append-only rule: a re-run gets a **new** `run_id`. Overwriting an existing run is a protocol violation and
must fail loudly. This is what Inspect AI's `.eval` log model provides if that framework is adopted
(docs bundled at `resources/documentation/inspect_ai/`).

## 7. Leakage prevention checklist

Run before every reported evaluation:

* [ ] Keys are stored outside the candidate's read scope; only their hash is in the run directory.
* [ ] No TEST item, and no text derived from a TEST source, appears in any prompt, few-shot example,
      cache, index used for tuning, or optimisation trace.
* [ ] The candidate model's training cutoff date is recorded, and compared against each item's creation
      date and each source's publication date. If the model could have seen the source, the item is
      flagged `contamination-risk` and reported separately.
* [ ] Retrieval indexes used during tuning are rebuilt from TRAIN sources only, or the run is flagged.
* [ ] Any cached model response from an earlier run is invalidated (cache keys include candidate id and
      prompt hash) — otherwise you are scoring yesterday's answer.
* [ ] The scorer version is hashed; scoring is re-runnable from stored outputs without re-invoking the
      candidate.
* [ ] The number of configurations compared is recorded, and a correction is applied if > 1.
* [ ] Held-out sources are not committed to this repository. Only their provenance templates and hashes.

## 8. Four kinds of test — never conflated

| Kind | What it proves | Example here |
|---|---|---|
| **Mechanical test** | Code does what it says, deterministically | Idempotency-key test: a retried intent creates exactly one effect. Truncation-equivalence test: no look-ahead |
| **Synthetic fixture test** | Behaviour under constructed conditions | RULER-generated multi-hop tasks; injected regime shifts; hostile documents in a sandbox |
| **Source-based qualification** | Capability on real, held-out documents | Field extraction from a previously unexposed specification, with evidence and abstention scored |
| **Deployment proof** | It works in production, on live data, over time | **Not achievable in this collection.** Requires authorised operation and elapsed time. No component here is deployment-proven |

A passing mechanical test is not a qualification. A good synthetic score is not source-based capability.
A source-based qualification is not deployment proof. Reports must state which kind each number is.

## 9. Reporting

Use [templates/evaluation-report.md](templates/evaluation-report.md). Minimum contents:

* candidate id + all frozen hashes; item counts per set; rights/provenance statement for each source
* every metric in §4 with its denominator, and a confidence interval or exact test for headline numbers
* the number of configurations compared and the correction applied
* contamination flags per item
* resource traces (peak RSS/PSS, p95 latency, tokens, cost)
* the failure list, verbatim, with reasons
* an explicit statement of which of the four test kinds each result is
* an explicit statement of what was **not** tested
* the accept/reject/inconclusive verdict against the pre-declared criteria, and who made the call

Adopt HELM's reporting *shape* (metrics × scenarios × models, all shown together, including efficiency)
rather than reporting a single accuracy number. Its docs are bundled at `resources/documentation/helm/`.

## 10. What this plan does not claim

* It does not make an AI evaluation equivalent to human certification. An independent AI evaluator is
  better than self-evaluation and worse than a qualified human review; both are recorded as what they are.
* It does not guarantee that a candidate which passes will work on documents nobody anticipated. It
  guarantees only that the claims made about it are traceable, reproducible and honestly bounded.
* It does not measure trading profitability. Nothing in this collection does, and no result here should be
  read as evidence that any strategy makes money.
