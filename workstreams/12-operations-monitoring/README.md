# Workstream 12 — Operations, Idempotency, Checkpoints and Monitoring

**Objectives served:** fail conservatively under resource shortage; reproducible research; never duplicate
work after an ambiguous failure; keep the whole thing observable on one machine.

**Reported context:** nothing in R1–R5 describes operations. R1 (limited spare RAM) is the constraint that
decides this workstream's shape: every orchestrator with a server process was rejected, and the
recommendation is a **SQLite run log plus in-process scheduling plus file-existence checkpoints** — roughly
a hundred lines instead of a platform.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 12.1 | An **ambiguous timeout must not automatically cause duplicate work** | The central operational failure mode; shared with workstream 11 |
| 12.2 | **Checkpoints as artefact targets**: a step is complete iff its output exists with a recorded hash | Resume by existence, not by re-execution |
| 12.3 | **Atomic artefact publication**: temp → hash → verify → rename | A half-written artefact must never look complete |
| 12.4 | A **run log** recording run id, task, state, attempt, timestamps, checkpoint path and outcome | Process ownership: who did what, when, and what happened |
| 12.5 | **Bounded retries with explicit predicates** (`tenacity`), never blind retry | Requirement 11.3 |
| 12.6 | **Cancellation** that leaves the store consistent | A killed job must be resumable |
| 12.7 | **Misfire policy** declared for scheduled jobs: run once, run all, or skip | An undeclared misfire policy is a duplicate-work policy |
| 12.8 | **Telemetry**: RSS, queue depth, cache hit rate, step latency — written locally, no metrics server | Observability without a Prometheus daemon |
| 12.9 | **Alerts on declared thresholds only**, each actionable | An alert nobody acts on is noise that hides the real one |
| 12.10 | **Dependency pinning with hashes**, and an advisory audit | Reproducibility plus supply-chain visibility |

**Not a goal.** A data platform. No scheduler server, no webserver, no metadata database.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: run log + target existence + in-process scheduling

| Concern | Choice | Licence | Why |
|---|---|---|---|
| Retry policy | **`tenacity`** | Apache-2.0 | Declarative and therefore auditable: which conditions retry, how many times, what backoff, what on exhaustion. Tiny |
| Checkpointing | **Luigi's target-existence pattern**, re-implemented | Apache-2.0 | "A step is complete iff its output exists with a recorded hash" is exactly requirement 12.2. Adopt the *idea*, not the scheduler |
| Scheduling | **`APScheduler`** in-process, SQLite jobstore | MIT | No server process; a declared misfire policy |
| Run log | **SQLite** table | stdlib | run id, task, state, attempt, started/finished, checkpoint path, outcome. ~100 lines |
| Metrics | **`prometheus_client`** metric *shapes* written to a local file or SQLite | Apache-2.0 | The exposition format and metric types are worth having; the server and Grafana are not |
| Operator visibility | **`rich`** terminal dashboards | MIT | Tiny, pure rendering, no service |
| Resource sampling | **`psutil`**, out-of-process | BSD-3 | Requirement 8.11; shared with workstream 01 |
| Data quality in the pipeline | **`pandera`** | MIT | Fail loudly at ingest |
| Parallelism (if ever needed) | **`joblib`** with `max_n_procs=1` by default | BSD-3 | Worker processes multiply model RAM |

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **Apache Airflow** | **Rejected** | Scheduler + webserver + metadata database: multiple long-lived processes for a small number of daily jobs |
| **Temporal** | **Rejected** | Requires a Temporal server (or Temporal Cloud). Its durable-execution model is genuinely good and its SDK code is bundled — but the footprint and the operational surface are wrong for one laptop |
| **Dagster** | **Rejected** | Daemon + webserver for full use. Its software-defined-assets *model* is a good way to think about artefacts; the runtime is not needed |
| **Prefect** | Catalogued, not adopted | Can run without a server (ephemeral/local), which makes it the least objectionable orchestrator here — but the API and UI add processes, and a run log covers the requirement |
| **Dask** | Not the primary mechanism | Scheduler + workers; worker processes each re-import and can re-load models, multiplying RAM |
| **Great Expectations** | Documented alternative to `pandera` | Heavier framework; validation runs plus stored results; upstream org moved to Fivetran during the check window |
| **Prometheus server + Grafana** | **Rejected** | Running a metrics server and a dashboard for a single-machine research system is footprint without benefit. Grafana is AGPL-3.0 besides |
| **Luigi as a scheduler** | Pattern adopted, scheduler not | Its central scheduler is a process; target existence is the valuable part |
| **LiteLLM proxy** | **Not adopted as a proxy** | MIT **except the `enterprise/` directory**; library mode is light but proxy mode adds a server. Its API-normalisation *pattern* is noted for workstream 13 |
| **`simonw-llm`** (Apache-2.0) | Catalogued for its **logging model** | A light CLI whose value here is the way it records every call and response to a local SQLite database — a good pattern for the run log's model-call section |
| **`trivy`** (Apache-2.0) | Adopt for **dependency and filesystem scanning** | A single Go binary that scans filesystems, images, dependencies and IaC; overlaps `pip-audit` and `osv-scanner` (workstream 14) |

### 2.3 The rule that makes this workstream worth having

**Every retry must be able to answer "did the previous attempt have an effect?"** If it cannot, the correct
behaviour is to stop and reconcile, not to try again. Requirements 12.1, 12.5 and 12.7 are three expressions
of that one rule: idempotency keys (workstream 11), explicit retry predicates, and a declared misfire policy.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `tenacity` (Apache-2.0) | [documentation](../../resources/documentation/tenacity/) · [code examples](../../resources/code-examples/tenacity/) · [licence](../../resources/licenses/tenacity/) |
| `luigi` (Apache-2.0) | [documentation](../../resources/documentation/luigi/) · [licence](../../resources/licenses/luigi/) |
| `apscheduler` (MIT) | [documentation](../../resources/documentation/apscheduler/) · [licence](../../resources/licenses/apscheduler/) |
| `prometheus-client` (Apache-2.0) | [documentation](../../resources/documentation/prometheus-client/) · [code examples](../../resources/code-examples/prometheus-client/) · [licence](../../resources/licenses/prometheus-client/) |
| `rich` (MIT) | [documentation](../../resources/documentation/rich/) · [code examples](../../resources/code-examples/rich/) · [licence](../../resources/licenses/rich/) |
| `psutil` (BSD-3) | [documentation](../../resources/documentation/psutil/) · [licence](../../resources/licenses/psutil/) |
| `pandera` (MIT) | [documentation](../../resources/documentation/pandera/) · [licence](../../resources/licenses/pandera/) |
| `joblib` (BSD-3) | [documentation](../../resources/documentation/joblib/) · [licence](../../resources/licenses/joblib/) |
| `pip-audit` (Apache-2.0) | [documentation](../../resources/documentation/pip-audit/) · [licence](../../resources/licenses/pip-audit/) |
| `detect-secrets` (Apache-2.0) | [documentation](../../resources/documentation/detect-secrets/) · [code examples](../../resources/code-examples/detect-secrets/) · [licence](../../resources/licenses/detect-secrets/) |
| `trivy` (Apache-2.0) | [documentation](../../resources/documentation/trivy/) · [licence](../../resources/licenses/trivy/) |
| `simonw-llm` (Apache-2.0) | [documentation](../../resources/documentation/simonw-llm/) · [licence](../../resources/licenses/simonw-llm/) — its SQLite call-logging model |
| `litellm` (MIT except `enterprise/`) | [documentation](../../resources/documentation/litellm/) · [licence](../../resources/licenses/litellm/) |
| `quantstats` (Apache-2.0) | [documentation](../../resources/documentation/quantstats/) · [code examples](../../resources/code-examples/quantstats/) — research-report telemetry |
| `ollama` (MIT) | [documentation](../../resources/documentation/ollama/) — a **resident daemon** with unload timers; an operational object to monitor, shared with workstream 13 |
| Baseline dependencies | numpy, pandas, scipy, sqlalchemy, requests, pydantic — [registry metadata](../../resources/documentation/_pypi-metadata/); version pinning affects RAM and reproducibility |
| Rejected on footprint | [airflow](../../resources/documentation/airflow/) · [temporal-python](../../resources/documentation/temporal-python/) + [code](../../resources/code-examples/temporal-python/) · [dagster](../../resources/documentation/dagster/) · [prefect](../../resources/documentation/prefect/) · [dask](../../resources/documentation/dask/) · [great_expectations](../../resources/documentation/great_expectations/) |
| Execution-side references | [freqtrade](../../resources/documentation/freqtrade/) · [nautilus](../../resources/documentation/nautilus/) · [hummingbot](../../resources/documentation/hummingbot/) · [ccxt](../../resources/documentation/ccxt/) — shared with workstream 11 |
| `stripe-idempotency` | **Not bundled** — metadata-only; vendor docs are not redistributable and were unreachable for download |
| `owasp-llm-top10` (CC BY-SA 4.0) | [documentation](../../resources/documentation/owasp-llm-top10/) — **LLM10 Unbounded Consumption** is an operational control, shared with workstream 14 |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| tenacity | https://github.com/jd/tenacity |
| Luigi | https://github.com/spotify/luigi |
| APScheduler | https://github.com/agronholm/apscheduler |
| prometheus_client | https://github.com/prometheus/client_python |
| Rich | https://github.com/Textualize/rich |
| psutil | https://github.com/giampaolo/psutil |
| pandera | https://github.com/unionai-oss/pandera |
| joblib | https://github.com/joblib/joblib |
| pip-audit | https://github.com/pypa/pip-audit |
| detect-secrets | https://github.com/Yelp/detect-secrets |
| Trivy | https://github.com/aquasecurity/trivy |
| LLM CLI | https://github.com/simonw/llm · https://llm.datasette.io/ (**unreachable for download from the build sandbox**) |
| LiteLLM | https://github.com/BerriAI/litellm (**2.35 GB — never tarball**) |
| Ollama | https://github.com/ollama/ollama |
| Airflow | https://github.com/apache/airflow — **rejected** |
| Temporal | https://github.com/temporalio/sdk-python — **rejected** |
| Dagster | https://github.com/dagster-io/dagster (**1.49 GB**) — **rejected** |
| Prefect | https://github.com/PrefectHQ/prefect |
| Stripe idempotency / AWS SQS deduplication | Metadata-only; see workstream 11 §4 |

## 5. Adoption steps

1. **Create the run log** first: `runs(run_id, task, state, attempt, started_at, finished_at,
   checkpoint_path, outcome, error, resource_trace_path)` in SQLite. Everything else writes to it.
2. **Implement target-existence checkpoints**: each step declares its output path and hash; a step is
   complete iff the output exists **and** its hash matches. Publish atomically (temp → hash → rename).
3. **Add idempotency keys** for anything with an external effect (workstream 11), persisted before acting.
4. **Configure `tenacity`** with an explicit predicate per exception class. Ambiguous outcomes are **not**
   in the retry predicate; they route to reconciliation.
5. **Declare the misfire policy** for every scheduled job (`coalesce` / `run all` / `skip`) and record it in
   the config artefact.
6. **Add cancellation** that leaves the store consistent: a killed job resumes without redoing completed
   steps and without duplicating any of them.
7. **Add telemetry**: RSS (out-of-process `psutil`), queue depth, cache hit rate, step latency, spill
   events, refusals and vetoes. Write locally with `prometheus_client` shapes; render with `rich`.
8. **Declare alert thresholds** in config, each with the action it implies. No undeclared alerts.
9. **Pin dependencies with hashes** and add `pip-audit` (or `trivy`) to a periodic check. Record the audit
   date and every unresolved finding.
10. **Cap parallelism explicitly** (`joblib max_n_procs=1` by default) and record why.

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| SQLite run log | Negligible | Grows with runs; rotate the resource traces, never the outcomes |
| `tenacity` | Tiny | Pure Python |
| `APScheduler` in-process | Small; SQLite jobstore | No server |
| `prometheus_client` | Tiny; optional multiprocess mode | Writing to a file avoids the server entirely |
| `rich` | Tiny | Pure rendering |
| `psutil` sampler | Small; C extension per OS | Out-of-process by requirement |
| `joblib` workers | **Model RAM × worker count** | `max_n_procs=1` by default |
| Dask | Scheduler + workers, each re-importing | Rejected as primary |
| Airflow / Temporal / Dagster | Multiple long-lived processes plus a database | Rejected |
| Prefect (local) | Lightest of the orchestrators, still an API process | Not adopted |
| Ollama daemon | **Resident RAM/VRAM while a model is loaded**; unload timers configurable via `keep_alive` | An idle cost versus a per-call start cost — two different budgets, both measured |
| LiteLLM proxy | A server process | Library mode only, if used at all |
| `trivy` | A single Go binary; scans can be I/O heavy | Run periodically, not on the hot path |

## 7. Qualification requirements

All **mechanical tests** in the taxonomy of [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §8.

1. **Race test**: two processes attempt the same step → exactly one artefact, one run-log outcome.
2. **Ambiguous-timeout test**: a simulated timeout plus three retries → exactly one effect record and one
   reconciliation entry.
3. **Kill-and-resume test**: a job killed mid-run resumes without redoing completed steps and without
   duplicating any of them.
4. **Atomicity test**: a crash during publication leaves no artefact that looks complete.
5. **Misfire test**: a missed schedule fires according to the declared policy, and the policy is recorded.
6. **Cancellation test**: a cancelled job leaves the store consistent and the run log says so.
7. **Telemetry test**: a deliberate memory-ceiling breach produces a logged spill/degrade/refuse event
   *and* a telemetry point, without being sampled by the process that breached it.
8. **Alert test**: each declared threshold fires once, with its action recorded; no undeclared alert fires.
9. **Dependency audit**: pinned hashes verified; advisory audit run and every finding resolved or recorded
   with a reason.
10. The whole pipeline runs **without any server process**, verified by inspection of what is listening.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Airflow, Temporal, Dagster | Server processes plus a database for a small number of daily jobs; footprint and operational surface |
| Prefect | The least objectionable orchestrator, still not needed |
| Dask as the primary parallel mechanism | Worker processes multiply model RAM |
| Prometheus server + Grafana | Footprint without benefit on one machine; Grafana is AGPL-3.0 |
| Great Expectations | Overlaps `pandera`; heavier; upstream org moved during the check window |
| Luigi's central scheduler | A process; target existence is the valuable part |
| LiteLLM in proxy mode | Adds a server; `enterprise/` is excluded from the MIT licence besides |
| Blind retries | Requirement 12.5 |
| An undeclared misfire policy | Requirement 12.7 |
| Self-reported resource telemetry | Requirement 8.11 |
| Alerts without a declared action | Requirement 12.9 |
| Unpinned dependencies | Requirement 12.10; also a supply-chain risk given the ownership changes observed during the check window |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| What scheduling and logging SAM-X already does | Steps 1–6 | Ask; inventory |
| Whether any long-lived process is acceptable at all (for example an Ollama daemon) | Requirement 12.8's telemetry design and workstream 13 | Depends on Q1–Q3 |
| Alert thresholds and who acts on them | Requirement 12.9 | A decision for the user |
| Whether a periodic dependency audit is authorised against the SAM-X codebase | Step 9 | Needs explicit approval |
| Retention policy for run logs and resource traces | Step 1 | A decision for the user; outcomes are never deleted, traces may be |
| Whether any step has an external effect that needs an idempotency key | Step 3 | Depends on Q9 and on the answer to workstream 11 §9 |
| Nothing here was executed | All of §7 | Requires authorisation this engagement did not have |
