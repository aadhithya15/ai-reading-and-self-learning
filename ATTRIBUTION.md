# ATTRIBUTION AND THIRD-PARTY NOTICES

This repository bundles third-party documentation, code examples, configuration files, licence texts and one PDF,
collected on **2026-10-14** from public sources. Nothing here is an endorsement by any upstream project. All
trademarks and product names belong to their owners.

## How to read this file

Machine-readable provenance for every bundled file — upstream repository, exact commit SHA, upstream path,
retrieval URL, byte size, SHA-256, detected licence and redistribution status — is in `ASSET_MANIFEST.json`.
Per-component assessment is in `RESOURCE_CATALOG.csv`. The licence texts themselves are in `resources/licenses/`
with an index at `resources/licenses/INDEX.md`.

## Attribution by licence family

### Apache License 2.0

Bundled files from Apache-2.0 projects are redistributed under Apache-2.0 with their licence text retained in
`resources/licenses/<component>/`. Apache-2.0 requires attribution, a copy of the licence, and a statement of
changes. **Statement of changes: the bundled files are unmodified copies of the upstream files at the recorded
commit; no upstream file was edited.** Projects include (non-exhaustive; see the manifest for the complete list):
sqlitedict, joblib, DuckDB documentation, hnswlib, USearch, delta-rs, great_expectations, yfinance, unstructured,
NVIDIA RULER, GraphRAG, Vespa, Letta, mem0, Graphiti, Zep, cognee, MemOS, self-refine, OPRO, DeepEval, RAGAS,
TruLens, HELM, HF Evaluate, AgentBench, Vectara Answer, QuantStats, zipline-reloaded, QuantConnect Lean,
gs-quant, Hummingbot, uncertainty-baselines, PyMC, Prefect, Dagster, Apache Airflow, Luigi, prometheus_client,
tenacity, NautilusTrader documentation (LGPL-3.0 — see below), Ollama documentation is MIT, vLLM, Transformers,
PEFT, Unsloth, lmdeploy, smolagents, Text Embeddings Inference, pip-audit, Bandit, Trivy, OSV-Scanner, garak,
nsjail, gVisor, E2B, detect-secrets (Apache-2.0), simonw/llm, LiteLLM (MIT except `enterprise/`),
openai-python, google-genai, DeepDoctection, docTR, GROBID, Tesseract, MinerU (Apache-2.0 plus additional terms).

### MIT Licence

Bundled files from MIT projects are redistributed with their copyright notice and licence text retained in
`resources/licenses/<component>/`. Projects include: faiss, sqlite-vec (dual MIT/Apache-2.0), Frictionless,
pandera, zarr-python, markitdown, Docling, Marker and Surya (code; model weights are separately licensed under a
modified OpenRAIL-M — the text of which is bundled), Camelot, LongBench, needle-in-a-haystack (code only; the
Paul Graham essays bundled upstream were NOT collected), InfiniteBench, RAPTOR, LightRAG, LlamaIndex, LangChain,
DSPy, LMOps, Inspect AI, lm-evaluation-harness, promptfoo, Polars, DuckDB-web docs, ml4trading companion code,
bt, Jesse, MemoryBank, A-MEM, Reflexion, TextGrad, Voyager, Tree-of-Thought-llm, ExpeL, ACE, llama.cpp, mlx-lm,
bitsandbytes, AutoGPTQ (archived upstream), AutoAWQ (archived upstream), Gitleaks, TruffleHog is AGPL-3.0 (see below),
rich, APScheduler, Temporal Python SDK, ib_async (BSD-2-Clause).

### BSD family (BSD-2-Clause, BSD-3-Clause)

Bundled with copyright notice and disclaimer retained. Projects include: psutil, memory_profiler (New BSD), Dask,
pypdf (BSD-3-Clause style text), sqlitedict is Apache-2.0, River, hmmlearn, ruptures (BSD-2-Clause), MAPIE,
Riskfolio-Lib, ib_async (BSD-2-Clause), weaviate-client.

### Copyleft (AGPL-3.0, GPL-3.0, LGPL-3.0, LGPL-2.1)

Bundled files are limited to documentation, READMEs, configuration examples and licence texts. Copyleft
obligations attach only if this material is combined into a distributed work; reading it does not. Projects:
PyMuPDF (**AGPL-3.0 or Artifex commercial — dual licensed; a deliberate adoption decision is required**),
backtesting.py (AGPL-3.0), TruffleHog (AGPL-3.0), Backtrader (GPL-3.0), Freqtrade (GPL-3.0),
NautilusTrader (LGPL-3.0), Semgrep (LGPL-2.1).

### Creative Commons

- **CC BY 4.0** — *Google LLM Tuning Playbook* (`google-research/tuning_playbook`). Full text bundled as
  `resources/documentation/tuning-playbook/README.md`, unmodified. Attribution: Google LLC, "Google LLM Tuning
  Playbook", https://github.com/google-research/tuning_playbook, CC BY 4.0.
- **CC BY-SA 4.0** — *OWASP Top 10 for LLM Applications 2025*. Bundled as the official PDF and as the eleven
  `2_0_vulns/LLM*.md` files, unmodified. Attribution: OWASP GenAI Security Project,
  https://owasp.org/www-project-top-10-for-large-language-model-applications/, CC BY-SA 4.0. Notes written in this
  repository reference and summarise that material with attribution rather than adapting it; if you adapt it,
  ShareAlike applies to the adaptation.

### Restrictive or conditional licences (read before any adoption)

- **Business Source License 1.1** — Alibi Detect (Seldon). Non-production use only until each version's change date
  (four years), then Apache-2.0. Text bundled.
- **Commons Clause v1.0 over Apache-2.0** — vectorbt. Redistribution permitted; selling the software is not. Text bundled.
- **Modified OpenRAIL-M** — Marker and Surya MODEL WEIGHTS. Use restrictions apply. No weights were downloaded; only
  the licence text and the Apache-2.0 code documentation were bundled.
- **MinerU Open Source License** — Apache-2.0 plus additional terms. Text bundled.
- **LiteLLM** — MIT except the `enterprise/` directory. Nothing from that directory was collected.
- **Composite licence** — google-deepmind/long-form-factuality: Apache-2.0 for `eval/`, `longfact/`, `common/`,
  `data_creation/`, `main/`; MIT for `third_party/factscore/`. The root README is not explicitly enumerated.

## Registry metadata

`resources/documentation/_pypi-metadata/*.json` are snapshots of the public PyPI JSON API (retrieved 2026-10-14),
trimmed to factual fields: name, version, summary, classifiers, requires_python, project URLs, yanked status and
release file names with sizes and SHA-256 digests. Where a package's metadata contains licence text, that text
belongs to the package's copyright holder and is reproduced here only as registry metadata.

## Original material in this repository

All analysis, cataloguing, diagrams (`resources/diagrams/*.svg`), templates, notes, evaluation plans and
implementation guidance authored for this collection are original works created for the SAM-X research collection
on 2026-10-14 and are provided as-is, without warranty. They are not affiliated with, reviewed by, or endorsed by
any upstream project.

## Corrections

If you hold rights in any bundled material and believe it is included in error or without adequate attribution,
open an issue on this repository: the file will be removed or corrected. Provenance for every file is recorded in
`ASSET_MANIFEST.json` so removal is a single-file operation.
