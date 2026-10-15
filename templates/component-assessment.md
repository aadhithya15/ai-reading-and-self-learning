# COMPONENT ASSESSMENT — <component id>

> One of these per component. The filled-in versions live as rows in
> [RESOURCE_CATALOG.csv](../RESOURCE_CATALOG.csv); this template is the long-form shape, for a component
> that needs more room than a CSV cell, or for a component you are adding.
>
> All **15 points** are mandatory. If you cannot answer one, write `UNKNOWN — <what would be needed to find
> out>`. Do not leave it blank and do not guess.
>
> Evidence discipline used throughout this collection:
> * **measured** — you observed it on a real machine, with an instrument, and can show the trace
> * **verified** — you confirmed it against an authoritative source (licence text, official docs, an API
>   response) and can cite it
> * **inspected** — you read the code or document and can point at the file
> * **estimate** — derived from documentation or reasoning; not observed
> * **reported** — someone else's claim, including the vendor's own
> * **proposed** — a design nobody has built or tested
> * **unknown** — the honest default
>
> Star counts, README claims and published benchmark gains are **leads**. They are not proof, and they are
> not evidence of a gain for SAM-X.

---

## 1. Identity and links

| Field | Value |
|---|---|
| Stable component id | `<lowercase-hyphenated, unique across the catalog>` |
| Display name | `<...>` |
| Official URL | `<project homepage or repository>` |
| Upstream repository | `<owner/name>` |
| Pinned commit / release | `<full sha or tag>` — **never** "latest" or a branch name |
| Package registry entry | `<PyPI / npm / crates.io name, or n/a>` |
| Workstreams | `<comma-separated ids from workstreams/>` |
| Type | `library` \| `tool` \| `service` \| `model` \| `dataset` \| `benchmark` \| `documentation` \| `paper` \| `specification` \| `reference-implementation` |
| Local paths (if bundled) | `<relative paths, or "NOT BUNDLED">` |
| Catalog row | `<id>` · manifest asset ids `<A0000…>` |

## 2. The specific SAM-X problem it addresses

Not "it does retrieval". Which objective, which reported position, which failure mode?

> `<...>`

Objectives are numbered in [PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md) §1. Reported positions R1–R5 are in
§3. If you cannot tie the component to one of them, it probably does not belong in the collection.

## 3. Kind of thing

`working code` \| `prototype` \| `documentation` \| `service` \| `link collection` \| `reference
implementation (not maintained as a library)`

Justify the label: `<what makes it that and not something stronger>`

## 4. Relevant files or document sections

Name the specific files or sections that matter — not the whole repository.

| Path or section | Why it matters | Bundled? |
|---|---|---|
| `<...>` | `<...>` | yes / no |

## 5. What was inspected or tested

| Activity | Extent | Result |
|---|---|---|
| Read licence text | `<which file, which lines>` | `<...>` |
| Read source | `<which files, how much>` | `<...>` |
| Read documentation | `<which pages>` | `<...>` |
| Executed | **no** (prohibited by this engagement) | n/a |
| Installed | **no** (prohibited) | n/a |
| Measured resource use | **no** | `UNKNOWN` |

Anything not done is recorded as not done. Never describe an untested component as installed, compatible
or proven.

## 6. Version pinning

| Field | Value |
|---|---|
| Pinned commit SHA | `<...>` |
| Upstream default branch at check time | `<...>` |
| Latest release at check time | `<tag or "none">` |
| HEAD commit date | `<YYYY-MM-DD>` |
| Checked date | `<YYYY-MM-DD>` — the date **you** actually checked |

## 7. Licence and restrictions

| Field | Value |
|---|---|
| Licence (as read from the text) | `<SPDX id or full name>` |
| Licence evidence | `<path to the bundled licence text, or the URL you read>` |
| Detector said | `<GitHub/PyPI SPDX detection>` — and whether you overrode it, and why |
| Commercial-use restrictions | `<none found / Commons Clause / non-production / paid tier / UNKNOWN>` |
| **Model-weight restrictions** | `<separate from code! e.g. modified OpenRAIL-M, Llama community licence, n/a>` |
| Copyleft reach | `<does it touch a networked service? is it a link-time or runtime dependency?>` |
| Redistribution status | `permitted` \| `permitted-with-copyleft-notice` \| `permitted-with-additional-terms` \| `permitted-scoped` \| `permitted-no-sell` \| `permitted-non-production-only` \| `permitted-cc-by` \| `permitted-cc-by-sa` \| `permitted-except-enterprise-dir` \| `permitted-registry-metadata` \| `review-required` \| `not-permitted` |
| Attribution required | `<exact notice text or "see ATTRIBUTION.md">` |
| Decision | `bundle` \| `bundle-reference-only` \| `metadata-only` \| `do-not-use` |

If the licence is unclear or absent: **do not bundle**. Create a metadata-only entry with the official
link, access requirements and the reason.

## 8. Maintenance status

| Field | Value |
|---|---|
| Last upstream push | `<YYYY-MM-DD>` |
| Archived upstream? | yes / no |
| Ownership or organisation changed? | `<e.g. iterative/dvc → treeverse/dvc>` — treat as a supply-chain signal |
| Release cadence | `<...>` |
| Open-issue signal | `<...>` |
| Verdict | `actively maintained` \| `dormant but usable as reference` \| `archived` \| `unmaintained — do not depend on` |

## 9. Dependencies and OS support

| Field | Value |
|---|---|
| Runtime dependencies | `<name + version constraints>` |
| Native / compiled components | `<yes/no — which, and what they need to build>` |
| Python / language versions | `<...>` |
| OS support | `<Linux / macOS / Windows — verified how?>` |
| Conflicts with existing SAM-X dependencies | `<UNKNOWN until an inventory exists>` |

## 10. Documented resource needs

Every figure here is an **estimate from documentation** until someone measures it on the target machine.

| Resource | Documented value | Source of the figure | Measured on target? |
|---|---|---|---|
| RAM (resident) | `<...>` | `<doc path or URL>` | **no** |
| VRAM | `<...>` | `<...>` | **no** |
| CPU | `<...>` | `<...>` | **no** |
| Disk | `<...>` | `<...>` | **no** |
| Network | `<egress required? to which hosts? bandwidth?>` | `<...>` | **no** |
| Startup overhead | `<...>` | `<...>` | **no** |
| Idle/resident cost when daemonised | `<...>` | `<...>` | **no** |

Distinguish **application RAM** from **system RAM** from **VRAM** from **disk**, and say whether an
`mmap`-backed structure is being counted in process RSS or in the OS page cache.

## 11. Costs, quotas and privacy

| Field | Value |
|---|---|
| Licence cost | `<none / paid tier / enterprise edition>` |
| Hosted-service cost | `<n/a / pricing page URL + the date you read it>` |
| Free tier | `<terms, and the date checked — never assume it is unlimited or permanent>` |
| Rate limits / quotas | `<...>` |
| Data sent off-box | `<none / what exactly / UNKNOWN>` |
| Telemetry | `<on by default? opt-out? what is sent?>` |
| Privacy or compliance constraints | `<...>` |

## 12. Limitations, unresolved issues, failed reproductions

| Item | Evidence label |
|---|---|
| `<limitation 1>` | `<measured / verified / inspected / estimate / reported>` |
| `<unresolved issue>` | `<...>` |
| `<something you tried to reproduce and could not>` | `<...>` |

Include the things that make the component *look* worse than its README claims. If you found none, say so
explicitly rather than leaving the section empty.

## 13. Complements or replaces

| Field | Value |
|---|---|
| Relationship to existing SAM-X components | `complements` \| `extends` \| `replaces` \| `overlaps-with` |
| Which components it overlaps | `<catalog ids>` |
| **Do-not-install-together group** | `<group name from HANDOFF_FOR_NEXT_AI.md §7>` |
| Integration difficulty | `low` \| `medium` \| `high` — and why |
| Conservative fallback | `<what you do if this component fails, is unavailable, or is rejected by its experiment>` |
| Reversibility | `<can it be removed cleanly? what state does it leave behind?>` |

Reported position R5 says compatible existing components should be reused. If this component **replaces**
rather than complements, that is a decision for the user, not a default.

## 14. Bounded experiment

A single experiment that could **demonstrate a benefit or reject the component**. Copy the shape from
[experiment-contract.md](experiment-contract.md); summarise it here.

| Field | Value |
|---|---|
| Hypothesis (falsifiable) | `<...>` |
| Unchanged baseline | `<...>` |
| Independent variable | `<the one thing that differs>` |
| Items and sources | `<counts; held-out status; rights confirmed?>` |
| Primary measurement | `<...>` |
| Resource measurement | `<peak RSS/PSS, p95 latency, tokens, cost>` |
| Negative cases | `<at least: missing information, partial constraint, contradiction, stale source, resource failure>` |
| Pre-declared acceptance | `<...>` |
| Pre-declared rejection | `<...>` |
| Effort bound | `<≤ 1 day / ≤ 1 week>` |
| Reversibility | `<...>` |

## 15. Classification and priority

| Field | Value |
|---|---|
| Classification | `trial-ready` \| `needs-more-evidence` \| `rejected` |
| Justification for the classification | `<one or two sentences naming the deciding factor>` |
| Priority | `P1` (start here) \| `P2` (valuable, sequenced later) \| `P3` (catalogued for completeness or rejected) |
| What would upgrade it to `trial-ready` | `<the specific evidence needed>` |
| What would make it `rejected` | `<the specific finding that would settle it>` |

`trial-ready` means: licence verified, pinned, inspected, no authorisation gate, no server, no weights, and
a bounded experiment written down. It does **not** mean "proven to help SAM-X". Nothing in this collection
is proven to help SAM-X.

---

## Provenance of this assessment

| Field | Value |
|---|---|
| Assessed by | `<name/agent>` |
| Assessment date | `<YYYY-MM-DD>` |
| Sources consulted | `<list, with access dates>` |
| What was **not** consulted | `<paywalled material, unreachable hosts, documentation you did not read>` |
| Re-verify before adoption? | yes — licences, `pushed_at`, `archived` and HEAD SHA all move |
