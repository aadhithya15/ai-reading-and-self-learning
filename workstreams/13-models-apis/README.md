# Workstream 13 — Local Models, Hosted APIs, Costs and Terms

**Objectives served:** work within a resource budget; never invent parameters (including model parameters);
fail conservatively under resource shortage; keep costs and privacy explicit.

> **This workstream is blocked on hardware questions Q1–Q3** in
> [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) §4. No model choice, no RAM figure, no quantisation level
> and no context length is committed anywhere in this collection. What *is* here: the redistributable
> guidance for making that choice, the typed API surfaces of the major providers, and the licensing and
> cost traps that decide it.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 13.1 | **Measure before choosing**: total RAM, RAM already committed, VRAM if any, free disk, disk throughput | Every figure in this collection is an estimate from documentation |
| 13.2 | **Exact token accounting** (`tiktoken`) for every context assembled | Context budgets are how overruns happen |
| 13.3 | Understand that **KV-cache size grows with context length independently of weight size** | The most common way a "small" local model exhausts a small machine |
| 13.4 | A decision about **resident daemon versus per-call invocation**, with both costs measured | Ollama's `keep_alive` is an idle cost; per-call CLI is a start cost |
| 13.5 | **Weight licences read per model**, at adoption time, from the model card | Apache-2.0 / Llama community licence / OpenRAIL-M / custom are not interchangeable |
| 13.6 | **Terms, pricing and quotas re-verified on the adoption date**, never quoted from memory or from a bundled snapshot | Commercial pages change and are not redistributable |
| 13.7 | **Never assume a free tier is unlimited or permanent** | A standing instruction |
| 13.8 | **Never propose quota evasion or account rotation** | A standing instruction |
| 13.9 | Data egress declared explicitly: what leaves the machine, to whom, under what terms | A hosted call with document content is a privacy and rights decision (Q4, Q8) |
| 13.10 | **Fail conservatively** on quota exhaustion, timeout or resource shortage: degrade, then refuse, and log it | Objective 9 |

**Not a goal.** Choosing a model. The goal is making the choice *after* measurement, with the licences and
costs read, and with a documented fallback.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: measure, then pick between three shapes

| Shape | When | Components |
|---|---|---|
| **No generative model in the loop** | If Q1/Q2 show there is no room | Retrieval + typed extraction contract + evidence gate + abstention. This is a *complete* design, not a degraded one — and it is the conservative default |
| **Local, small, CPU** | If measurement shows headroom for weights **plus** KV cache at the needed context length | `llama.cpp` (or `llama-cpp-python` bindings) with its built-in quantisation; or `Ollama` for model management and `keep_alive` control |
| **Hosted API, budgeted** | Only if already authorised (Q8) | The typed SDK surfaces (`openai-python`, `anthropic-python`, `google-genai`) with an explicit budget, a queue, defer-and-retry, and an egress declaration |

The bundled **Google LLM Tuning Playbook** (CC BY 4.0, ~120 KB of text — the only fully redistributable
long-form technical report in this collection) is the guidance to read first regardless of shape. Its
evaluation-first discipline is the same discipline workstream 08 requires.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **vLLM** (Apache-2.0) | **Rejected** | GPU-first serving engine; a CPU path exists but is not the design target. 15 bundled docs kept for reference |
| **lmdeploy** (Apache-2.0) | **Rejected as an engine** | TurboMind is GPU-oriented. Its **KV-cache quantisation documentation** is bundled and genuinely useful for requirement 13.3 |
| **Text Embeddings Inference** (Apache-2.0) | Not adopted | A Rust server; batches requests well, but it is a process. No PyPI snapshot resolved — GitHub-only component |
| **AutoGPTQ**, **AutoAWQ** | **Rejected** | Both **archived upstream** (2025-04-11 and 2025-05-11). llama.cpp's built-in quantisation and Ollama's model formats cover the need without an unmaintained dependency |
| **bitsandbytes** | Catalogued for documentation value | Useful quantisation reference; not a learning mechanism and not needed for CPU inference |
| **PEFT / Unsloth** | **Rejected** | Fine-tuning category; see [workstream 07](../07-self-learning/README.md) §8 |
| **MLX-LM** (Apple Silicon) | Conditional | Only relevant if Q1 says the machine is Apple Silicon; otherwise dead weight |
| **Transformers on CPU** | Catalogued | `model_memory_anatomy.md`, `perf_infer_cpu` and the quantisation guides are bundled and are the best available explanation of where the memory actually goes. `device_map="auto"` can silently spill to disk and stall |
| **`sentence-transformers`** | Catalogued; weights gated | Small embedding models are documented at a few hundred MB resident — an **estimate**, and weights are an approval gate |
| **LiteLLM** | Not adopted as a dependency | MIT **except `enterprise/`**; proxy mode adds a server. Its normalisation *pattern* is worth knowing if multiple providers are ever used |
| **`smolagents`** (Apache-2.0) | Catalogued | A very light agent loop — but an agent loop enlarges the tool surface workstream 14 must contain, and it is not needed for document reading |
| **`simonw-llm`** (Apache-2.0) | Catalogued for its **logging model** | Records every call and response to local SQLite; a good pattern for cost and egress auditing |
| **E2B** | **Rejected** | Remote, **paid** sandboxes; sending document content to a third party is a decision the user has not made, and starting paid services is outside authorisation |
| **Hugging Face model cards** | **Metadata-only (MO-03)** | huggingface.co was unreachable for download from the build sandbox, and weights must not be downloaded without approval. Card licences must be read at adoption time |
| **Pricing/quota pages** | **Metadata-only (MO-04)** | They change frequently and are not licensed for redistribution; a stale copy is worse than a link. Summarised here with the check date and a mandatory re-verification step |

### 2.3 The memory arithmetic that decides everything

For a local model the resident cost is roughly **weights + KV cache + runtime overhead**, and the KV-cache
term scales with **context length × layers × heads**, not with weight size. A small quantised model asked
for a 128K-token context can exceed a large model at 4K. The bundled documentation that explains this
concretely: `llama.cpp`'s performance and KV-cache docs, `transformers`' `model_memory_anatomy.md`, and
`lmdeploy`'s KV-cache quantisation docs. Requirement 13.3 exists because this is the single most common way
a "resource-efficient" plan fails.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `tuning-playbook` (**CC BY 4.0**) | [full playbook text](../../resources/documentation/tuning-playbook/) · [licence](../../resources/licenses/tuning-playbook/) |
| `llama-cpp` (MIT) | [documentation](../../resources/documentation/llama-cpp/) — 13 files including performance, KV-cache, MLX and Vulkan guides · [licence](../../resources/licenses/llama-cpp/) |
| `llama-cpp-python` | [registry metadata](../../resources/documentation/_pypi-metadata/) |
| `ollama` (MIT) | [documentation](../../resources/documentation/ollama/) — `faq`, `modelfile`, `gpu`, `api`, `import`, `troubleshooting` · [licence](../../resources/licenses/ollama/) |
| `tiktoken` (MIT) | [registry metadata](../../resources/documentation/_pypi-metadata/) |
| `transformers` (Apache-2.0) | [documentation](../../resources/documentation/transformers/) — 15 files: `model_memory_anatomy.md`, `perf_infer_cpu`, `perf_hardware`, quantisation overview/GGUF/bitsandbytes, `generation_strategies.md`, `peft.md` · [licence](../../resources/licenses/transformers/) |
| `openai-python` | [documentation](../../resources/documentation/openai-python/) — including `api.md` (0.14 MB) · [licence](../../resources/licenses/openai-python/) |
| `anthropic-python` | [documentation](../../resources/documentation/anthropic-python/) — including `api.md` (0.19 MB) · [licence](../../resources/licenses/anthropic-python/) |
| `google-genai` | [documentation](../../resources/documentation/google-genai/) · [licence](../../resources/licenses/google-genai/) |
| `lmdeploy` (Apache-2.0) | [documentation](../../resources/documentation/lmdeploy/) — 13 files including KV-cache quantisation · [licence](../../resources/licenses/lmdeploy/) |
| `mlx-lm` | [documentation](../../resources/documentation/mlx-lm/) · [code examples](../../resources/code-examples/mlx-lm/) · [licence](../../resources/licenses/mlx-lm/) |
| `bitsandbytes` | [documentation](../../resources/documentation/bitsandbytes/) · [licence](../../resources/licenses/bitsandbytes/) |
| `peft`, `unsloth` | [PEFT docs](../../resources/documentation/peft/) · [Unsloth docs](../../resources/documentation/unsloth/) — **rejected** |
| `vllm`, `tei` | [vLLM docs](../../resources/documentation/vllm/) (15 files) · [TEI docs](../../resources/documentation/tei/) — **rejected / not adopted** |
| `autogptq`, `autoawq` | [AutoGPTQ](../../resources/documentation/autogptq/) · [AutoAWQ](../../resources/documentation/autoawq/) — **archived upstream** |
| `litellm` (MIT except `enterprise/`) | [documentation](../../resources/documentation/litellm/) · [licence](../../resources/licenses/litellm/) |
| `smolagents`, `simonw-llm` | [smolagents](../../resources/documentation/smolagents/) · [LLM CLI](../../resources/documentation/simonw-llm/) |
| `sentence-transformers` | [registry metadata](../../resources/documentation/_pypi-metadata/) — weights gated |
| `hf-model-cards` | **Not bundled** (MO-03) — metadata-only row listing the candidate families to evaluate |
| `e2b` | [documentation](../../resources/documentation/e2b/) · [licence](../../resources/licenses/e2b/) — **rejected** |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| Google LLM Tuning Playbook | https://github.com/google-research/tuning_playbook (CC BY 4.0; dormant since 2024-06) |
| llama.cpp | https://github.com/ggml-org/llama.cpp |
| llama-cpp-python | https://github.com/abetlen/llama-cpp-python |
| Ollama | https://github.com/ollama/ollama · https://docs.ollama.com/ |
| tiktoken | https://github.com/openai/tiktoken |
| Transformers | https://github.com/huggingface/transformers |
| OpenAI Python SDK | https://github.com/openai/openai-python · pricing at https://openai.com/api/pricing/ (**metadata-only**) |
| Anthropic Python SDK | https://github.com/anthropics/anthropic-sdk-python · pricing at https://www.anthropic.com/pricing (**metadata-only**) |
| Google Gen AI SDK | https://github.com/googleapis/python-genai · pricing at https://ai.google.dev/pricing (**metadata-only**) |
| lmdeploy | https://github.com/InternLM/lmdeploy |
| MLX-LM | https://github.com/ml-explore/mlx-lm |
| bitsandbytes | https://github.com/bitsandbytes-foundation/bitsandbytes |
| vLLM | https://github.com/vllm-project/vllm |
| Text Embeddings Inference | https://github.com/huggingface/text-embeddings-inference (**no PyPI snapshot resolved**) |
| AutoGPTQ | https://github.com/PanQiWei/AutoGPTQ — **archived** |
| AutoAWQ | https://github.com/casper-hansen/AutoAWQ — **archived** |
| LiteLLM | https://github.com/BerriAI/litellm |
| Hugging Face | https://huggingface.co/ — **unreachable for download from the build sandbox** (MO-03) |

## 5. Adoption steps

1. **Answer Q1–Q3 first.** Total RAM, RAM already committed by an existing end-to-end job (measured with
   `psutil`), VRAM if any, free disk, disk throughput, OS. Write it into a `RESOURCE_BUDGET.md`.
2. **Read the Tuning Playbook** — specifically its evaluation-first and resource sections. It is the only
   redistributable long-form guidance bundled here.
3. **Compute the memory arithmetic** for any candidate: weights at the intended quantisation **plus** KV
   cache at the intended context length **plus** runtime overhead. Compare against the declared ceiling
   with a safety margin. If it does not fit, choose the no-model shape — that is a complete design.
4. **Read the weight licence on the model card** at adoption time (MO-03): Apache-2.0, Llama community
   licence, OpenRAIL-M or custom. Treat weights as a separate licence from code, as Marker/Surya
   demonstrated.
5. **If hosted is authorised (Q8)**: read the pricing and quota pages **on that date**, record the URL and
   date, declare what data egresses, and implement a budget, a queue, defer-and-retry, and a
   quota-exhaustion refusal path.
6. **Decide daemon versus per-call** and measure both: Ollama `keep_alive` idle cost versus CLI start cost.
7. **Add exact token accounting** (`tiktoken`) at every context assembly point.
8. **Add conservative failure**: on timeout, quota exhaustion or resource shortage → degrade (shorter
   context, smaller top-k) → refuse, and log which happened.
9. **Record the model, version, prompt hash and config hash** in every run (workstream 08) so that a result
   can be attributed to a specific model at a specific version.

## 6. Resource implications

All **estimates from documentation**; none measured. Nothing here is a commitment.

| Item | Expectation | Note |
|---|---|---|
| Weights at 4-bit quantisation | Roughly proportional to parameter count | The *documented* figure per model must be read at adoption time |
| **KV cache** | Grows with context length × layers × heads, **independently of weight size** | Requirement 13.3; `lmdeploy`'s KV-cache quantisation docs are bundled for this reason |
| `llama.cpp` on CPU | Workable for small models at short contexts | Threads and batch size matter; the bundled performance docs cover it |
| `Ollama` daemon | **Resident RAM/VRAM while a model is loaded**; `keep_alive` controls unload | Idle cost versus start cost — measure both |
| `transformers` on CPU | `device_map="auto"` can **silently spill to disk and stall** | `perf_infer_cpu` and `model_memory_anatomy.md` are bundled |
| Small embedding model | A few hundred MB resident (**documented estimate**) | Weights are an approval gate |
| Small NLI model (for the evidence gate) | Similar order | Rules are the zero-weight fallback |
| Hosted API | Off-box compute; **on-box cost is network and queueing** | The real constraints are budget, quota, latency and egress |
| MLX-LM | Apple Silicon only | Irrelevant unless Q1 says so |
| vLLM / lmdeploy / TEI | GPU-first or a server process | Rejected |

## 7. Qualification requirements

1. A written, measured `RESOURCE_BUDGET.md` exists, and every model decision cites a number from it.
2. The memory arithmetic (weights + KV cache + overhead at the intended context length) is computed and
   compared against the declared ceiling **before** any model is downloaded.
3. The weight licence was read on the model card, on a recorded date, and is quoted in the decision record.
4. If hosted: pricing and quota were read **on the adoption date**, the URL and date are recorded, the egress
   declaration is written, and a budget plus a quota-exhaustion refusal path exist.
5. Token accounting is exact (`tiktoken`), not estimated, at every context assembly point.
6. The daemon-versus-per-call decision is backed by two measurements, not a preference.
7. Conservative failure is demonstrated: a simulated timeout, quota exhaustion and memory-ceiling breach each
   produce a logged degrade-or-refuse, and never a partial answer presented as complete.
8. Every run records model, version, prompt hash and config hash.
9. **No quota evasion and no account rotation is proposed anywhere** — verified by review.
10. No free tier is assumed to be unlimited or permanent.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| vLLM, lmdeploy (as an engine), TEI | GPU-first or a server process |
| AutoGPTQ, AutoAWQ | **Archived upstream** |
| PEFT, Unsloth, bitsandbytes-as-a-learning-mechanism | Fine-tuning category; see workstream 07 |
| E2B | Paid, remote, and moves document content off-box |
| Bundling Hugging Face model cards or pricing pages | Host unreachable; not redistributable; a stale copy is worse than a link |
| Bundling model weights | Prohibited without approval, and an approval gate in any case |
| Quoting pricing or quotas from memory or from a snapshot | Requirement 13.6 |
| Assuming a free tier is unlimited or permanent | Requirement 13.7 |
| Proposing quota evasion or account rotation | Requirement 13.8 — prohibited |
| Choosing a model before measuring | Requirement 13.1 |
| Ignoring KV-cache growth because the weights are small | Requirement 13.3 |
| Promising a specific RAM saving | Prohibited; nothing here was measured on the target machine |
| Treating a hosted call as free of privacy consequences | Requirement 13.9 |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **Q1: the actual machine** | Everything in this workstream | Ask; measure |
| **Q2: peak RSS of an existing end-to-end job** | The declared ceiling | Phase 0 resource trace |
| **Q3: free disk and disk throughput** | Whether a local model or a spill tier is viable | Measure |
| **Q8: is a hosted API authorised, and under what budget and data-handling terms?** | The hosted shape | Ask; read the terms on that date |
| Model card licences | Requirement 13.5 | HF was unreachable for download; read the cards at adoption time |
| Pricing and quota details | Requirement 13.6 | Vendor pages unreachable and not redistributable; read them at adoption time |
| Whether `tiktoken` encoding tables are available offline on the target machine | Requirement 13.2 | Check at install time |
| Whether the machine is Apple Silicon | MLX-LM's relevance | Q1 |
| Whether any local model fits at the needed context length | The local shape | Step 3's arithmetic, once Q1–Q3 are answered |
| Nothing here was executed, downloaded or installed | All measurements | Requires authorisation this engagement did not have |
