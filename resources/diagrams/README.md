# DIAGRAMS

Four original SVG diagrams authored for this collection. They contain **no upstream material** — no copied
figures, no model weights, no dataset content — and they are not listed in
[ASSET_MANIFEST.json](../../ASSET_MANIFEST.json) because they were not downloaded from anywhere.

> **Every diagram depicts a PROPOSED design.** Nothing in them was built, executed or measured during the
> build of this collection. Resource figures shown or implied are **estimates from documentation**, never
> measurements on the target machine. Read them as architecture intentions to be tested, not as descriptions
> of a working system.

| # | File | What it shows | Workstreams |
|---|---|---|---|
| 1 | [01-bounded-memory-reading-pipeline.svg](01-bounded-memory-reading-pipeline.svg) | The end-to-end reading path: sandboxed ingest → dual-extractor extraction → page map → bounded-memory spine → locate/retrieve/reopen → evidence gate → typed answer, with the memory stores and the out-of-process resource trace attached | 01, 02, 03, 04, 05, 06, 14 |
| 2 | [02-four-store-memory.svg](02-four-store-memory.svg) | The four stores (`facts`, `procedures`, `lessons`, `hypotheses`) with their **write authority**, the temporal-validity columns, contradiction handling, the query log, and poisoning containment | 06, 07, 14 |
| 3 | [03-evidence-gate-and-abstention.svg](03-evidence-gate-and-abstention.svg) | The three gates and the **four labelled abstention outcomes**, plus the other conditions that require abstention and how abstention is scored | 04, 05, 08 |
| 4 | [04-frozen-evaluation-protocol.svg](04-frozen-evaluation-protocol.svg) | The frozen evaluation protocol end to end, with the two **leakage barriers** drawn explicitly and the immutable run record's contents | 08, 03, 04, 07 |

## Reading order

If you read one, read **diagram 1** — it is the shape of the whole proposal. Then **diagram 3**, because the
evidence gate and the four abstention labels are the part most often omitted and the part the objective
explicitly demands. **Diagram 2** is the change with the highest leverage and the highest migration risk.
**Diagram 4** is what makes any of the others verifiable.

## Conventions used

* **Red** — a trust boundary, a hard stop, or a refusal path.
* **Green** — storage, or a bounded resource with an enforced ceiling.
* **Blue** — document handling.
* **Yellow** — retrieval, or a decision that is pre-declared rather than discovered.
* **Purple** — the typed output contract.
* **Grey** — measurement and record-keeping.

Arrows follow data flow. Red arrows are refusals and rejections; green arrows are storage reads and writes.

## Correspondence to the text

| Diagram element | Where it is specified |
|---|---|
| Bounded-memory spine, ceiling, spill/degrade/refuse | [TOP_RECOMMENDATIONS.md](../../TOP_RECOMMENDATIONS.md) Rank 1 · [workstreams/01-low-ram](../../workstreams/01-low-ram/README.md) |
| Page map, dual extraction, coverage states | [workstreams/03-document-reading](../../workstreams/03-document-reading/README.md) |
| Lexical-first retrieval, reopen-and-verify | [TOP_RECOMMENDATIONS.md](../../TOP_RECOMMENDATIONS.md) Rank 5 |
| Four stores and write authority | [TOP_RECOMMENDATIONS.md](../../TOP_RECOMMENDATIONS.md) Rank 3 · [workstreams/06-memory](../../workstreams/06-memory/README.md) |
| Typed contract and the four field states | [workstreams/04-semantic-interpretation](../../workstreams/04-semantic-interpretation/README.md) |
| Evidence gate, abstention labels, attempted denominator | [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §4–§5 |
| Freeze, barriers, immutable run record | [EVALUATION_PLAN.md](../../EVALUATION_PLAN.md) §6–§7 · [templates/experiment-contract.md](../../templates/experiment-contract.md) |
| Structural containment (no order-placing tool on the reading path) | [workstreams/14-security-isolation](../../workstreams/14-security-isolation/README.md) requirement 14.4 |

## Editing these diagrams

They are hand-authored SVG with a small amount of structure: rectangles, text and arrow markers, no
embedded scripts, no external references, no fonts beyond a generic sans-serif stack. They are safe to open
in any viewer and safe to edit as text.

If you change a design, change the diagram **and** the corresponding workstream README in the same commit —
a diagram that disagrees with the text is worse than no diagram.
