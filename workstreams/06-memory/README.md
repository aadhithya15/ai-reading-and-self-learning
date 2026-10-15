# Workstream 06 — Memory: Separated Stores, Provenance and Temporal Validity

**Objectives served:** keep separate stores for source-linked facts, reusable procedures, independently
reviewed lessons and unverified hypotheses; demonstrate retention; handle stale and conflicting information
safely; navigate with bounded memory.

**The central finding of this workstream** (`inspected`, across every memory component in the collection):
the tools solve *storage and consolidation*. Almost none of them enforce **write authority** — which store
may be written by whom, and what makes a claim a fact. That is an architectural decision SAM-X must make
itself, and it is why the recommendation here is a schema-and-write-path change rather than a dependency.

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 6.1 | **Four physically separate stores**: `facts`, `procedures`, `lessons`, `hypotheses` | Objective 6, verbatim |
| 6.2 | **Write authority enforced in code**: only code that has re-read a source may write to `facts` | The failure is not schema shape, it is who may write |
| 6.3 | **All summaries live in `hypotheses`** and may never appear in an answer's `evidence` field | Objective 3 |
| 6.4 | Every fact carries: claim, exact quote, source id, page, document version, hash, retrieval timestamp | Without all seven it is not a source-linked fact |
| 6.5 | **Temporal validity**: `valid_from`, `valid_to`, `superseded_by`, `invalidated_reason` | "What did we believe at time T?" must stay answerable |
| 6.6 | Stale facts are **closed with an interval, never deleted** | Deletion destroys the audit trail |
| 6.7 | Contradictions **flagged, never merged or silently resolved** | Merging is how a real contradiction becomes a wrong value |
| 6.8 | Retrieval failure distinguishable from non-existence, via a query log with outcomes | Requirement 5.5 depends on it |
| 6.9 | Bounded memory: paging between a working set and the store, with triggers | Objective 2 |
| 6.10 | Memory writes may **never** alter trading, risk, approval, holding or open-position parameters | Retrieval poisoning is a verified threat — see §2.4 |

**Not a goal.** Zero forgetting. Saving bytes is not learning, and a smaller store is not a better one.
Retention is measured by re-asking, not by size.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: four stores in SQL, with temporal validity columns

```
facts         (fact_id, claim, quote, source_id, page, doc_version, source_sha256,
               retrieved_at, valid_from, valid_to, superseded_by, invalidated_reason)
              -- WRITE AUTHORITY: verified-source code path only. Never model-written.

procedures    (procedure_id, name, preconditions, steps, validation, scope_shown_to_work,
               evaluation_id, valid_from, valid_to)
              -- Declarative recipes. NOT arbitrary executable code.

lessons       (lesson_id, statement, evidence_ids, reviewer, review_kind, review_ref,
               accepted_at, valid_from, valid_to)
              -- Acceptance requires an EXTERNAL verifier. Self-critique may propose, never accept.

hypotheses    (hypothesis_id, statement, origin, generated_at, status, promoted_to, rejected_because)
              -- Everything model-generated and unconfirmed. ALL SUMMARIES LIVE HERE.
```

Plus a `memory_queries` log (query, store, outcome ∈ {found, not_found, retrieval_error}, latency) so
requirement 6.8 is a query, not a hope.

Storage: the workstream-01 spine (`sqlitedict` / SQLite, `diskcache` spill). Paging triggers borrowed from
MemGPT's architecture. Validity intervals borrowed from Graphiti's bi-temporal model — **as SQL columns, not
as a graph database**.

### 2.2 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| One table with a `type` column | **Rejected** | The property that matters is write authority, which a column does not enforce and cannot be audited |
| `mem0` | Schema catalogued, not adopted | Library mode can be light, but extraction needs a vector store **and** an LLM, and the platform option moves data off-box. Vendor accuracy claims are **reported**, not reproduced |
| `cognee` | Schema catalogued, not adopted | Graph + vector stores, pluggable; consolidation rewrites records |
| `MemOS` | Vocabulary catalogued, not adopted | A useful taxonomy of memory types; the framework depends on backends this project does not want |
| `A-MEM` | Pattern noted, not adopted | LLM-driven linking between memories — linking is consolidation by another name |
| `MemoryBank` | Concept noted, not adopted | Its Ebbinghaus-curve forgetting schedule is interesting and **wrong here**: an auditable research store must not decay facts on a timer. Dormant since 2023-05 |
| `Letta` / MemGPT server | **Architecture adopted, server not** | Main context / external context / explicit paging triggers is exactly right (arXiv:2310.08560v2, **verified**). The server needs a process plus Postgres. `letta-ai/letta`'s tree held only 12 files at the pinned commit — the SDK/server split had moved |
| `Graphiti` + Neo4j | **Pattern adopted, database not** | Bi-temporal edges are the right model; a graph process is not justified when three columns deliver it. Apache-2.0 core code bundled |
| `Zep` (OSS server) | **Rejected** | Server + database. Its paper (arXiv:2501.13956v1, **verified**) reports beating MemGPT on DMR — a **reported** result on someone else's benchmark |
| `GraphRAG` / `LightRAG` as memory | **Not adopted** | Community summaries are model-written hypotheses; index builds are LLM-call heavy |
| `RAPTOR` tree as the summary store | **Pattern adopted** | Its hierarchical summaries are exactly what belongs in `hypotheses` — provided they stay there |
| `Chroma` / `LanceDB` for the memory backend | Not needed | The spine already provides storage; adding a vector format adds a dependency |
| LLM-driven consolidation of any kind | **Rejected** | The single most dangerous feature in this category for an auditable system |

### 2.3 Procedures and lessons: the two stores people conflate

* A **procedure** is a declarative recipe: preconditions, ordered steps, validation, and the *scope in which
  it was shown to work*. It is not executable code, and a procedure whose preconditions are unmet must
  refuse to run. The Voyager skill-library pattern (MIT, code bundled) is the reference — with the caveat
  that its transfer result is in a Minecraft environment and is an **analogy, not evidence** for document
  reading.
* A **lesson** is a statement accepted only after **independent** review: a human, a frozen key, or a
  verifiable external signal such as an execution result. Reflexion (MIT, code bundled; arXiv:2303.11366v4
  reported 91% pass@1 on HumanEval versus GPT-4's 80%) and Self-Refine (arXiv:2303.17651v2, ~20% average
  absolute improvement on GPT-3.5/4-era models) both demonstrate gains **in environments with ground-truth
  feedback**. Neither demonstrates that a model's own critique is supervision. ACE's itemised, append-only
  playbook growth (Apache-2.0) is adopted as a *pattern* because it avoids whole-context rewrites; its
  published gains are the authors' and are not reproduced here.

The relevant negative literature — that LLMs cannot reliably self-correct reasoning without external
feedback — was **not re-verified in this session** and its identifier is labelled unverified in
[PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md). The design rule above does not depend on it.

### 2.4 Memory is an attack surface

Verified threat evidence, all metadata-only (paper PDFs are not redistributable):

* **PoisonedRAG** (arXiv:2402.07867v3, USENIX Security 2025) — five injected texts achieved ~90% attack
  success over a corpus of millions, and the defenses it evaluated were reported insufficient.
* **InjecAgent** (arXiv:2403.02691v3, ACL 2024 Findings) — 1 054 test cases; a ReAct-prompted GPT-4 was
  vulnerable in 24% of them, roughly doubling with a "hacking" prompt.
* **Greshake et al.** (arXiv:2302.12173v2) — indirect prompt injection through retrieved content.
* **AgentDojo** (arXiv:2406.13352v3) — 97 tasks and 629 security tests; state-of-the-art LLMs fail many even
  unattacked.

Consequence, encoded as requirement 6.10: every memory write carries provenance, writes from retrieved
content are quarantined as hypotheses until reviewed, and **no memory write may alter a risk, holding or
approval parameter**. See [workstream 14](../14-security-isolation/README.md).

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `sqlitedict` (Apache-2.0) | [documentation](../../resources/documentation/sqlitedict/) · [code examples](../../resources/code-examples/sqlitedict/) · [licence](../../resources/licenses/sqlitedict/) |
| `diskcache` (Apache-2.0) | [documentation](../../resources/documentation/diskcache/) · [code examples](../../resources/code-examples/diskcache/) · [licence](../../resources/licenses/diskcache/) |
| `sqlite-vec` (MIT/Apache-2.0) | [documentation](../../resources/documentation/sqlite-vec/) · [examples](../../resources/configurations/sqlite-vec/) · [licences](../../resources/licenses/sqlite-vec/) |
| `graphiti` (Apache-2.0) | [documentation](../../resources/documentation/graphiti/) · [core code](../../resources/code-examples/graphiti/) — node and edge models, error handling · [licence](../../resources/licenses/graphiti/) |
| `letta` (Apache-2.0) | [documentation](../../resources/documentation/letta/) — README, CONTRIBUTING, SECURITY · [licence](../../resources/licenses/letta/) |
| `raptor` (MIT) | [full implementation](../../resources/code-examples/raptor/) · [documentation](../../resources/documentation/raptor/) |
| `voyager` (MIT) | [documentation](../../resources/documentation/voyager/) · [code examples](../../resources/code-examples/voyager/) · [licence](../../resources/licenses/voyager/) — dormant since 2024-04 |
| `reflexion` (MIT) | [documentation](../../resources/documentation/reflexion/) · [code examples](../../resources/code-examples/reflexion/) · [licence](../../resources/licenses/reflexion/) — dormant since 2025-01 |
| `ace` (Apache-2.0) | [documentation](../../resources/documentation/ace/) · [licence](../../resources/licenses/ace/) (**slug corrected from `ShengranHu/ACE` to `ace-agent/ace`**) |
| `a-mem` (MIT) | [documentation](../../resources/documentation/a-mem/) · [licence](../../resources/licenses/a-mem/) |
| `memorybank` (MIT) | [documentation](../../resources/documentation/memorybank/) · [licence](../../resources/licenses/memorybank/) — dormant since 2023-05 |
| `expel` (Apache-2.0) | [documentation](../../resources/documentation/expel/) · [licence](../../resources/licenses/expel/) — **upstream `LeapLabTHU/ExpeL` has no licence file; only what the licence permitted was kept** |
| `mem0`, `cognee`, `memos` | [mem0](../../resources/documentation/mem0/) · [cognee](../../resources/documentation/cognee/) (licence + NOTICE) · [MemOS](../../resources/documentation/memos/) |
| `zep` (Apache-2.0) | [documentation](../../resources/documentation/zep/) · [licence](../../resources/licenses/zep/) — **rejected as a server** |
| `graphrag`, `lightrag` | [GraphRAG](../../resources/documentation/graphrag/) · [LightRAG](../../resources/documentation/lightrag/) |
| `llama_index`, `chromadb` | [LlamaIndex](../../resources/documentation/llama_index/) · registry metadata for Chroma |
| `nuster-survey` | **Not bundled** — metadata-only row for the LLM-agent memory survey (arXiv:2404.13501v1, 39 pp, **verified**), whose evaluation dimensions are adopted in §7 |
| `prompt-injection-refs` | **Not bundled** — metadata-only row; the four verified papers in §2.4 |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) — MemGPT, Zep, memory survey, Generative Agents, Voyager, Reflexion |

## 4. Official upstream references

| Component | Upstream |
|---|---|
| sqlitedict | https://github.com/piskvorky/sqlitedict |
| DiskCache | https://github.com/grantjenks/python-diskcache (**corrected from `grantjenks/free-diskcache`**) |
| sqlite-vec | https://github.com/asg017/sqlite-vec |
| Graphiti | https://github.com/getzep/graphiti · arXiv:2501.13956v1 (**verified**) |
| Letta / MemGPT | https://github.com/letta-ai/letta · arXiv:2310.08560v2 (**verified**) |
| Zep | https://github.com/getzep/zep |
| RAPTOR | https://github.com/parthsarthi03/raptor |
| Voyager | https://github.com/MineDojo/Voyager · arXiv:2305.16291v2 (**verified**) |
| Reflexion | https://github.com/noahshinn/reflexion · arXiv:2303.11366v4 (**verified**) |
| ACE | https://github.com/ace-agent/ace |
| A-MEM | https://github.com/agiresearch/A-mem |
| MemoryBank | https://github.com/zhongwanjun/MemoryBank-SiliconFriend · arXiv:2305.10250v3 (**verified**) |
| ExpeL | https://github.com/LeapLabTHU/ExpeL (**slug did not resolve via the API on 2026-10-14; no upstream licence**) |
| mem0 | https://github.com/mem0ai/mem0 |
| cognee | https://github.com/topoteretes/cognee |
| MemOS | https://github.com/MemTensor/MemOS |
| Memory survey | arXiv:2404.13501v1 (**verified**, 39 pp) |
| Generative Agents | arXiv:2304.03442v2 (**verified**) |

## 5. Adoption steps

1. **Create the four stores as separate tables in separate files** (or one file with strict write paths —
   separate files make the authority boundary enforceable at the filesystem level).
2. **Implement write authority first**, before migrating anything: a single code path may write to `facts`,
   and it must have re-read the source and hold quote + page + doc version + hash. Add a test that attempts
   a model-written fact and **must fail**.
3. **Add the validity columns** (`valid_from`, `valid_to`, `superseded_by`, `invalidated_reason`) to all
   four stores.
4. **Route every existing summary into `hypotheses`.** Add the hard rule: a hypothesis may not appear in an
   answer's `evidence` field.
5. **Migrate new writes only.** Existing memory becomes read-only legacy with `provenance: UNKNOWN` recorded
   honestly. Do not rewrite history to make it look clean.
6. **Add the contradiction path**: on conflict, write both, flag the pair, and never merge. Two facts from
   two document versions with non-overlapping validity are *not* a contradiction (workstream 04, C8).
7. **Add the query log** with outcomes `found` / `not_found` / `retrieval_error`.
8. **Add paging triggers** (MemGPT pattern): what enters the working set, what is evicted, and what is
   logged when the ceiling is hit.
9. **Quarantine writes derived from retrieved content** as hypotheses until reviewed, per §2.4.
10. **Add the lesson gate**: `review_kind ∈ {human, frozen_key, external_signal}` with a reference. A lesson
    without one cannot be inserted.

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| Four SQL stores | Negligible resident cost; disk-bound | The spine already provides the engine |
| Validity columns | A few bytes per record; one extra index | Interval queries are cheap with an index on `(valid_from, valid_to)` |
| Query log | Grows without bound | Rotate or summarise it — but never delete a fact's provenance |
| Paging / working set | Bounded by the workstream-01 ceiling | Eviction must be logged |
| `Letta` server | Process + Postgres | Rejected on footprint |
| `Zep` server | Process + database | Rejected on footprint |
| `Graphiti` + Neo4j | JVM-free but a graph process | Rejected on footprint |
| `mem0` extraction | Vector store + LLM calls per write | Cost per write, not just per read |
| `MemoryBank` decay | LLM calls dominate | Rejected on principle, not cost |

## 7. Qualification requirements

The evaluation dimensions below are adapted from the memory survey (arXiv:2404.13501v1, **verified**
metadata) and from [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §4.

1. **Zero facts without a resolvable quote + page + document version + hash.** An audit query returns the
   count; the count must be 0.
2. **No code path allows a model-generated string into `facts`** — verified by inspection *and* by a test
   that attempts it and must fail.
3. 10 planted contradictions → **10 flags, 0 silent merges**.
4. 10 stale-source items → a query at time T returns the then-current fact, and the superseded fact is still
   retrievable with its interval and reason.
5. Scope/version differences are **not** flagged as contradictions (the inverse of item 3).
6. Retrieval failure is reported distinctly from non-existence, verified by planting a fact that exists but
   is not findable by the query used.
7. **Retention**: 20 items re-asked after 5 unrelated sessions, with no decay beyond a pre-declared
   tolerance.
8. **Transfer**: the same procedures applied to a third document class, with no collapse.
9. Missing information recorded as "not specified", never guessed; partial constraints recorded as partial.
10. Store sizes, peak RSS and paging-event counts reported with the scores.
11. Every accepted lesson names its `review_kind` and reference; a lesson without one cannot exist.
12. No memory write can alter a trading, risk, approval, holding or open-position parameter — verified by
    inspection and by a test that attempts it and must fail.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| LLM-driven consolidation (mem0, cognee, A-MEM, MemOS, MemoryBank decay) | Rewriting or decaying records is precisely what an auditable research store must not do |
| Graph database (Neo4j via Graphiti, Zep server) | Footprint; validity intervals need three columns, not a graph engine |
| Letta/MemGPT server | Architecture adopted, server rejected |
| Single table with a `type` column | Cannot enforce or audit write authority |
| Deleting stale facts | Destroys "what did we believe at time T?" |
| Merging contradictions | Converts a real contradiction into a silent wrong value |
| Treating self-critique as supervision | Reflexion/Self-Refine/ACE gains come from environments with ground-truth feedback; a model judging itself is not independent |
| Voyager's transfer result as evidence for document reading | Different environment entirely; an analogy at most |
| Zep's DMR result as evidence | **Reported** by the vendor on their own benchmark; not reproduced here |
| Claiming retention from a smaller store | Saving bytes is not learning and not zero forgetting |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| What memory SAM-X has today, and whether summaries are already cited as evidence (Q7) | Migration design and urgency | Ask; inspect the existing answer path |
| Whether trading/risk/approval/holding safeguards live in the same database (Q10) | Whether step 1 can use one file or must use separate files | Ask; if shared, use a separate file and do not touch the existing one |
| Whether any existing memory can be migrated with provenance intact | Step 5 | Inspect; if provenance is absent, mark it `UNKNOWN` rather than inventing it |
| Who or what performs independent lesson review | Requirement 6.2's `lessons` gate | A human, a frozen key, or a verifiable external signal — the user must say which is available |
| Retention and transfer thresholds | §7 items 7 and 8 | Must be pre-declared before the first run; inventing them after the fact invalidates the result |
| The ExpeL upstream slug did not resolve and has no licence | Citing or bundling more of it | Re-check upstream; treat as metadata-only until a licence appears |
| The memory-survey companion repository is metadata-only | Its evaluation checklist | Derived from the verified abstract; re-verify against the full text when accessible |
| Nothing here was executed | All measurements | Requires authorisation this engagement did not have |
