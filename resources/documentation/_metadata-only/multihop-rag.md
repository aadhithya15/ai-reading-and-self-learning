# METADATA-ONLY ENTRY — MultiHop-RAG (not bundled)

| Field | Value |
|---|---|
| Component id | `multihop-rag` |
| Name | MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries |
| Upstream repository | https://github.com/yixuantt/MultiHop-RAG |
| Paper (arXiv, verified via arXiv API 2026-10-14) | arXiv:2401.15391v1, submitted 2024-01-27, Yixuan Tang, Yi Yang |
| Checked date | 2026-10-14 |
| Upstream HEAD commit at check | see `ASSET_MANIFEST.json` → component `multihop-rag` (recorded, file not retained) |
| Licence | **No licence file present in the repository at the check date** (GitHub licence detection returned none; repository root listing showed `README.md`, `agentic_rag/`, `bm25_retrieval.py`, `hybrid_retriever.py`, `pipeline/`, `qa_evaluate.py`, `qa_llama.py`, `requirement.txt`, `rerank_result.py`, `resource/`, `retrieval_evaluate.py`, `rrf_fusion.py` and no `LICENSE`) |
| Redistribution status | **NOT PERMITTED — nothing from this repository may be copied into this collection.** Absence of a licence means default "all rights reserved" under copyright law. |
| Bundled? | **No.** A first collection pass downloaded `README.md` and `pipeline/readme.md`; these were deleted on 2026-10-14 during the licence audit and are not present in the published tree. |

## Why it is still catalogued

MultiHop-RAG is one of the few public benchmarks whose *unit of evaluation* matches a real SAM-X
failure mode: questions that require **two or more separate pieces of evidence** to be retrieved and
combined, with the supporting evidence itself labelled. SAM-X needs exactly that behaviour
(find information via summaries, then reopen original passages and cite them). The paper's reported
finding — that existing RAG systems retrieve and answer multi-hop queries poorly — is a directly
relevant negative result.

## What to do instead (lawful alternatives)

1. **Read the paper through the official arXiv link** (arXiv:2401.15391) and cite it. Reading is not
   redistribution.
2. **Ask the authors for an explicit licence** if the dataset or code is wanted locally. An email or a
   GitHub issue requesting licence clarification is the correct route; do not mirror the repository
   meanwhile.
3. **Re-implement the construct, not the data.** The multi-hop *task shape* (query → ≥2 supporting
   passages → answer, with per-passage evidence labels) is not itself copyrightable. SAM-X can build
   its own multi-hop items from documents it already holds the rights to index, using
   `templates/experiment-contract.md` and `workstreams/08-independent-evaluation/README.md`.
4. **Use lawfully licensed substitutes** already bundled in this collection: RULER's multi-hop
   tracing and variable-tracking generators (Apache-2.0, code bundled under
   `resources/code-examples/ruler/`) produce multi-hop retrieval tasks synthetically and can be
   regenerated locally without redistributing any dataset.

## Related entries

- Workstream: `workstreams/05-retrieval-evidence/README.md`, `workstreams/08-independent-evaluation/README.md`
- Comparable lawfully-bundled assets: `resources/code-examples/ruler/`, `resources/benchmark-descriptions/longbench/`
