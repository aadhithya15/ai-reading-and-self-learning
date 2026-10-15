# Workstream 03 — Whole-Document Reading, Navigation and Extraction

**Objectives served:** interpret unfamiliar documents rather than recall benchmark answers; navigate
documents, chapters and pages with bounded memory; use summaries to *locate* and originals to *verify*;
never invent setup parameters.

**Reported context this workstream exists for:** a disk-backed prototype indexed **147 pages across 2
documents** (R2 — reported). Indexing is a navigation achievement and says nothing about comprehension. The
rejected reader qualification (R3: 13/32 exact field judgments, 0/4 fully correct cases) is the honest
baseline this workstream has to move.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 3.1 | A **page map**: page → byte range → heading path → SHA-256 of the extracted text | Every citation must resolve to a page that can be re-read |
| 3.2 | **Reopen-and-verify**: before emitting an answer, re-read the cited page from the source of record and check the claim against it | Objective 3, verbatim |
| 3.3 | Extraction failure is a **recorded state**, never a silent empty string | A missing page that produces a wrong answer is a data problem masquerading as a comprehension problem |
| 3.4 | Distinguish `extracted` / `image-only` / `failed` / `hash-mismatched` per page, and report coverage with every score | Coverage gaps change what a score means |
| 3.5 | Tables extracted **and verified cell by cell** before any parameter is read from them | A missed table row means an invented or dropped parameter |
| 3.6 | Two extractors, with **disagreement treated as an error signal** rather than resolved by preference | Silent extraction differences are how values get corrupted |
| 3.7 | Chapter/section navigation by heading path, not by page number alone | Page numbers move between versions; heading paths are more stable and are what a reader cites |
| 3.8 | Summaries used to **locate**, never to **support** | Summaries are hypotheses (workstream 06) |
| 3.9 | Bounded memory throughout — no whole-document strings held in RAM | Workstream 01's ceiling applies here |

**Not a goal.** Perfect extraction. The goal is extraction whose failures are enumerated, so that a wrong
answer can be attributed to the right cause.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended text path

`pypdf` (BSD-3) for the page map, outlines, metadata and structural navigation **+** `pdfminer.six` (MIT)
for layout-aware text extraction. Run both where cost allows and treat disagreement as an extraction-error
signal (requirement 3.6). `camelot` (MIT) for tables, with human cell-by-cell verification.

Licence is the deciding factor here: this is the only capable combination in the shortlist whose licences
are unambiguously permissive and whose dependencies are pure Python.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **PyMuPDF / pymupdf4llm** | **Not adopted as a dependency** | AGPL-3.0 **or** Artifex commercial. Copyleft reaches a networked service; the commercial route is a purchase decision outside this engagement. Fastest and most capable option in the shortlist — that is exactly why the licence matters |
| **Marker** | Reference only | Code Apache-2.0; **weights are "AI PUBS OPEN RAIL-M LICENSE (MODIFIED)" v0.1**, and restrictions propagate to derivative models. GPU recommended |
| **Surya** | Reference only | Same split: Apache-2.0 code, modified OpenRAIL-M weights |
| **Docling** | Catalogued; weights are an approval gate | MIT code and a good document model, but layout/TableFormer need model downloads and RAM in the hundreds of MB (documented estimate) |
| **MinerU** | Not adopted | Apache-2.0 **plus additional terms** that must be read before any adoption; GPU strongly recommended; multi-GB model downloads |
| **Unstructured** | Catalogued | Apache-2.0; `hi_res` strategy pulls in models. Its fast/CPU strategies overlap `pypdf`+`pdfminer.six` |
| **deepdoctection**, **docTR** | Catalogued | Model-based pipelines; OCR and layout weights required |
| **GROBID** | Not adopted | A **JVM service** with several hundred MB of heap, oriented to scholarly PDFs rather than specifications |
| **MarkItDown** | Conditional | MIT, and a single normalisation step is attractive — **adopt only if page provenance survives conversion**. That is the pre-declared rejection criterion in its catalog row: if converting to Markdown loses the page boundary, it cannot support requirement 3.1 |
| **Tesseract OCR** | Deferred | The first fix for scanned documents is *detection* (an image-only page is a distinct state from an empty page). OCR becomes relevant only when the coverage report shows image-only pages that matter. Native binary; weights/language data are a download |
| **RAGFlow** | **Rejected** | Multi-container Compose stack; a full RAG product, not a laptop component |
| **LlamaIndex / Haystack / txtai** | **Pattern sources, not adoption targets** | Overlapping frameworks; adopting one would replace the reading stack, contradicting R5 |
| **RAPTOR** | **Pattern adopted, dependency not** | Unmaintained since 2024-09-03 and pulls Faiss plus a clustering stack. Its full MIT implementation is bundled to read; the document → chapter → page tree is re-implemented in a few dozen lines |

### 2.3 The rule that governs this whole workstream

**Extraction and indexing do not establish understanding.** R2's 147 indexed pages are a navigation result.
Everything in this workstream is designed so that the difference between "we have the text" and "we
understood the document" stays visible in the measurements — coverage reported next to accuracy, and every
answer resolving to a re-readable page.

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `pypdf` | [documentation](../../resources/documentation/pypdf/) — including `docs/user/robustness.md` and `docs/dev/cmaps.md` · [licence](../../resources/licenses/pypdf/) |
| `pdfminer.six` | [documentation](../../resources/documentation/pdfminer-six/) — including `docs/README.md` and the CMap resources note · [licence](../../resources/licenses/pdfminer-six/) |
| `camelot` | [documentation](../../resources/documentation/camelot/) — `docs/user/quickstart.rst`, `docs/user/faq.rst`, `docs/api.rst` · [licence](../../resources/licenses/camelot/) |
| `markitdown` | [documentation](../../resources/documentation/markitdown/) — including the sample-plugin README · [licence](../../resources/licenses/markitdown/) |
| `pymupdf` | [documentation](../../resources/documentation/pymupdf/) · [**COPYING (AGPL-3.0)**](../../resources/licenses/pymupdf/) |
| `marker` | [documentation + benchmarks](../../resources/documentation/marker/) · [**MODEL_LICENSE (modified OpenRAIL-M)**](../../resources/licenses/marker/) |
| `surya` | [documentation](../../resources/documentation/surya/) · [**MODEL_LICENSE**](../../resources/licenses/surya/) |
| `docling` | [documentation](../../resources/documentation/docling/) — `docs/concepts/docling_document.md` and the integration guides · [licence](../../resources/licenses/docling/) |
| `mineru` | [documentation](../../resources/documentation/mineru/) · [licence with additional terms](../../resources/licenses/mineru/) |
| `unstructured` | [documentation](../../resources/documentation/unstructured/) · [licence](../../resources/licenses/unstructured/) |
| `deepdoctection` | [documentation + tutorials](../../resources/documentation/deepdoctection/) · [licence](../../resources/licenses/deepdoctection/) |
| `doctr` | [documentation](../../resources/documentation/doctr/) · [licence](../../resources/licenses/doctr/) |
| `grobid` | [documentation](../../resources/documentation/grobid/) — including `doc/Coordinates-in-PDF.md`, directly relevant to requirement 3.1 · [licence](../../resources/licenses/grobid/) |
| `tesseract` | [documentation + install notes](../../resources/documentation/tesseract/) · [licence](../../resources/licenses/tesseract/) |
| `raptor` | [full reference implementation](../../resources/code-examples/raptor/) — `tree_builder.py`, `cluster_utils.py`, `tree_retriever.py`, `RetrievalAugmentation.py`, `FaissRetriever.py`, `tree_structures.py`, `Retrievers.py`, `QAModels.py` · [documentation](../../resources/documentation/raptor/) · [licence](../../resources/licenses/raptor/) |
| `ruler` | [generators and configs](../../resources/configurations/ruler/) — shared with workstreams 04 and 08 |
| `transformers` | [documentation](../../resources/documentation/transformers/) — `model_memory_anatomy.md`, quantisation guides, `perf_infer_cpu` · [licence](../../resources/licenses/transformers/) |
| `letta` | [documentation](../../resources/documentation/letta/) — paging architecture, shared with workstream 06 |
| `llama_index`, `haystack-ai`, `txtai` | [LlamaIndex docs](../../resources/documentation/llama_index/) · registry metadata for the others — **pattern sources only** |
| `ragflow` | [documentation](../../resources/documentation/ragflow/) — **rejected**, bundled as a reference architecture |
| Scanned-source records | [_metadata-only](../../resources/documentation/_metadata-only/) |

Note: two arXiv PDFs exist inside `docling`'s test fixtures upstream (`2203.01017v2.pdf`,
`2305.03393v1.pdf`). They were **deliberately not copied** — a PDF inside an MIT repository inherits the
*paper's* licence, and arXiv's non-exclusive distribution licence does not grant third-party
redistribution.

## 4. Official upstream references

| Component | Upstream |
|---|---|
| pypdf | https://github.com/py-pdf/pypdf |
| pdfminer.six | https://github.com/pdfminer/pdfminer.six |
| Camelot | https://github.com/camelot-dev/camelot |
| MarkItDown | https://github.com/microsoft/markitdown |
| PyMuPDF | https://github.com/pymupdf/PyMuPDF · https://pymupdf.readthedocs.io/ |
| Marker | https://github.com/datalab-to/marker (**moved from `VikParuchuri/marker`**) |
| Surya | https://github.com/datalab-to/surya (**moved from `VikParuchuri/surya`**) |
| Docling | https://github.com/docling-project/docling |
| MinerU | https://github.com/opendatalab/MinerU |
| Unstructured | https://github.com/Unstructured-IO/unstructured |
| deepdoctection | https://github.com/deepdoctection/deepdoctection |
| docTR | https://github.com/mindee/doctr |
| GROBID | https://github.com/grobidOrg/grobid (**moved from `kermitt2/grobid`; 2.08 GB — never tarball**) |
| Tesseract | https://github.com/tesseract-ocr/tesseract |
| RAPTOR | https://github.com/parthsarthi03/raptor |
| RAGFlow | https://github.com/infiniflow/ragflow |

## 5. Adoption steps

1. **Build the page map first**, before any question answering: page number → byte range → heading path →
   sha256 of the extracted text. Store it in the workstream-01 spine.
2. **Extract twice** (`pypdf` for structure, `pdfminer.six` for layout) and record disagreements per page.
   A disagreement is a flag, not a choice.
3. **Classify every page**: `extracted`, `image-only`, `failed`, `hash-mismatched`, `disagreement`. Publish
   the coverage report alongside every score, forever.
4. **Extract tables separately** with `camelot`, and have a human verify cell by cell before any parameter
   is read from a table. Record who verified what and when.
5. **Index heading paths**, not just page numbers, so a citation can say "§4.2(b), page 37 of version 2.1"
   and survive a re-pagination.
6. **Implement reopen-and-verify**: any emitted answer must re-read its cited page from the stored text,
   confirm the quote is present, and record the check outcome. An answer that cannot be re-read is not
   emitted.
7. **Route summaries to location only.** A hierarchical summary (document → chapter → page, the RAPTOR tree
   idea) narrows the search; the answer's evidence is always the reopened page. Summaries are stored as
   hypotheses (workstream 06).
8. **Handle version differences**: two document versions are two sources with validity intervals, not a
   contradiction (workstream 04's eighth confusion).
9. **Defer OCR** until the coverage report shows image-only pages that matter; then treat weights download
   as an approval gate.

## 6. Resource implications

All **estimates from documentation**; none measured on the target machine.

| Item | Expectation | Note |
|---|---|---|
| `pypdf` | Pure Python; a whole-document object model can be RAM-heavy on a large PDF | Read page by page; do not hold the document object for the whole run |
| `pdfminer.six` | Pure Python; layout analysis (`LAParams`) is **slower** than `pypdf` | Budget CPU time; it is the accuracy leg of the pair |
| `camelot` | Pure Python plus **ghostscript** for the lattice parser | A native binary dependency — check availability before committing |
| `markitdown` | Light; conversion cost proportional to document size | The open question is provenance survival, not cost |
| `PyMuPDF` | C extension; fast; low RAM per page | The licence, not the footprint, is the blocker |
| `Docling` | Model downloads for layout/TableFormer; RAM in the hundreds of MB | Documented estimate; weights are an approval gate |
| `Marker` / `Surya` | GPU recommended; per-model downloads | Weights under modified OpenRAIL-M |
| `MinerU` | GPU strongly recommended; multi-GB model downloads | Not a laptop option |
| `GROBID` | JVM service, several hundred MB heap | Rejected on footprint |
| `RAPTOR` tree build | **LLM-call heavy** at build time; embeddings per tree level at query time | Build cost is the reason to use a simple 3-level tree instead |
| `Tesseract` | Native binary; CPU; per-page cost | Language data is a separate download |

## 7. Qualification requirements

1. A coverage report exists for every document: pages total / extracted / image-only / failed /
   hash-mismatched / disagreement, and it is published **next to** every accuracy number.
2. 100% of emitted answers resolve to a page whose stored text hash matches the source of record.
3. Reopen-and-verify is demonstrably active: removing it changes a measured outcome, or it is ceremony.
4. Extractor disagreement is detected and flagged on a planted test case.
5. A table with a deliberately dropped row is detected, not silently accepted.
6. An image-only page produces the `image-only` state, never an empty string and never a guess.
7. Peak RSS stays within the workstream-01 ceiling across a full 147-page run, measured out-of-process.
8. Chapter navigation by heading path survives a re-pagination test (same content, different page breaks).
9. Extraction quality is reported **separately from** comprehension quality. A high extraction score with a
   low comprehension score is the expected starting state, and it is the finding — not a failure of this
   workstream.

Public long-context benchmarks are **not** qualification evidence for this workstream. See
[BENCHMARK_NOTES.md](../../resources/benchmark-descriptions/BENCHMARK_NOTES.md).

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| PyMuPDF as a dependency | AGPL-3.0 or commercial; copyleft reaches a networked service |
| Marker / Surya / Docling / MinerU weights | Weight licences (modified OpenRAIL-M, additional terms) plus GPU and multi-GB downloads; approval gate |
| GROBID | JVM service footprint; oriented to scholarly PDFs |
| RAGFlow | Multi-container stack |
| LlamaIndex / LangChain / Haystack / txtai as the reading stack | Would **replace** existing components rather than complement them (contradicts R5). At most one, ever, and none is needed |
| RAPTOR as a dependency | Unmaintained since 2024-09-03; Faiss + clustering stack for a three-level tree |
| GraphRAG / LightRAG for document navigation | Index build is LLM-call heavy; community summaries are model-written hypotheses that must never be cited as facts |
| Single-extractor pipelines | Requirement 3.6 exists precisely because one extractor's silent error is undetectable |
| Treating extraction coverage as comprehension | The central error this workstream is designed to prevent |
| Copying arXiv PDFs found inside permissive repositories | The paper's licence applies, not the repository's |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **The document classes SAM-X must actually read are not stated anywhere** | The entire extraction and evaluation design | Ask: broker specifications? research reports? regulatory filings? vendor manuals? Scanned or born-digital? |
| Whether the two indexed documents are born-digital or scanned (Q4/Q5) | Whether OCR is needed at all | Inspect the existing prototype's coverage report, if it has one |
| Rights to store, index and quote the documents (Q4) | Whether any of this may be built | Question for the user |
| `ghostscript` availability for `camelot`'s lattice parser | Table extraction | Check at install time; the stream parser is a fallback with lower accuracy on ruled tables |
| Whether `markitdown` preserves page provenance | Requirement 3.1 | One bounded test on a known document — the pre-declared rejection criterion in its catalog row |
| Whether `pypdf` + `pdfminer.six` disagreement rates are usable as a signal or are mostly noise | Requirement 3.6 | Measure the disagreement rate on the existing corpus; if it is uniformly high, the signal needs refining |
| Heading-path stability across the actual document versions in use | Requirement 3.7 | A re-pagination test on real version pairs |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
