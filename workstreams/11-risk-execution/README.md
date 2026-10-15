# Workstream 11 — Risk Representation and Execution Reliability (Research Only)

**Objectives served:** preserve trading, risk, approval, holding-rule and open-position safeguards; fail
conservatively; never invent parameters.

> **Hard scope limit.** This workstream is **research only**. Nothing here places an order, configures a
> credential, contacts a venue, or changes a live policy. No component in this collection was executed,
> installed or connected. The bundled material is used as a **factual map** of how execution reliability and
> risk representation are modelled elsewhere, so that SAM-X's own research code can be made idempotent,
> reconcilable and conservative.
>
> If the goal is to change anything about live trading, that is a different engagement with different
> authorisations, and it is not this one.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 11.1 | **Order idempotency**: a deterministic key, stored *before* acting; retries replay the recorded outcome | An ambiguous timeout must not cause a duplicate effect |
| 11.2 | **Reconciliation with an explicit `unknown` state that refuses to act** | "Probably filled" is how a position becomes wrong |
| 11.3 | **Bounded retries with explicit predicates** — never a blind retry on an ambiguous timeout | Retrying an unknown is duplicating an unknown |
| 11.4 | **Stale-data refusal**: data older than a declared horizon blocks the dependent step | Shared with workstream 10 |
| 11.5 | Risk rules as **explicit typed objects with unit tests**: exposure limits, position sizing, stop/target, holding rules | A rule in a comment is not a rule |
| 11.6 | A **pre-trade gate that can veto**, as an interface | The zipline `controls.py` pattern |
| 11.7 | Per-venue capability facts recorded from an authoritative map: client order ids, partial-fill reporting, error taxonomy, rate limits | Capabilities differ per venue; assuming is inventing |
| 11.8 | **Safeguards untouched**: source separation, protected holdouts, trading/risk/approval/holding rules, open positions | A standing constraint of this engagement |

**Not a goal.** An execution system. Nothing here connects to anything.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: idempotency + reconciliation + typed risk objects, all research-side

1. **Idempotency key** = `hash(intent + parameters + window)`, persisted **before** the action is attempted.
   A retry looks the key up and replays the recorded outcome instead of acting again. Vendor design
   references (Stripe's idempotency keys, AWS SQS exactly-once semantics) are catalogued as
   **metadata-only**: their documentation pages are not redistributable and were unreachable for download
   from the build sandbox, so the *pattern* is recorded and the *text* is linked.
2. **Bounded retries** with `tenacity` (Apache-2.0, tiny): the retry policy is declarative and therefore
   auditable — which conditions retry, how many times, with what backoff, and what happens on exhaustion.
   The critical rule is the predicate: an **ambiguous** outcome does not retry; it goes to reconciliation.
3. **Reconciliation state machine** with an explicit `unknown` that **refuses to act** and raises a
   recorded exception requiring human or policy resolution.
4. **Typed risk objects** with unit tests, plus a **pre-trade veto interface** following
   `zipline-reloaded`'s `finance/controls.py` (Apache-2.0, bundled).
5. **Venue capability map** read from CCXT's `wiki/Manual.md` (MIT, 0.52 MB bundled): which venues support
   client order ids, how partial fills are reported, what the error taxonomy is, what the rate limits are.
   Read as facts about venues — **not** executed, and **not** connected.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **NautilusTrader** (LGPL-3.0) | **Strongest open design reference; platform not adopted** | 19 bundled assets including its RiskEngine documentation — the clearest open statement of how a pre-trade risk gate should be structured. But LGPL, a native Rust core, and adopting the platform would **replace** existing components (contradicts R5) |
| **Freqtrade** (GPL-3.0) | Reference only | Good dry-run mode and protection logic; GPL and a whole bot framework |
| **Hummingbot** (Apache-2.0) | Config templates adopted | Its bundled `conf_*_TEMPLATE.yml` files are a practical example of declaring risk and inventory limits in configuration rather than code. The framework itself is a market-making bot, not a research component |
| **`ib_async`** (BSD-2) | Catalogued, **not adopted** | Requires a running TWS/IB Gateway — a separate process with notable RAM — and adopting it implies a brokerage connection this engagement must not make |
| **CCXT as a live connector** | **Not adopted**; Manual adopted as a reference | The library is the standard way to talk to venues, and using it would mean connecting. Its Manual is the useful part here |
| **QuantConnect LEAN** (Apache-2.0, C#) | Not adopted | .NET runtime, substantial footprint, different stack |
| **`gs-quant`** | **Rejected** | Most functions require a Goldman Sachs account |
| **`PyPortfolioOpt`** (MIT), **`riskfolio`** (BSD-3) | Catalogued for **risk-measure arithmetic** | Useful for computing risk measures in research; they are not execution controls and must not be confused with one |
| **Temporal / Airflow / Prefect / Dagster** for durable retries | **Rejected** | Server processes and a database footprint; a SQLite run log plus `tenacity` covers the requirement (workstream 12) |
| Implementing idempotency in the database alone | Insufficient | A unique constraint prevents a duplicate *row*; it does not prevent a duplicate *effect*. The key must be persisted before the action, and the retry must replay |

### 2.3 The failure mode this workstream exists to prevent

A request times out. The client does not know whether the effect happened. Three plausible responses:

| Response | Outcome |
|---|---|
| Retry immediately | Possible duplicate effect |
| Assume it failed | Possible missing effect, silently |
| Assume it succeeded | Possible unrecorded effect, silently |
| **Look up the idempotency key; if the outcome is recorded, replay it; if not, enter reconciliation and refuse to act** | Correct, and auditable |

The fourth is the only acceptable one, and it requires the key to have been persisted **before** the action
— which is why requirement 11.1 says "before", not "with".

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `tenacity` (Apache-2.0) | [documentation](../../resources/documentation/tenacity/) · [code examples](../../resources/code-examples/tenacity/) · [licence](../../resources/licenses/tenacity/) |
| `zipline` (Apache-2.0) | [code examples](../../resources/code-examples/zipline/) — `finance/controls.py`, `finance/slippage.py`, `finance/commission.py` · [documentation](../../resources/documentation/zipline/) · [licence](../../resources/licenses/zipline/) |
| `ccxt` (MIT) | [documentation](../../resources/documentation/ccxt/) — including `wiki/Manual.md` (0.52 MB), the per-venue capability map · [licence](../../resources/licenses/ccxt/) (**8.67 GB repository — individual files only**) |
| `nautilus` (LGPL-3.0) | [documentation](../../resources/documentation/nautilus/) — 18 files including the RiskEngine design · [configurations](../../resources/configurations/nautilus/) · [licence](../../resources/licenses/nautilus/) |
| `hummingbot` (Apache-2.0) | [config templates](../../resources/configurations/hummingbot/) — `conf_*_TEMPLATE.yml` · [code examples](../../resources/code-examples/hummingbot/) · [documentation](../../resources/documentation/hummingbot/) |
| `freqtrade` (GPL-3.0) | [documentation](../../resources/documentation/freqtrade/) · [config templates](../../resources/configurations/freqtrade/) · [licence](../../resources/licenses/freqtrade/) |
| `ib-async` (BSD-2) | [documentation](../../resources/documentation/ib-async/) · [code examples](../../resources/code-examples/ib-async/) · [licence](../../resources/licenses/ib-async/) — **not adopted** |
| `pyportfolioopt` (MIT), `riskfolio` (BSD-3) | [PyPortfolioOpt](../../resources/documentation/pyportfolioopt/) · [Riskfolio-Lib](../../resources/documentation/riskfolio/) |
| `lean` (Apache-2.0, C#) | [documentation](../../resources/documentation/lean/) · [configurations](../../resources/configurations/lean/) |
| `luigi` (Apache-2.0) | [documentation](../../resources/documentation/luigi/) — target-existence checkpointing, shared with workstream 12 |
| `stripe-idempotency` | **Not bundled** — metadata-only catalog row (MO-04 family): vendor documentation pages are not redistributable and were unreachable for download. The pattern is recorded; the text is linked |
| Shared with workstream 12 | [apscheduler](../../resources/documentation/apscheduler/) (misfire policy) · [prometheus-client](../../resources/documentation/prometheus-client/) · [rich](../../resources/documentation/rich/) |
| Shared with workstream 14 | [owasp-llm-top10](../../resources/documentation/owasp-llm-top10/) — LLM06 Excessive Agency is directly about limiting what an agent may do |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| tenacity | https://github.com/jd/tenacity |
| zipline-reloaded | https://github.com/stefan-zhao/zipline-reloaded |
| CCXT | https://github.com/ccxt/ccxt · https://docs.ccxt.com/ |
| NautilusTrader | https://github.com/nautechsystems/nautilus_trader · https://nautilustrader.io/docs |
| Hummingbot | https://github.com/hummingbot/hummingbot |
| Freqtrade | https://github.com/freqtrade/freqtrade |
| ib_async | https://github.com/ib-api-reloaded/ib_async |
| PyPortfolioOpt | https://github.com/PyPortfolio/PyPortfolioOpt |
| Riskfolio-Lib | https://github.com/dcajasn/Riskfolio-Lib |
| LEAN | https://github.com/QuantConnect/Lean |
| Stripe idempotency keys | https://docs.stripe.com/api/idempotent_requests (**unreachable for download from the build sandbox; not redistributable**) |
| AWS SQS exactly-once semantics | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/ (**same**) |

## 5. Adoption steps

1. **Do not start here if workstream 14's question Q9 is unanswered.** If SAM-X already executes
   model-generated or downloaded code, containment comes first and this workstream waits.
2. **Write the risk objects as typed structures with unit tests**: exposure limit, position size, stop,
   target, holding rule, approval requirement. Each carries its unit, its source (a document quote or a
   policy decision, with a reference), and its validity interval.
3. **Add the pre-trade veto interface** (zipline `controls.py` pattern) as a **research-time** gate. It
   exercises the same logic live trading would, without touching live trading.
4. **Implement the idempotency key**: deterministic, persisted before the action, with a replay path. Test
   it with a race (two processes, same intent) and assert exactly one effect record.
5. **Implement the reconciliation state machine** with an explicit `unknown` that refuses to act. Test it by
   simulating an ambiguous timeout followed by three retries and asserting exactly one effect record and one
   `unknown` requiring resolution.
6. **Configure bounded retries** with `tenacity`, with an explicit predicate per exception class. An
   ambiguous outcome is **not** in the retry predicate.
7. **Add stale-data refusal** with a declared horizon per data type (shared with workstream 10).
8. **Record per-venue capability facts** from CCXT's Manual into a typed table: client-order-id support,
   partial-fill reporting, error taxonomy, rate limits. Mark each with its source and check date. **Do not
   connect to a venue to verify it** — that requires authorisation this engagement does not have.
9. **Log every refusal, veto, replay and `unknown`** into the workstream-12 run log. A refusal that is not
   logged will be "fixed" by someone later.

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| `tenacity` | Tiny | Pure Python decorators |
| Idempotency key store | One SQLite table | Persist-before-act means a write on the hot path; measure it |
| Reconciliation state machine | Negligible compute; **human attention on `unknown`** | The real cost is operational, not computational |
| Typed risk objects + tests | Negligible at runtime | Cost is in authoring and maintaining the tests |
| CCXT Manual reading | Human time | 0.52 MB of dense per-venue detail |
| NautilusTrader | Rust core, low latency, **real memory footprint** | Reference only |
| `ib_async` | Requires a running TWS/IB Gateway — a separate process with notable RAM | Not adopted |
| LEAN | .NET runtime, substantial | Not adopted |
| Temporal / Airflow | Server + database | Rejected on footprint |

## 7. Qualification requirements

All of these are **mechanical tests** in the taxonomy of
[EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §8. None is a source-based qualification and none is
live-performance evidence.

1. **Race test**: two processes attempt the same intent concurrently → exactly one effect record.
2. **Ambiguous-timeout test**: a simulated timeout followed by three retries → exactly one effect record,
   and one `unknown` requiring resolution.
3. **Replay test**: a retry after a recorded outcome returns the recorded outcome without acting again.
4. **Veto test**: a request that breaches a typed risk limit is refused, with the breached limit named.
5. **Stale-data test**: data older than the declared horizon blocks the dependent step and says why.
6. **Unit test coverage** for every risk object, including its unit and its validity interval.
7. **No safeguard modified**: a diff review confirms that source separation, protected holdouts,
   trading/risk/approval/holding rules and open-position handling are unchanged. This is a **standing
   requirement**, verified by inspection, not by a test.
8. Every refusal, veto, replay and `unknown` appears in the run log.
9. Per-venue capability facts each carry a source and a check date, and none was obtained by connecting to a
   venue during this engagement.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Adopting NautilusTrader, Freqtrade, Hummingbot or LEAN | Copyleft or platform-scale replacement of existing components (contradicts R5); their **designs** are adopted instead |
| `ib_async` / any brokerage connection | Implies a live gateway; outside authorisation |
| CCXT as a live connector | Same; the Manual is adopted as a reference map |
| `gs-quant` | Most functions require a Goldman Sachs account |
| Temporal / Airflow / Prefect / Dagster for durable retries | Server and database footprint; a run log plus `tenacity` covers it |
| Database-unique-constraint-only idempotency | Prevents a duplicate row, not a duplicate effect |
| Blind retry on an ambiguous timeout | Requirement 11.3; the core failure mode of this workstream |
| Assuming a venue supports client order ids | Requirement 11.7; capabilities differ and assuming is inventing |
| Bundling vendor ToS/API documentation | Not redistributable, and unreachable for download; metadata-only with links |
| Placing an order, changing a live limit, or touching a safeguard | Prohibited by this engagement's authorisation |
| Presenting any of this as execution readiness | It is research; nothing was connected or run |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **Q9: does SAM-X execute model-generated or downloaded code anywhere?** | The phase order — if yes, workstream 14 comes first | Ask. This is the highest-leverage unknown in the collection |
| **Q10: are safeguards enforced in code, in configuration, or by convention?** | What "do not touch safeguards" concretely means, and how much care step 7 needs | Ask; a convention is not a control |
| What execution-related code SAM-X already has | Steps 2–6 | Ask; inventory |
| Whether any live venue interaction is intended at all | Whether this workstream has a future phase | Ask; it is outside this engagement either way |
| Per-venue capability facts are read from CCXT's Manual, not verified against a venue | Requirement 11.7's accuracy | Verification requires connecting, which requires authorisation |
| Stale-data horizons per data type | Requirement 11.4 | A decision for the user, informed by vendor update cadence |
| Vendor idempotency documentation is metadata-only | Citing exact vendor semantics | Read the linked pages at adoption time; they change and are not redistributable |
| Nothing here was executed, installed or connected | All of §7 | Requires authorisation this engagement did not have |
