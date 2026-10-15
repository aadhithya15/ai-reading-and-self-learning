# Workstream 14 — Security, Isolation and Untrusted Input

**Objectives served:** preserve source separation and all safeguards; fail conservatively; treat every
downloaded asset as untrusted.

> **Every control in this workstream is labelled `proposed` until its test passes.** Nothing here was
> executed, installed or demonstrated during the build of this collection. A control that is written down is
> not a control that works. The distinction is enforced by requirement 14.10.
>
> **If question Q9 is answered "yes" — SAM-X already executes model-generated or downloaded code — this
> workstream becomes Phase 1 and everything else waits.**

---

## 1. Requirements and purpose

| # | Requirement | Why |
|---|---|---|
| 14.1 | **Every document is an attack surface**: parsed text is data, never instructions | Verified threat literature — see §2.4 |
| 14.2 | Untrusted parsing runs in a **sandbox with resource limits and no network** | A hostile document must not be able to write, call out, or exhaust the machine |
| 14.3 | A **source/sink inventory** for anything that can execute or be executed | You cannot contain what you have not enumerated |
| 14.4 | The **reading/research path has no tool** that can place an order or alter a risk parameter | Structural containment beats detection |
| 14.5 | **Dependencies pinned and hash-locked**, with a periodic advisory audit | Verified supply-chain movement during the check window (§2.3) |
| 14.6 | **Secret scanning** of the repository and its history, offline | A credential in a public repository is an incident |
| 14.7 | **Memory writes carry provenance** and may never alter risk, holding or approval parameters | Retrieval poisoning is verified — §2.4 |
| 14.8 | Hostile-fixture tests: path traversal, resource-exhaustion document, embedded instruction | Requirement 14.2 is a claim until tested |
| 14.9 | The OWASP Top 10 for LLM Applications mapped to SAM-X's actual assets, with owners and residual gaps | A standard nobody maps is a poster |
| 14.10 | **`proposed` versus `demonstrated`** labelled for every control, with the test that would move it | The central honesty requirement of this workstream |

**Not a goal.** A penetration test, a certification, or a claim that SAM-X is secure. The goal is an
enumerated, testable set of controls with their status recorded honestly.

## 2. Strongest approaches, and the alternatives

### 2.1 Recommended: contain structurally, then detect

1. **Structural containment first.** The reading and research path is given **no tool** that can place an
   order, alter a risk parameter, write outside its directory, or reach the network. This is the single most
   effective control available and it costs nothing at runtime. It must be **verified by code inspection**,
   not asserted — OWASP LLM06 (Excessive Agency) is exactly this failure.
2. **Sandbox untrusted parsing** with `nsjail` (Apache-2.0; config and schema bundled): mount namespace, no
   network, memory cap, CPU-time cap, file-size cap, read-only input. **Portable fallback:** OS-level
   `rlimits` plus a subprocess with a timeout and a read-only mount — weaker, but available everywhere and
   requiring no binary download.
3. **Detect what containment cannot**: `bandit` (Apache-2.0) finds dangerous sinks in Python; `semgrep`
   (LGPL-2.1) taint rules find paths from source to sink; `pip-audit` (Apache-2.0) checks advisories;
   `gitleaks` (rules bundled) and `detect-secrets` (Apache-2.0) scan for credentials **offline**.
4. **Probe the model layer** with `garak` (Apache-2.0) and `promptfoo` (MIT) — only against models the
   project is authorised to test.
5. **Map OWASP Top 10 for LLM Applications 2025** (CC BY-SA 4.0; the official 10.7 MB PDF plus all eleven
   vulnerability markdown files are bundled) onto SAM-X's actual assets, with an owner and a residual-gap
   note per entry.

### 2.2 The three OWASP entries that matter most here

| Entry | Why it is central to SAM-X |
|---|---|
| **LLM01 Prompt Injection** | Documents are untrusted input. An embedded instruction in a retrieved passage is the verified attack (Greshake et al.; InjecAgent) |
| **LLM08 Vector and Embedding Weaknesses** | Retrieval corpus poisoning: PoisonedRAG reports ~90% attack success from five injected texts in a corpus of millions, and reports the defenses it evaluated as insufficient |
| **LLM10 Unbounded Consumption** | The workstream-01 memory ceiling **is** a security control, not just a performance one. A resource-exhaustion document is an attack |

LLM02 (sensitive information disclosure), LLM03 (supply chain), LLM04 (data and model poisoning), LLM05
(improper output handling), LLM06 (excessive agency), LLM07 (system prompt leakage) and LLM09
(misinformation) are all bundled and all applicable; LLM06 and LLM04 are the next most important after the
three above.

### 2.3 Supply-chain findings, verified during the check window

* `iterative/dvc` → **`treeverse/dvc`**; `great-expectations/great_expectations` →
  **`fivetran/great_expectations`**; `VikParuchuri/marker` and `surya` → **`datalab-to/*`**;
  `explodinggradients/ragas` → **`vibrantlabsai/ragas`**; `robertmartin8/PyPortfolioOpt` →
  **`PyPortfolio/PyPortfolioOpt`**; `hsiehjackson/RULER` → **`NVIDIA/RULER`**; `kermitt2/grobid` →
  **`grobidOrg/grobid`**; `princeton-nlp/Helmet` → **`HELMET`**.
* `twopirllc/pandas-ta` returned **HTTP 404** — the canonical slug of a widely used library is gone.
* `AutoGPTQ` and `AutoAWQ` are **archived**.

An ownership change is not automatically a problem, but it is a **signal worth reading the announcement
for**, and it is why every catalog row pins a commit SHA and records `checked_date`, `upstream_last_pushed`
and `upstream_archived`.

### 2.4 Verified threat evidence (all metadata-only — paper PDFs are not redistributable)

| Paper | Identifier (status) | Finding |
|---|---|---|
| Greshake et al., *Not what you've signed up for* | arXiv:2302.12173v2 (**verified**) | Indirect prompt injection through retrieved content |
| **PoisonedRAG** | arXiv:2402.07867v3, USENIX Security 2025 (**verified**) | Five injected texts → ~90% attack success over a corpus of millions; evaluated defenses reported insufficient |
| **InjecAgent** | arXiv:2403.02691v3, ACL 2024 Findings (**verified**) | 1 054 test cases; a ReAct-prompted GPT-4 was vulnerable in 24% of them, roughly doubling with a "hacking" prompt |
| **AgentDojo** | arXiv:2406.13352v3 (**verified**) | 97 tasks and 629 security tests; state-of-the-art LLMs fail many even unattacked |
| Universal and Transferable Adversarial Attacks | `llm-attacks` repository (bundled docs; arXiv id **not re-verified**) | Adversarial suffixes transfer across models |

### 2.5 Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **TruffleHog** | **Not adopted — documented trap** | AGPL-3.0, and it **verifies findings by default**, which makes live network calls using discovered credentials. Running it against credentials you do not own is an incident. `gitleaks` and `detect-secrets` are the offline recommendations |
| **gVisor** | Not adopted | A container runtime requiring specific kernel support; not installable as a library and nothing may be installed here. Catalogued for when `nsjail` proves insufficient |
| **E2B** | **Rejected** | Remote **paid** sandboxes; sending document content to a third party is an unmade decision |
| **Semgrep as a dependency** | Rules adopted, tool not installed | LGPL-2.1; the bundled taint rules are readable and re-implementable |
| **`osv-scanner`, `trivy`** | Catalogued | Overlap `pip-audit`; `trivy` is a single Go binary that also scans filesystems and IaC. Choose one advisory source and record which |
| **`smolagents`** | Catalogued with a warning | A light agent loop, but every agent loop **enlarges the tool surface** this workstream has to contain. Its bundled docs are useful precisely because they discuss tool restrictions |
| **`simonw-llm`** | Catalogued for its logging model | Local SQLite logging of every call is a good egress-audit pattern |
| **`promptfoo`** | Adopted for its **deterministic assertion vocabulary** | MIT; a Node.js CLI. Its `jailbreak` and red-team features are leads, not validation |
| **Detection-first security** | **Rejected as the primary strategy** | Requirement 14.4: structural containment (no order-placing tool on the reading path) is stronger and cheaper than detecting an attempt |

## 3. Bundled assets

| Component | Bundled material |
|---|---|
| `owasp-llm-top10` (**CC BY-SA 4.0**) | [16 files](../../resources/documentation/owasp-llm-top10/) — the official **PDF** (`OWASP-Top-10-for-LLMs-v2025.pdf`, 10.72 MB, the only bundled PDF in the collection), `LLM00_Preface`, `LLM01_PromptInjection`, `LLM02_SensitiveInformationDisclosure`, `LLM03_SupplyChain`, `LLM04_DataModelPoisoning`, `LLM05_ImproperOutputHandling`, `LLM06_ExcessiveAgency`, `LLM07_SystemPromptLeakage`, `LLM08_VectorAndEmbeddingWeaknesses`, `LLM09_Misinformation`, `LLM10_UnboundedConsumption`, `README.md`, `changes.md` · [licence](../../resources/licenses/owasp-llm-top10/) |
| `nsjail` (Apache-2.0) | [documentation](../../resources/documentation/nsjail/) · [licence](../../resources/licenses/nsjail/) — sandbox config and schema |
| `bandit` (Apache-2.0) | [documentation](../../resources/documentation/bandit/) · [code examples](../../resources/code-examples/bandit/) · [licence](../../resources/licenses/bandit/) |
| `semgrep` (**LGPL-2.1**) | [documentation](../../resources/documentation/semgrep/) · [licence](../../resources/licenses/semgrep/) |
| `gitleaks` | [documentation](../../resources/documentation/gitleaks/) · [**rules**](../../resources/configurations/gitleaks/) · [licence](../../resources/licenses/gitleaks/) |
| `detect-secrets` (Apache-2.0) | [documentation](../../resources/documentation/detect-secrets/) · [code examples](../../resources/code-examples/detect-secrets/) · [licence](../../resources/licenses/detect-secrets/) |
| `pip-audit` (Apache-2.0) | [documentation](../../resources/documentation/pip-audit/) · [licence](../../resources/licenses/pip-audit/) |
| `osv-scanner` | [documentation](../../resources/documentation/osv-scanner/) · [licence](../../resources/licenses/osv-scanner/) |
| `trivy` (Apache-2.0) | [documentation](../../resources/documentation/trivy/) · [licence](../../resources/licenses/trivy/) |
| `garak` (Apache-2.0) | [documentation](../../resources/documentation/garak/) · [code examples](../../resources/code-examples/garak/) · [licence](../../resources/licenses/garak/) |
| `promptfoo` (MIT) | [documentation](../../resources/documentation/promptfoo/) · [licence](../../resources/licenses/promptfoo/) |
| `gvisor` (Apache-2.0) | [documentation](../../resources/documentation/gvisor/) · [licence](../../resources/licenses/gvisor/) (**1.40 GB repository — never tarball**) |
| `llm-attacks` | [documentation](../../resources/documentation/llm-attacks/) · [licence](../../resources/licenses/llm-attacks/) — dormant since 2024-08 |
| `trufflehog` (**AGPL-3.0**) | [documentation](../../resources/documentation/trufflehog/) · [licence](../../resources/licenses/trufflehog/) — **not recommended; see §2.5** |
| `e2b` | [documentation](../../resources/documentation/e2b/) · [licence](../../resources/licenses/e2b/) — **rejected** |
| `smolagents`, `simonw-llm` | [smolagents](../../resources/documentation/smolagents/) (14 files) · [LLM CLI](../../resources/documentation/simonw-llm/) |
| `prompt-injection-refs` | **Not bundled** — metadata-only row for the four verified papers in §2.4 |
| Papers | [PAPER_INDEX.md](../../resources/papers/PAPER_INDEX.md) |

**Note on two bundled files.** `resources/configurations/gitleaks/config__gitleaks.toml` is gitleaks' own
published configuration; its `[allowlist]` section contains 16 Google-API-key-shaped strings that gitleaks
allowlists so its own examples and test fixtures are not reported. They are upstream's, not this project's,
and no attempt was made to use or test any of them. The file is kept **unmodified** — editing a bundled asset
would break its recorded SHA-256 and misrepresent the upstream artefact — so anyone scanning this repository
should expect those 16 strings and treat them as reviewed. Separately,
`resources/documentation/trufflehog/README.md` quotes an example AWS access key
id in its sample scanner output. That key is a **canary token** deliberately published by
`trufflesecurity/test_keys` (the surrounding JSON contains a `canarytokens.com` ARN). It is not a live
credential and not this project's. The finding is reviewed and recorded in the
`BUNDLED_CREDENTIAL_LOOKALIKES` table inside [scripts/validate_catalog.py](../../scripts/validate_catalog.py)
so that the scan stays honest: a credential-shaped string in a file authored here is always an error, and
one in bundled upstream content is an error unless someone has read it and written down why it is
acceptable. Both files are listed there. The pattern set covers GitHub PAT/OAuth tokens, AWS access key ids,
PEM private key blocks, Slack tokens, Google API keys, Stripe live/test keys, Anthropic keys, JWTs and
credential-shaped assignments, with an explicit exclusion for documentation placeholders such as
`YOUR_API_KEY` and `<your-token>`.

## 4. Official upstream references

| Component | Upstream |
|---|---|
| OWASP Top 10 for LLM Applications | https://github.com/OWASP/www-project-top-10-for-large-language-model-applications · https://owasp.org/www-project-top-10-for-large-language-model-applications/ |
| nsjail | https://github.com/google/nsjail |
| Bandit | https://github.com/PyCQA/bandit |
| Semgrep | https://github.com/semgrep/semgrep · https://semgrep.dev/docs |
| Gitleaks | https://github.com/gitleaks/gitleaks |
| detect-secrets | https://github.com/Yelp/detect-secrets |
| pip-audit | https://github.com/pypa/pip-audit |
| OSV-Scanner | https://github.com/google/osv-scanner |
| Trivy | https://github.com/aquasecurity/trivy |
| garak | https://github.com/NVIDIA/garak |
| promptfoo | https://github.com/promptfoo/promptfoo · https://promptfoo.dev/ (**unreachable for download from the build sandbox**) |
| gVisor | https://github.com/google/gvisor |
| llm-attacks | https://github.com/llm-attacks/llm-attacks |
| TruffleHog | https://github.com/trufflesecurity/trufflehog — **AGPL-3.0; verifies by default** |
| E2B | https://github.com/e2b-dev/e2b |
| Threat papers | arXiv:2302.12173v2 · arXiv:2402.07867v3 · arXiv:2403.02691v3 · arXiv:2406.13352v3 (all **verified** 2026-10-14) |

## 5. Adoption steps

1. **Answer Q9 first**: does SAM-X execute model-generated or downloaded code anywhere? If yes, stop and do
   steps 3–5 before anything else in the whole roadmap.
2. **Write the source/sink inventory** (14.3): every input that crosses a trust boundary (documents,
   retrieved passages, model outputs, vendor data, configuration) and every sink that can act (file writes,
   network calls, subprocess execution, database writes, anything touching risk or order state).
3. **Verify structural containment** (14.4) by code inspection: enumerate the tools available to the
   reading/research path and confirm none can place an order or alter a risk, holding or approval parameter.
   Record the enumeration; it is the evidence.
4. **Sandbox untrusted parsing** (14.2): `nsjail` with the bundled config on Linux, or OS `rlimits` plus a
   timeouted subprocess and a read-only mount as the portable fallback. **Treat any sandbox binary as
   untrusted until its hash is verified against upstream** — and note that building or downloading one needs
   approval this engagement did not have.
5. **Add hostile-fixture tests** (14.8): a path-traversal filename, a resource-exhaustion document, an
   embedded instruction in body text, an instruction hidden in a table cell or PDF metadata. Assert: no
   write outside the sandbox, enforced memory cap, enforced timeout, no tool invocation from the reading
   path.
6. **Pin and hash-lock dependencies**; add a periodic `pip-audit` (or `trivy` / `osv-scanner`) run and record
   every finding with its resolution or its accepted risk.
7. **Scan for secrets offline** with `gitleaks` rules and `detect-secrets`, over the working tree **and the
   full Git history**. Never run TruffleHog in verify mode against credentials you do not own.
8. **Add provenance to every memory write** (14.7) and quarantine writes derived from retrieved content as
   hypotheses until reviewed. No memory write may alter a risk, holding or approval parameter.
9. **Map the OWASP Top 10** to SAM-X's actual assets: per entry, the affected asset, the control, its status
   (`proposed` / `demonstrated`), an owner, and the residual gap.
10. **Re-label every control** from `proposed` to `demonstrated` only when its test passes (14.10).

## 6. Resource implications

All **estimates**; none measured.

| Item | Expectation | Note |
|---|---|---|
| `nsjail` sandbox | A process per parse, with enforced caps | The caps are the point: memory, CPU time, file size, no network |
| OS `rlimits` fallback | Negligible | Weaker isolation, available everywhere |
| `bandit`, `semgrep` | Scan-time CPU and I/O | Run in CI or periodically, not on the hot path |
| `pip-audit` | Light, but **queries an advisory database over the network** | Record the audit date; an offline-only mode changes the guarantee |
| `gitleaks`, `detect-secrets` | Light; history scans are I/O bound | Offline |
| `garak` | **Many payloads against the target model** — token cost and time | Only against authorised targets |
| `promptfoo` | Node.js CLI; light | Judge-based assertions add model cost |
| `trivy`, `osv-scanner` | Single binaries; scans can be I/O heavy | Periodic |
| gVisor | A container runtime | Not installable here; catalogued for later |
| Structural containment | **Zero runtime cost** | The cheapest and strongest control available |

## 7. Qualification requirements

1. **Structural containment verified by inspection**: an enumerated tool list for the reading/research path,
   with none able to place an order or alter a risk, holding or approval parameter.
2. **Hostile-fixture tests pass**: path traversal, resource-exhaustion document, embedded instruction
   (body text, table cell and PDF metadata) → no write outside the sandbox, memory cap enforced, timeout
   enforced, no tool invocation.
3. **Sandbox escape attempts fail**, and the attempt is logged.
4. **Dependency audit**: every dependency pinned and hash-locked; advisory audit run on a recorded date;
   every finding resolved or accepted with a written reason.
5. **Secret scan clean** over the working tree and the full Git history, with any bundled upstream
   look-alike reviewed and explained.
6. **Memory-write provenance**: every write carries a source; a test that attempts a model-written fact
   fails; a test that attempts to alter a risk parameter through memory fails.
7. **OWASP mapping complete**: all ten entries mapped to assets, controls, status, owner and residual gap.
8. **Every control carries a `proposed` or `demonstrated` label**, and no control is labelled
   `demonstrated` without a passing test.
9. **No safeguard modified**: a diff review confirms source separation, protected holdouts,
   trading/risk/approval/holding rules and open-position handling are unchanged.
10. The scan and audit tooling was never run against credentials, accounts or systems the project does not
    own.

## 8. Rejected approaches

| Rejected | Reason |
|---|---|
| TruffleHog | AGPL-3.0, and it verifies findings by default using the discovered credentials over the network |
| gVisor | A container runtime needing specific kernel support; nothing may be installed here |
| E2B | Paid, remote, and moves document content off-box |
| Detection-first security | Structural containment is stronger and cheaper (14.4) |
| Running any scanner against systems or credentials the project does not own | Prohibited |
| Treating a written control as a working control | Requirement 14.10 |
| Installing Semgrep or any scanner during this engagement | Prohibited; rules are bundled for reading |
| Bundling `garak` probe runs against a third-party model | Not authorised |
| Assuming a document is benign because its source is reputable | Requirement 14.1; PoisonedRAG's corpus was ordinary |
| Treating the memory ceiling as only a performance concern | OWASP LLM10: unbounded consumption is a security failure |
| Claiming SAM-X is secure | Nothing here demonstrates that; §7 is a test plan, not a result |

## 9. Unresolved gaps

| Gap | Blocks | How to close it |
|---|---|---|
| **Q9: does SAM-X execute model-generated or downloaded code?** | The entire phase order | Ask. Highest-leverage unknown in the collection |
| **Q10: are safeguards enforced in code, in configuration, or by convention?** | What "do not touch safeguards" means concretely | Ask; a convention is not a control |
| Whether the target OS supports `nsjail` (Linux-specific) | Requirement 14.2's primary form | Q1; otherwise use the `rlimits` fallback and record the weaker guarantee |
| Approval to scan the SAM-X codebase with any tool | Steps 6–7 | Explicit authorisation required |
| Approval to build or download a sandbox binary | Step 4 | Explicit authorisation; hash-verify against upstream first |
| Approval to probe any model with `garak` or `promptfoo` | §5 step 10's tests | Explicit authorisation, plus budget |
| Whether an advisory database is reachable from the target machine | `pip-audit`'s guarantee | It queries the network; an offline-only mode is a weaker guarantee and must be recorded as such |
| The OWASP mapping itself | Requirement 14.9 | Requires knowing SAM-X's assets — nobody outside the project does |
| Residual risk after every control is demonstrated | An honest security posture | Recorded per OWASP entry; never claimed to be zero |
| Nothing here was executed, installed or demonstrated | All of §7 | Requires authorisation this engagement did not have |
