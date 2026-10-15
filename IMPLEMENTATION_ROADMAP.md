# IMPLEMENTATION ROADMAP

Sequenced phases for adopting this collection. Each phase has: a **goal**, the **components** involved,
an **exit criterion** that is falsifiable, an **explicit non-goal**, and the **authorisation** it needs.

Two rules govern the whole roadmap:

1. **Nothing is adopted without a bounded experiment that could reject it.** Every experiment is written
   down before it runs, using [templates/experiment-contract.md](templates/experiment-contract.md).
2. **No phase touches live trading policy, risk limits, approvals, holding rules or open-position
   safeguards.** Research only. If a phase appears to require that, stop and escalate — see
   [RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) §4.

Sequencing rationale: *measure → freeze the evaluation → make memory trustworthy → improve reading →
prove transfer → harden operations → then, and only then, consider research/backtesting upgrades and
model changes.* Putting evaluation before capability work is deliberate: without a frozen protocol, every
later improvement is unverifiable.

---

## Phase 0 — Establish ground truth (blocking)

**Goal.** Replace reported context with measured facts about the machine and the existing system.

**Do**

1. Answer Q1–Q10 in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §4. Q1–Q3 (hardware, spare RAM under load,
   disk) block every resource-fit decision; Q5–Q7 (existing prototype interface, summarisation path,
   whether summaries are cited as evidence) block every reuse decision.
2. Instrument one existing end-to-end job with `psutil` sampling (RSS, PSS, available memory, 500 ms
   interval) and produce a resource trace. Catalog row `psutil` contains the exact experiment.
3. Write the measured numbers into a `RESOURCE_BUDGET.md` of your own: total RAM, RAM already committed,
   declared ceiling for the reader, safety margin, disk free, disk throughput.
4. Inventory the existing disk-backed navigation prototype: what it stores, its interface, its page map
   (or absence of one), and whether it records hashes.

**Exit criterion.** A written, measured resource budget exists, and every later phase can cite a number
from it instead of the phrase "limited spare RAM". The 147-page prototype's storage schema is documented.

**Non-goal.** No optimisation, no new dependency, no code change to SAM-X.

**Authorisation.** Read access to the machine and to the existing prototype's code. No approvals needed.

---

## Phase 1 — Freeze the evaluation before changing anything

**Goal.** Make future results comparable, reproducible and hard to fool.

**Do**

1. Adopt the protocol in [EVALUATION_PLAN.md](EVALUATION_PLAN.md): candidate freeze, item freeze, key
   freeze, immutable log, layered scoring (deterministic → entailment → judge).
2. Prepare the held-out source set (§3 of that plan): at least one document class the candidate has never
   seen, with items and keys written by someone/something other than the candidate, frozen before any
   output. Keep keys **out** of this repository.
3. Implement or configure the runner. Two acceptable options, in order of preference:
   * **hand-rolled ~150 lines** (JSONL items → candidate → JSONL outputs → scorer → write-once results
     dir), or
   * **Inspect AI** (MIT; docs bundled under `resources/documentation/inspect_ai/`) if its concepts map
     cleanly onto the existing environment.
4. Re-score the **existing** rejected candidate's recorded outputs (reported result R5: 13/32 exact field
   judgments, 0/4 fully correct) under the new protocol **without re-running it**.

**Exit criterion.** A second operator or agent can reproduce the frozen scores bit-for-bit from the
recorded candidate id, item file hash, key hash, scorer version and config hash. The log is append-only:
an attempted overwrite fails loudly. Every failure case is retrievable by item id.

**Non-goal.** Do not improve the candidate in this phase. Do not run public leaderboards. Do not publish
keys.

**Authorisation.** Access to the prior candidate's outputs; confirmation of document rights for the
held-out set (Q4).

**Why first.** If R5 cannot be reproduced under the frozen protocol, the discrepancy is the single most
informative finding available, and it must be known before any "improvement" is claimed.

---

## Phase 2 — Make memory trustworthy (four stores + temporal validity)

**Goal.** Ensure nothing model-generated can be mistaken for a source-linked fact.

**Do**

1. Implement the four stores from [TOP_RECOMMENDATIONS.md](TOP_RECOMMENDATIONS.md) Rank 3: `facts`,
   `procedures`, `lessons`, `hypotheses`, each with write authority enforced in code.
2. Add `valid_from`, `valid_to`, `superseded_by`, `invalidated_reason` (Graphiti's bi-temporal pattern,
   in SQL — bundled reference: `resources/code-examples/graphiti/`).
3. Migrate **new writes only**. Existing memory becomes read-only legacy, clearly labelled, with unknown
   provenance recorded as unknown.
4. Route **every summary** into `hypotheses`. Add a hard rule: a hypothesis may not appear in the
   `evidence` field of an answer.

**Exit criterion.** An audit query returns zero facts without a resolvable quote + page + document version
+ hash. Feeding 10 deliberate contradictions results in 10 flags and zero silent merges. A stale-source
query at time T returns the then-current fact, and the superseded fact is still retrievable with its
interval. No code path allows a model-generated string into `facts` (verified by inspection plus a test
that attempts it and must fail).

**Non-goal.** No graph database. No LLM-driven consolidation. No deletion of historical memory.

**Authorisation.** Schema change in the research store only. Must not touch trading, risk, approval,
holding or open-position tables — if they share a database, use a separate file.

---

## Phase 3 — Bounded-memory reading spine

**Goal.** Navigate documents with a measured, enforced memory ceiling and page-accurate citations.

**Do**

1. Build the Rank 1 spine: page map (page → byte range → heading path → hash), per-page text, FTS5
   lexical index, `diskcache` spill tier, `tiktoken` budgets, `psutil` enforcement.
2. Reuse the existing 147-page prototype's storage where compatible; extend rather than replace (Q5).
3. Implement **reopen-and-verify**: before emitting an answer, re-read the cited page from the source of
   record and check the claim against it. Record the check outcome.
4. Handle extraction failure explicitly: missing page, image-only page, extraction disagreement between
   two extractors, table content. Each becomes a recorded state, never a silent empty string.

**Exit criterion.** Peak RSS ≤ the declared ceiling on every run of the 147-page corpus, with spill events
logged. 100% of emitted answers resolve to a page whose stored text hash matches the source. Extraction
failures are enumerated in a coverage report (pages extracted / image-only / failed / hash-mismatched).

**Non-goal.** No dense retrieval yet (Phase 4 decides whether it is needed). No OCR unless Phase 3's
coverage report shows image-only pages that matter.

**Authorisation.** None beyond Phase 0's read access. If a document class turns out to be scanned, OCR
weights become an approval gate (see workstream 03 and catalog rows `tesseract`, `doctr`, `surya`).

---

## Phase 4 — Retrieval and the evidence gate

**Goal.** Find the right passage, and never claim support that is not there.

**Do**

1. Measure **lexical first**: FTS5 and/or `rank_bm25` over the Phase 3 index (Rank 5 experiment).
2. Add the evidence gate: quote-presence (deterministic) → entailment (small local NLI model or rules) →
   abstain with one of four labelled outcomes: *missing information*, *partial constraint*, *unsupported
   interpretation*, *genuine contradiction*.
3. Only if lexical demonstrably fails on a query class, add a dense tier (`sqlite-vec`, then a small
   embedding model — weights are an approval gate).
4. Adopt hierarchical summaries for **location only** (RAPTOR tree pattern bundled at
   `resources/code-examples/raptor/`), stored in `hypotheses`.

**Exit criterion.** On 40 frozen queries (20 exact-token, 20 paraphrastic) plus 8 deliberately
unanswerable items: recall@5 of the correct page measured and reported; the gate catches a pre-declared
share of deliberately unsupported claims; abstention is correct on unanswerable items; the gate does not
block correct answers more often than wrong ones.

**Non-goal.** No GraphRAG/LightRAG index build (LLM-cost heavy) unless global "themes" questions are
proven necessary by a recorded failure of the hierarchical-summary approach.

**Authorisation.** Approval gate if embedding weights are to be downloaded.

---

## Phase 5 — Interpretation discipline (the eight confusions)

**Goal.** Stop inventing parameters and stop conflating things that look alike.

**Do**

1. Implement typed extraction contracts (pydantic or equivalent) that encode the eight distinctions in
   [workstreams/04-semantic-interpretation/README.md](workstreams/04-semantic-interpretation/README.md):
   dataset description ≠ trading rule; sampling frequency ≠ execution timeframe; benchmark date ≠ holding
   period; action vocabulary ≠ signal; indicator name ≠ parameter setting; partial constraint ≠ complete
   specification; unsupported interpretation ≠ genuine absence; different scope/version ≠ contradiction.
2. Make **partial specification** a first-class output: a field may be `specified`, `partially_specified`
   (with what is known recorded), `absent_from_source`, or `ambiguous`.
3. Never fill a missing parameter from a library default. Record the default as a hypothesis at most.

**Exit criterion.** On a frozen set containing deliberately partial and deliberately absent parameters,
the system produces zero invented parameters and correctly distinguishes `absent_from_source` from
`ambiguous` at a pre-declared rate. Any default value appearing in an output is traceable to a source
quote or flagged as an invention (which fails the run).

**Non-goal.** No parameter search, no optimisation of defaults.

**Authorisation.** None.

---

## Phase 6 — Learning, transfer and retention

**Goal.** Demonstrate learning rather than assert it.

**Do**

1. Procedural memory: declarative recipes with preconditions and validation (Voyager skill-library
   pattern, bundled at `resources/code-examples/voyager/`) — **not** generated executable code.
2. Lesson acceptance gate: a lesson enters `lessons` only with independent review (human, frozen key, or
   verifiable external signal). Reflexion-style self-reflection is allowed to *propose*, never to *accept*.
3. Retention probe: re-ask previously answered items after N unrelated sessions.
4. Transfer set: a third document class, never used in tuning.
5. Regression suite: the frozen Phase 1 items, re-run after every change.

**Exit criterion.** Regression suite shows no degradation beyond a declared tolerance; retention probe
shows no decay beyond tolerance; transfer set shows no collapse; every accepted lesson names its
independent reviewer or signal.

**Non-goal.** No fine-tuning, no RL, no weight updates. (Recorded as a deliberate rejection — see
[REJECTED_OPTIONS.md](REJECTED_OPTIONS.md).)

**Authorisation.** Human review time for lesson acceptance.

---

## Phase 7 — Operations, idempotency and monitoring

**Goal.** Make failures recoverable and never duplicate work.

**Do**

1. Bounded retries with `tenacity` (Apache-2.0) and **explicit predicates** — never blind retry on an
   ambiguous timeout.
2. Idempotency keys: deterministic key = hash(intent + parameters + window), stored **before** acting;
   retries look up the key and replay the recorded outcome. Pattern references in catalog row
   `stripe-idempotency`.
3. Artefact-target checkpoints (Luigi pattern): a step is complete iff its output exists with a recorded
   hash; resume by existence, not by re-execution.
4. Run log in SQLite: run_id, task, state, attempt, started_at, finished_at, checkpoint_path, outcome.
5. Telemetry: RSS, queue depth, cache hit rate, step latency; alerts on declared thresholds only.

**Exit criterion.** A race test (two processes, same step) produces exactly one artefact. A simulated
ambiguous timeout followed by three retries produces exactly one effect record. A killed job resumes
without redoing completed steps and without duplicating any of them.

**Non-goal.** No orchestrator server (Airflow/Prefect server/Dagster/Temporal) — see
[REJECTED_OPTIONS.md](REJECTED_OPTIONS.md).

**Authorisation.** None.

---

## Phase 8 — Historical data, generations and backtest hygiene

**Goal.** Reproducible research over immutable data.

**Do**

1. Immutable generations: directory-per-generation + manifest (schema, provenance, source, retrieval
   timestamp, hash) + atomic publication (write to temp, verify hash, rename). Rollback = repoint.
2. Observations vs estimates as separate typed columns; missing timestamps are **not** evidence of market
   closure (record the reason for the gap).
3. Coverage/gap inspection via DuckDB with an explicit `memory_limit`.
4. Look-ahead audit: every decision uses only data with timestamp ≤ decision time; resampled bars are
   complete bars only. Prove it with a truncation-equivalence test (Freqtrade's lookahead-analysis
   concept, doc bundled).
5. Multiple-testing discipline: record the number of trials; report a deflated/adjusted metric alongside
   any naive best result (MIT-licensed reference scripts bundled at `resources/code-examples/ml4t/`).

**Exit criterion.** Two independent runs from the same generation manifest produce byte-identical outputs.
A truncation-equivalence test passes: decisions at ≤ T are bit-identical whether or not post-T data
exists. Every reported backtest states its trial count and its adjusted metric.

**Non-goal.** No new data vendor. No live connection. No strategy promotion on a naive Sharpe alone.

**Authorisation.** Data-source rights confirmation (Q4).

---

## Phase 9 — Unfamiliar conditions, risk representation and security hardening

**Goal.** Fail conservatively, and make the security boundary real rather than asserted.

**Do**

1. Regime/OOD monitoring with constant-memory detectors (`river` ADWIN/KSWIN, `ruptures` with a **fixed**
   penalty) and conformal intervals (`MAPIE`). Report nominal vs realised coverage — a large gap *is* the
   unfamiliar-condition signal.
2. Strategy-suitability gate: if the current regime is outside the scope recorded for a procedure, the
   procedure refuses to run.
3. Risk representation: exposure limits, position sizing, stop/target and holding rules as **explicit
   typed objects with unit tests**, plus a pre-trade gate that can veto (zipline `controls.py` pattern,
   bundled).
4. Stale-data refusal: data older than a declared horizon blocks the dependent step.
5. Security: untrusted-document parsing inside a sandbox with resource limits and no network (`nsjail`
   config bundled; OS-level rlimits as fallback); a source/sink inventory for dynamic execution; pinned,
   hash-locked dependencies with an advisory audit; secret scanning of the repository and its history;
   the OWASP LLM Top 10 2025 mapped to SAM-X assets with owners and residual gaps.

**Exit criterion.** Injected regime shifts are detected with measured delay and a false-alarm count within
budget. A hostile-fixture test (path traversal, resource-exhaustion document, embedded instruction) shows
no write outside the sandbox, enforced memory cap, enforced timeout, and no tool invocation from the
reading path. Dependency audit and secret scan produce zero unresolved findings. Every control is labelled
**proposed** until its test passes, then **demonstrated**.

**Non-goal.** No order placement. No broker connection. No live policy change. No claim of universal
market handling.

**Authorisation.** Explicit approval to run scanners against the SAM-X codebase; explicit approval before
any sandbox binary is built or downloaded (treat it as untrusted until hash-verified).

---

## Dependencies between phases

```
Phase 0 (measure)  ──┬─> Phase 1 (freeze evaluation) ──> Phase 5 (interpretation)
                     │                              └──> Phase 6 (learning/transfer)
                     └─> Phase 3 (reading spine) ──> Phase 4 (retrieval + gate)
Phase 2 (memory stores) ──> Phase 4, Phase 6        Phase 7 (ops) ── independent, can start any time
Phase 8 (data/backtest) ── needs Phase 0 + Phase 7   Phase 9 (risk/security) ── needs Phase 7
```

Hard dependencies: **0 → 1** (nothing is comparable without measurement and a frozen protocol),
**2 → 4** (the evidence gate needs the fact/hypothesis split), **1 → 6** (learning claims need a frozen
regression suite). Phase 7 is deliberately dependency-light so it can be done in parallel.

## First three experiments, concretely

If you do only three things:

1. **Phase 0 resource trace** — `psutil` sampling over one existing job. Produces the numbers every other
   decision needs. Cannot fail, cannot break anything. (Catalog row `psutil`.)
2. **Phase 1 re-score of the rejected candidate** — deterministic exact-match + quote-presence scoring of
   the already-recorded outputs, under a frozen protocol. Tests the protocol, not the model. (Catalog rows
   `inspect_ai`, `hf-evaluate`.)
3. **Phase 3 reopen-and-verify over the 147 indexed pages** — measure whether every answer resolves to a
   page whose hash matches the source, and what peak RSS the spine needs. (Catalog rows `diskcache`,
   `sqlite-vec`, `tiktoken`.)

Each is bounded (≤ 1 day of work), reversible, and produces a number that can reject a hypothesis.

## What would change this roadmap

| If this turns out to be true | Then |
|---|---|
| Q9: SAM-X already executes model-generated or downloaded code | Phase 9's security items move to Phase 1. Everything else waits |
| Q1: no usable spare RAM for even a small local model | Phase 3/4 proceed (they are storage work); Phase 13-model choices collapse to hosted-with-budget or abstain; document reading must be designed to work without a generative model in the loop |
| Q4: the two indexed documents cannot be used as evaluation sources | Phase 1 needs a different held-out corpus before it can start |
| Q6: R5's key was not frozen before outputs | The 13/32 number is not a baseline; Phase 1 must establish a new one and R5 becomes "uninterpretable" |
| Q5: the existing prototype already stores hashes and a page map | Phase 3 shrinks to adding the token budget, spill tier and reopen-verify |
