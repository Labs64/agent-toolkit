# Codex tool fallbacks

Use these substitutions when running `branch-review-tracker` in Codex. The skill's review standards and verification requirements stay the same.

| Claude Code tool or behavior | Codex fallback |
|---|---|
| `AskUserQuestion` | Use Codex's structured question interface when available. Otherwise ask the user in chat, using the same target, base, and ticket choices. Wait for their answers before continuing. |
| `Agent` or `code-review` skill | Use an available independent reviewer when present. Otherwise review the branch directly in the current session, follow the skill's review and verification steps, and label the result as a single-agent review. |
| `Artifact` page | Keep `index.html`, `issues.json`, and `context.json` together in Codex's scratch area. If no persistent scratch location is available, ask the user for a directory outside the repository. Do not add review data to the project or claim an Artifact URL. Give the user the local paths. |
| `Edit` tool paired with Artifact | For Codex, edit the local `index.html` with the available file editor. Artifact editing instructions apply only when publishing an Artifact. |
| `Skill` tool | Use Codex's supported skill invocation mechanism. If a helper skill is not available, record it as missing and state what the review will lack, as the main skill directs. |

For later rounds, load the saved local files from the path the user provides. Update and validate them in place. Set `artifact` to `null`; write the local directory into the resume notes so a later Codex session can continue. The user must provide or retain that directory for the review to persist across sessions.
