# Workstream 05 — Retrieval, Evidence and Citation Integrity

**Objectives served:** use summaries to locate and originals to verify; recognise unsupported claims and
real contradictions; keep source-linked facts separate from hypotheses; handle stale and conflicting
sources safely.

**The trap this workstream exists to prevent**, stated in the assignment: *a matching quote or a valid
citation identifier does not necessarily support an answer.* The bundled evidence backs the concern — ALCE
(arXiv:2305.14627v2, EMNLP 2023, **verified** metadata) reports that even the best systems lacked complete
citation support about half the time on ELI5.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 5.1 | **Lexical retrieval first** (SQLite FTS5, `rank_bm25`), dense second, graph only on documented failure | Specification text is dominated by exact tokens: clause numbers, parameter names, "except when" |
| 5.2 | A **mandatory evidence gate** before any answer is emitted: quote-presence → entailment → abstain | Requirement 5.1 finds passages; only a gate makes them evidence |
| 5.3 | Abstention with one of four labelled outcomes: `missing_information`, `partial_constraint`, `unsupported_interpretation`, `genuine_contradiction` | "I don't know" is not informative; the *kind* of not-knowing is |
| 5.4 | **Freshness as a retrieval filter**, not a post-hoc warning | A stale source must be excluded or flagged at query time using validity intervals |
| 5.5 | Retrieval failure distinguishable from non-existence | "We couldn't find it" and "it isn't there" require different responses |
| 5.6 | Hierarchical summaries for **location only**, stored as hypotheses | Objective 3 |
| 5.7 | Every retrieved candidate passage stored with its score, rank and page, so the decision is auditable | A retrieval choice nobody can replay is not a decision |
| 5.8 | Contradictions **flagged, never merged** | Merging is how a real contradiction becomes a silent wrong value |

**Not a goal.** Maximising recall. A retrieval layer that returns 50 passages to avoid missing one has
moved the problem into the context window, where workstream 01's ceiling and workstream 04's position
sensitivity will punish it.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: FTS5/BM25 → evidence gate → abstain

1. **Retrieve lexically** over the workstream-03 page index (SQLite FTS5 from the stdlib; `rank_bm25` as a
   comparison or where FTS5's tokenisation is wrong for the corpus).
2. **Optionally locate hierarchically**: a document → chapter → page summary tree (RAPTOR's pattern) narrows
   the search. Summaries live in the `hypotheses` store and may never appear in an answer's `evidence` field.
3. **Gate**: is the cited string literally present on the cited page (deterministic)? Does the cited passage
   **entail** the claim (small local NLI model or rules)? If not, abstain with a label from 5.3.
4. **Filter by validity**: exclude or flag sources whose validity interval does not cover the query time.
5. **Record everything**: query, candidate list with scores, gate decision and reason.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| Dense embeddings first | **Measure second** | Blurs exactly the distinctions that decide trading questions, and needs weights (an approval gate). May win on paraphrastic queries — that is what the experiment measures |
| `sqlite-vec` | **Recommended dense tier if one is needed** | Inside the same file and the same query language as everything else; MIT/Apache-2.0 dual-licensed (both texts bundled) |
| `Faiss` on-disk IVF, `USearch` | Catalogued | Capable, but `mmap`-backed indexes reduce process RSS without reducing machine pressure, and they add a native format for a two-document corpus |
| `LanceDB`, `Chroma` (embedded) | Catalogued | Overlap `sqlite-vec` entirely, with a native format or an extra dependency |
| Qdrant server, Weaviate, Milvus, Vespa | **Rejected** | Server processes / distributed clusters. Full reasoning in [REJECTED_OPTIONS.md](../../REJECTED_OPTIONS.md) §1 |
| `GraphRAG` | **Not adopted** | Index build is LLM-call heavy (cost + RAM) and community summaries are model-written hypotheses. Adopt only if a recorded failure of hierarchical summaries shows global "what are the themes" questions are necessary |
| `LightRAG` | **Not adopted** | Cheaper build than GraphRAG per its authors (**reported**, not reproduced), same fundamental objection about model-written summaries |
| `graphiti` + Neo4j | **Pattern adopted, database not** | Its bi-temporal edge model is exactly right and its Apache-2.0 code is bundled; a graph database process is not justified when three SQL columns deliver validity intervals |
| `cognee`, `mem0`, `MemOS`, `A-MEM` | **Schemas catalogued, not adopted** | Each consolidates or rewrites records. An auditable research system must not consolidate |
| `RAGFlow` | **Rejected** | Multi-container Compose stack |
| `LlamaIndex` / `Haystack` / `txtai` | **Pattern sources only** | Adopting one replaces the reading stack, contradicting R5. Borrow their node/relationship schemas |
| `DSPy` | Catalogued for its **signature and metric vocabulary** | Optimisers make many LLM calls; optimisation must never touch held-out sources |
| `sentence-transformers`, `TEI` | Catalogued | Weights and (for TEI) a Rust server; both gated |
| `Ragas`, `DeepEval` | **Metric vocabulary only** | LLM-judged, therefore not independent supervision; neither was run |
| Citation metrics from ALCE / ARES / RAGTruth / TRUE | **Concepts adopted** | ALCE and ARES and RAGTruth metadata **verified**; TRUE's identifier (2204.04991) was **not re-verified this session** and is labelled as such |
| `long-form-factuality` (SAFE) | Decomposition idea adopted | Its rater is a hosted model judging a model; composite licence, scoped in the manifest |
| `prompt-injection-refs` | **Mandatory reading, metadata-only** | Retrieval is the injection vector: PoisonedRAG (arXiv:2402.07867v3, USENIX Security 2025, **verified**) reports ~90% attack success from five injected texts in a corpus of millions, and reports the defenses it evaluated as insufficient |

### 2.3 Why lexical first is a position, not a prejudice

Recorded so it can be **refuted by measurement**: specification documents are dominated by exact tokens
(`4.2(b)`, `except when`, an indicator name, a parameter key). Dense similarity is trained to make
paraphrases close, which is the opposite of what distinguishes a rule from its exception. The catalog row
for `rank_bm25` contains the bounded experiment: 40 frozen queries (20 exact-token, 20 paraphrastic), 8
deliberately unanswerable, recall@5 of the correct page, plus the gate's effect on both correct and
incorrect answers. **The answer may differ per query class**, and if it does, that is the finding.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `rank_bm25` (Apache-2.0) | [documentation](../../resources/documentation/rank_bm25/) · [package source](../../resources/code-examples/rank_bm25/) · [licence](../../resources/licenses/rank_bm25/) |
| `sqlite-vec` (MIT / Apache-2.0) | [documentation](../../resources/documentation/sqlite-vec/) · [examples](../../resources/configurations/sqlite-vec/) · [both licence texts](../../resources/licenses/sqlite-vec/) |
| `raptor` (MIT) | [full implementation](../../resources/code-examples/raptor/) — `tree_builder.py`, `tree_retriever.py`, `cluster_utils.py`, `RetrievalAugmentation.py`, `FaissRetriever.py`, `Retrievers.py`, `tree_structures.py` · [documentation](../../resources/documentation/raptor/) |
| `faiss` (MIT) | [on-disk IVF demo](../../resources/code-examples/faiss/) · [documentation](../../resources/documentation/faiss/) · [licence](../../resources/licenses/faiss/) |
| `usearch` (Apache-2.0) | [documentation](../../resources/documentation/usearch/) · [code examples](../../resources/code-examples/usearch/) · [licence](../../resources/licenses/usearch/) |
| `graphiti` (Apache-2.0) | [documentation](../../resources/documentation/graphiti/) · [core code](../../resources/code-examples/graphiti/) · [licence](../../resources/licenses/graphiti/) |
| `graphrag` (MIT) | [documentation](../../resources/documentation/graphrag/) — `docs/index/overview.md`, `docs/query/overview.md`, `docs/prompt_tuning/overview.md`, `docs/cli.md` · [licence](../../resources/licenses/graphrag/) |
| `lightrag` (MIT) | [documentation](../../resources/documentation/lightrag/) · [licence](../../resources/licenses/lightrag/) |
| `dspy` (MIT) | [documentation](../../resources/documentation/dspy/) — signatures, modules, metrics, evaluation and optimisation guides · [licence](../../resources/licenses/dspy/) |
| `llama_index` (MIT) | [documentation](../../resources/documentation/llama_index/) · [licence](../../resources/licenses/llama_index/) |
| `cognee` (Apache-2.0) | [documentation](../../resources/documentation/cognee/) · [licence and NOTICE](../../resources/licenses/cognee/) |
| `mem0` (Apache-2.0) | [documentation](../../resources/documentation/mem0/) · [licence](../../resources/licenses/mem0/) |
| `memos` (Apache-2.0) | [documentation](../../resources/documentation/memos/) · [licence](../../resources/licenses/memos/) |
| `a-mem` (MIT) | [documentation](../../resources/documentation/a-mem/) · [licence](../../resources/licenses/a-mem/) |
| `ragas`, `deepeval` | [RAGAS docs](../../resources/documentation/ragas/) · [DeepEval docs](../../resources/documentation/deepeval/) — metric definitions only |
| `long-form-factuality` | [documentation](../../resources/documentation/long-form-factuality/) — `eval/README.md`, `longfact/README.md` · [scoped licence](../../resources/licenses/long-form-factuality/) |
| `vectara-answer` (Apache-2.0) | [documentation](../../resources/documentation/vectara-answer/) · [licence](../../resources/licenses/vectara-answer/) |
| `owasp-llm-top10` (CC BY-SA 4.0) | [**LLM08 Vector and Embedding Weaknesses**](../../resources/documentation/owasp-llm-top10/) plus LLM01, LLM04, LLM09 and the full PDF · [licence](../../resources/licenses/owasp-llm-top10/) |
| `unstructured`, `grobid`, `tei`, `chromadb`, `lancedb`, `qdrant-client`, `weaviate-client`, `pymilvus`, `vespa`, `ragflow`, `txtai`, `haystack-ai`, `sentence-transformers`, `transformers` | [documentation](../../resources/documentation/) and [registry metadata](../../resources/documentation/_pypi-metadata/) — catalogued, mostly not adopted |
| `multihop-rag` | **Not bundled** — no upstream licence. See [_metadata-only record](../../resources/documentation/_metadata-only/multihop-rag.md) |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| rank_bm25 | https://github.com/dorianbrown/rank_bm25 |
| sqlite-vec | https://github.com/asg017/sqlite-vec |
| RAPTOR | https://github.com/parthsarthi03/raptor (dormant since 2024-09-03) |
| Faiss | https://github.com/facebookresearch/faiss |
| USearch | https://github.com/unum-cloud/USearch (**corrected from `unum-cloud/usearch`**) |
| Graphiti | https://github.com/getzep/graphiti |
| GraphRAG | https://github.com/microsoft/graphrag |
| LightRAG | https://github.com/HKUDS/LightRAG |
| DSPy | https://github.com/stanfordnlp/dspy |
| LlamaIndex | https://github.com/run-llama/llama_index |
| cognee | https://github.com/topoteretes/cognee |
| mem0 | https://github.com/mem0ai/mem0 |
| RAGAS | https://github.com/vibrantlabsai/ragas (**moved from `explodinggradients/ragas`**) |
| DeepEval | https://github.com/confident-ai/deepeval |
| Long-form factuality | https://github.com/google-deepmind/long-form-factuality |
| Vectara Answer | https://github.com/vectara/vectara-answer (dormant since 2025-05) |
| RAGFlow | https://github.com/infiniflow/ragflow |
| Vespa | https://github.com/vespa-engine/vespa (**no PyPI snapshot — GitHub-only component**) |
| OWASP Top 10 for LLM Applications 2025 | https://github.com/OWASP/www-project-top-10-for-large-language-model-applications |
| Papers | ALCE arXiv:2305.14627v2 · ARES arXiv:2311.09476v2 · RAGTruth arXiv:2401.00396v2 · RAG arXiv:2005.11401v4 · PoisonedRAG arXiv:2402.07867v3 (all **verified** 2026-10-14); TRUE 2204.04991 · Self-RAG 2310.11511 · CRAG 2401.15884 (**not re-verified this session**) |

## 5. Adoption steps

1. **Turn on FTS5** over the workstream-03 page index. Record the tokeniser choice; it is a decision, not a
   default, and it decides whether `4.2(b)` is one token or three.
2. **Build the 40-query frozen set**: 20 exact-token, 20 paraphrastic, plus 8 deliberately unanswerable and
   at least 4 "quote present but not entailing" trap items.
3. **Measure lexical recall@5 of the correct page** before adding anything. This is the number everything
   else is compared against.
4. **Implement the deterministic gate first**: quote-presence. It costs nothing and catches fabricated
   citations outright.
5. **Add entailment** — rules first if no weights are approved, then a small local NLI model as an approval
   gate. Record which was used; the two are not interchangeable.
6. **Wire abstention** to the four labels in 5.3, and score abstention correctness from the first run.
7. **Add validity filtering** using the workstream-06 temporal columns: a source whose interval does not
   cover the query time is excluded or flagged, and the flag is visible in the answer.
8. **Add hierarchical location** (three levels: document, chapter, page) only if step 3 shows recall
   failing on long documents. Store summaries as hypotheses.
9. **Only then consider a dense tier**, and only for the query class where lexical demonstrably failed.
10. **Log every retrieval decision**: query, candidate list with scores and ranks, gate outcome and reason.

## 6. Resource implications

All **estimates from documentation**; none measured.

| Item | Expectation | Note |
|---|---|---|
| SQLite FTS5 | In-file index; RAM bounded by the configured page cache | Effectively free at 147-page scale |
| `rank_bm25` | In-memory term statistics | Trivial at current corpus size; grows linearly |
| `sqlite-vec` | Vectors in shadow tables inside SQLite; brute-force scan | Scan cost grows with corpus size — fine now, revisit at 10⁵ pages |
| Small embedding model | A few hundred MB resident (**documented estimate**) | Weights are an approval gate |
| Small NLI model for entailment | Similar order | Same gate; rules are the zero-weight fallback |
| `Faiss` on-disk IVF / `USearch` | Low RSS, **high page-cache pressure** | Report PSS and available memory, not RSS alone |
| RAPTOR tree build | **LLM-call heavy** | The reason to use a plain three-level tree instead |
| GraphRAG / LightRAG index build | Many LLM calls; graph plus vector stores at query time | Conflicts with the reported RAM and API budget |
| TEI (Rust server), Qdrant, Weaviate, Milvus, Vespa, RAGFlow | Separate processes / clusters | Rejected on footprint |

## 7. Qualification requirements

1. Lexical recall@5 of the **correct page** measured on the frozen 40-query set, with a denominator and an
   interval.
2. Evidence completeness: quote-presence **100%** of cited claims; entailment rate at or above the
   pre-declared threshold.
3. Zero answers whose `evidence` field contains a summary or any other hypothesis.
4. The gate's effect measured **both ways**: how many wrong answers it blocks *and* how many correct answers
   it blocks. A gate that blocks correct answers more often is rejected.
5. Abstention correct on the deliberately unanswerable items, with the four labels used correctly.
6. The trap items (quote present, entailment absent) are caught — this is the specific failure the
   assignment names.
7. Stale-source queries return the current source and flag the stale one; a query at time T returns the
   then-current fact.
8. Contradictions flagged, never merged; scope/version differences **not** flagged as contradictions.
9. Retrieval failure reported distinctly from non-existence.
10. **Transfer**: the same retrieval configuration re-run on a different document class, with no assumed
    carry-over of tuned parameters.
11. Peak RSS and p95 latency within the workstream-01 ceiling, measured out-of-process.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| Dense-first retrieval | Blurs rule-versus-exception distinctions; needs weights; unmeasured against lexical here |
| Milvus, Weaviate, Qdrant server, Vespa, RAGFlow | Server processes or clusters for a two-document corpus |
| GraphRAG / LightRAG as the primary retriever | LLM-heavy index build; model-written community summaries that must never be cited as facts |
| Graphiti + Neo4j as a database | Three SQL columns deliver validity intervals without a graph process |
| `mem0` / `cognee` / `MemOS` / `A-MEM` / hosted memory platforms | Consolidation rewrites records; hosted options move document content off-box (a rights and privacy decision the user has not made) |
| LlamaIndex / LangChain / Haystack / txtai as the retrieval stack | Replaces rather than complements (contradicts R5); at most one, ever |
| Ragas / DeepEval scores as an acceptance gate | LLM-judged; not independent supervision |
| MultiHop-RAG | No upstream licence; files deleted during the audit |
| Retrieval without an evidence gate | Produces confident answers with real-looking citations — the failure that destroys trust |
| Reporting recall without the gate's false-block rate | Would hide a gate that makes things worse |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| Whether lexical actually beats dense **on SAM-X's documents** | Step 9 | The frozen 40-query experiment; the answer may differ per query class |
| No entailment model chosen; weights are an approval gate | Requirement 5.2's automated form | Approve a small NLI model, or ship the rule-based gate first and label it as such |
| FTS5 tokenisation for clause identifiers and units | Step 1 | Test on real document text once rights are confirmed (Q4) |
| The document classes are unknown | Query-set design | Ask the user (also workstream 04 §9) |
| Whether a corpus-scale increase is planned | `sqlite-vec` brute-force viability | Ask; at 10⁵ pages an ANN index becomes worth its footprint |
| TRUE / Self-RAG / CRAG identifiers not re-verified | Citing them | Re-query the arXiv API in batches of ≤ 6 ids |
| PoisonedRAG's finding that evaluated defenses were insufficient | Any claim that provenance alone prevents poisoning | Treat provenance as necessary, not sufficient; combine with a source allowlist and write-path restrictions (workstreams 06 and 14) |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
