#!/usr/bin/env python3
"""Checks a review tracker's issues.json and context.json.

Checks the schema, that every location exists at the reviewed commit, that every
location's link is current, that the index in context.json matches the issues, and
that every file listed in context.json "attachments" is in the tracker folder.
Exits non-zero and lists the problems if any check fails.

    validate-issues.py <issues.json> [--context <context.json>] [--repo <path>] [--link]

--link first writes each location's "url" into issues.json. For a GitHub pull
request, a line that the PR's "Files changed" tab shows links there; any other
line links to the file at the reviewed commit. Without a GitHub PR, locations get
no link.

context.json defaults to the file next to issues.json; a missing file is reported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

STATUSES = {"open", "in progress", "partial", "fixed", "dismissed", "wontfix"}
ISSUE_REQUIRED = ("n", "status", "title", "commit", "commitRole", "locations", "detail", "verified")
CONTEXT_REQUIRED = ("updatedAt", "reviewed", "resumePrompt", "index", "sections")
GITHUB_PR = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)/?$")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("issues")
    parser.add_argument("--context")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--link", action="store_true", help="write each location's url first")
    args = parser.parse_args()

    with open(args.issues, encoding="utf-8") as f:
        review = json.load(f)
    if args.link:
        link(review, args.repo)
        with open(args.issues, "w", encoding="utf-8") as f:
            json.dump(review, f, indent=2, ensure_ascii=False)
            f.write("\n")
    problems = check(review, args.repo)

    context_path = args.context or os.path.join(os.path.dirname(args.issues) or ".", "context.json")
    if os.path.exists(context_path):
        with open(context_path, encoding="utf-8") as f:
            problems += check_context(json.load(f), review, os.path.dirname(context_path) or ".")
    else:
        problems.append(f"{context_path} not found")

    for problem in problems:
        print(problem)
    if not problems:
        print(f"{len(review['issues'])} issues, all locations exist at {review['reviewed']} and their links are current; context.json matches")
    return 1 if problems else 0


def check(review: dict, repo: str) -> list[str]:
    problems = [
        f"missing top-level field {key!r}"
        for key in ("title", "branch", "base", "reviewed", "commits", "issues", "log")
        if key not in review
    ]
    if problems:
        return problems
    reviewed = review["reviewed"]
    if _git(repo, "rev-parse", "--verify", "--quiet", f"{reviewed}^{{commit}}") is None:
        return [f"reviewed commit {reviewed} not found in {repo}"]

    urls = location_urls(review, repo)
    numbers = [issue.get("n") for issue in review["issues"]]
    if len(set(numbers)) != len(numbers):
        problems.append(f"duplicate issue numbers: {numbers}")
    line_counts: dict[str, int | None] = {}
    for issue in review["issues"]:
        label = f"issue {issue.get('n', '?')}"
        problems += [f"{label}: missing {key!r}" for key in ISSUE_REQUIRED if key not in issue]
        status = issue.get("status")
        if status not in STATUSES:
            problems.append(f"{label}: unknown status {status!r}")
        if status == "fixed" and not _has(issue.get("fix"), "what", "behavior"):
            problems.append(f"{label}: 'fixed' needs 'fix' with 'what' and 'behavior'")
        if status in ("dismissed", "wontfix") and not _has(issue.get("dismissal"), "by", "at", "reason"):
            problems.append(f"{label}: {status!r} needs 'dismissal' with 'by', 'at' and 'reason'")
        commit = issue.get("commit")
        if commit and commit != review["base"] and commit not in review["commits"]:
            problems.append(f"{label}: commit {commit} is not in 'commits'")
        if not issue.get("detail"):
            problems.append(f"{label}: empty 'detail'")
        for location in issue.get("locations", []):
            path, line = location.get("path"), location.get("line")
            if not path or not isinstance(line, int):
                problems.append(f"{label}: location needs 'path' and an integer 'line'")
                continue
            if path not in line_counts:
                text = _git(repo, "show", f"{reviewed}:{path}")
                line_counts[path] = None if text is None else len(text.splitlines())
            count = line_counts[path]
            if count is None:
                problems.append(f"{label}: {path} does not exist at {reviewed}")
            elif not 1 <= line <= count:
                problems.append(f"{label}: {path}:{line} is past the end ({count} lines)")
            expected = urls(path, line)
            if location.get("url") != expected:
                problems.append(f"{label}: {path}:{line} link is missing or stale; run with --link")
    for i, entry in enumerate(review["log"]):
        if not _has(entry, "at", "text"):
            problems.append(f"log entry {i}: needs 'at' and 'text'")
    return problems


def link(review: dict, repo: str) -> None:
    urls = location_urls(review, repo)
    for issue in review.get("issues", []):
        for location in issue.get("locations", []):
            path, line = location.get("path"), location.get("line")
            if not path or not isinstance(line, int):
                continue
            url = urls(path, line)
            if url:
                location["url"] = url
            else:
                location.pop("url", None)


def location_urls(review: dict, repo: str):
    """Returns a function giving a location's url, or None where there is no GitHub PR."""
    match = GITHUB_PR.match((review.get("pr") or {}).get("url") or "")
    sha = _git(repo, "rev-parse", "--verify", "--quiet", f"{review.get('reviewed')}^{{commit}}")
    if not match or not sha:
        return lambda path, line: None
    owner, name, number = match.groups()
    sha = sha.strip()
    shown = _diff_lines(repo, review.get("base"), sha)

    def url(path: str, line: int) -> str:
        if line in shown.get(path, ()):
            anchor = hashlib.sha256(path.encode("utf-8")).hexdigest()
            return f"https://github.com/{owner}/{name}/pull/{number}/files#diff-{anchor}R{line}"
        return f"https://github.com/{owner}/{name}/blob/{sha}/{path}#L{line}"

    return url


def _diff_lines(repo: str, base: str | None, head: str) -> dict[str, set[int]]:
    """The new-side lines of each file that the PR's diff shows, context included."""
    base_ref = next((ref for ref in (f"origin/{base}", base) if ref and
                     _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")), None)
    if not base_ref:
        return {}
    # Three dots: from the merge base, as the "Files changed" tab compares.
    diff = _git(repo, "-c", "core.quotePath=off", "diff", "--no-color", "--no-ext-diff",
                "--unified=3", "-M", f"{base_ref}...{head}") or ""
    shown: dict[str, set[int]] = {}
    lines: set[int] | None = None
    for row in diff.splitlines():
        if row.startswith("+++ "):
            target = row[4:]
            lines = shown.setdefault(target[2:], set()) if target.startswith("b/") else None
        elif lines is not None and (hunk := HUNK.match(row)):
            start, size = int(hunk.group(1)), int(hunk.group(2) or 1)
            lines.update(range(start, start + size))
    return shown


def check_context(context: dict, review: dict, folder: str) -> list[str]:
    problems = [f"context.json: missing field {key!r}" for key in CONTEXT_REQUIRED if key not in context]
    if problems:
        return problems
    if context["reviewed"] != review["reviewed"]:
        problems.append(f"context.json: reviewed {context['reviewed']} differs from issues.json {review['reviewed']}")
    issues = {issue.get("n"): issue for issue in review["issues"]}
    indexed = {entry.get("n"): entry for entry in context["index"]}
    for n in sorted(set(issues) - set(indexed), key=str):
        problems.append(f"context.json: issue {n} missing from 'index'")
    for n in sorted(set(indexed) - set(issues), key=str):
        problems.append(f"context.json: 'index' lists issue {n}, which issues.json does not have")
    for n in sorted(set(issues) & set(indexed), key=str):
        for key in ("status", "title"):
            if indexed[n].get(key) != issues[n].get(key):
                problems.append(f"context.json: issue {n} {key} {indexed[n].get(key)!r} differs from {issues[n].get(key)!r}")
        if bool(indexed[n].get("blocker")) != bool(issues[n].get("blocker")):
            problems.append(f"context.json: issue {n} blocker flag differs from issues.json")
    for i, section in enumerate(context["sections"]):
        if not _has(section, "title", "text"):
            problems.append(f"context.json: section {i} needs 'title' and 'text'")
    for i, item in enumerate(context.get("waiting", [])):
        if not _has(item, "kind", "text"):
            problems.append(f"context.json: waiting item {i} needs 'kind' and 'text'")
        for n in item.get("issues", []):
            if n not in issues:
                problems.append(f"context.json: waiting item {i} names issue {n}, which issues.json does not have")
    for i, item in enumerate(context.get("attachments", [])):
        path = item.get("path") if isinstance(item, dict) else None
        # The page refuses the same shapes: a URL, an absolute path or a parent step.
        if not isinstance(path, str) or not path or re.match(r"^[a-z]+:|^/", path, re.I) or ".." in path:
            problems.append(f"context.json: attachment {i} needs a relative 'path' inside the tracker")
        elif not os.path.isfile(os.path.join(folder, path)):
            problems.append(f"context.json: attachment {path} is not in the tracker folder; read it back or remove the entry")
    return problems


def _has(value: object, *keys: str) -> bool:
    return isinstance(value, dict) and all(value.get(key) for key in keys)


def _git(repo: str, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, check=False
    )
    return result.stdout if result.returncode == 0 else None


if __name__ == "__main__":
    sys.exit(main())
