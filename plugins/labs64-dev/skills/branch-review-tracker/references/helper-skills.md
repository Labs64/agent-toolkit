# Helper skills for branch reviews

`branch-review-tracker` runs the same review flow in every project. What is specific
to a project, such as its toolchain, its data or its risk areas, belongs in the
project's own skills. Each helper below makes one part of the review more reliable.
A project needs only the ones that apply to it.

Put a helper where the project keeps its skills, for example
`<repo>/.claude/skills/<name>/SKILL.md` or a workspace `.claude/skills` directory.
Write its `description` so that it names the capability, because the review finds
helpers by their descriptions, for example "Use when building or testing a commit
of <project> in isolation". Keep each helper to what the project needs, and point
to the project's own docs instead of copying them.

When a review lacks a helper, give the user the one-line hint from the helper's
"Hint" line below, and offer to draft it from what the review learned.

## Review checklist

**Hint:** "A review-checklist skill would list this project's risk areas, so the
review checks them every time instead of relying on general knowledge."

Holds:

- the security model: roles and how they are assigned, including the default when
  none is given; which inputs a caller controls; where authorization is decided;
- compatibility promises: which clients, deployed versions and data formats must
  keep working, and for how long;
- API and data contracts the project must not break, and how changes to them are
  announced;
- migration rules: schema changes, data backfills, rollbacks;
- the project's known recurring defect patterns, with one example each.

Improves: finding issues, and judging which ones block the merge.

## Build and test

**Hint:** "A build-and-test skill would say how to build and test one commit in
isolation here, so the review can reproduce findings and check fixes by running
tests."

Holds:

- an environment check the review runs in its preflight. Name the script in the
  helper's `SKILL.md`. It takes `--target <ref> [--base <ref>] [--ticket <id>]
  [--repo <dir>]`, prints one line per check as `LEVEL check message`, with LEVEL
  one of `OK`, `INFO`, `WARN` and `FAIL`, and exits 0 if all is fine, 1 on
  warnings only and 2 on a `FAIL`. It checks what a generic preflight cannot: the
  toolchain and the installed tools, whether the build outputs exist and load,
  whether they match the commits under review, and any project-specific place
  the ticket appears;
- how to get a commit into an isolated directory, and what blocks a worktree in
  this repository, with the workaround, for example encrypted paths to exclude
  from `git archive`;
- the build and test commands, including required settings or credentials files
  and how to pass them, never their content;
- the toolchain the project targets, for example the language runtime version, and
  how to select it when the default differs;
- how to run one test class or module quickly, and the known slow or flaky suites;
- which commands need the user's permission first.

Improves: the preflight's view of the environment, reproducing findings, and
confirming fixes beyond reading the code.

## Data checks

**Hint:** "A data-checks skill would say how to answer questions from this
project's real data safely, so the review can tell a theoretical issue from one
that affects existing records."

Holds:

- which environments exist, which of them hold real data, and who may query them;
- where the schema is defined, so that queries use real table and column names;
- rules for queries: read-only, replicas or off-peak times for scans, limits;
- pitfalls of the data: soft-deleted rows, case-insensitive keys, legacy formats;
- how to report a result: what it means, and that it holds only at query time.

Improves: checking preconditions, such as whether existing data can trigger an
issue.

## Prose rules

**Hint:** "A prose-rules skill would give this project's rules for comments,
docstrings, changelogs, commit messages and PR text, so the prose review checks
them."

Holds: the rules for each kind of prose, with examples of good and bad text. A
general writing standard, not tied to one project, may already cover most of it;
a project helper then lists only the differences.

Improves: the prose review.

## Ticket conventions

**Hint:** "A ticket-conventions skill would give this project's ticket projects,
types, priorities and required fields, so drafted tickets post without
corrections."

Holds:

- the ticket system and the project keys;
- the issue types and priorities that exist, and which ones to use for what;
- required and customary fields, labels and components;
- how tickets link to each other and to pull requests;
- what the description should and should not contain.

Improves: drafting and posting follow-up tickets.
