# Workstream 09 — Reproducible Historical Research and Backtesting

**Objectives served:** reproducible historical research and backtesting; never invent parameters; fail
conservatively; preserve source separation and protected holdouts.

**Scope limit stated up front: this workstream is research-only.** No order was placed, no credential
configured, no venue contacted and no strategy is recommended anywhere in this collection. Nothing here is
evidence that any strategy makes money, and no result here should be read as one.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 9.1 | **One config artefact pins every research decision** — data generation, universe, labels, features, model, costs, timing | A backtest nobody can re-run is an anecdote |
| 9.2 | **Immutable data generations** with hashes, and rollback by repointing | Workstream 02; without it the inputs can silently change |
| 9.3 | **Look-ahead prevention**, proven by a truncation-equivalence test | The most common way a backtest lies |
| 9.4 | Resampled bars are **complete bars only** | A partial bar in a decision is look-ahead |
| 9.5 | Costs, slippage and timing modelled explicitly, with the model written down | A frictionless backtest is a different experiment |
| 9.6 | **Stop-first semantics decided and tested**: on a bar where both stop and target are touched, which happens first? | Engines differ; an undecided rule is an invisible assumption |
| 9.7 | **Multiple-testing discipline**: record the number of trials; report an adjusted metric alongside any naive best result | The naive best of N trials is not an estimate of anything |
| 9.8 | Observations and estimates kept separate; missing data carries a recorded reason | Workstream 02, requirements 2.5 and 2.6 |
| 9.9 | Test kinds separated: synthetic engineering test ≠ observed-market research ≠ live-performance evidence | Requirement 8.12 |
| 9.10 | Copyleft engines are **read for semantics, never vendored** | Licensing, and R5's preference for reusing existing components |

**Not a goal.** A faster backtester. The goal is a backtest whose number means what it appears to mean.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: borrow the semantics, own the code

The strongest open backtesting engines in the shortlist are **copyleft**: backtesting.py (AGPL-3.0),
Backtrader (GPL-3.0), Freqtrade (GPL-3.0), NautilusTrader (LGPL-3.0), vectorbt (Apache-2.0 **plus a Commons
Clause**). Vendoring any of them changes SAM-X's licensing obligations, and adopting a whole platform would
**replace** existing components rather than complement them (contradicting R5).

So the recommendation is: **read them, implement the semantics you need, own the code.**

| Permissive reference (bundled) | What to take from it |
|---|---|
| `zipline-reloaded` (Apache-2.0) — `finance/slippage.py`, `finance/commission.py`, `finance/controls.py` | Explicit, typed slippage and commission models; a **pre-trade risk control** interface that can veto |
| `ml4t` (MIT) — `07_defining_the_learning_task/` | Labelling methods, maximum favourable/adverse excursion, signal evaluation, IC inference, and **multiple testing** |
| `qlib` (MIT) — 13 `workflow_config_*.yaml` | The single-artefact research config (requirement 9.1) |
| `freqtrade` (GPL-3.0, docs bundled) — `stoploss.md`, lookahead-analysis docs | Stop-first semantics and a **truncation-equivalence** test concept — re-implemented, not copied |
| `bt` (MIT), `quantstats` (Apache-2.0), `PyPortfolioOpt` (MIT), `riskfolio` (BSD-3) | Lightweight permissive building blocks for tree-based backtests, reporting telemetry, optimisation and risk measures |
| `duckdb` (MIT), `polars` (MIT), `pandera` (MIT), `xarray` (Apache-2.0) | Analysis, transformation and validation under a memory limit |

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **NautilusTrader** (LGPL-3.0) | **Reference design only** | The strongest open RiskEngine documentation bundled here (19 assets), and a real low-latency platform — but adopting it means replacing existing components, and it has a native Rust core with a real memory footprint |
| **Freqtrade** (GPL-3.0) | **Reference only** | Excellent dry-run mode and stoploss documentation; GPL and a whole bot framework |
| **backtesting.py** (AGPL-3.0) | **Reference only** | Light and single-process; AGPL reaches a networked service |
| **Backtrader** (GPL-3.0) | **Reference only** | Event-driven and well understood; GPL and dormant (last push 2024-08) |
| **vectorbt** | **Not adopted** | Apache-2.0 **plus Commons Clause** — redistribution allowed, **selling not allowed**; PRO is a separate paid product. Peak RAM also scales with the indicator matrix |
| **QuantConnect LEAN** (Apache-2.0, C#) | Not adopted | .NET runtime, substantial footprint, and a different language stack |
| **Jesse** (MIT) | Catalogued | Recent versions want Postgres for candles |
| **Qlib as a platform** | Config pattern adopted, platform not | Data server plus workflow engine, sized for research clusters |
| **`gs-quant`** | **Rejected** | Apache-2.0 client, but most functions require a Goldman Sachs account — an authorisation and counterparty relationship this project does not have |
| **`mlfinlab`** | **Rejected** | Proprietary, no redistribution right, dormant since 2023 (MO-05). Its MIT-licensed academic companion (`ml4t`) is bundled instead |
| **`pymc`** (Apache-2.0) | Catalogued | MCMC is CPU/RAM heavy; variational is lighter but weaker. Useful if a Bayesian treatment of a parameter is genuinely needed |
| **`hmmlearn`** (BSD-3) | Catalogued (shared with workstream 10) | Latent-state models for regime work; state labels are hypotheses, not facts |
| **`yfinance`** | Convenience source only | Unofficial client; no data licence or SLA; back-adjusted prices can **silently rewrite history**. Freeze every pull by hash |
| **`pandas-ta-classic`** (MIT) | Catalogued with a caveat | The original `twopirllc/pandas-ta` returned HTTP 404 on 2026-10-14. **A library default is never a document parameter** — workstream 04, confusion C5 |
| Copying López de Prado or Jansen book chapters | **Prohibited** | Copyrighted books, metadata-only (MO-07). Their MIT-licensed companion code is bundled instead |

### 2.3 The multiple-testing rule, stated plainly

If you try N configurations and report the best, you have not estimated performance; you have estimated the
maximum of N noisy draws. The bundled `ml4t/07_defining_the_learning_task/07_multiple_testing.py` is the
concrete arithmetic. The rule adopted here: **no strategy is promoted on a naive Sharpe alone** — the trial
count and an adjusted (deflated) metric are reported together, or the result is labelled a search artefact.
The same discipline applies to evaluations (workstream 08) and is enforced there by recording the number of
configurations compared.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `ml4t` (MIT) | [code examples](../../resources/code-examples/ml4t/) — `03_label_methods.py`, `04_maximum_favorable_adverse_excursion.py`, `05_signal_evaluation.py`, `06_ic_inference.py`, `07_multiple_testing.py` · [documentation](../../resources/documentation/ml4t/) · [licence](../../resources/licenses/ml4t/) |
| `zipline` (Apache-2.0) | [code examples](../../resources/code-examples/zipline/) — slippage, commission and controls modules · [documentation](../../resources/documentation/zipline/) · [licence](../../resources/licenses/zipline/) |
| `qlib` (MIT) | [13 workflow configs](../../resources/configurations/qlib/) · [documentation](../../resources/documentation/qlib/) |
| `freqtrade` (GPL-3.0) | [documentation](../../resources/documentation/freqtrade/) — including stoploss and lookahead analysis · [config templates](../../resources/configurations/freqtrade/) · [licence](../../resources/licenses/freqtrade/) |
| `nautilus` (LGPL-3.0) | [documentation](../../resources/documentation/nautilus/) — 18 files including the RiskEngine design · [configurations](../../resources/configurations/nautilus/) · [licence](../../resources/licenses/nautilus/) |
| `backtesting-py` (AGPL-3.0) | [documentation](../../resources/documentation/backtesting-py/) · [code examples](../../resources/code-examples/backtesting-py/) · [licence](../../resources/licenses/backtesting-py/) |
| `backtrader` (GPL-3.0) | [documentation](../../resources/documentation/backtrader/) · [licence](../../resources/licenses/backtrader/) |
| `vectorbt` (Commons Clause) | [documentation](../../resources/documentation/vectorbt/) · [licence](../../resources/licenses/vectorbt/) |
| `bt` (MIT), `quantstats` (Apache-2.0) | [bt](../../resources/documentation/bt/) · [bt code](../../resources/code-examples/bt/) · [QuantStats](../../resources/documentation/quantstats/) · [QuantStats code](../../resources/code-examples/quantstats/) |
| `pyportfolioopt` (MIT) | [documentation](../../resources/documentation/pyportfolioopt/) · [code examples](../../resources/code-examples/pyportfolioopt/) · [licence](../../resources/licenses/pyportfolioopt/) (**slug corrected from `robertmartin8/PyPortfolioOpt`**) |
| `riskfolio` (BSD-3) | [documentation](../../resources/documentation/riskfolio/) · [licence](../../resources/licenses/riskfolio/) |
| `duckdb`, `polars`, `pandera`, `xarray` | [duckdb](../../resources/documentation/duckdb/) · [polars](../../resources/documentation/polars/) · [pandera](../../resources/documentation/pandera/) · [xarray](../../resources/documentation/xarray/) |
| `hmmlearn` (BSD-3), `pymc` (Apache-2.0) | [hmmlearn](../../resources/documentation/hmmlearn/) · [pymc](../../resources/documentation/pymc/) — dormant since 2024-10 (hmmlearn) |
| `lean` (Apache-2.0, C#) | [documentation](../../resources/documentation/lean/) · [configurations](../../resources/configurations/lean/) · [licence](../../resources/licenses/lean/) |
| `jesse` (MIT) | [documentation](../../resources/documentation/jesse/) · [licence](../../resources/licenses/jesse/) |
| `yfinance`, `pandas-ta-classic` | [yfinance](../../resources/documentation/yfinance/) · [pandas-ta-classic](../../resources/documentation/pandas-ta-classic/) |
| `gs-quant` | [documentation](../../resources/documentation/gs-quant/) — **rejected**: most functions require a Goldman account |
| Books | **Not bundled** (MO-07) — metadata-only |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| ml4t | https://github.com/stefan-jansen/machine-learning-for-trading (**1.30 GB — never tarball**) |
| zipline-reloaded | https://github.com/stefan-zhao/zipline-reloaded (community continuation) |
| Qlib | https://github.com/microsoft/qlib |
| Freqtrade | https://github.com/freqtrade/freqtrade · https://www.freqtrade.io/ |
| NautilusTrader | https://github.com/nautechsystems/nautilus_trader |
| backtesting.py | https://github.com/kernc/backtesting.py |
| Backtrader | https://github.com/mementum/backtrader (dormant since 2024-08) |
| vectorbt | https://github.com/polakowo/vectorbt |
| bt | https://github.com/pmorissette/bt |
| QuantStats | https://github.com/ranaroussi/quantstats |
| PyPortfolioOpt | https://github.com/PyPortfolio/PyPortfolioOpt |
| Riskfolio-Lib | https://github.com/dcajasn/Riskfolio-Lib |
| LEAN | https://github.com/QuantConnect/Lean |
| Jesse | https://github.com/jesse-ai/jesse |
| gs-quant | https://github.com/goldmansachs/gs-quant |
| mlfinlab | https://github.com/hudson-and-thames/mlfinlab — **proprietary, nothing bundled** (MO-05) |
| López de Prado, *Advances in Financial Machine Learning* | Wiley — **copyrighted book, metadata-only** (MO-07) |

## 5. Adoption steps

1. **Inventory the existing research path** before changing it (R5). Which engine, which data source, which
   config mechanism, which reports?
2. **Adopt the single-artefact config** (Qlib pattern): one YAML/JSON per research run pinning the data
   generation id and hash, universe, label definition, features, model, cost model, timing rule, random
   seeds and the trial count. Hash it into the run record (workstream 08).
3. **Point every run at an immutable generation** (workstream 02). No run reads a mutable path.
4. **Write the truncation-equivalence test** (requirement 9.3): decisions at times ≤ T must be bit-identical
   whether or not post-T data exists in the store. This one test catches most look-ahead bugs, including
   resampling and normalisation leaks.
5. **Decide and document stop-first semantics** (9.6), then write a test with a bar where both stop and
   target are inside the range and assert the documented outcome.
6. **Model costs, slippage and timing explicitly**, following the zipline `slippage.py` / `commission.py`
   typed-model pattern, and record the model in the config artefact.
7. **Add the pre-trade veto interface** (zipline `controls.py` pattern) as a research-time gate — never as a
   live-trading change.
8. **Record the trial count** for every search, and report a deflated/adjusted metric next to any naive best
   (`ml4t/07_multiple_testing.py`).
9. **Label every result with its test kind** (9.9) and state explicitly that nothing here is
   live-performance evidence.

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| DuckDB analysis | Bounded by `memory_limit`, **advisory for some operators**; spills to disk | Set it and verify with a sampler |
| Polars streaming | Bounds intermediate memory; Arrow zero-copy | The non-streaming path can materialise everything |
| vectorbt | Fast, but **peak RAM scales with the indicator matrix** | Plus the Commons Clause |
| NautilusTrader | Rust core, low latency, **a real memory footprint** | Native build required |
| Qlib platform | Data server + workflow engine | Sized for research clusters |
| LEAN | .NET runtime, substantial | Different language stack |
| Jesse | Postgres for candles in recent versions | An extra service |
| `pymc` MCMC | CPU/RAM heavy | Variational is lighter and weaker |
| `ml4t` notebooks | Heavy only when run | The bundled scripts are small |
| Freqtrade | Python plus optional Postgres | Dry-run mode is light |
| Truncation-equivalence test | Two full runs per check | Worth it; run it in CI, not by hand |

## 7. Qualification requirements

1. Two independent runs from the same generation manifest and the same config artefact produce
   **byte-identical** outputs.
2. The truncation-equivalence test passes: decisions at ≤ T are bit-identical with and without post-T data.
3. Resampling produces complete bars only; a planted partial-bar case is rejected.
4. Stop-first behaviour matches the documented rule on a bar where both stop and target are touched.
5. Costs, slippage and timing are all non-zero and recorded in the config artefact; a frictionless run is
   visibly labelled as such.
6. Every reported result states its **trial count** and an adjusted metric alongside any naive best.
7. Observations and estimates are never combined; every gap carries a reason.
8. Every result is labelled mechanical / synthetic / observed-market research, and **none** is labelled
   live-performance evidence.
9. No copyleft engine code is present in the project's own source tree — verified by inspection and by a
   licence scan.
10. A vendor re-pull that differs from the frozen generation is detected (workstream 02, §7 item 6).

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Vendoring backtesting.py / Backtrader / Freqtrade / NautilusTrader | AGPL / GPL / GPL / LGPL obligations; and adopting a platform replaces existing components (contradicts R5) |
| vectorbt | Commons Clause: no selling; PRO is a separate paid product |
| `gs-quant` | Most functions require a Goldman Sachs account |
| `mlfinlab` | Proprietary; no redistribution right; dormant since 2023 |
| Copying book chapters | Copyrighted; metadata-only (MO-07) |
| `yfinance` as a system of record | Unofficial client; back-adjustment can silently rewrite history |
| Promoting a strategy on a naive Sharpe alone | Requirement 9.7 |
| Reporting a backtest without its trial count | Same |
| Assuming stop-first semantics | Requirement 9.6; engines differ |
| Treating a synthetic engineering test as observed-market research | Requirement 9.9 |
| Placing an order, connecting to a venue, or changing live policy | Outside this engagement's authorisation, and prohibited |
| Claiming or implying profitability | Prohibited; no result here is evidence about trading performance |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| What research/backtesting path SAM-X already has (engine, data, configs, reports) | Every adoption step | Ask; inventory |
| Rights over the historical data (storage, derived works, redistribution) | Whether generations may leave the machine | Question for the user, related to Q4 |
| Whether the vendors in use back-adjust or rewrite history | The freeze-by-hash design | The two-pull diff experiment; needs network access and vendor authorisation |
| The project's stop-first rule | Requirement 9.6 | A decision for the user; it is a semantic choice, not a technical one |
| An exchange-calendar source | Gap-reason classification (workstream 02) | None bundled; none assessed |
| Acceptable trial-count and adjusted-metric thresholds | Requirement 9.7 | Pre-declare before the first search |
| Whether any existing backtest has ever been truncated-tested | How much of the existing research is trustworthy | Run the test; the answer may be uncomfortable and is worth knowing |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
