#!/usr/bin/env python3
"""
validate_catalog.py — structural validation for the SAM-X research collection.

SCOPE (deliberately narrow, per the collection's safety boundaries):
  * CSV/JSON well-formedness of RESOURCE_CATALOG.csv and ASSET_MANIFEST.json
  * required columns / required manifest keys are present and non-empty where mandatory
  * every local_path recorded in the manifest exists on disk, and every bundled file
    under resources/ is accounted for in the manifest (no orphans, no ghosts)
  * every relative markdown link in *.md resolves to an existing file
  * classification / priority / evidence-status vocabularies are used consistently
  * cross-document counts agree with the generated artefacts

This script NEVER executes, imports, installs or network-fetches anything it validates.
It reads files as bytes/text only. Exit code 0 = pass, 1 = findings, 2 = script error.

Usage:
    python3 scripts/validate_catalog.py            # full run
    python3 scripts/validate_catalog.py --quiet    # summary only
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_CSV_COLUMNS = [
    "id", "name", "workstreams", "type", "official_url", "upstream_repo", "local_paths",
    "version_or_commit", "license", "redistribution_status", "checked_date",
    "evidence_status", "hardware_needs", "costs_privacy", "integration_role", "priority",
    "samx_problem", "what_inspected", "limitations", "fallback", "experiment",
    "classification", "assets_bundled",
]
MANDATORY_NON_EMPTY = ["id", "name", "workstreams", "type", "official_url", "checked_date",
                       "evidence_status", "integration_role", "priority", "samx_problem",
                       "limitations", "fallback", "experiment", "classification"]
CLASSIFICATIONS = {"trial-ready", "needs-more-evidence", "rejected"}
PRIORITIES = {"P1", "P2", "P3"}
WORKSTREAMS = {f"{i:02d}" for i in range(1, 15)}
REQUIRED_MANIFEST_KEYS = ["asset_id", "component_ids", "category", "original_url",
                          "retrieval_date", "local_path", "file_size_bytes", "sha256",
                          "local_git_blob_sha", "upstream_git_blob_sha",
                          "license_spdx_detected", "redistribution_status", "status",
                          "verification_limits", "access_limits"]
# Renamed in manifest 1.2. The old single field was ambiguous: it held the SHA of
# the *upstream* Git object, which for symlinked upstream paths is not a hash of
# the bundled bytes at all.
LEGACY_MANIFEST_KEYS = ["git_blob_sha"]
CATEGORIES = {"papers", "documentation", "code-examples", "configurations",
              "benchmark-descriptions", "diagrams", "licenses"}
LINK_RX = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SECRET_PATTERNS = [
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained personal access token"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "GitHub classic personal access token"),
    (re.compile(r"\bgho_[A-Za-z0-9]{20,}\b"), "GitHub OAuth token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"), "OpenAI-style secret key"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
    (re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}\b"), "Google API key"),
    (re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{15,}\b"), "Stripe-style secret/publishable key"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"), "Anthropic-style API key"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{5,}\b"),
     "JSON web token"),
    # A credential-shaped assignment whose value is NOT an obvious placeholder. Placeholders
    # such as YOUR_API_KEY, <your-token>, abc123, xxx, changeme and GEMINI_API_KEY are how
    # upstream documentation shows configuration shape, and flagging them drowns the real
    # findings -- so they are excluded here and reviewed by reading the file.
    (re.compile(r"""(?ix)\b(?:password|passwd|pwd|secret|api_?key|access_?token|auth_?token)\b
                     \s*[=:]\s*["']
                     (?!\s*(?:your|my|the|<|\{|\$|xx+|\*+|\.\.\.|changeme|placeholder|example|
                              none|null|empty|token-abc123|[a-z_]*api[_-]?key[a-z_]*|
                              this-will-ordinarily|willalso|zqt_abcdef|falkor_password))
                     [^"'\s]{12,}["']"""), "credential-shaped assignment with a non-placeholder value"),
]
# Kept for compatibility; the reviewed-explanation mechanism is BUNDLED_CREDENTIAL_LOOKALIKES below.
SECRET_SCAN_SKIP = ()


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def ok(self, msg: str) -> None:
        self.checks += 1
        print(f"  [ok]   {msg}")

    def err(self, msg: str) -> None:
        self.checks += 1
        self.errors.append(msg)
        print(f"  [FAIL] {msg}")

    def warn(self, msg: str) -> None:
        self.checks += 1
        self.warnings.append(msg)
        print(f"  [warn] {msg}")


def rel(path: str) -> str:
    return os.path.relpath(path, REPO)


def check_csv(rep: Report) -> list[dict]:
    path = os.path.join(REPO, "RESOURCE_CATALOG.csv")
    print("\n== RESOURCE_CATALOG.csv ==")
    if not os.path.exists(path):
        rep.err("RESOURCE_CATALOG.csv is missing")
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)
    missing_cols = [c for c in REQUIRED_CSV_COLUMNS if c not in header]
    extra_cols = [c for c in header if c not in REQUIRED_CSV_COLUMNS]
    if missing_cols:
        rep.err(f"missing required columns: {missing_cols}")
    else:
        rep.ok(f"all {len(REQUIRED_CSV_COLUMNS)} required columns present")
    if extra_cols:
        rep.warn(f"unexpected extra columns (allowed, but undocumented): {extra_cols}")
    if not rows:
        rep.err("catalog has no rows")
        return []

    ids = [r["id"] for r in rows]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    rep.err(f"duplicate component ids: {dupes}") if dupes else rep.ok(f"{len(ids)} unique component ids")

    bad_class = sorted({r["classification"] for r in rows} - CLASSIFICATIONS)
    rep.err(f"unknown classification values: {bad_class}") if bad_class else rep.ok("classification vocabulary valid")
    bad_prio = sorted({r["priority"] for r in rows} - PRIORITIES)
    rep.err(f"unknown priority values: {bad_prio}") if bad_prio else rep.ok("priority vocabulary valid")

    bad_ws = []
    for r in rows:
        for w in (r["workstreams"] or "").split(";"):
            w = w.strip()
            if w and w not in WORKSTREAMS:
                bad_ws.append((r["id"], w))
    rep.err(f"workstream codes outside 01..14: {bad_ws[:10]}") if bad_ws else rep.ok("all workstream codes are 01..14")

    empty = [(r["id"], c) for r in rows for c in MANDATORY_NON_EMPTY if not (r.get(c) or "").strip()]
    rep.err(f"{len(empty)} mandatory fields empty, e.g. {empty[:8]}") if empty else rep.ok("mandatory fields populated on every row")

    non_url = [r["id"] for r in rows if not re.match(r"^https?://", (r["official_url"] or "").strip())]
    rep.err(f"official_url is not an http(s) URL for: {non_url[:10]}") if non_url else rep.ok("every row has an http(s) official_url")

    bad_date = sorted({r["checked_date"] for r in rows if not re.match(r"^\d{4}-\d{2}-\d{2}$", r["checked_date"] or "")})
    rep.err(f"checked_date not ISO-8601: {bad_date}") if bad_date else rep.ok("checked_date is ISO-8601 on every row")

    ws_count = Counter()
    for r in rows:
        for w in (r["workstreams"] or "").split(";"):
            if w.strip():
                ws_count[w.strip()] += 1
    uncovered = sorted(WORKSTREAMS - set(ws_count))
    rep.err(f"workstreams with no catalogued component: {uncovered}") if uncovered else rep.ok(
        "every workstream 01..14 has at least one catalogued component")
    print("         per-workstream coverage: " + ", ".join(f"{k}={ws_count[k]}" for k in sorted(ws_count)))
    return rows


def check_manifest(rep: Report) -> dict:
    path = os.path.join(REPO, "ASSET_MANIFEST.json")
    print("\n== ASSET_MANIFEST.json ==")
    if not os.path.exists(path):
        rep.err("ASSET_MANIFEST.json is missing")
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            man = json.load(fh)
    except json.JSONDecodeError as exc:
        rep.err(f"ASSET_MANIFEST.json is not valid JSON: {exc}")
        return {}
    rep.ok("ASSET_MANIFEST.json parses as JSON")

    assets = man.get("assets", [])
    if not assets:
        rep.err("manifest lists no assets")
        return man
    ids = [a.get("asset_id") for a in assets]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    rep.err(f"duplicate asset_ids: {dupes[:10]}") if dupes else rep.ok(f"{len(ids)} unique asset ids")

    key_missing = [(a.get("asset_id"), k) for a in assets for k in REQUIRED_MANIFEST_KEYS if k not in a]
    rep.err(f"{len(key_missing)} assets missing required keys, e.g. {key_missing[:6]}") if key_missing \
        else rep.ok(f"all {len(REQUIRED_MANIFEST_KEYS)} required keys present on every asset")

    sha_bad = [a["asset_id"] for a in assets if not re.match(r"^[0-9a-f]{64}$", str(a.get("sha256", "")))]
    rep.err(f"sha256 not a 64-char hex digest for: {sha_bad[:10]}") if sha_bad else rep.ok("every sha256 is a 64-char hex digest")

    legacy = [(a.get("asset_id"), k) for a in assets for k in LEGACY_MANIFEST_KEYS if k in a]
    rep.err(f"{len(legacy)} assets still use the ambiguous pre-1.2 key(s), e.g. {legacy[:4]}") if legacy \
        else rep.ok("no asset uses the ambiguous pre-1.2 'git_blob_sha' key")

    # local_git_blob_sha must be a usable hash of the bundled bytes for every asset.
    lb_bad = [a["asset_id"] for a in assets if not re.match(r"^[0-9a-f]{40}$", str(a.get("local_git_blob_sha", "")))]
    rep.err(f"local_git_blob_sha is not a 40-char hex SHA-1 for: {lb_bad[:10]}") if lb_bad \
        else rep.ok("every local_git_blob_sha is a 40-char hex SHA-1")

    # upstream_git_blob_sha is provenance: either null with a recorded reason, or a
    # 40-char hex SHA-1. Null is expected for package-registry metadata records.
    ub_null_no_note = [a["asset_id"] for a in assets
                       if a.get("upstream_git_blob_sha") is None and not a.get("upstream_git_blob_sha_note")]
    ub_bad = [a["asset_id"] for a in assets
              if a.get("upstream_git_blob_sha") is not None
              and not re.match(r"^[0-9a-f]{40}$", str(a.get("upstream_git_blob_sha")))]
    rep.err(f"upstream_git_blob_sha is null with no recorded reason for: {ub_null_no_note[:10]}") if ub_null_no_note \
        else rep.ok(f"every null upstream_git_blob_sha carries a recorded reason "
                    f"({sum(1 for a in assets if a.get('upstream_git_blob_sha') is None)} registry-metadata assets)")
    rep.err(f"upstream_git_blob_sha is not a 40-char hex SHA-1 for: {ub_bad[:10]}") if ub_bad \
        else rep.ok("every non-null upstream_git_blob_sha is a 40-char hex SHA-1")

    # Where the upstream path is a symlink the two hashes legitimately differ, and
    # the record must say so and name the target.
    sym = [a for a in assets if a.get("upstream_path_is_symlink")]
    sym_bad = [a["asset_id"] for a in sym
               if not a.get("upstream_symlink_target") or not a.get("upstream_git_blob_sha_note")]
    rep.err(f"symlink-flagged assets missing a target or an explanation: {sym_bad}") if sym_bad \
        else rep.ok(f"all {len(sym)} symlink-flagged assets record their upstream target and an explanation")
    diff = [a["asset_id"] for a in assets
            if a.get("upstream_git_blob_sha") and a.get("local_git_blob_sha")
            and a["upstream_git_blob_sha"] != a["local_git_blob_sha"] and not a.get("upstream_path_is_symlink")]
    rep.err(f"assets whose upstream and local blob SHAs differ without a recorded reason: {diff}") \
        if diff else rep.ok("no unexplained upstream/local blob SHA differences")

    size_bad = [a["asset_id"] for a in assets if not isinstance(a.get("file_size_bytes"), int) or a["file_size_bytes"] < 0]
    rep.err(f"file_size_bytes not a non-negative int for: {size_bad[:10]}") if size_bad else rep.ok("file_size_bytes valid on every asset")

    cat_bad = sorted({a.get("category") for a in assets} - CATEGORIES)
    rep.err(f"category outside the resources/ taxonomy: {cat_bad}") if cat_bad else rep.ok("asset categories match the resources/ taxonomy")

    paths = [a["local_path"] for a in assets]
    dup_paths = [p for p, n in Counter(paths).items() if n > 1]
    rep.err(f"duplicate local_path entries: {dup_paths[:6]}") if dup_paths else rep.ok("every local_path is unique")

    ghosts = [p for p in paths if not os.path.exists(os.path.join(REPO, p))]
    if ghosts:
        rep.err(f"{len(ghosts)} manifest paths do not exist on disk, e.g. {ghosts[:6]}")
    else:
        rep.ok(f"all {len(paths)} manifest paths exist on disk")

    on_disk = set()
    res = os.path.join(REPO, "resources")
    for root, _dirs, files in os.walk(res):
        for f in files:
            on_disk.add(rel(os.path.join(root, f)).replace(os.sep, "/"))
    authored = {p for p in on_disk if p.endswith(".md") or p.endswith(".svg")}
    orphans = sorted(on_disk - set(paths) - authored - {p for p in on_disk if "/_metadata-only/" in p})
    if orphans:
        rep.warn(f"{len(orphans)} files under resources/ are not in the manifest (authored .md/.svg are expected): {orphans[:8]}")
    else:
        rep.ok("no unexplained files under resources/")

    if man.get("totals", {}).get("assets") != len(assets):
        rep.err(f"totals.assets ({man['totals'].get('assets')}) != len(assets) ({len(assets)})")
    else:
        rep.ok("totals.assets agrees with the asset list length")
    total_bytes = sum(a["file_size_bytes"] for a in assets)
    recorded_bytes = man.get("totals", {}).get("total_bytes",
                         man.get("totals", {}).get("bytes"))
    if recorded_bytes != total_bytes:
        rep.err(f"totals.total_bytes ({recorded_bytes}) != sum of file sizes ({total_bytes})")
    else:
        rep.ok(f"totals.total_bytes agrees with the sum of recorded file sizes ({total_bytes/1e6:.2f} MB)")
    print(f"         bundled size: {total_bytes/1e6:.2f} MB across {len(assets)} files")
    return man


def cross_check(rep: Report, rows: list[dict], man: dict) -> None:
    print("\n== catalog <-> manifest cross-checks ==")
    if not rows or not man:
        rep.warn("skipped: catalog or manifest unavailable")
        return
    assets = man.get("assets", [])
    by_comp = Counter()
    for a in assets:
        for c in a.get("component_ids", []):
            by_comp[c] += 1
    catalog_ids = {r["id"] for r in rows}
    unmatched = sorted({c for c in by_comp if c not in catalog_ids})
    rep.warn(f"asset component_ids with no catalog row: {unmatched[:10]}") if unmatched \
        else rep.ok("every asset component_id has a catalog row")

    mismatch = []
    for r in rows:
        claimed = int(r.get("assets_bundled") or 0)
        actual = by_comp.get(r["id"], 0)
        if claimed and actual < claimed:
            mismatch.append((r["id"], claimed, actual))
    rep.err(f"rows claiming more bundled assets than exist: {mismatch[:8]}") if mismatch \
        else rep.ok("no row overstates its bundled asset count")

    meta_only = [r["id"] for r in rows if int(r.get("assets_bundled") or 0) == 0]
    rep.ok(f"{len(meta_only)} catalog rows bundle nothing (metadata-only): {meta_only}")

    trial = sum(1 for r in rows if r["classification"] == "trial-ready")
    nme = sum(1 for r in rows if r["classification"] == "needs-more-evidence")
    rej = sum(1 for r in rows if r["classification"] == "rejected")
    print(f"         classification counts: trial-ready={trial} needs-more-evidence={nme} rejected={rej}")


def check_links(rep: Report, man: dict) -> None:
    """Check relative markdown links in AUTHORED files only.

    Bundled upstream documents are deliberately excluded. A copied upstream README
    naturally links to its own repository tree (CHANGELOG.md, INSTALL.md,
    docs/user-guide/...), and only a bounded selection of that tree was collected.
    Those links are expected not to resolve and are not a defect in this collection;
    reporting them as errors would bury the real navigation bugs. Every excluded
    file is still checked for existence and hash by verify_asset_hashes.py.
    """
    print("\n== relative markdown links (authored files) ==")
    bundled = {a["local_path"] for a in man.get("assets", []) if a.get("local_path")}
    md_files = []
    skipped = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        for f in files:
            if f.endswith(".md"):
                full = os.path.join(root, f)
                if rel(full) in bundled:
                    skipped += 1
                    continue
                md_files.append(full)
    print(f"         {len(md_files)} authored .md files checked; "
          f"{skipped} bundled upstream .md files excluded (their links point into "
          f"their own repository trees)")
    bad = []
    checked = 0
    for md in md_files:
        base = os.path.dirname(md)
        try:
            text = open(md, encoding="utf-8").read()
        except OSError:
            continue
        for target in LINK_RX.findall(text):
            t = target.strip()
            if t.startswith(("http://", "https://", "mailto:", "#", "file://")):
                continue
            t = t.split("#", 1)[0]
            if not t:
                continue
            checked += 1
            dest = os.path.normpath(os.path.join(base, t.replace("%20", " ")))
            if not os.path.exists(dest):
                bad.append(f"{rel(md)} -> {target}")
    if bad:
        rep.err(f"{len(bad)} broken relative links: {bad[:12]}")
    else:
        rep.ok(f"all {checked} relative markdown links resolve")


def check_workstreams(rep: Report) -> None:
    print("\n== workstream structure ==")
    for i in range(1, 15):
        d = os.path.join(REPO, "workstreams")
        matches = [x for x in os.listdir(d) if x.startswith(f"{i:02d}-")]
        if not matches:
            rep.err(f"no workstream directory for {i:02d}")
            continue
        readme = os.path.join(d, matches[0], "README.md")
        if not os.path.exists(readme):
            rep.err(f"workstreams/{matches[0]}/README.md missing")
        else:
            size = os.path.getsize(readme)
            if size < 2000:
                rep.warn(f"workstreams/{matches[0]}/README.md is only {size} bytes — likely incomplete")
            else:
                rep.ok(f"workstreams/{matches[0]}/README.md present ({size} bytes)")


def check_required_top_level(rep: Report) -> None:
    print("\n== required top-level files ==")
    required = ["README.md", "START_HERE.md", "PROJECT_CONTEXT.md", "RESOURCE_CATALOG.csv",
                "ASSET_MANIFEST.json", "RESEARCH_REPORT.md", "TOP_RECOMMENDATIONS.md",
                "IMPLEMENTATION_ROADMAP.md", "EVALUATION_PLAN.md", "RISKS_AND_UNKNOWNS.md",
                "REJECTED_OPTIONS.md", "RESEARCH_LOG.md", "HANDOFF_FOR_NEXT_AI.md",
                "ATTRIBUTION.md"]
    for f in required:
        p = os.path.join(REPO, f)
        if not os.path.exists(p):
            rep.err(f"missing {f}")
        elif os.path.getsize(p) < 400:
            rep.warn(f"{f} exists but is only {os.path.getsize(p)} bytes")
        else:
            rep.ok(f"{f} present ({os.path.getsize(p)} bytes)")
    for f in ["templates/experiment-contract.md", "templates/component-assessment.md",
              "templates/evaluation-report.md", "templates/source-provenance.json",
              "scripts/validate_catalog.py", "scripts/verify_asset_hashes.py"]:
        p = os.path.join(REPO, f)
        rep.ok(f"{f} present") if os.path.exists(p) else rep.err(f"missing {f}")


# Credential-shaped strings inside BUNDLED UPSTREAM files are handled differently
# from strings inside files authored for this collection. An authored file that
# contains a credential is a publishing accident and is always an error. A bundled
# upstream file may legitimately quote an example credential in its own
# documentation; that is only acceptable if it has been read, explained and
# recorded here. Anything bundled that is not on this list is an error.
BUNDLED_CREDENTIAL_LOOKALIKES = {
    "resources/configurations/gitleaks/config__gitleaks.toml": (
        "Gitleaks' own published configuration file, retrieved from the upstream repository at a "
        "pinned commit. Its [allowlist] section contains 16 Google-API-key-shaped strings that "
        "gitleaks itself allowlists so that its own example and test keys are not reported. They "
        "are published by the upstream project, are not this project's credentials, and were not "
        "verified as live or dead -- no attempt was made to use or test any of them. The file was "
        "kept unmodified because editing a bundled asset would break its recorded SHA-256 and "
        "misrepresent the upstream artefact; anyone running a secret scanner over this repository "
        "should expect these 16 strings and treat them as reviewed. Read and confirmed 2026-10-14."
    ),
    "resources/documentation/trufflehog/README.md": (
        "Upstream TruffleHog README reproducing example scanner output. The AWS "
        "access key id it shows is a canary token that trufflesecurity deliberately "
        "published in github.com/trufflesecurity/test_keys; the surrounding JSON "
        "contains an arn under canarytokens.com. Not a live credential, and not this "
        "project's. Read and confirmed on 2026-10-14. TruffleHog itself is AGPL-3.0 "
        "and is NOT recommended: it verifies findings by default, which makes live "
        "network calls using discovered credentials. See REJECTED_OPTIONS.md."
    ),
}


def check_secrets(rep: Report, man: dict) -> None:
    print("\n== secret / private-data scan of tracked text files ==")
    bundled = {a["local_path"] for a in man.get("assets", []) if a.get("local_path")}
    authored_hits: list[str] = []
    bundled_hits: list[str] = []
    unexplained: list[str] = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        for f in files:
            p = os.path.join(root, f)
            rp = rel(p)
            if rp in SECRET_SCAN_SKIP:
                continue
            try:
                if os.path.getsize(p) > 12_000_000:
                    continue
                text = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for rx, label in SECRET_PATTERNS:
                if rx.search(text):
                    if rp in bundled:
                        bundled_hits.append(f"{rp}: {label}")
                        if rp not in BUNDLED_CREDENTIAL_LOOKALIKES:
                            unexplained.append(f"{rp}: {label}")
                    else:
                        authored_hits.append(f"{rp}: {label}")
                    break

    if authored_hits:
        rep.err(f"credential-shaped strings in AUTHORED files (must be removed before "
                f"publishing): {authored_hits[:10]}")
    else:
        rep.ok("no credential-shaped strings in any file authored for this collection")

    for h in bundled_hits:
        path = h.split(":", 1)[0]
        if path in BUNDLED_CREDENTIAL_LOOKALIKES:
            rep.warn(f"bundled upstream file quotes an example credential "
                     f"({h}) -- reviewed and explained in BUNDLED_CREDENTIAL_LOOKALIKES")
    if unexplained:
        rep.err(f"bundled upstream files contain credential-shaped strings that have "
                f"NOT been reviewed and explained: {unexplained[:10]}")
    elif bundled_hits:
        rep.ok(f"all {len(bundled_hits)} credential look-alike(s) in bundled upstream "
               f"content are reviewed and explained")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true", help="print only the summary")
    args = ap.parse_args()
    if args.quiet:
        buf = sys.stdout
        sys.stdout = open(os.devnull, "w")
    rep = Report()
    try:
        print("SAM-X collection structural validation")
        print(f"repository root: {REPO}")
        rows = check_csv(rep)
        man = check_manifest(rep)
        cross_check(rep, rows, man)
        check_links(rep, man)
        check_workstreams(rep)
        check_required_top_level(rep)
        check_secrets(rep, man)
    finally:
        if args.quiet:
            sys.stdout.close()
            sys.stdout = buf
    print("\n== summary ==")
    print(f"checks run : {rep.checks}")
    print(f"errors     : {len(rep.errors)}")
    print(f"warnings   : {len(rep.warnings)}")
    for e in rep.errors[:40]:
        print(f"  ERROR: {e}")
    for w in rep.warnings[:40]:
        print(f"  WARN : {w}")
    print("\nRESULT:", "PASS" if not rep.errors else "FAIL")
    return 0 if not rep.errors else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover
        print(f"validator crashed: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
