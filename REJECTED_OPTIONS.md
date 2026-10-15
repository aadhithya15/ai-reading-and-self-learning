# REJECTED OPTIONS

Components and approaches that were researched, catalogued, and **deliberately not recommended** — with the
reason, the evidence for the reason, and what would have to change for the decision to be revisited.

Recording rejections matters as much as recording recommendations: without this file, the next reader
re-derives the same shortlist, re-evaluates the same rejected option, and loses the reason it was rejected.

Every rejected component still has a row in [RESOURCE_CATALOG.csv](RESOURCE_CATALOG.csv) with
`classification=rejected` (15 rows) or with its rejection recorded in the assessment fields (many of the
112 `needs-more-evidence` rows carry "alternative, do not adopt" guidance). Nothing was deleted from the
record.

Rejection reasons, in order of how often they apply:

* **resource-fit** — would not fit the reported machine, or would need a server process
* **licence** — copyleft, dual-licence, non-production, or no licence at all
* **replaces-rather-than-complements** — adopting it means discarding existing SAM-X components
* **not-independent-evidence** — it is a model judging a model, or a vendor's own accuracy claim
* **maintenance** — archived or long-dormant upstream for something intended as a live dependency
* **category-mismatch** — solves a different problem than the one stated
* **contamination-risk** — a public benchmark or dataset that is likely in training corpora

---

## 1. Rejected on resource fit

| Component | Licence | Why rejected | What would change the decision |
|---|---|---|---|
| **Milvus** | Apache-2.0 | Full deployment needs etcd + MinIO + Pulsar. A three-service cluster for a corpus of two documents | A corpus large enough that embedded options fail, plus a machine that can host services (Q1) |
| **Weaviate** | BSD-3 | Server daemon with a JVM-free but non-trivial resident footprint; GraphQL layer unused here | Same as above |
| **Qdrant (server mode)** | Apache-2.0 | The *server* is rejected; the in-process/embedded option remains worth measuring | Measured evidence that `sqlite-vec` recall or latency is insufficient |
| **Vespa** | Apache-2.0 | JVM-based, designed for large-scale serving | Never, at this project's scale |
| **RAGFlow** | Apache-2.0 | Multi-container Docker Compose stack (Elasticsearch/Infinity, MySQL, Redis, MinIO) | Never, at this project's scale |
| **Apache Airflow** | Apache-2.0 | Scheduler + webserver + metadata database to sequence a small number of daily jobs | A DAG with real fan-out, retries across hosts, and backfills that a run log cannot express |
| **Temporal** | MIT | Long-running server plus a database; heavyweight for bounded batch steps | Multi-day, multi-host workflows with durable state requirements |
| **Dagster** | Apache-2.0 | Daemon + webserver; software-defined assets are a good model but the runtime does not fit | Same as Airflow |
| **Zep (server)** | Apache-2.0 | The *server* is rejected. Its bi-temporal knowledge-graph memory **pattern** is adopted via Graphiti's Apache-2.0 code, implemented in SQL | Evidence that graph traversal (not interval queries) is genuinely required |
| **gVisor** | Apache-2.0 | A container runtime requiring specific kernel support; not installable as a library, and this engagement cannot install anything | A Linux host where `nsjail` is insufficient and a runtime-level sandbox is justified (Q9) |
| **E2B** | Apache-2.0 (SDK) | Remote, **paid** sandbox service; sending document content to a third party is a privacy decision the user has not made, and starting paid services is outside authorisation | Explicit authorisation plus a data-handling review |
| **vLLM** | Apache-2.0 | GPU-first serving engine; CPU path exists but is not the design target | A GPU with enough VRAM, and a measured need for throughput (Q1) |
| **lmdeploy** (as an engine) | Apache-2.0 | TurboMind engine is GPU-oriented | Same as vLLM. Its KV-cache quantisation **docs** remain bundled as reference |
| **Dask** (as the primary parallel mechanism) | BSD-3 | Worker processes each re-import and can re-load models, multiplying RAM — the opposite of the goal | A genuinely parallelisable workload on a machine with RAM to spare; kept as a catalogued option |

## 2. Rejected or restricted on licence

| Component | Licence found | Decision |
|---|---|---|
| **PyMuPDF / pymupdf4llm** | AGPL-3.0 **or** Artifex commercial | Not adopted as a dependency. Copyleft reaches a networked service; the commercial option is a purchase decision outside this engagement. Catalogued with both paths documented. `pypdf` (BSD-3) + `pdfminer.six` (MIT) recommended instead |
| **backtesting.py** | AGPL-3.0 | **Reference semantics only** — read how it models broker constraints; do not vendor |
| **Backtrader** | GPL-3.0 | Reference semantics only; also dormant (last push 2024-08) |
| **Freqtrade** | GPL-3.0 | Reference semantics only. Its `stoploss.md` and lookahead-analysis docs are bundled for reading, not for import |
| **NautilusTrader** | LGPL-3.0 | Reference design only — its RiskEngine documentation is the strongest open reference for risk gates, but the platform would **replace** existing components rather than complement them |
| **TruffleHog** | AGPL-3.0 | Not adopted. Plus a documented trap: it **verifies findings by default**, making live network calls with discovered credentials. `gitleaks` rules and `detect-secrets` recommended (offline) |
| **vectorbt** | Apache-2.0 **+ Commons Clause** | Redistribution allowed, **selling not allowed**; the PRO edition is a separate paid product. Catalogued with the restriction recorded; not adopted |
| **Alibi Detect** | **BSL 1.1** (Seldon) | Non-production use only until each version's change date (4 years), then Apache-2.0. This is why `river` (BSD-3) is the recommended drift-detection path |
| **MinerU** | Apache-2.0 **+ additional terms** | Additional terms must be read before any adoption; not adopted |
| **LiteLLM** | MIT **except `enterprise/`** | The excluded directory is out of bounds. Not adopted as a dependency (it is a proxy service); its API-normalisation *pattern* is noted |
| **semgrep** | LGPL-2.1 | Rules bundled for reading; the tool is not installed by this engagement |
| **hudson-and-thames/mlfinlab** | Proprietary | **Rejected.** No redistribution right; dormant (2023). Its MIT-licensed academic companion (`ml4t`) is bundled instead |
| **yixuantt/MultiHop-RAG** | **No licence file** | **Removed after download.** Absence of a licence means all rights reserved. Replaced by a metadata-only record: `resources/documentation/_metadata-only/multihop-rag.md` |
| **arXiv paper PDFs** (including those found inside permissively-licensed repos: `docling` test fixtures `2203.01017v2.pdf`, `2305.03393v1.pdf`; `unstructured`/`langchain` `layout-parser-paper.pdf`) | arXiv non-exclusive distribution licence | **Never bundled.** The licence does not grant third-party redistribution, and a PDF inside an Apache-2.0 repo inherits the *paper's* licence, not the repo's. 31 papers are metadata-only with verified identifiers |
| **Marker / Surya weights** | Code Apache-2.0; weights **"AI PUBS OPEN RAIL-M LICENSE (MODIFIED)" v0.1** | Weights carry use restrictions that propagate to derivative models — a policy question for a trading application. Code catalogued; weights are an approval gate |
| **Docling model weights** | Code MIT; weights separate | Same treatment: code docs bundled, weights are an approval gate |

## 3. Rejected as "alternative, do not adopt alongside"

These are good projects. They are rejected **for this project** because adopting them means replacing
existing SAM-X components, which contradicts reported position R7 (prefer reusing compatible existing
components).

| Component | Category | Decision |
|---|---|---|
| **LlamaIndex** | RAG framework | **Pattern source, not an adoption target.** Its node/relationship abstractions are worth borrowing as a schema; installing it would replace the reading stack |
| **LangChain / LangGraph** | Orchestration framework | Same. Its graph/state abstractions are useful vocabulary; the dependency is not |
| **Haystack** | RAG framework | Same — third overlapping framework. At most one may ever be adopted, and none is needed if the Rank 1 spine is built |
| **txtai** | Embeddings database | Overlaps SQLite + `sqlite-vec` entirely, with a native dependency |
| **mem0 / cognee / MemOS / A-MEM** | Memory layers | Each brings a vector or graph store plus LLM-driven consolidation that **rewrites records**. An auditable research system must not consolidate. Their schemas and vocabularies are catalogued; the four-store SQL design is adopted instead |
| **Letta (MemGPT) server** | Agent memory server | Its **architecture** (main context / external context / explicit paging triggers) is adopted; its server is not. `letta-ai/letta`'s tree had only 12 files at the pinned commit — the SDK/server split moved |
| **Graphiti + Neo4j** | Temporal knowledge graph | Bi-temporal validity is needed; a graph database is not. Three SQL columns (`valid_from`, `valid_to`, `superseded_by`) deliver it. Graphiti's Apache-2.0 edge/node code is bundled as the reference implementation |
| **GraphRAG / LightRAG** | Graph-based RAG | Index build is LLM-call heavy (cost + RAM), and community summaries are model-written hypotheses that must never be cited as facts. Adopt only if global "what are the themes" questions are proven necessary by a recorded failure of hierarchical summaries |
| **RAPTOR as a dependency** | Hierarchical retrieval | **The pattern is adopted, the dependency is not** (unmaintained since 2024-09-03; pulls Faiss + a clustering stack). Its full MIT implementation is bundled to read |
| **Delta Lake / delta-rs** | Table format | Directory-per-generation + manifest + atomic rename gives ~80% of the benefit with no native dependency. Catalogued as the upgrade path if concurrent readers or time travel become real |
| **DVC** | Data version control | Ownership changed during the check window (`iterative/dvc` → `treeverse/dvc`) — a supply-chain signal. A sha256 manifest is a few lines and is fully under project control |
| **Zarr** | Chunked array storage | A v2/v3 format transition is a live migration risk for a store meant to be readable years later. Parquet + a manifest is the recommendation |
| **Great Expectations** | Data quality | Overlaps `pandera` (MIT); upstream org moved to Fivetran during the check window. `pandera` recommended; GX kept as the documented alternative |
| **Inspect AI as a mandatory dependency** | Evaluation framework | The **protocol** is mandatory; the framework is optional. A ~150-line runner satisfies every requirement. Catalogued as the preferred option *if* its concepts map cleanly onto the existing environment |
| **Ragas / DeepEval** | LLM-judged evaluation | **Metric definitions only.** Both are LLM-judged, therefore not independent supervision, and neither was run. Their metric vocabularies are borrowed; their scores are never an acceptance gate |

## 4. Rejected categories

| Category | Examples catalogued | Why rejected for this project |
|---|---|---|
| **Fine-tuning / parameter updates as the learning mechanism** | PEFT, Unsloth, transformers Trainer, QLoRA docs | (a) Laptop resource fit is unknown and probably hostile (Q1). (b) Weights changing underneath a frozen evaluation destroys comparability — the exact property Phase 1 exists to create. (c) Contamination and reproducibility become much harder. Learning is pursued through **external memory** (procedures, lessons, prompts) instead. Revisit only if external-memory adaptation demonstrably plateaus *and* hardware permits |
| **Quantisation toolkits** | AutoGPTQ (**archived** 2025-04-11), AutoAWQ (**archived** 2025-05-11), bitsandbytes | Both leading toolkits are archived upstream. llama.cpp's built-in quantisation and Ollama's model formats cover the need without an unmaintained dependency. bitsandbytes remains catalogued for its documentation value |
| **Public long-context leaderboards as qualification evidence** | HELM scenarios, lm-evaluation-harness tasks, LongBench data, ∞Bench data, NovelQA | They say nothing about unfamiliar trading documents, they cost scarce RAM, and they are contamination magnets. **Their harnesses, scorers, reporting formats and decontamination practices are adopted; their scenarios are not run.** LongBench's average English length is 6 711 words (verified metadata) — it does not test a 147-page scale at all |
| **Vanilla needle-in-a-haystack as a qualification** | `gkamradt/needle-in-a-haystack` (MIT) | RULER (arXiv:2404.06654v3, verified) reports near-perfect vanilla NIAH scores coexisting with sharp degradation at 32K and on complex tasks. Passing NIAH alone is close to meaningless. The repo's **code** is bundled as a generator reference; the Paul Graham essays used as its haystack were **not** collected (copyright, and not needed) |
| **Tree-of-Thoughts / exhaustive search over reasoning paths** | ToTH, multi-agent debate | Search multiplies token cost and RAM per question, and produces more confident wrong answers when the evidence gate is absent. Bounded retrieval + abstention is cheaper and safer |
| **Multi-agent debate as a verification mechanism** | `composable-models/llm_multi_agent_debate` (slug unresolved at check date) | Agreement between models is not independent evidence. It is also the most expensive verification available |
| **Hosted memory / hosted RAG platforms** | Zep cloud, mem0 platform, Vectara | Moves document content off-box. A privacy and rights decision (Q4, Q8) that the user has not made, and one this engagement is not authorised to make |
| **yfinance as a system of record** | `yfinance` (Apache-2.0 code) | Unofficial client: no data licence, no SLA, and back-adjusted prices can **silently rewrite history** — fatal for reproducible backtests. Acceptable as a convenience source only if every pull is frozen by hash into an immutable generation |
| **memory_profiler** | BSD (New) | Unmaintained since 2022-10-19. `psutil` sampling achieves the same with a maintained dependency |
| **Prometheus server / Grafana** | Apache-2.0 / AGPL-3.0 | Running a metrics server and a dashboard for a single-machine research system is footprint without benefit. `prometheus_client` **metric shapes** are adopted, written to a local file or SQLite; Grafana is AGPL and not adopted |

## 5. Approaches rejected on method

| Approach | Why rejected |
|---|---|
| Downloading whole repositories or tarballs | Explicitly out of scope, and infeasible: ccxt 8.67 GB, litellm 2.35 GB, grobid 2.08 GB, dagster 1.49 GB, gvisor 1.40 GB, ML4T 1.30 GB, great_expectations 253 MB. Individual files at pinned commits were fetched instead |
| Downloading model weights or datasets | Out of scope by instruction, and an approval gate in any case |
| Bundling hundreds of weakly relevant papers to look thorough | Explicitly rejected. 31 papers with verified metadata, each tied to a specific decision, beat 300 with no connection to SAM-X |
| Running any downloaded code to "check it works" | Prohibited. Every asset is treated as untrusted; the two validation scripts authored here are read-only and offline |
| Asserting RAM figures from documentation as measurements | Prohibited by the evidence-label scheme. Every footprint statement in this collection is labelled `estimate` until Phase 0 measures it |
| Using GitHub Releases or Git LFS for the bundle | Checked against GitHub's own limits: 20.40 MB total with a 10.72 MB largest file fits comfortably in-repo. Releases and LFS add discoverability friction and quota questions for zero benefit. Both are documented as the path to take if the collection grows past ~100 MB ([PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §8) |
| Splitting the collection into multiple repositories | Prohibited by the assignment (single entry point). Workstreams are directories, not repos |
| Publishing evaluation keys or protected questions | Prohibited. Only templates and hashes are published |

## 6. What is *not* rejected — common misreadings of this file

* **SQLite, FTS5, `sqlite-vec`, `diskcache`, `tiktoken`, `psutil`, `tenacity`, `rank_bm25`, `pypdf`,
  `pdfminer.six`, `camelot`, `river`, `ruptures`, `MAPIE`, `pandera`, `DuckDB`, `Polars`, `inspect_ai`,
  `hf-evaluate`, `nsjail`, `pip-audit`, `gitleaks`, `detect-secrets`, `bandit`, `semgrep` rules, `zipline`
  finance modules, `ml4t` scripts, Qlib workflow configs, RULER generators** — these are the recommended
  set. Their rows are `trial-ready` or `needs-more-evidence`, not `rejected`.
* **Graphiti, Letta, RAPTOR, Voyager, ACE, HELM, lm-evaluation-harness, LongBench, NautilusTrader,
  Freqtrade, vectorbt** — rejected *as dependencies*, adopted *as reference code or semantics*. The
  distinction is recorded per row and matters: reading GPL/AGPL code to understand semantics is normal
  engineering; vendoring it is not.
* **The OWASP Top 10 for LLM Applications 2025 and the Google LLM Tuning Playbook** — fully bundled with
  verified permissive/CC licences. They are the two strongest redistributable documents in the collection.
