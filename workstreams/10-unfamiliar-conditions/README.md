# Workstream 10 — Unfamiliar Conditions, Regime Change and Conservative Failure

**Objectives served:** demonstrate transfer; handle stale and conflicting information safely; **fail
conservatively under unfamiliar conditions, uncertainty or resource shortage**.

**The framing that governs this workstream:** the goal is **recognising situations the system does not
support**, not claiming reliable performance in all market conditions. No component here makes SAM-X work
everywhere, and nothing in this collection promises universal market handling.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 10.1 | **Constant-memory** monitoring — the detector must not become the thing that exhausts the budget | Workstream 01's ceiling applies to monitoring too |
| 10.2 | A recorded **scope** for every procedure, and a gate that refuses to run outside it | "This was shown to work on X" is only useful if X is written down and checked |
| 10.3 | **False-alarm budget** declared before thresholds are chosen | A detector that always fires is a detector nobody reads |
| 10.4 | **Nominal versus realised coverage** reported for any interval estimate | A large gap *is* the unfamiliar-condition signal |
| 10.5 | Change-point detection with a **fixed, recorded penalty** | An auto-tuned penalty is an invisible parameter |
| 10.6 | Latent-state labels recorded as **hypotheses**, never as facts | Workstream 06, requirement 6.3 |
| 10.7 | **Stale-data refusal**: data older than a declared horizon blocks the dependent step | Objective: fail conservatively |
| 10.8 | Resource shortage handled by **degrade-then-refuse**, with the event logged | Requirement 1.2 |
| 10.9 | Detection quality measured against **injected** shifts, with measured delay and false-alarm count | "It detected the regime change" is not a measurement without a denominator |

**Not a goal.** Predicting regimes. Detecting that the current situation is outside the recorded scope is
a much weaker and much more achievable claim, and it is the one that prevents damage.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: three small permissive libraries, plus a suitability gate

| Layer | Component | Licence | Why |
|---|---|---|---|
| Drift / online detection | **`river`** — ADWIN, DDM, KSWIN, HDDM | BSD-3 | Pure-Python online learners with **constant memory per model by design** — the only drift option in the shortlist whose memory behaviour is a stated design property |
| Change points | **`ruptures`** — Pelt, binopt, dynp | BSD-2 | Light; cost depends on the method. Use a **fixed, recorded penalty** |
| Interval estimates | **`MAPIE`** — conformal prediction | BSD-3 | sklearn-compatible; light; the cost is repeated fits. Nominal-vs-realised coverage is the signal (10.4) |
| Latent states (optional) | **`hmmlearn`** | BSD-3 | sklearn-style, CPU, light — but state labels go to `hypotheses` |

The **suitability gate** is the part that actually delivers the objective, and it is not a library: every
procedure in the workstream-06 `procedures` store carries `scope_shown_to_work`; before running, the gate
checks the current regime description against that scope and **refuses with a recorded reason** if it does
not match. A refusal is a successful outcome of this workstream, not a failure.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **Alibi Detect** (Seldon) | **Not adopted** | **Business Source License 1.1** — non-production use only until each version's change date (4 years), then Apache-2.0. Its drift detectors (KSWIN, Page-Hinkley) are light and would otherwise be an obvious choice; `river` provides the same family under BSD-3. This licence finding is one of the reasons the recommendation changed |
| **`crepes`** | Catalogued, weak evidence | Very light vectorised conformal wrappers, but **no resolvable GitHub repository** (`M4LC0N/crepes`) — only PyPI registry metadata. Inspectable source is a requirement for something that decides when to refuse |
| **Google Uncertainty Baselines** | Reference only | TensorFlow/JAX research-grade implementations; heavy, and aimed at model uncertainty rather than regime suitability |
| **`pymc`** | Catalogued | MCMC is CPU/RAM heavy; variational inference is lighter but weaker. Useful only if a genuinely Bayesian treatment is required |
| **`var-anomaly`** (arXiv:2105.07538v1, Maeng / Eckley / Fearnhead, **verified** metadata) | **Metadata-only, but the most relevant paper here** | A lasso-based sparse-VAR collective anomaly test with **Type-I error control**. Relevant precisely because most ad-hoc drift detectors have no false-alarm guarantee, which requirement 10.3 asks for. PDF not bundled: no binary download route, and arXiv's licence does not grant redistribution |
| **Deep OOD / neural detectors** | Not assessed | Weights and GPU; out of scope for the reported machine (Q1) |
| Regime **prediction** | Rejected as a goal | See §1: detection of out-of-scope conditions, not prediction |

### 2.3 Why injected shifts are the only honest way to measure this

Real regime changes are rare, unlabelled and retrospectively argued about. An injected shift is a synthetic
fixture with a known onset time, so **detection delay** and **false-alarm count** become measurable against
a denominator. That makes this a *synthetic fixture test* in the taxonomy of
[EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §8 — explicitly **not** a source-based qualification and
explicitly **not** evidence about real markets. The distinction is recorded in every report.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `river` (BSD-3) | [documentation](../../resources/documentation/river/) · [licence](../../resources/licenses/river/) |
| `ruptures` (BSD-2) | [documentation](../../resources/documentation/ruptures/) · [licence](../../resources/licenses/ruptures/) (**slug corrected from `centre-borelli/ruptures` to `deepcharles/ruptures`**) |
| `mapie` (BSD-3) | [documentation](../../resources/documentation/mapie/) · [licence](../../resources/licenses/mapie/) |
| `hmmlearn` (BSD-3) | [documentation](../../resources/documentation/hmmlearn/) · [licence](../../resources/licenses/hmmlearn/) — dormant since 2024-10 |
| `alibi-detect` (**BSL 1.1**) | [documentation](../../resources/documentation/alibi-detect/) · [licence](../../resources/licenses/alibi-detect/) — **non-production only until the change date** |
| `crepes` | [registry metadata](../../resources/documentation/_pypi-metadata/) only — **no resolvable upstream repository** |
| `uncertainty-baselines` (Apache-2.0) | [documentation](../../resources/documentation/uncertainty-baselines/) · [licence](../../resources/licenses/uncertainty-baselines/) |
| `pymc` (Apache-2.0) | [documentation](../../resources/documentation/pymc/) · [licence](../../resources/licenses/pymc/) — bundled MIT notices also present |
| `var-anomaly` | **No bundled asset** — metadata-only catalog row; arXiv:2105.07538v1 (**verified** 2026-10-14). See [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) |
| Shared with workstream 02 | [duckdb](../../resources/documentation/duckdb/) · [polars](../../resources/documentation/polars/) · [pandera](../../resources/documentation/pandera/) — feature pipelines under a memory limit |
| Shared with workstream 12 | [tenacity](../../resources/documentation/tenacity/) · [prometheus-client](../../resources/documentation/prometheus-client/) — degrade/refuse events must be telemetry-visible |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| River | https://github.com/online-ml/river |
| ruptures | https://github.com/deepcharles/ruptures · https://centre-borelli.github.io/rupture-docs/ |
| MAPIE | https://github.com/scikit-learn-contrib/MAPIE |
| hmmlearn | https://github.com/hmmlearn/hmmlearn |
| Alibi Detect | https://github.com/SeldonIO/alibi-detect — **BSL 1.1; read the change date before any production use** |
| crepes | https://pypi.org/project/crepes/ — **no resolvable GitHub repository at the check date** |
| Uncertainty Baselines | https://github.com/google/uncertainty-baselines |
| PyMC | https://github.com/pymc-devs/pymc |
| VAR anomaly paper | arXiv:2105.07538v1 (**verified**) — Maeng, Eckley, Fearnhead |

## 5. Adoption steps

1. **Write the scope descriptor** for each existing procedure: which symbols, timeframes, volatility
   conditions, liquidity conditions and data-quality conditions it was shown to work under. Without this,
   there is nothing for a gate to check.
2. **Add `river` drift detectors** on the features that define that scope, one per monitored series, with
   the detector's memory behaviour verified against the workstream-01 ceiling.
3. **Add `ruptures` change-point detection** with a **fixed, recorded penalty**. Never an auto-tuned one.
4. **Add `MAPIE` conformal intervals** where an interval estimate is used, and report nominal versus
   realised coverage every cycle.
5. **Implement the suitability gate**: current regime description versus `scope_shown_to_work` → run, or
   refuse with a recorded reason. A refusal is logged as a success of the gate.
6. **Implement stale-data refusal** (10.7): a declared horizon per data type; data older than the horizon
   blocks the dependent step and says why.
7. **Wire degrade-then-refuse on resource shortage** (10.8) to the workstream-01 enforcement hook, with
   every event logged and telemetry-visible.
8. **Build the injected-shift fixture set** and measure detection delay and false-alarm count against the
   declared budget (10.3, 10.9).
9. **Route any latent-state label to `hypotheses`** (10.6).

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| `river` detectors | **Constant memory per model by design** | The defining property; verify it with a sampler anyway |
| `ruptures` (Pelt) | Light; cost depends on method and signal length | `dynp` and `binopt` are more expensive |
| `MAPIE` | Light; the cost is **repeated fits** | Declare how often intervals are refit |
| `hmmlearn` | Light, sklearn-style, CPU | Fitting cost grows with states and sequence length |
| `alibi-detect` | TensorFlow/PyTorch backends | Heavier than `river`, and licence-restricted besides |
| `uncertainty-baselines` | TensorFlow/JAX, research-grade, **heavy** | Reference only |
| `pymc` MCMC | CPU/RAM heavy | Variational is lighter and weaker |
| Injected-shift fixtures | Storage for the fixtures plus repeated runs | Cheap; run them in CI |

## 7. Qualification requirements

1. Injected shifts are detected with a **measured delay** and a **false-alarm count within the declared
   budget**, on a pre-declared fixture set.
2. Detector memory is verified constant (or bounded) over a long run, sampled out-of-process.
3. The suitability gate **refuses** on a planted out-of-scope condition and records the reason; and **runs**
   on an in-scope condition.
4. A procedure with no recorded scope **cannot run** — verified by a test that attempts it and must fail.
5. `ruptures` penalty is fixed and recorded; changing it changes the run id.
6. MAPIE nominal versus realised coverage is reported every cycle; a large gap raises the unfamiliarity
   signal rather than being silently absorbed.
7. Stale data older than the declared horizon blocks the dependent step, and the block is visible in the run
   log.
8. Resource shortage produces a logged degrade-then-refuse sequence, never a partial answer presented as
   complete.
9. Every latent-state label is in `hypotheses`, and no answer's `evidence` field contains one.
10. Every result is labelled a **synthetic fixture test** — never observed-market research, never
    live-performance evidence.
11. **Transfer**: the same gate, on a different symbol or timeframe, is re-measured rather than assumed to
    hold.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Alibi Detect in production | BSL 1.1 — non-production only until the change date |
| `crepes` as the conformal layer | No resolvable upstream repository; only registry metadata. Inspectable source is a requirement for a refusal decision |
| Deep neural OOD detectors | Weights and GPU; Q1 unanswered |
| Auto-tuned change-point penalties | An invisible parameter (requirement 10.5) |
| Regime **prediction** as a goal | Out of scope; detection of out-of-scope conditions is the achievable claim |
| Treating a latent-state label as a fact | Requirement 10.6 |
| Claiming reliable performance in all market conditions | Prohibited |
| Reporting detection without a false-alarm denominator | Requirement 10.9 |
| Treating an injected-shift result as evidence about real markets | Requirement 10 and [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §8 |
| Monitoring that itself exhausts the memory budget | Requirement 10.1 |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **Threshold selection and the false-alarm budget** | Requirements 10.3, 10.9 | A decision for the user; it is a risk-tolerance question, not a technical one |
| The scope descriptors for existing procedures | Step 1 — the whole gate | Ask; inspect existing research records |
| Whether detection transfers between symbols, timeframes and regimes | §7 item 11 | Measure per class; never assume |
| Whether `river`'s constant-memory property holds under the actual feature rate | Requirement 10.1 | Sample it (needs install authorisation) |
| The stale-data horizon per data type | Requirement 10.7 | A decision for the user, informed by the data vendor's update cadence |
| `var-anomaly`'s method is metadata-only | Whether a Type-I-controlled test is worth implementing | Re-derive from the official source; the lasso sparse-VAR construction is described in the verified abstract |
| Alibi Detect's change date for the specific version considered | Any future reconsideration | Read the bundled licence text; it is version-specific |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
