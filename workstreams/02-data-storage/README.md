# Workstream 02 — Historical Data, Storage and Reproducible Generations

**Objectives served:** reproducible historical research and backtesting; safe handling of stale and
conflicting information; never inventing parameters — including never inventing *data*.

**Reported context:** nothing in R1–R5 speaks to data infrastructure directly. R5 (prefer reusing
compatible existing components) applies strongly here: whatever store SAM-X already uses is the baseline,
and this workstream's first job is to inventory it, not replace it.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 2.1 | **Immutable generations**: once published, a data generation is never edited in place | A backtest whose inputs can silently change is not reproducible |
| 2.2 | A manifest per generation: schema, provenance, source, retrieval timestamp, per-file hash | Provenance is a first-class object, not a comment |
| 2.3 | **Atomic publication**: write to a temporary location, verify the hash, rename | A half-written generation must never be readable |
| 2.4 | Rollback by **repointing** at an earlier generation, never by restoring mutated files | Reversibility without data loss |
| 2.5 | **Observations and estimates as separate typed columns** | Mixing them silently manufactures data |
| 2.6 | A recorded **reason** for every gap: `closure`, `no-trade`, `vendor-gap`, `unknown` | A missing timestamp is *not* evidence of a market closure |
| 2.7 | Coverage and gap inspection without loading the corpus into RAM | Ties into workstream 01 |
| 2.8 | Schema and unit validation at ingest, failing loudly | A unit error is a silent research error |
| 2.9 | Every data pull frozen by hash at ingestion | Vendor back-adjustment can rewrite history after the fact |

**Not a goal.** Building a data platform. The recommendation is a directory layout plus a manifest plus a
validator — deliberately less than Delta Lake, DVC or Zarr, and the reasoning is in §8.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: generation directories + manifest + atomic rename

```
data/
  generations/
    2026-10-14T09:12:00Z__bars__v3/
      manifest.json          # schema, provenance, source ids, retrieval timestamps, per-file sha256
      part-0000.parquet
      part-0001.parquet
    ...
  CURRENT -> generations/2026-10-14T09:12:00Z__bars__v3     # rollback = repoint this
```

Validation with `pandera` (MIT) at ingest; coverage/gap inspection with `DuckDB` under an explicit
`memory_limit`; reshaping with `Polars` streaming. This delivers ~80% of what a table format provides, with
no native dependency and no format migration risk.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| `delta-rs` / Delta Lake | **Upgrade path**, catalogued | Worth it if concurrent readers or true time travel become real needs; not needed for a single-writer research store |
| `DVC` | **Not adopted** | Ownership changed during the check window (`iterative/dvc` → `treeverse/dvc`) — a supply-chain signal. A sha256 manifest is a few lines and is fully under project control |
| `Zarr` | **Not adopted as primary** | A live v2/v3 format transition is a migration risk for a store meant to be readable years later |
| `xarray` | Adopt **for labelled arrays only** | Excellent model for multi-dimensional labelled data; not a versioning or provenance mechanism |
| `Great Expectations` | Documented alternative to `pandera` | Overlapping scope; upstream org moved to Fivetran during the check window |
| `Frictionless` | Adopt the **descriptor idea** | A schema/metadata descriptor per generation is worth borrowing without the framework |
| `Luigi` | Adopt the **target-existence pattern** | "A step is complete iff its output exists with a recorded hash" is exactly the checkpoint model workstream 12 needs; the scheduler is not |
| `Prefect`, `Dagster`, `Airflow` | **Rejected** | Server/daemon footprint; see §8 |
| `Qlib` | Adopt the **workflow-config pattern** | Its 13 bundled `workflow_config_*.yaml` files are the clearest example of pinning every research decision in one artefact |

### 2.3 The provenance rule that matters most

A fact extracted from a document, and a bar read from a vendor, are the same kind of object: **a value with
a source, a version and a retrieval time**. Both go through the same manifest discipline. This is what makes
"the data changed under us" detectable rather than mysterious.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `ml4t` (Jansen companion code, MIT) | [code examples](../../resources/code-examples/ml4t/) — including `07_defining_the_learning_task/` with `03_label_methods.py`, `04_maximum_favorable_adverse_excursion.py`, `05_signal_evaluation.py`, `06_ic_inference.py`, `07_multiple_testing.py` · [documentation](../../resources/documentation/ml4t/) · [licence](../../resources/licenses/ml4t/) |
| `qlib` (MIT) | [13 workflow configs](../../resources/configurations/qlib/) · [documentation](../../resources/documentation/qlib/) |
| `duckdb` | [documentation](../../resources/documentation/duckdb/) — `guides/performance/environment.md`, `how_to_tune_workloads.md` · [licence](../../resources/licenses/duckdb/) |
| `polars` | [documentation](../../resources/documentation/polars/) · [licence](../../resources/licenses/polars/) |
| `pandera` | [documentation](../../resources/documentation/pandera/) · [licence](../../resources/licenses/pandera/) |
| `great_expectations` | [documentation](../../resources/documentation/great_expectations/) · [licence](../../resources/licenses/great_expectations/) |
| `luigi` | [documentation](../../resources/documentation/luigi/) · [licence](../../resources/licenses/luigi/) |
| `delta-rs` | [documentation](../../resources/documentation/delta-rs/) · [licence](../../resources/licenses/delta-rs/) |
| `xarray` | [documentation](../../resources/documentation/xarray/) · [licence](../../resources/licenses/xarray/) |
| `zarr` | [registry metadata](../../resources/documentation/_pypi-metadata/) · [licence](../../resources/licenses/zarr/) |
| `dvc` | [documentation](../../resources/documentation/dvc/) · [licence](../../resources/licenses/dvc/) |
| `frictionless` | [documentation](../../resources/documentation/frictionless/) · [licence](../../resources/licenses/frictionless/) |
| `sqlitedict` | [documentation](../../resources/documentation/sqlitedict/) · [code examples](../../resources/code-examples/sqlitedict/) |
| `ccxt` | [documentation](../../resources/documentation/ccxt/) — including `wiki/Manual.md` (0.52 MB), the factual map of per-venue capabilities · [licence](../../resources/licenses/ccxt/) |
| `yfinance` | [documentation](../../resources/documentation/yfinance/) · [licence](../../resources/licenses/yfinance/) |
| `pandas-ta-classic` | [documentation](../../resources/documentation/pandas-ta-classic/) · [registry metadata](../../resources/documentation/_pypi-metadata/) · [licence](../../resources/licenses/pandas-ta-classic/) |
| `river`, `ruptures` | [river docs](../../resources/documentation/river/) · [ruptures docs](../../resources/documentation/ruptures/) — streaming ingest and change detection (shared with workstream 10) |
| `var-anomaly` | **No bundled asset** — metadata-only catalog row for arXiv:2105.07538v1 (Maeng, Eckley, Fearnhead), verified 2026-10-14. See [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) |
| Rejected on footprint | [dagster](../../resources/documentation/dagster/) · [prefect](../../resources/documentation/prefect/) · [airflow](../../resources/documentation/airflow/) · [dask](../../resources/documentation/dask/) |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| ml4t | https://github.com/stefan-jansen/machine-learning-for-trading |
| Qlib | https://github.com/microsoft/qlib |
| DuckDB | https://github.com/duckdb/duckdb-web · https://duckdb.org/ (unreachable from the build sandbox) |
| Polars | https://github.com/pola-rs/polars |
| pandera | https://github.com/unionai-oss/pandera |
| Great Expectations | https://github.com/fivetran/great_expectations (**org moved from `great-expectations/` during the check window**) |
| Luigi | https://github.com/spotify/luigi |
| delta-rs | https://github.com/delta-io/delta-rs |
| xarray | https://github.com/pydata/xarray |
| Zarr | https://github.com/zarr-developers/zarr-python |
| DVC | https://github.com/treeverse/dvc (**moved from `iterative/dvc` during the check window**) |
| Frictionless | https://github.com/frictionlessdata/frictionless-py |
| CCXT | https://github.com/ccxt/ccxt (**8.67 GB — never tarball; individual files only**) |
| yfinance | https://github.com/ranaroussi/yfinance |
| pandas-ta-classic | https://github.com/xgboosted/pandas-ta-classic (**the original `twopirllc/pandas-ta` returned HTTP 404 on 2026-10-14**) |
| López de Prado, *Advances in Financial Machine Learning* | Publisher page only — **copyrighted book, not bundled** (MO-07) |

## 5. Adoption steps

1. **Inventory what exists.** Which store does SAM-X use today, at what version, with what schema? Nothing
   below is safe to plan until this is known (R5 asks for reuse; reuse requires an inventory).
2. **Introduce generations for new data only.** Do not migrate history in place. Existing data becomes a
   read-only `legacy` generation with `provenance: UNKNOWN` recorded honestly.
3. **Write the manifest schema**: generation id, created timestamp, schema version, column types and units,
   source records (each pointing at a filled
   [source-provenance.json](../../templates/source-provenance.json)), per-file sha256, total bytes.
4. **Implement atomic publication**: temp directory → write → hash → verify → rename → repoint `CURRENT`.
   A crash at any step must leave the previous generation intact and readable.
5. **Split observations from estimates** as separate typed columns, with `pandera` enforcing the types and
   units at ingest.
6. **Add gap records with reasons.** A missing bar carries `gap_reason ∈ {closure, no-trade, vendor-gap,
   unknown}`. `unknown` is the honest default and must never be silently upgraded to `closure`.
7. **Freeze every vendor pull by hash at ingestion.** The catalog row for `yfinance` contains the experiment:
   fetch the same symbol and date range twice, seven days apart, and diff the series. If it differs, the
   vendor rewrites history and only the frozen copy is usable for research.
8. **Add coverage inspection** with DuckDB under an explicit `memory_limit`, producing a per-generation
   coverage report (rows, symbols, date range, gap counts by reason, null counts by column).
9. **Pin every research decision in one config artefact**, following the Qlib `workflow_config_*.yaml`
   pattern, and hash it into the run record (workstream 08).

## 6. Resource implications

All **estimates from documentation**; none measured on the target machine.

| Item | Expectation | Note |
|---|---|---|
| Parquet generations on disk | Disk-bound, not RAM-bound | Compression is per column chunk; read only what you scan |
| DuckDB scans | Bounded by `memory_limit`, which is **advisory for some operators** | Set it explicitly; verify with a sampler rather than trusting the setting |
| Polars streaming | Keeps intermediate state on disk | The non-streaming path can materialise everything |
| `pandera` validation | CPU cost proportional to rows | Validate a sample plus the boundaries, or the full frame if it fits |
| Manifest hashing | I/O cost proportional to generation size | Hash once at publication, never on read |
| CCXT | Library import is light; the **repository** is 8.67 GB | Only individual files were bundled |
| Luigi / Prefect / Dagster / Airflow | Scheduler plus metadata store plus webserver | Rejected on footprint — see §8 |

## 7. Qualification requirements

1. Two independent runs from the **same** generation manifest produce **byte-identical** outputs.
2. A killed publication leaves the previous generation intact and readable; no partial generation is ever
   discoverable through `CURRENT`.
3. Rollback by repointing is demonstrated, and the rolled-back run reproduces its original outputs.
4. Every column has a declared type and unit, enforced at ingest; a deliberately wrong unit fails loudly.
5. Every gap has a recorded reason; a query for "market closures" returns only rows whose reason is
   `closure`, never rows whose reason is `unknown`.
6. A vendor re-pull that differs from the frozen generation is **detected** and reported, not silently
   accepted.
7. Observations and estimates are never combined into one column, verified by schema inspection and by a
   test that attempts it and must fail.
8. The coverage report is produced for every generation and archived with the run.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Delta Lake / `delta-rs` as the primary store | Native dependency and a format commitment for a single-writer research store; catalogued as the upgrade path |
| DVC | Ownership moved during the check window; a sha256 manifest replaces most of its value in a few lines |
| Zarr as the primary format | Live v2/v3 transition; a store meant to be readable in years should not be mid-migration |
| Airflow, Prefect, Dagster, Temporal | Scheduler + webserver + metadata database (or a server plus a database) to sequence a small number of daily jobs. A SQLite run log covers it — see workstream 12 |
| `yfinance` as a system of record | Unofficial client: no data licence, no SLA, and back-adjusted prices can silently rewrite history. Acceptable only as a convenience source frozen by hash |
| `twopirllc/pandas-ta` | Upstream no longer resolves (HTTP 404 on 2026-10-14). The MIT fork `pandas-ta-classic` is catalogued **with the caveat that library defaults are never document parameters** |
| Inferring market closures from missing timestamps | Prohibited by requirement 2.6 |
| Copying chapters of *Advances in Financial Machine Learning* or *Machine Learning for Trading* | Copyrighted books; metadata-only (MO-07). Their MIT-licensed companion code is bundled instead |
| `mlfinlab` | Proprietary, no redistribution right, dormant since 2023 — see [REJECTED_OPTIONS.md](../../REJECTED_OPTIONS.md) §2 |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| SAM-X's current store, schema and versions are unknown | Every adoption step | Inventory (step 1); question for the user |
| Whether concurrent readers or time travel are ever needed | Delta Lake decision | Observe actual usage; upgrade only on evidence |
| Whether the vendors in use back-adjust or rewrite history | Step 7's freeze design | Run the two-pull diff experiment; it needs network access and vendor authorisation |
| Rights over the historical data (redistribution, storage, derived works) | Whether generations may leave the machine | Question for the user — related to Q4 |
| Symbol/calendar reference data source | Gap-reason classification | Needs an exchange calendar; none is bundled and none was assessed |
| No component here was executed or installed | All measurements | Requires authorisation this engagement did not have |
| `var-anomaly` (arXiv:2105.07538v1) is metadata-only | Its lasso sparse-VAR change test | Paper PDF not redistributable and not downloadable from the sandbox; re-derive from the official source |
