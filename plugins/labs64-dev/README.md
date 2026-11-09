# labs64-dev

Labs64 skills for software development workflows. Each section below
describes one skill.

## branch-review-tracker

Reviews a branch or a pull/merge request, verifies every finding against the
code, and keeps one page per review listing each issue with its status,
evidence and `file:line`. Each later round re-reviews the branch, assesses the
fixes and updates the page. A small `context.json` on the page lets a new
session resume the review without the earlier conversation.

Requirements:

- git, and `gh` or `glab` for the pull or merge request;
- Python 3 for `scripts/validate-issues.py`;
- in Claude Code, the `Artifact` tool for the page; without it the skill keeps
  the tracker files locally and gives their paths.

The skill finds project helpers, such as a review checklist or a build-and-test
guide, by their descriptions. `references/helper-skills.md` lists what each
helper should contain.

## mr-description

Drafts or revises the title and description of a merge or pull request, on
GitLab, GitHub or another host, before it is created or updated. The
description opens with the defect or the goal, lists the changes, and leaves
out the history of the working session.

## Install

    claude plugin marketplace add Labs64/agent-toolkit
    claude plugin install labs64-dev@labs64
