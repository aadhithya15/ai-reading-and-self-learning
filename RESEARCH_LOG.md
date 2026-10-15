# RESEARCH LOG

Dated record of how this collection was built: what was searched, what was reached, what failed, what was
decided and why. Written so that a future reader can tell **verified findings** apart from **search leads**
and can repeat or extend the work.

All activity took place on **2026-10-14** (UTC) in a single working session, inside a sandbox whose network
egress is restricted. No prior deliverables existed in the repository: its history contained exactly one
commit (`10bb5f6`, "Fresh start", `README.md` only).

Log-entry types: `search` · `fetch` · `decision` · `failure` · `audit` · `author`.

---

## 1. Search scope and access limitations

### 1.1 What was reachable from the sandbox shell

| Host | Result | Used for |
|---|---|---|
| `github.com` | reachable | licence and file contents |
| `codeload.github.com` | reachable (test fetch: `faiss` v1.7.4 tarball, discarded) | confirming an archive route existed as a fallback |
| `api.github.com` | reachable, authenticated as `aadhithya15` | repository metadata, recursive file trees, pinned file contents, search |
| `pypi.org` | reachable | registry metadata snapshots |
| `files.pythonhosted.org` | reachable | not used (no sdists/wheels downloaded) |
| `registry.npmjs.org` | reachable | not used (no JS components shortlisted) |

### 1.2 What was NOT reachable from the sandbox shell

All failed at the network layer (no HTTP response), on 2026-10-14:

`arxiv.org`, `export.arxiv.org`, `huggingface.co`, `raw.githubusercontent.com`, `docs.python.org`,
`aclanthology.org`, `openreview.net`, `proceedings.mlr.press`, `sqlite.org`, `duckdb.org`,
`llm.datasette.io`.

A separate read-only page-fetch capability reached general web **text** (used for arXiv metadata) but
cannot save binary files and truncates long responses.

### 1.3 Consequences, recorded at the time

* **No paper PDFs could be bundled** — blocked twice over (no binary route; and arXiv's non-exclusive
  distribution licence does not grant third-party redistribution anyway).
* **No Hugging Face model or dataset cards could be bundled** — host unreachable. Recorded as metadata-only
  (MO-03).
* **Vendor documentation sites could not be downloaded** (Stripe idempotency, AWS SQS deduplication,
  Datasette LLM, promptfoo) — recorded as metadata-only patterns (MO-04) rather than silently skipped.
* **Coverage is broad but not exhaustive.** No claim of complete internet coverage is made anywhere in this
  collection, and no browsing result was fabricated.

### 1.4 Search strategy actually used

1. Prior-knowledge shortlist of ~150 upstream projects mapped onto the 14 workstreams (written to
   `repos.txt`, 147 slugs).
2. GitHub REST API resolution of each slug → `repo_meta2.json` (146 attempted, 137 resolved, 9 errors).
3. `gh search repos` sweeps to fill gaps and to find replacements for unresolved slugs (+13 new repos
   resolved, 6 confirmed missing).
4. Recursive `git/trees` at each repository's HEAD SHA → 152 pinned inventories, so individual files could
   be chosen instead of whole repositories.
5. Targeted greps of those inventories for PDFs, licences, config templates, benchmark harnesses and
   reference implementations.
6. File-level download at the pinned commit via the contents API, with blob SHA, size and SHA-256 recorded.
7. PyPI registry metadata snapshot for 126 package names (124 resolved; `vespa-engine` and
   `text-embeddings-inference` 404 → GitHub-only components).
8. arXiv API metadata verification for paper identifiers, in batches of ≤ 6 ids.
9. Licence audit: read every root licence file, plus GitHub's detector output, and override the detector
   where the two disagreed.
10. Authoring: catalog, manifest, plans, templates, diagrams, workstream READMEs, this log.

Search domains covered beyond GitHub: package registries (PyPI), primary papers (arXiv metadata),
official documentation and release notes (as bundled repository docs), issue-tracker signals (via
`pushed_at`/`archived`), public benchmarks (harness code, not data), and vendor/commercial offerings
(catalogued with cost and restriction fields, marked metadata-only where their pages were unreachable).
Discussions, videos and marketing material were treated as **leads only**, never as validation.

---

## 2. Chronological log

### Environment and baseline

* `decision` — Inspected repository history: one commit (`10bb5f6`), one file (`README.md`). **No earlier
  task deliverables existed to remove.** The "preserve a recoverable snapshot then replace superseded work"
  instruction was satisfied by creating `archive/pre-samx-collection` and tag
  `archive/fresh-start-pre-collection` at `10bb5f6` before any new file was written.
* `audit` — Confirmed remote state: `main` only, no tags, no other branches.
* `audit` — Confirmed GitHub authentication works as `aadhithya15` via the sandbox token. **A GitHub PAT was
  pasted into the chat by the user during this engagement. It was not used, not stored, not echoed into any
  file, and not committed.** It must still be revoked by its owner — see [RISKS_AND_UNKNOWNS.md](RISKS_AND_UNKNOWNS.md) D4.
* `fetch` — Measured the sandbox: 3 939 MB RAM (~3 699 MB available), **0 swap**, ~20 GB free disk, 2 CPUs.
  Recorded as *the build machine, not the target machine*.
* `decision` — GitHub storage policy checked before uploading anything: the final bundle is 20.40 MB with a
  10.72 MB largest file, which fits in-repo without Releases or LFS. LFS quotas/costs were therefore not
  needed; the ~100 MB revisit threshold is recorded in [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §8.

### Upstream resolution

* `search` — Wrote `repos.txt` (147 slugs) from the workstream shortlist.
* `failure` — A shell probe script mangled its JSONL output; discarded and rewritten in Python.
* `failure` — A raw-content probe using assumed slugs produced 3 × 404; abandoned that route in favour of
  the authenticated API.
* `fetch` — Python probe → `repo_meta2.json`: 146 attempted, 137 OK, 9 slug errors.
* `search` — `gh search repos` sweeps + a second probe: 13 additional repositories resolved, 6 confirmed
  missing.
* `failure` — `gh search repos --json licenseInfo` → "Unknown JSON field" (available fields: createdAt,
  defaultBranch, description, fullName, stargazersCount, updatedAt). Worked around by fetching licence
  info per repository instead.
* `failure` — `gh api --jq … @tsv` mangles 404 rows into unusable output. Replaced with Python
  `subprocess` + `json.loads` per request.
* `fetch` — Recursive `git/trees` for every resolved repository at its HEAD SHA → `trees/<owner>__<repo>.json`
  (152 pinned inventories). This is what made **file-level** rather than repository-level collection possible.
* `decision` — Never tarball a large repository. Recorded sizes: ccxt 8.67 GB, litellm 2.35 GB, grobid
  2.08 GB, dagster 1.49 GB, gvisor 1.40 GB, ML4T 1.30 GB, great_expectations 253 MB.
* `fetch` — Grepped the ML4T inventory and found `07_defining_the_learning_task/` with five `.py`
  companions — this became the strongest bundled evidence for workstream 09's multiple-testing discipline.
* `decision` — `letta-ai/letta`'s tree contained only 12 files at the pinned commit: the SDK/server split
  had moved. Recorded rather than treated as a collection failure; the MemGPT architecture is adopted from
  the verified paper metadata instead.

### Licence verification (the decisive audit)

* `fetch` — Read the licence head of `needle-in-a-haystack`, `long-form-factuality`, `mlfinlab`, `nomic`,
  `ace-agent/ace`.
* `fetch` — Retrieved `MODEL_LICENSE` heads for `datalab-to/marker` @ `ad1b414` and `datalab-to/surya` @
  `a2363d3` → **"AI PUBS OPEN RAIL-M LICENSE (MODIFIED)" v0.1, 2023-03-02, licenses.ai**. This is the
  finding that separates Marker/Surya *code* (Apache-2.0) from their *weights* (restricted).
* `audit` — GitHub's licence detector returned `NOASSERTION` for several repositories that **do** have
  licences (`needle-in-a-haystack` → MIT, `long-form-factuality` → Apache-2.0 per-directory + MIT for
  `factscore`, `python-diskcache` → Apache-2.0). Rule adopted: **always read the bundled licence text
  before classifying**; never trust the detector alone.
* `decision` — arXiv's default licence is the **arXiv non-exclusive distribution licence**, which does not
  grant third-party redistribution. Therefore: metadata-only for all papers, and **never** bundle an arXiv
  PDF found inside a permissively-licensed repository (it inherits the paper's licence, not the repo's).
  Specifically declined: `docling-project/docling` `tests/data/pdf/sources/2203.01017v2.pdf` (7.22 MB) and
  `2305.03393v1.pdf` (4.32 MB); `Unstructured-IO/unstructured` / `langchain` `layout-parser-paper.pdf`
  (4.69 MB).
* `audit` — Suspicious-content scan of every bundled file: **clean**. No embedded instructions, no
  executable payloads, no credential-shaped strings.
* `audit` — Credential-pattern scan over all new files **and over every revision of the repository's Git
  history**: **zero findings in anything authored for this collection.**
* `audit` — A wider credential-shape sweep (GitHub PAT/OAuth, AWS access key id, PEM private key blocks,
  Slack, Google API key, Stripe live/test, Anthropic, JWT, and credential-shaped assignments) was then run
  over the **whole tree**, which surfaced 11 bundled upstream files containing credential-shaped strings.
  Every one was read and classified:
  * **10 are placeholders** in upstream documentation — `'YOUR_KRAKEN_API_KEY'`,
    `<YOUR_HUGGINGFACEHUB_API_TOKEN>`, `API_KEY = "token-abc123"` (longbench `pred.py`),
    `api_key: "zqt_abcdef..."` (vectara-answer), `password="falkor_password"` (graphiti),
    `api_key='GEMINI_API_KEY'` (google-genai), `'this-will-ordinarily-be-detected-by-a-plugin'`
    (detect-secrets), plus ccxt's Manual and README and two smolagents guides. None is a live credential.
  * **1 contains real-shaped strings**: `resources/configurations/gitleaks/config__gitleaks.toml` carries
    16 Google-API-key-shaped values in its own `[allowlist]` — keys gitleaks publishes so that its own
    examples and test fixtures are not reported. They are upstream's, not this project's, and **no attempt
    was made to use or test any of them**. The file was kept **unmodified**, because editing a bundled
    asset would break its recorded SHA-256 and misrepresent the upstream artefact.
* `decision` — Both real-shaped cases (the gitleaks allowlist and the TruffleHog canary token in its README)
  are recorded with a written explanation in the `BUNDLED_CREDENTIAL_LOOKALIKES` table inside
  `scripts/validate_catalog.py`. That table enforces the rule that matters: a credential-shaped string in a
  file **authored here** is always an error, and one in **bundled upstream** content is an error unless
  someone has read it and written down why it is acceptable. The validator's pattern set was widened in the
  same pass to cover Google API keys, Stripe live/test keys, Anthropic keys and JWTs, with an explicit
  placeholder exclusion so upstream documentation examples do not drown real findings.
* `decision` — Recorded licence traps verbatim: Alibi Detect **BSL 1.1** (non-production until change date);
  vectorbt **Commons Clause** over Apache-2.0 (no selling); MinerU Apache-2.0 **+ additional terms**;
  LiteLLM MIT **except `enterprise/`**; PyMuPDF **AGPL-3.0 or Artifex commercial**; TruffleHog **AGPL-3.0
  and verifies by default** (makes live network calls with found credentials).
* `failure` → `audit` — **`yixuantt/MultiHop-RAG` has no licence file.** Three files had already been
  downloaded. They were **deleted** (`resources/documentation/multihop-rag/`,
  `resources/benchmark-descriptions/multihop-rag/`), the asset record list was filtered 890 → 886, and a
  metadata-only record was written at `resources/documentation/_metadata-only/multihop-rag.md` with the
  official link, access requirements and the reason nothing is bundled. RULER's `variable_tracking.py` +
  `qa.py` (Apache-2.0) provide the same multi-hop construct lawfully.

### Collection passes

* `author` — Built an offline candidate-path specification (`spec.py`: 306 path patterns + 126 PyPI names)
  from the pinned inventories, so downloads were targeted rather than exploratory.
* `failure` — One unbalanced-parenthesis regex (`MineDojo/Voyager` pattern) raised
  `re.error: missing ), unterminated subpattern` mid-run. Rule adopted: compile-check generated regex
  dictionaries before use.
* `fetch` — **Pass 1** (`collect.py`, 191 s): 448 assets, 16.79 MB, 154 misses. Notable successes: OWASP
  Top 10 for LLM Applications v2025 PDF, ccxt `wiki/Manual.md`, `tuning_playbook` README, PyPI snapshots.
* `audit` — Analysed the 154 misses. Root causes: query-key vs `full_name` mismatches, and licence filename
  variants (`LICENSE.txt`, `MODEL_LICENSE`, `Readme.md`, `AGPL.md`).
* `fetch` — **Pass 2** (`collect2.py`, 234 s): +442 assets → 890 records / 883 files / 22 MB, **0
  unresolved repositories**. Alias map applied: `grantjenks/free-diskcache` → `python-diskcache`,
  `unum-cloud/usearch` → `USearch`, `VikParuchuri/marker|surya` → `datalab-to/*`, `hsiehjackson/RULER` →
  `NVIDIA/RULER`, `robertmartin8/PyPortfolioOpt` → `PyPortfolio/PyPortfolioOpt`, `princeton-nlp/Helmet` →
  `HELMET`, `iterative/dvc` → `treeverse/dvc`, `kermitt2/grobid` → `grobidOrg/grobid`,
  `explodinggradients/ragas` → `vibrantlabsai/ragas`.
* `failure` — 11 spec hits were skipped for exceeding per-file caps (40/60/80 KB by class). Accepted:
  caps keep the bundle bounded, which is a stated requirement.
* `audit` — 15 upstream paths had been collected under two different component ids; deduplicated in the
  manifest generator. Intermediate total: **880 assets**.
* `audit` — PyPI 404s for `vespa-engine` and `text-embeddings-inference` → both catalogued as GitHub-only
  components. `M4LC0N/crepes` has no resolvable GitHub repository at all → catalogued from PyPI registry
  metadata only, and labelled as such.

### Paper metadata verification

* `fetch` — arXiv API `id_list` batches (≤ 6 ids per call to keep the response inside one chunk):
  **31 papers verified on 2026-10-14**, including 2005.11401v4 (RAG), 2310.08560v2 (MemGPT),
  2404.06654v3 (RULER), 2307.03172v3 (Lost in the Middle), 2402.14848v2 (Same Task, More Tokens),
  2308.14508v2 (LongBench), 2402.07867v3 (PoisonedRAG), 2403.02691v3 (InjecAgent), 2302.12173v2
  (indirect prompt injection), 2406.13352v3 (AgentDojo), 2105.07538v1 (collective anomaly detection in
  high-dimensional VAR models).
* `failure` — Two identifiers I expected to be correct were **wrong**: `2409.12181` is *A Controlled Study
  on Long Context Extension and Generalization in LLMs*, **not** HELMET; `2105.07538` is the VAR
  anomaly-detection paper, **not** the conformal-prediction introduction. Both are recorded as verified
  findings and the affected catalog entries were flagged. (The VAR paper turned out to be genuinely useful
  for workstream 10.)
* `failure` — A retry of one 8-id batch failed with `SignatureDoesNotMatch` (proxy URL mangling). Those ids
  remain **unverified** and are labelled "arXiv id not re-verified" in
  [resources/papers/PAPER_INDEX.md](resources/papers/PAPER_INDEX.md) rather than asserted. 46 identifiers
  are in that state, including HELMET's.
* `decision` — Where an identifier could not be verified, the entry cites the **repository** (which was
  resolved and pinned) rather than the paper, and says so.

### Manifest and catalog construction

* `author` — Wrote and ran the manifest generator (v1.0) → 62 assets flagged `review-required` and 8
  flagged `NOT-PERMITTED`.
* `audit` — Reviewed all 70 flags individually. Outcome after the MultiHop-RAG removal and per-asset
  licence classification: **0 review-required, 0 not-permitted**. Status vocabulary recorded: `permitted`
  674, `copyleft-notice` 49, `cc-by-sa` 16, `registry-metadata` 124, `scoped` 5, `cc-by` 4,
  `additional-terms` 2, `no-sell` 2, `non-production-only` 2, `except-enterprise-dir` 2.
* `author` — Authored the per-component assessments in five batches (`cat_a`–`cat_e`, 30+30+29+37+38 = 164
  candidate rows), then merged and de-duplicated to 163 unique component rows, dropped a placeholder
  (`polars-meta`, superseded by the real `polars` row), and added 6 baseline-dependency rows (numpy, scipy,
  pandas, sqlalchemy, requests, pydantic) that are prerequisites rather than discoveries → **169 rows**.
* `audit` — **Duplicate-content check.** Hashing every bundled file found 18 distinct digests stored at
  59 paths. Nine were the *same upstream file collected twice under two categories* (for example
  `THUDM/LongBench pred.py` under both `code-examples/` and `benchmark-descriptions/`). Because the
  assignment requires shared assets to be stored once and referenced from multiple sections, the redundant
  copies were **deleted** and the survivors annotated with a `shared_with` cross-reference naming the
  removed path, its category and its component ids. Canonical-location rule adopted: licence text →
  `resources/licenses/`; a benchmark's own README → `resources/benchmark-descriptions/`; runnable harness
  code → `resources/code-examples/`; dependency manifests and changelogs → `resources/documentation/`.
  Result: **880 → 871 assets**, 20.45 MB → 20.40 MB, `benchmark-descriptions` 10 → 5 (now exactly one
  README per benchmark), `documentation` 603 → 599. No content was lost: every removed digest was verified
  to survive at its canonical path before deletion.
* `audit` — The remaining 9 duplicated digests are all inside `resources/licenses/`: identical MIT /
  Apache-2.0 / BSD texts shipped by many different upstreams. These were **kept** deliberately — each
  component directory carries its own notice so that attribution travels with the component. Recorded in
  `resources/licenses/INDEX.md`.
* `audit` — Verified every one of the 871 asset paths is attributed to exactly one catalog row
  (`sum(assets_bundled) = 871`); 162 rows bundle assets, 7 are metadata-only.
* `audit` — Re-parsed the finished CSV: 0 rows missing key fields; spot-checked a full row field-by-field
  (`ruler`: commit `c3f5e3b4…`, Apache-2.0, priority P1, `trial-ready`, 5 bundled assets).

### Authoring

* `author` — `resources/licenses/INDEX.md` (144 components with bundled licence text, redistribution
  vocabulary, and an explicit "deliberately NOT collected" list) and `ATTRIBUTION.md` at the repository root.
* `author` — `README.md`, `START_HERE.md`, `PROJECT_CONTEXT.md`, `RESOURCE_CATALOG.csv`,
  `ASSET_MANIFEST.json`.
* `author` — `scripts/validate_catalog.py` (structure, links, existence, hashes, vocabulary; **read-only and
  offline — it never executes a collected asset**) and `scripts/verify_asset_hashes.py`.
* `author` — `TOP_RECOMMENDATIONS.md`, `IMPLEMENTATION_ROADMAP.md`, `EVALUATION_PLAN.md`,
  `RESEARCH_REPORT.md`, `RISKS_AND_UNKNOWNS.md`, `REJECTED_OPTIONS.md`, `HANDOFF_FOR_NEXT_AI.md`, this log.
* `author` — 14 workstream READMEs, `PAPER_INDEX.md`, `BENCHMARK_NOTES.md`, four templates, and the
  architecture diagrams.

### Publication

* `publish` — Committed on branch `arena/7f817b55-ai-reading-and-self-learning`, pushed, opened
  [PR #1](https://github.com/aadhithya15/ai-reading-and-self-learning/pull/1) and merged it into `main`
  (merge commit `503a516`, 2026-10-15). The superseded placeholder `README.md` remains recoverable as
  commit `10bb5f6`, which is an ancestor of `main`.
* `audit` — **Verified the published state through the GitHub API rather than trusting local files.** The
  remote tree at `main` holds **914 blobs**, is not truncated, and contains all 13 required top-level
  documents, `ATTRIBUTION.md`, both scripts, all four templates, all 14 workstream directories and all
  880 files under `resources/`.
* `audit` — **Re-downloaded published bytes and recomputed their SHA-256** for a sample of six assets plus
  the largest file: 6/6 identical to the manifest, including the 10,716,216-byte OWASP PDF. Publication is
  therefore confirmed end-to-end, not inferred from a successful local write.

### Post-publication integrity audit (manifest 1.1 → 1.2)

* `audit` — Compared the blob SHA recomputed from every bundled file against the `git_blob_sha` recorded in
  the manifest. **740 matched, 124 were null, 7 differed.**
* `audit` — Investigated all 7 differences rather than assuming they were benign. Each recorded
  `git_blob_sha` was fetched from the upstream repository: all seven resolve to a **short path string, not
  file content** — `dagster-io/dagster` `README.md` → `python_modules/dagster/README.md`, `jd/tenacity`
  `README.rst` → `doc/source/index.rst`, `mindee/doctr` `docs/source/notebooks.rst` →
  `../../notebooks/README.rst`, `UKGovernmentBEIS/inspect_ai` `docs/CHANGELOG.md` → `../CHANGELOG.md`,
  `mem0ai/mem0` `docs/CLAUDE.md` → `AGENTS.md`, `deepcharles/ruptures` `docs/index.md` → `../README.md` and
  `docs/contributing.md` → `../CONTRIBUTING.md`. Those upstream paths are **symlinks**: GitHub's Contents
  API serves the resolved target's bytes while reporting the blob SHA of the link, so the recorded value
  was never a hash of what we bundled. Byte-level comparison against the upstream content confirmed the
  bundled files are identical to their resolved targets — **no content drift, no integrity problem.**
* `decision` — Renamed the field rather than leaving an ambiguity in published data. `git_blob_sha` became
  `upstream_git_blob_sha` (provenance, never re-fetched) and a new `local_git_blob_sha` (a hash **of the
  bundled bytes**, recomputed offline by `verify_asset_hashes.py`) was added to all 871 records. The 7
  symlinked assets are flagged `upstream_path_is_symlink` with their target and a written explanation; the
  124 package-registry metadata records keep `upstream_git_blob_sha: null` with a recorded reason. No
  `sha256` or `file_size_bytes` value changed. `manifest_version` is now **1.2** with a `revision_notes`
  history.
* `audit` — All 871 `local_git_blob_sha` values match the **published remote tree** at `main` exactly
  (0 mismatches), which independently confirms that what is on GitHub is what was assessed.
* `author` — `verify_asset_hashes.py` now recomputes and compares the Git blob SHA as well as SHA-256 and
  size. Its `human()` helper was also corrected: it used base-1024 and printed "19.45 MB" for the same
  content the manifest and every document call **20.40 MB** (base-1000), which read as a discrepancy in the
  collection's own totals.
* `author` — `validate_catalog.py` gained six checks: the pre-1.2 key must not reappear; every
  `local_git_blob_sha` is a 40-char hex SHA-1; every null `upstream_git_blob_sha` carries a reason; every
  non-null one is 40-char hex; all symlink-flagged assets record a target and an explanation; and no asset
  may have differing upstream/local blob SHAs without a recorded reason. It now runs **68 checks**.

---

## 3. Decisions register

| # | Decision | Reason | Revisit when |
|---|---|---|---|
| D1 | Bundle **files at pinned commits**, never repositories or tarballs | Repositories are up to 8.67 GB; file-level pinning gives exact provenance and a bounded bundle | Never — this is the right granularity |
| D2 | **No paper PDFs**, metadata-only for all 31 papers | arXiv non-exclusive licence ≠ redistribution right; plus no binary download route | Only if a paper is separately licensed for redistribution (e.g. a CC BY preprint explicitly checked) |
| D3 | Delete the MultiHop-RAG files after discovering no licence | Absence of a licence = all rights reserved | If upstream adds a permissive licence |
| D4 | Read every licence file rather than trusting GitHub's detector | Detector returned `NOASSERTION` for repos that do have licences | Never |
| D5 | Keep the bundle **in-repo**; no Releases, no LFS | 20.40 MB total, 10.72 MB largest file — well inside limits; Releases/LFS add discoverability friction and quota questions | Bundle exceeds ~100 MB, or a single file approaches 100 MB |
| D6 | One repository, workstreams as directories | Assignment requires a single entry point | Never |
| D7 | **Nothing executed** — not even a `pip install` or an import | Standing constraint; every downloaded asset is untrusted | Never, without explicit authorisation |
| D8 | Prefer embedded/in-process storage over servers | Reported RAM constraint; 12 server-class components rejected on footprint | Q1 is answered and shows real headroom |
| D9 | Bi-temporal validity in **SQL**, not a graph database | Three columns deliver the requirement; Neo4j does not fit the machine | Graph traversal (not interval queries) is demonstrably required |
| D10 | Lexical retrieval **first**, dense second, graph only on documented failure | Specification documents are dominated by exact tokens; dense needs weights (approval gate) | A measured failure of lexical on a real query class |
| D11 | Learning via **external memory**, not fine-tuning | Resource fit unknown; weights changing under a frozen evaluation destroys comparability | External-memory adaptation plateaus *and* hardware permits |
| D12 | Generate evaluation items **locally** from RULER's Apache-2.0 generators instead of downloading benchmark data | Data hosts unreachable; public benchmarks are contamination magnets; generators are re-seedable and auditable | A lawful, uncontaminated, scale-appropriate benchmark appears |
| D13 | Publish **templates and hashes**, never keys or held-out sources | Keys in a public repository destroy the evaluation | Never |
| D14 | Copyleft/GPL/AGPL components catalogued as **reference semantics only** | Vendoring them would change SAM-X's licensing obligations | A deliberate, reviewed decision to adopt one, with legal sign-off |
| D15 | Store each shared upstream file **once**, at a canonical category path, and cross-reference it | The assignment requires shared assets to be stored once and referenced from many sections; nine files had been collected twice under two categories | A component genuinely needs a private copy of a file |
| D16 | Archive branch created **before** any new file was written | Recoverability requirement; nothing was lost because nothing existed | Never |
| D17 | Name integrity fields for **what they hash**: `local_git_blob_sha` for the bundled bytes, `upstream_git_blob_sha` for provenance | One ambiguous `git_blob_sha` field silently meant two different things; for 7 symlinked upstream paths it was not a hash of the bundled content at all | Never — but re-check any new hash field for the same ambiguity |
| D18 | Verify the **published** state through the GitHub API, including re-downloading bytes and recomputing digests | A successful local write does not prove publication; the assignment requires confirming the remote commit and published files | Never |

---

## 4. Failures and dead ends (do not retry)

| Failure | Why | Do not retry because |
|---|---|---|
| `curl`/`wget` to arxiv.org, export.arxiv.org, huggingface.co, raw.githubusercontent.com, docs.python.org, aclanthology.org, openreview.net, proceedings.mlr.press, sqlite.org, duckdb.org, llm.datasette.io | Network egress blocked | All returned no HTTP response; the block is environmental |
| The signed proxy URL for the failed arXiv API batch | `SignatureDoesnotMatch` from URL mangling | Rebuild as a plain `http://export.arxiv.org/api/query?id_list=…&max_results=N` and use ≤ 6 ids per call; do not reuse the failed signed URL |
| `gh search repos --json licenseInfo` | Unknown JSON field | Use per-repository licence lookup instead |
| `gh api --jq … @tsv` on mixed 200/404 results | Mangled rows | Use Python `subprocess` + `json.loads` |
| `column` for table formatting | Not installed in the sandbox | Use Python formatting |
| The shell probe script that produced mangled JSONL | Quoting/escaping | Python for anything structured |
| `re.error: missing ), unterminated subpattern` | Unescaped paren in a generated pattern | Compile-check generated regex dicts |
| Assumed slugs for `raw.githubusercontent.com` content | 3 × 404 | Always resolve `full_name` through the API first |
| PyPI snapshots for `vespa-engine`, `text-embeddings-inference` | 404 | GitHub-only components |
| `twopirllc/pandas-ta` | 404 — upstream gone | Use `xgboosted/pandas-ta-classic` (MIT) with the fork caveat recorded |
| `M4LC0N/crepes` on GitHub | No resolvable repository | PyPI metadata only, labelled as such |

## 5. Reproducing or extending this collection

Everything needed is in the repository or derivable from it:

1. `ASSET_MANIFEST.json` (version 1.2) — for each of the 871 assets: original URL, retrieval date, local
   path, size, SHA-256, `local_git_blob_sha`, upstream commit and `upstream_git_blob_sha`, licence,
   attribution, status and limitations. Re-fetching any single asset is one URL. Verify with `sha256`;
   `upstream_git_blob_sha` differs by design on the 7 assets flagged `upstream_path_is_symlink`.
2. `RESOURCE_CATALOG.csv` — for each of the 169 components: upstream repository, pinned commit, licence,
   redistribution status, checked date, evidence status and the full 15-point assessment.
3. `scripts/verify_asset_hashes.py` — recomputes SHA-256, size and Git blob SHA for every bundled asset
   and compares all three against the manifest. Offline, read-only.
4. `scripts/validate_catalog.py` — structural validation: CSV columns and vocabularies, manifest keys and
   digests, catalog↔manifest cross-checks, relative-link resolution, workstream README presence, required
   top-level files, and a credential-pattern scan. Offline, read-only.
5. To extend: add the asset, add its manifest entry, add or update the catalog row, add the workstream link,
   re-run both scripts. `checked_date` must be the date you actually checked, not the date you copied.

**Re-verification cadence.** Licence, `pushed_at`, `archived` and HEAD SHA were captured on 2026-10-14.
Ownership changes were observed *during* that single day (`dvc`, `great_expectations`). Re-verify before any
adoption decision, and treat a changed org as a supply-chain signal worth reading the announcement for.
