# labs64-dev

Labs64 skills for software development workflows. Each section below
describes one skill.

## branch-review-tracker

Reviews a branch or a pull/merge request, verifies every finding against the
code, and keeps one page per review listing each issue with its status,
evidence and `file:line`. Each later round re-reviews the branch, assesses the
fixes and updates the page. A small `context.json` stored with the tracker lets a
new session resume the review without the earlier conversation.

Requirements:

- git, and `gh` or `glab` for the pull or merge request;
- Python 3 for `scripts/validate-issues.py`;
- in Claude Code, the `Artifact` tool for publishing the page; in Codex or
  without it, the skill keeps tracker files locally and gives their paths.
  Codex-specific tool fallbacks are in
  `skills/branch-review-tracker/references/codex-tools.md`.

The skill finds project helpers, such as a review checklist or a build-and-test
guide, by their descriptions. `references/helper-skills.md` lists what each
helper should contain.

## mr-description

Drafts or revises the title and description of a merge or pull request, on
GitLab, GitHub or another host, before it is created or updated. The
description opens with the defect or the goal, lists the changes, and leaves
out the history of the working session.

## Install

Claude Code:

    claude plugin marketplace add Labs64/agent-toolkit
    claude plugin install labs64-dev@labs64

Codex:

    codex plugin marketplace add Labs64/agent-toolkit

Restart the Codex desktop app after adding or updating the marketplace, then
open the Plugins Directory, choose the Labs64 marketplace, and install
`labs64-dev`.