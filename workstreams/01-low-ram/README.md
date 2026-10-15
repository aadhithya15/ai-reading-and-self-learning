# Workstream 01 — Low-RAM and Resource-Efficient Computing

**Objective served:** interpret unfamiliar documents *within a hard resource budget*, and fail
conservatively when the budget is exceeded.

**Reported context this workstream exists for:** spare laptop RAM is limited (R1 — **reported, no number
ever given**); a disk-backed navigation prototype already indexed 147 pages across 2 documents (R2 —
**reported**). Nothing here has been measured on the target machine. Phase 0 of the
[roadmap](../../IMPLEMENTATION_ROADMAP.md) exists to convert R1 into a number.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 1.1 | A **declared resident-memory ceiling** for the reading path, enforced in code, not hoped for | "Limited spare RAM" is not a budget. A ceiling is |
| 1.2 | **Defined behaviour when the ceiling is reached** — spill, degrade or refuse; never crash mid-answer and never silently drop evidence | Failing conservatively is an explicit objective |
| 1.3 | Page-level random access over already-extracted text without holding the corpus in RAM | 147 pages now; more later |
| 1.4 | **Exact** token accounting for every context assembled | Context budget guesses are how overruns happen |
| 1.5 | Independent measurement of RSS, PSS and available system memory, sampled out-of-process | A component must not self-report its own footprint |
| 1.6 | Application RAM distinguished from system RAM, VRAM and disk — and `mmap` page-cache pressure counted honestly | `mmap` reduces process RSS without reducing machine pressure |
| 1.7 | Bounded startup overhead and a decision about resident daemons versus per-call processes | Idle cost and start cost are different budgets |
| 1.8 | No new server processes | Every server-class option was rejected on resource fit — see §8 |

**Not a goal.** Squeezing a large model onto a small machine. If measurement shows there is no room, the
correct outcome is retrieval plus abstention without a generative model in the loop, not a slower model.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: SQLite-anchored spine with an enforced ceiling

`SQLite + FTS5` (stdlib) as the page map and lexical index · `diskcache` as the spill tier ·
`sqlitedict` where dict semantics are wanted · `tiktoken` for exact token counts · `psutil` for independent
measurement and enforcement. All permissive, all in-process, all pure-Python-plus-one-extension.

This is the **minimal generalisation of what already exists** (R2): same storage engine, same in-process
model, plus the three things an index does not give a reader — a heading/page map, an exact token budget,
and an enforced ceiling with defined spill behaviour.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| Raw `sqlite3` + hand-written LRU with disk spill | **Stated fallback** | Entirely viable (~150 lines). Choose it if you would rather own the code than add a dependency |
| `DuckDB` as the primary store | Use **alongside**, not instead | Superb for analytical scans over bar history (workstream 02); wrong shape for page-level random access under a hard ceiling. Its `memory_limit` is the useful knob |
| `Polars` streaming / lazy engine | Use for transforms | Streaming keeps intermediate state on disk; ideal for reshaping extracted tables |
| `Faiss` on-disk IVF, `USearch`, `LanceDB`, `Chroma`, `hnswlib` | Measure only if lexical fails | Adds a native format for a two-document corpus. `sqlite-vec` lives in the same file and the same query language |
| `Dask` | **Not the primary mechanism** | Worker processes each re-import and can re-load models, multiplying RAM — the opposite of the goal |
| `joblib` / `loky` parallelism | Use with a worker cap | Same multiplication effect; one worker per model copy |
| Memory-mapped everything | Report both numbers | Page-cache residency still competes with the application |

### 2.3 The measurement discipline

`psutil` sampling out-of-process at a fixed interval, recording **RSS, PSS and system available memory**
together. Peak RSS alone hides shared-page behaviour; available memory alone hides which process caused the
pressure. The catalog row for `psutil` contains the exact experiment.

## 3. Bundled assets

Shared assets are stored **once** under `resources/` and referenced from every workstream that needs them.

| Component | Bundled material |
|---|---|
| `diskcache` | [documentation](../../resources/documentation/diskcache/) · [code examples](../../resources/code-examples/diskcache/) (core, fanout and persistent-cache implementations) · [licence](../../resources/licenses/diskcache/) |
| `sqlitedict` | [documentation](../../resources/documentation/sqlitedict/) · [code examples](../../resources/code-examples/sqlitedict/) · [licence](../../resources/licenses/sqlitedict/) |
| `sqlite-vec` | [documentation](../../resources/documentation/sqlite-vec/) · [config/example SQL](../../resources/configurations/sqlite-vec/) · [licence](../../resources/licenses/sqlite-vec/) |
| `psutil` | [documentation](../../resources/documentation/psutil/) · [licence](../../resources/licenses/psutil/) |
| `tiktoken` | [registry metadata](../../resources/documentation/_pypi-metadata/) |
| `duckdb` | [documentation](../../resources/documentation/duckdb/) — including `guides/performance/environment.md` and `how_to_tune_workloads.md` · [licence](../../resources/licenses/duckdb/) |
| `polars` | [documentation](../../resources/documentation/polars/) · [licence](../../resources/licenses/polars/) |
| `faiss` | [documentation](../../resources/documentation/faiss/) · [code examples](../../resources/code-examples/faiss/) (on-disk inverted lists) · [licence](../../resources/licenses/faiss/) |
| `usearch` | [documentation](../../resources/documentation/usearch/) · [code examples](../../resources/code-examples/usearch/) · [licence](../../resources/licenses/usearch/) |
| `joblib` | [documentation](../../resources/documentation/joblib/) · [licence](../../resources/licenses/joblib/) |
| `dask` | [documentation](../../resources/documentation/dask/) (memory management) · [licence](../../resources/licenses/dask/) |
| `memory_profiler` | [documentation](../../resources/documentation/memory_profiler/) — catalogued, **not recommended** (unmaintained since 2022-10-19) |
| `llama.cpp` | [documentation](../../resources/documentation/llama-cpp/) — performance and KV-cache sizing · [licence](../../resources/licenses/llama-cpp/) |
| `ollama` | [documentation](../../resources/documentation/ollama/) — `keep_alive`, GPU and troubleshooting docs · [licence](../../resources/licenses/ollama/) |
| `river` | [documentation](../../resources/documentation/river/) — constant-memory by design · [licence](../../resources/licenses/river/) |
| `prometheus_client` | [documentation](../../resources/documentation/prometheus-client/) · [code examples](../../resources/code-examples/prometheus-client/) — metric shapes without a server |
| Baseline dependencies | numpy, scipy, pandas, sqlalchemy, requests, pydantic — [registry metadata](../../resources/documentation/_pypi-metadata/) only, catalogued as prerequisites rather than discoveries |
| Rejected on footprint | [vllm](../../resources/documentation/vllm/) · [lmdeploy](../../resources/documentation/lmdeploy/) · [tei](../../resources/documentation/tei/) · [memos](../../resources/documentation/memos/) · [letta](../../resources/documentation/letta/) · [lancedb metadata](../../resources/documentation/_pypi-metadata/) |

Every path above is listed in [ASSET_MANIFEST.json](../../ASSET_MANIFEST.json) with its upstream commit,
size and SHA-256, and assessed in [RESOURCE_CATALOG.csv](../../RESOURCE_CATALOG.csv).

## 4. Official upstream references

| Component | Upstream (pinned by commit in the manifest) |
|---|---|
| diskcache | https://github.com/grantjenks/python-diskcache |
| sqlitedict | https://github.com/piskvorky/sqlitedict |
| sqlite-vec | https://github.com/asg017/sqlite-vec |
| psutil | https://github.com/giampaolo/psutil |
| tiktoken | https://github.com/openai/tiktoken |
| DuckDB | https://github.com/duckdb/duckdb-web (docs) · https://duckdb.org/ (**unreachable from the build sandbox**) |
| Polars | https://github.com/pola-rs/polars |
| Faiss | https://github.com/facebookresearch/faiss |
| USearch | https://github.com/unum-cloud/USearch |
| joblib | https://github.com/joblib/joblib |
| Dask | https://github.com/dask/dask |
| llama.cpp | https://github.com/ggml-org/llama.cpp |
| Ollama | https://github.com/ollama/ollama |
| SQLite / FTS5 | https://sqlite.org/ (**unreachable from the build sandbox** — FTS5 is exposed through the stdlib `sqlite3`) |

Access limitation recorded: `sqlite.org`, `duckdb.org` and `docs.python.org` could not be reached on
2026-10-14, so their material is represented by bundled repository documentation and registry metadata, not
by copies of the official sites.

## 5. Adoption steps

1. **Measure before choosing.** Instrument one existing end-to-end job with out-of-process `psutil` sampling
   (RSS, PSS, available memory, 500 ms interval). Write the result into a `RESOURCE_BUDGET.md`: total RAM,
   RAM already committed, declared ceiling for the reader, safety margin, free disk, disk throughput.
2. **Declare the ceiling** as a config value with a stated safety margin below the measured available
   memory. Everything downstream references this number.
3. **Build the page map**: page → byte range → heading path → SHA-256 of the extracted text. Reuse the
   existing prototype's storage where compatible (R5, and question Q5).
4. **Add the spill tier** (`diskcache`) with an explicit eviction policy and a **logged spill event**. A
   spill that is not logged is a ceiling that is not enforced.
5. **Add exact token accounting** (`tiktoken`) at every point a context is assembled. No estimated token
   counts anywhere in the path.
6. **Add the enforcement hook**: before each candidate action, check the sampled resident memory against the
   ceiling; on breach, spill → degrade (smaller top-k) → refuse, in that order, and record which happened.
7. **Record the failure modes**: corrupt or truncated page text, hash mismatch against the source of record,
   page never extracted (image-only), budget exhaustion mid-query, concurrent second reader on the same
   file (needs WAL and a tested race path).
8. **Re-measure** after every change and compare against the step-1 trace.

## 6. Resource implications

All figures below are **estimates from documentation** or reasoning. None is a measurement on the target
machine — that is what step 1 produces.

| Item | Expectation | Note |
|---|---|---|
| SQLite + FTS5 | Process-resident cost dominated by the page cache you configure | Bounded by `cache_size`; the file lives on disk |
| `diskcache` | Small resident footprint by design; spills to disk | Disk throughput becomes the latency variable |
| `sqlite-vec` | One loaded extension; vectors on disk | Brute-force scan cost grows with corpus size — fine at 147 pages |
| `tiktoken` | Tiny; encoding tables cached on first use | First use may need the table files; check offline availability |
| `psutil` sampler | Negligible, in a separate process | Sampling interval trades resolution for overhead |
| `Faiss` on-disk IVF | Low RSS, **high page-cache pressure** | Report PSS and available memory, not just RSS |
| `llama.cpp` | Weights + **KV cache that grows with context length independently of weight size** | A 128K-token context can dwarf a small model's weights |
| `Ollama` daemon | Idle resident cost while a model is loaded (`keep_alive`) versus per-call start cost | Two different budgets; measure both |
| `Dask` / `joblib` workers | Model RAM **multiplied by worker count** | Cap workers explicitly |

**Hidden allocations found in the bundled documentation** (all `inspected`, none `measured`):
`device_map="auto"` in Transformers can silently spill to disk and stall; DuckDB's `memory_limit` is
advisory for some operators; per-worker re-import in Dask/joblib; llama.cpp KV-cache growth; `mmap`-backed
index residency.

## 7. Qualification requirements

A component in this workstream is qualified only when **all** of the following are recorded:

1. Peak RSS, peak PSS and minimum available system memory, sampled out-of-process, over a full run of the
   147-page corpus — **measured**, with the trace preserved.
2. Peak resident memory **at or below** the declared ceiling on every run, with every breach accompanied by
   a logged spill/degrade/refuse event.
3. p50 and p95 latency for a locate-then-reopen query, with the spill tier both warm and cold.
4. Cold-start time and on-disk footprint.
5. Correct behaviour on the negative cases: corrupt page, hash mismatch, image-only page, budget exhaustion
   mid-query, concurrent second reader.
6. 100% of returned answers resolve to a page whose stored text hash matches the source of record.
7. A regression run showing that adding the component did not degrade any workstream-08 metric.

Star counts, README performance claims and published benchmarks are **not** qualification evidence.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Milvus, Weaviate, Qdrant (server), Vespa, LanceDB-as-a-service | Server processes / multi-service deployments for a two-document corpus. Full reasoning in [REJECTED_OPTIONS.md](../../REJECTED_OPTIONS.md) §1 |
| RAGFlow | Multi-container Compose stack (Elasticsearch/Infinity, MySQL, MinIO, Redis) |
| Dask as the primary parallel mechanism | Worker processes multiply model RAM |
| `memory_profiler` as a dependency | Unmaintained since 2022-10-19; `psutil` sampling is maintained and more precise |
| vLLM, lmdeploy as an engine, Text Embeddings Inference | GPU-first serving; CPU paths are not the design target |
| AutoGPTQ, AutoAWQ | **Archived upstream** (2025-04-11 and 2025-05-11) |
| Promising a specific RAM saving | Prohibited. No component here has been measured on the target machine, so no saving can be promised |
| Reporting only process RSS | Hides `mmap` page-cache pressure; both RSS and PSS plus available memory are required |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **No measured RAM figure for anything, anywhere** (Q1, Q2) | Every resource-fit decision in this collection | Phase 0 resource trace |
| Disk throughput unknown (Q3) | Whether the spill tier is viable at all | Measure sequential and random read rates on the target disk |
| Existing prototype's schema and interface unknown (Q5) | Extend-versus-replace decision | Inventory the prototype's storage, page map and hashing |
| Whether `tiktoken` encoding tables are available offline on the target machine | Exact token accounting | Check at install time; a pure-Python fallback counter is acceptable if labelled as approximate |
| SQLite concurrent-reader behaviour under the actual workload | Step 7's race path | WAL mode plus a two-process race test |
| Whether the ceiling should be per-process or system-wide | Enforcement design | Depends on what else runs on the machine — part of Q1/Q2 |
| No component here has been executed, imported or installed | All of the above | Requires authorisation this engagement did not have |
