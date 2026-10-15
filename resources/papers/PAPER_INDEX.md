# PAPER INDEX

Bibliographic index of the research papers this collection relies on.

**No paper PDF is bundled, and none may be.** Two independent reasons:

1. **Licence.** arXiv's default terms are the *arXiv non-exclusive distribution licence*, which does not
   grant third-party redistribution. An arXiv PDF found **inside** a permissively-licensed repository
   inherits the *paper's* licence, not the repository's — so `docling`'s bundled `2203.01017v2.pdf` and
   `2305.03393v1.pdf`, and `unstructured`/`langchain`'s `layout-parser-paper.pdf`, were deliberately not
   copied either.
2. **Access.** `arxiv.org` and `export.arxiv.org` were unreachable for binary download from the build
   sandbox on 2026-10-14. A separate read-only page-fetch path reached arXiv **metadata**, which is what was
   used to verify the identifiers below.

So this index gives: the identifier, the version verified, the title and first author as returned by the
arXiv API, the venue where the API reported one, the workstream it informs, and the specific claim it is
used for. Full texts must be obtained from the official source by whoever is authorised to do so.

**Verification status is recorded per entry.** An identifier that was not re-queried this session is labelled
`NOT RE-VERIFIED` and must not be cited without checking it first. Guessing an arXiv identifier is how
fabricated citations happen: two identifiers assumed during this build were **wrong** (see §3).

---

## 1. Verified against the arXiv API on 2026-10-14 (31 papers)

Status key: **verified** = the identifier resolved and the returned title matched the intended paper.

### 1.1 Retrieval-augmented generation and evidence

| arXiv id | Title | First author / venue (as reported) | Workstream | Claim it is used for |
|---|---|---|---|---|
| 2005.11401v4 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Lewis et al., NeurIPS 2020 | 05 | The RAG formulation: a retriever plus a generator, with the parametric memory the retrieval replaces |
| 2305.14627v2 | Enabling Large Language Models to Generate Text with Citations (ALCE) | Gao et al., EMNLP 2023 | 05, 08 | **Even the best systems lacked complete citation support ~50% of the time on ELI5** — citation *presence* is a weak signal, so quote-presence plus entailment are both required |
| 2311.09476v2 | ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems | Saad-Falcon et al., NAACL 2024 | 05, 08 | Automated RAG evaluation with a small amount of human-annotated data; adopted as a *concept*, not run |
| 2401.00396v2 | RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Generation Systems | Niu et al. | 05, 08 | A corpus specifically about RAG hallucination; supports treating the evidence gate as mandatory |
| 2405.14831v3 | HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models | Gutiérrez et al. | 05, 06 | **Reported** single-step retrieval 10–30× cheaper and 6–13× faster than IRCoT, up to +20% on multi-hop. Adopted as a lead about single-step multi-hop retrieval; **not reproduced here** |
| 2404.16130v2 | From Local to Global: A Graph RAG Approach to Query-Focused Summarization | Edge et al. (Microsoft) | 05, 06 | The GraphRAG method. Adopted as an *alternative to reject on resource fit*: LLM-heavy index build, and community summaries are model-written hypotheses |
| 2004.12832v2 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | Khattab & Zaharia | 05 | Late-interaction retrieval as the middle option between lexical and single-vector dense; relevant if lexical recall fails on paraphrastic queries |
| 2409.04701v3 | Late Chunking in Large Language Models | Günther et al. (Jina AI) | 03, 05 | Chunking *after* long-context embedding preserves cross-chunk context — relevant to how pages are chunked without losing clause scope |

### 1.2 Long context, position sensitivity and benchmarks

| arXiv id | Title | First author / venue | Workstream | Claim it is used for |
|---|---|---|---|---|
| 2404.06654v3 | RULER: What's the Real Context Size of Your Long-Context Language Models? | Hsieh et al., COLM 2024 | 03, 04, 08 | **The most load-bearing finding in this collection.** Near-perfect vanilla needle-in-a-haystack scores coexist with sharp drops as length and task complexity grow; of models claiming ≥32K context, only about half held up at 32K. Its Apache-2.0 **generators** are bundled and are the recommended item source |
| 2307.03172v3 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al., TACL 2023 | 03, 04, 08 | Evidence **position** changes accuracy — so position must be swept and the curve reported, not a single point |
| 2402.14848v2 | Same Task, More Tokens: the Impact of Input Length on the Reasoning Performance of Large Language Models | Levy et al., ACL 2024 | 03, 04 | Performance degrades with input length at **fixed** task difficulty: length is an independent variable |
| 2402.13718v3 | InfiniteBench: Extending Long Context Evaluation Beyond 100K Tokens | Zhang et al. | 04, 08 | 100K+ token task construction; harness and scorers bundled (MIT). Data not downloaded |
| 2308.14508v2 | LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding | Bai et al. | 04, 08 | 21 datasets, **average 6 711 English words** — which is why it does not test SAM-X's 147-page scale. Retrieval helps weak long-context models and lags strong ones |
| 2403.12766v3 | NovelQA: Benchmarking Retrieval-Augmented and Long-Context Language Models with Long Narrative QA | Wu et al., ICLR 2025 | 04, 08 | >200K-token copyrighted novels: a genuine long-narrative construct whose corpus is **not redistributable** — hence metadata-only |
| 2404.16811v2 | Found in the Middle: How Language Models Use Long Contexts Better via Plug-and-Play Positional Encoding / IN2 training | Hsieh et al. | 04 | **Reported**: 4K–32K synthetic QA training repairs lost-in-the-middle on Mistral-7B. Two lessons — synthetic item generation is a legitimate tool, and a model's behaviour may already have been shaped by synthetic data (a contamination consideration) |
| 2401.15391v1 | MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | Tang & Yang | 04, 05, 08 | The multi-hop RAG construct. **The repository has no licence file**, so nothing was bundled; RULER's `variable_tracking.py` + `qa.py` produce the same construct lawfully |

### 1.3 Memory, agents and learning

| arXiv id | Title | First author / venue | Workstream | Claim it is used for |
|---|---|---|---|---|
| 2310.08560v2 | MemGPT: Towards LLMs as Operating Systems | Packer et al. | 03, 06 | The **paging architecture** adopted here: main context versus external context with explicit paging triggers. The *server* is not adopted |
| 2404.13501v1 | A Survey on the Memory Mechanism of Large Language Model based Agents (39 pp) | Zhang et al. | 06 | Supplies the **evaluation-dimension checklist** adopted in workstream 06 §7 |
| 2304.03442v2 | Generative Agents: Interactive Simulacra of Human Behavior | Park et al. | 06 | Memory stream → reflection → planning. The reflection step is exactly what workstream 07 refuses to let *accept* a lesson |
| 2305.10250v3 | MemoryBank: Enhancing Large Language Models with Long-Term Memory | Zhong et al. | 06 | An Ebbinghaus-curve forgetting schedule — **rejected here**: an auditable research store must not decay facts on a timer |
| 2501.13956v1 | Zep: A Temporal Knowledge Graph Architecture for Agent Memory | Rasmussen et al. | 06 | **Reported** to beat MemGPT on the Deep Memory Retrieval benchmark. The **bi-temporal** idea is adopted; the server is rejected; the benchmark result is a vendor claim, not reproduced |
| 2305.16291v2 | Voyager: An Open-Ended Embodied Agent with Large Language Models | Wang et al. | 06, 07 | **Reported** 3.3× more unique items and skills that transfer to a **new** world. The skill-library *pattern* is adopted; the transfer result is a Minecraft result and therefore an **analogy, not evidence** for document reading |
| 2303.11366v4 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. | 07 | **Reported** 91% pass@1 on HumanEval versus GPT-4's 80%. Its gains come from an environment with a **ground-truth test suite** — which document interpretation does not have. Self-reflection may propose, never accept |
| 2303.17651v2 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al. | 07 | **Reported** ~20% average absolute improvement on GPT-3.5/4-era models, on tasks with checkable outputs. Same limitation as Reflexion |
| 2401.10020v3 | Self-Rewarding Language Models | Yuan et al. | 07 | The model is its own judge — precisely the configuration workstream 07 §7.2 forbids for lesson acceptance. Catalogued as the counter-example |

### 1.4 Uncertainty, inference and anomaly detection

| arXiv id | Title | First author / venue | Workstream | Claim it is used for |
|---|---|---|---|---|
| 2112.10510v7 | Transformers Can Do Bayesian Inference | Müller et al., ICLR 2022 | 04, 10 | Prior-fitted networks: a transformer can amortise Bayesian inference. Relevant to representing uncertainty about an extracted parameter rather than emitting a point value |
| 2105.07538v1 | Collective anomaly detection in high-dimensional VAR models | Maeng, Eckley & Fearnhead | 10 | A lasso-based sparse-VAR **collective** anomaly test with **Type-I error control**. Relevant because most ad-hoc drift detectors have no false-alarm guarantee, and workstream 10 requires a declared false-alarm budget |

> Note on 2105.07538: this identifier was **assumed** during the build to be a conformal-prediction
> introduction. The arXiv API resolved it to the VAR anomaly-detection paper above. The mistake is recorded
> rather than hidden, and the paper turned out to be relevant to workstream 10 anyway.

### 1.5 Security and adversarial input

| arXiv id | Title | First author / venue | Workstream | Claim it is used for |
|---|---|---|---|---|
| 2302.12173v2 | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | Greshake et al. | 05, 06, 14 | Indirect injection **through retrieved content** — the reason parsed text must be data, never instructions |
| 2402.07867v3 | PoisonedRAG: Knowledge Poisoning Attacks to Retrieval-Augmented Generation of Large Language Models | Zou et al., USENIX Security 2025 | 05, 06, 14 | **Five injected texts → ~90% attack success over a corpus of millions**, and the defenses it evaluated were reported insufficient. Provenance is therefore necessary but not sufficient |
| 2403.02691v3 | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents | Zhan et al., ACL 2024 Findings | 14 | 1 054 test cases; a ReAct-prompted GPT-4 was vulnerable in **24%**, roughly **doubling** with a "hacking" prompt |
| 2406.13352v3 | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | Debenedetti et al. | 14 | 97 tasks and 629 security tests; state-of-the-art LLMs **fail many even unattacked** — utility and security must be measured together |

## 2. Referenced by repository only — identifier NOT RE-VERIFIED

These papers are cited by their **repository**, which *was* resolved and pinned to a commit. The arXiv
identifier listed is the one commonly associated with the work and was **not** confirmed against the arXiv
API in this session. Do not cite the identifier without re-querying it.

| Work / repository | Commonly cited id | Status |
|---|---|---|
| HELMET (`princeton-nlp/HELMET`) | **unknown** — `2409.12181` was queried and resolved to a *different* paper | **DISPROVED**; re-derive from the repository README (MO-08) |
| RAPTOR (`parthsarthi03/raptor`) | 2401.18059 | NOT RE-VERIFIED |
| LightRAG (`HKUDS/LightRAG`) | 2410.05779 | NOT RE-VERIFIED |
| Self-RAG (`AkariAsai/self-rag`) | 2310.11511 | NOT RE-VERIFIED |
| CRAG (`gitrlab/CRAG` / Meta) | 2401.15884 | NOT RE-VERIFIED |
| TRUE (`Elronband/TRUE`) | 2204.04991 | NOT RE-VERIFIED |
| DSPy (`stanfordnlp/dspy`) | 2310.03714 | NOT RE-VERIFIED |
| TextGrad (`zou-group/textgrad`) | 2406.07496 | NOT RE-VERIFIED |
| ACE (`ace-agent/ace`) | 2510.04618 | NOT RE-VERIFIED |
| MemOS (`MemTensor/MemOS`) | 2505.22101 | NOT RE-VERIFIED |
| ExpeL (`LeapLabTHU/ExpeL`) | 2308.10144 | NOT RE-VERIFIED — **and the repository has no licence file and did not resolve via the API** |
| LLMs cannot reliably self-correct reasoning (the negative result workstream 07 depends on) | not recorded | **NOT RE-VERIFIED** — the design rule in workstream 07 §7.2 does **not** depend on this citation |

## 3. Identifiers recorded as leads only (46 in total)

The following identifiers surfaced during the search and were recorded as leads. **None was verified this
session.** They are listed so that the next reader knows they exist and knows not to cite them without
checking. Re-query the arXiv API in batches of **≤ 6 ids** per call (larger batches were truncated, and one
retry failed with a proxy `SignatureDoesNotMatch` error).

```
2310.01798  2306.05499  2307.15043  2401.05566  2304.15004  2502.12110
2309.16058  2312.06648  2211.09110  2403.04132  2306.05685  2309.15217
2303.16634  2311.04850  2308.08493  2406.19314  2309.17016  2211.05102
2208.07339  2210.17323  2306.00978  2205.14135  2309.06180  1610.02136
2010.03759  2002.08791  1909.10155  2206.01062  2308.13418  2408.09869
2111.08609  2409.01704  2011.09926  2310.16787  2307.10789
```

Plus the eleven repository-linked identifiers in §2. Total recorded but unverified: **46**.

## 4. Rules for using this index

1. **A verified identifier is not a verified claim.** Each row above records the *specific* claim the paper
   is used for, and whether that claim is the paper's own **reported** result or something this collection
   measured. Nothing in this collection reproduced any paper's result.
2. **Check the training and publication dates for contamination** before using any paper's benchmark as an
   evaluation source. Most of the benchmarks above are 2023–2024 vintage and are plausibly inside the
   training data of any current model. See
   [BENCHMARK_NOTES.md](../benchmark-descriptions/BENCHMARK_NOTES.md).
3. **Vendor and author results are leads.** HippoRAG's cost/speed figures, Zep's DMR result, Reflexion's
   HumanEval score, Self-Refine's ~20%, FILM/IN2's repair of lost-in-the-middle, GraphRAG's summarisation
   quality — all are the authors' own measurements on their own tasks. None is evidence about SAM-X.
4. **Do not bundle a PDF.** If a full text is needed, obtain it through a route the project is authorised to
   use, keep it outside this repository unless its licence permits redistribution, and record it with
   [templates/source-provenance.json](../../templates/source-provenance.json).
5. **Update this file when you verify an identifier.** Move the entry from §2/§3 to §1 with the version
   string the API returned and the date you checked. Do not silently edit a `NOT RE-VERIFIED` label into a
   citation.

## 5. Where the redistributable long-form material actually is

Two documents in this collection are fully redistributable long-form technical works, and they carry more
practical weight per megabyte than any paper here:

| Document | Licence | Path |
|---|---|---|
| **Google LLM Tuning Playbook** (~120 KB of text) | CC BY 4.0 | [resources/documentation/tuning-playbook/](../documentation/tuning-playbook/) |
| **OWASP Top 10 for LLM Applications 2025** (10.72 MB PDF + 11 markdown files) | CC BY-SA 4.0 | [resources/documentation/owasp-llm-top10/](../documentation/owasp-llm-top10/) |

Both licences were read from the bundled text. Attribution is recorded in
[ATTRIBUTION.md](../../ATTRIBUTION.md).
