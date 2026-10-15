#!/usr/bin/env python3
"""verify_asset_hashes.py -- re-verify the integrity of every bundled asset.

WHAT THIS SCRIPT DOES
    * Reads ASSET_MANIFEST.json.
    * Recomputes SHA-256, byte size and the Git blob SHA for every asset with a
      local path.
    * Compares all three against the recorded values (sha256, file_size_bytes,
      local_git_blob_sha).
    * Reports: missing files, digest mismatches, size mismatches, duplicate
      digests that map to different paths, manifest entries with no local path,
      and files on disk under resources/ that no manifest entry claims.
    * Optionally verifies a single asset or one category.

WHAT THIS SCRIPT DELIBERATELY DOES NOT DO
    * It never executes, imports, unzips, parses or interprets a collected asset.
      A PDF is hashed as bytes. A Python file is hashed as bytes. Nothing is run.
    * It never touches the network. No re-download, no upstream comparison.
      Provenance (URL, commit, retrieval date) is recorded in the manifest and is
      checked for presence and shape only -- not re-fetched. In particular
      `upstream_git_blob_sha` is provenance and is deliberately NOT compared
      against the bundled bytes: for the 7 assets whose upstream path is a
      symlink, GitHub reports the link object's SHA while serving the resolved
      target's content, so a difference there is expected and is documented on
      the record itself (`upstream_git_blob_sha_note`).
    * It never writes to any file.

This is a deliberate scope limit: every downloaded asset is treated as untrusted,
so integrity checking must be possible without executing anything.

USAGE
    python3 scripts/verify_asset_hashes.py                 # verify everything
    python3 scripts/verify_asset_hashes.py --quiet         # errors only
    python3 scripts/verify_asset_hashes.py --category licenses
    python3 scripts/verify_asset_hashes.py --path resources/documentation/ruler/README.md
    python3 scripts/verify_asset_hashes.py --json          # machine-readable report

EXIT CODES
    0  every checked asset matched its recorded digest and size
    1  at least one mismatch, missing file or structural problem
    2  usage or I/O error (manifest unreadable, bad argument)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO_ROOT, "ASSET_MANIFEST.json")

# Files under resources/ that are authored for this collection rather than
# downloaded from upstream. They are hashed by nothing and claimed by no manifest
# entry, so the orphan check must not flag them.
AUTHORED_SUFFIXES = (".md", ".svg")
AUTHORED_DIRS = ("_metadata-only",)

CHUNK = 1 << 20  # 1 MiB -- keep peak memory tiny; these machines are small


def rel(path: str) -> str:
    """Path relative to the repository root, with forward slashes."""
    try:
        return os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    except ValueError:  # different drive on Windows
        return path.replace(os.sep, "/")


def sha256_of(path: str) -> str:
    """Stream-hash a file. Never loads it whole, never opens it in text mode."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def human(n: int) -> str:
    """Decimal (1000-based) formatting.

    Deliberately base-1000, not base-1024: ASSET_MANIFEST.json reports
    totals.total_mb = 20.4 for 20,398,632 bytes and every document in this
    collection quotes "20.40 MB", so this script must print the same number.
    Base-1024 here used to print 19.45 MB for the same content, which read as a
    discrepancy in the collection's own totals.
    """
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1000 or unit == "TB":
            return f"{n} B" if unit == "B" else f"{n:.2f} {unit}"
        n /= 1000.0
    return f"{n} B"


def git_blob_sha_of(path: str) -> str:
    """The Git blob object SHA-1 of a file's bytes: sha1("blob <len>\\0" + data).

    Streamed in two passes so a large file is never held in memory. This is the
    value `git hash-object` prints and the value that appears next to a path in
    `git ls-tree`, so it can be cross-checked against this repository's own
    published tree without any network access.
    """
    size = os.path.getsize(path)
    h = hashlib.sha1()
    h.update(b"blob " + str(size).encode("ascii") + b"\0")
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


class Report:
    def __init__(self, quiet: bool = False) -> None:
        self.quiet = quiet
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.checked = 0
        self.bytes_checked = 0

    def ok(self, msg: str) -> None:
        if not self.quiet:
            self.notes.append(msg)
            print(f"  ok    {msg}")

    def err(self, msg: str) -> None:
        self.errors.append(msg)
        print(f"  ERROR {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)
        if not self.quiet:
            print(f"  warn  {msg}")


def load_manifest(rep: Report) -> dict:
    if not os.path.isfile(MANIFEST):
        print(f"FATAL: manifest not found at {rel(MANIFEST)}", file=sys.stderr)
        raise SystemExit(2)
    try:
        with open(MANIFEST, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FATAL: cannot parse {rel(MANIFEST)}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def select(assets: list[dict], category: str | None, path: str | None) -> list[dict]:
    out = []
    for a in assets:
        if category and a.get("category") != category:
            continue
        if path and a.get("local_path") != path:
            continue
        out.append(a)
    return out


def verify(man: dict, rep: Report, category: str | None, path: str | None) -> None:
    assets = man.get("assets")
    if not isinstance(assets, list):
        rep.err("manifest has no 'assets' list")
        return

    chosen = select(assets, category, path)
    if category and not chosen:
        rep.err(f"no manifest assets match category={category!r}")
        return
    if path and not chosen:
        rep.err(f"no manifest asset has local_path={path!r}")
        return

    seen_ids: set[str] = set()
    digest_to_paths: dict[str, list[str]] = defaultdict(list)
    claimed: set[str] = set()
    no_local_path = 0
    structurally_bad = 0
    blob_ok = 0
    blob_bad = 0

    for a in chosen:
        aid = a.get("asset_id", "<no id>")
        if aid in seen_ids:
            rep.err(f"{aid}: duplicate asset_id in the manifest")
        seen_ids.add(aid)

        lp = a.get("local_path")
        recorded_sha = a.get("sha256")
        recorded_size = a.get("file_size_bytes")

        # Structural checks -- presence and shape only.
        for field in ("local_path", "sha256", "file_size_bytes", "original_url",
                      "retrieval_date", "license", "redistribution_status", "status"):
            if field == "license":
                if not (a.get("license") or a.get("license_spdx_detected")):
                    rep.err(f"{aid}: no licence recorded")
                    structurally_bad += 1
                continue
            if a.get(field) in (None, ""):
                rep.err(f"{aid}: manifest entry is missing '{field}'")
                structurally_bad += 1

        if not lp:
            # A metadata-only style entry: legitimate, but must say so.
            no_local_path += 1
            if a.get("status") not in ("metadata-only",):
                rep.warn(f"{aid}: no local_path and status={a.get('status')!r} (expected 'metadata-only')")
            continue

        abs_path = os.path.join(REPO_ROOT, lp)
        claimed.add(lp)

        # Containment: an asset must live inside the repository.
        if not os.path.abspath(abs_path).startswith(os.path.abspath(REPO_ROOT) + os.sep):
            rep.err(f"{aid}: local_path escapes the repository root: {lp}")
            continue

        if not os.path.isfile(abs_path):
            rep.err(f"{aid}: bundled file is MISSING at {lp}")
            continue

        actual_size = os.path.getsize(abs_path)
        if recorded_size is not None and actual_size != recorded_size:
            rep.err(f"{aid}: size mismatch at {lp} (recorded {recorded_size}, actual {actual_size})")

        recorded_blob = a.get("local_git_blob_sha")
        if not recorded_blob:
            rep.err(f"{aid}: no local_git_blob_sha recorded for {lp}")
            blob_bad += 1
        elif len(recorded_blob) != 40 or any(c not in "0123456789abcdef" for c in recorded_blob.lower()):
            rep.err(f"{aid}: local_git_blob_sha is not a 40-char hex SHA-1: {recorded_blob!r}")
            blob_bad += 1
        else:
            actual_blob = git_blob_sha_of(abs_path)
            if actual_blob != recorded_blob.lower():
                rep.err(f"{aid}: git blob SHA MISMATCH at {lp}\n"
                        f"          recorded {recorded_blob}\n"
                        f"          actual   {actual_blob}")
                blob_bad += 1
            else:
                blob_ok += 1

        if recorded_sha:
            if len(recorded_sha) != 64 or any(c not in "0123456789abcdef" for c in recorded_sha.lower()):
                rep.err(f"{aid}: recorded sha256 is not a 64-char hex digest: {recorded_sha!r}")
            else:
                actual_sha = sha256_of(abs_path)
                if actual_sha != recorded_sha.lower():
                    rep.err(f"{aid}: SHA-256 MISMATCH at {lp}\n"
                            f"          recorded {recorded_sha}\n"
                            f"          actual   {actual_sha}")
                else:
                    digest_to_paths[actual_sha].append(lp)
                    rep.checked += 1
                    rep.bytes_checked += actual_size
        else:
            rep.warn(f"{aid}: no recorded sha256 for {lp}; nothing to compare")

    rep.ok(f"{rep.checked} asset digests recomputed and matched ({human(rep.bytes_checked)})")
    if blob_ok:
        rep.ok(f"{blob_ok} Git blob SHAs recomputed and matched local_git_blob_sha")
    symlinks = [a for a in chosen if a.get("upstream_path_is_symlink")]
    if symlinks:
        rep.ok(f"{len(symlinks)} asset(s) are recorded as upstream symlinks; their "
               f"upstream_git_blob_sha identifies the link, not the bundled bytes")
    if no_local_path:
        rep.ok(f"{no_local_path} manifest entries have no local path (metadata-only)")
    if structurally_bad:
        rep.warn(f"{structurally_bad} structural field problems (see errors above)")

    # Identical content at different paths is usually deliberate (the same licence
    # text bundled under several components) but is worth surfacing.
    dupes = {d: p for d, p in digest_to_paths.items() if len(p) > 1}
    if dupes:
        total = sum(len(p) for p in dupes.values())
        rep.warn(f"{len(dupes)} distinct digests appear at {total} paths "
                 f"(expected for shared licence texts); first: "
                 f"{sorted(dupes.values())[0][:3]}")


def check_orphans(rep: Report, man: dict) -> None:
    """Every file under resources/ must be claimed, or be authored content."""
    claimed: set[str] = set()
    for a in man.get("assets", []):
        lp = a.get("local_path")
        if lp:
            claimed.add(lp)

    resources = os.path.join(REPO_ROOT, "resources")
    if not os.path.isdir(resources):
        rep.err("resources/ directory does not exist")
        return

    on_disk: list[str] = []
    for root, _dirs, files in os.walk(resources):
        for f in files:
            on_disk.append(rel(os.path.join(root, f)))

    orphans = []
    for p in on_disk:
        if p in claimed:
            continue
        if any(d in p for d in AUTHORED_DIRS):
            continue
        if p.endswith(AUTHORED_SUFFIXES):
            continue
        orphans.append(p)

    ghosts = sorted(claimed - set(on_disk))

    if orphans:
        rep.err(f"{len(orphans)} file(s) under resources/ are claimed by no manifest entry "
                f"and are not authored .md/.svg: {orphans[:10]}")
    else:
        rep.ok(f"all {len(on_disk)} files under resources/ are either claimed by the manifest "
               f"or are authored .md/.svg content")

    if ghosts:
        rep.err(f"{len(ghosts)} manifest local_path(s) do not exist on disk: {ghosts[:10]}")


def check_totals(rep: Report, man: dict) -> None:
    """The manifest's own summary must agree with its asset list."""
    totals = man.get("totals") or {}
    assets = [a for a in man.get("assets", []) if a.get("local_path")]
    actual_bytes = sum(a.get("file_size_bytes") or 0 for a in assets)
    if "total_bytes" in totals and totals["total_bytes"] != actual_bytes:
        rep.err(f"totals.total_bytes={totals['total_bytes']} but the asset list sums to {actual_bytes}")
    else:
        rep.ok(f"totals.total_bytes agrees with the asset list ({human(actual_bytes)})")

    if "assets" in totals and totals["assets"] != len(man.get("assets", [])):
        rep.err(f"totals.assets={totals['assets']} but there are {len(man.get('assets', []))} entries")

    by_cat: dict[str, int] = defaultdict(int)
    for a in man.get("assets", []):
        by_cat[a.get("category", "<none>")] += 1
    recorded_cat = totals.get("by_category") or {}
    for cat, n in sorted(by_cat.items()):
        if recorded_cat.get(cat) != n:
            rep.err(f"totals.by_category[{cat!r}]={recorded_cat.get(cat)} but {n} assets have that category")
    if recorded_cat and all(recorded_cat.get(c) == n for c, n in by_cat.items()):
        rep.ok(f"totals.by_category agrees with the asset list ({len(by_cat)} categories)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print warnings and errors only")
    ap.add_argument("--category", help="verify only assets in this category")
    ap.add_argument("--path", help="verify only the asset with this local_path")
    ap.add_argument("--no-orphans", action="store_true",
                    help="skip the on-disk orphan/ghost check")
    ap.add_argument("--no-totals", action="store_true",
                    help="skip the manifest self-consistency check")
    ap.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = ap.parse_args()

    rep = Report(quiet=args.quiet)
    man = load_manifest(rep)

    print(f"ASSET_MANIFEST.json: {man.get('manifest_version', '?')} "
          f"generated {man.get('generated_date', '?')}")
    print(f"repository: {man.get('repository', '?')} branch {man.get('branch', '?')}")
    print("verifying asset digests (read-only; no asset is executed or parsed)...")
    verify(man, rep, args.category, args.path)

    if not args.no_totals:
        print("checking manifest self-consistency...")
        check_totals(rep, man)
    if not args.no_orphans:
        print("checking for unclaimed files and missing paths...")
        check_orphans(rep, man)

    print()
    print(f"checked : {rep.checked} digests ({human(rep.bytes_checked)})")
    print(f"errors  : {len(rep.errors)}")
    print(f"warnings: {len(rep.warnings)}")

    if args.json:
        print(json.dumps({
            "checked": rep.checked,
            "bytes_checked": rep.bytes_checked,
            "errors": rep.errors,
            "warnings": rep.warnings,
        }, indent=2))

    if rep.errors:
        print("\nFAILED -- bundled assets do not match the manifest. Do not trust the "
              "collection until this is resolved.")
        return 1
    print("\nPASSED -- every checked asset matches its recorded SHA-256, size and Git blob SHA.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
