# AGENTS.md: agent-toolkit

Labs64 tools for coding agents, published as a Claude Code plugin marketplace.
Everything in this repository is public.

## Layout

- `.claude-plugin/marketplace.json` lists every plugin under `plugins/`.
- `plugins/<name>/` is one plugin: `.claude-plugin/plugin.json`, a `skills/`
  folder of Agent Skills (`SKILL.md` plus optional `scripts/`, `references/`
  and `assets/`), and a `README.md`.
- Manifests for other agents (`.codex-plugin/`, `.cursor-plugin/`,
  `gemini-extension.json`) go next to `.claude-plugin/` in the plugin folder
  and point at the same `skills/`.
- Hooks and MCP servers belong to the plugin that uses them.
- `assets/icon.svg` is the toolkit icon, and `assets/icon-small.svg` its cut
  for 32 px and below. Each plugin carries a 512 px export as `icon.png`,
  named by `icon` in its `plugin.json`:

      rsvg-convert -w 512 -h 512 assets/icon.svg -o plugins/<name>/icon.png

- `assets/social-preview.svg` is the repository's social preview, uploaded
  as a PNG under Settings > Social preview. The README shows it, and
  `social-preview-dark.svg` for readers in dark mode. Both hold a copy of
  the icon's shapes, so a change to `icon.svg` goes there too. The text is
  set in Avenir Next, which macOS ships:

      rsvg-convert -w 1280 -h 640 assets/social-preview.svg -o assets/social-preview.png
      rsvg-convert -w 1280 -h 640 assets/social-preview-dark.svg -o assets/social-preview-dark.png

## Rules

- No internal hosts, ticket keys, credentials, personal paths or e-mail
  addresses. `scripts/check-public.sh` checks this and runs in CI. It matches
  by shape against public allow-lists; names that need an explicit list come
  from the `CHECK_PUBLIC_EXTRA` secret, never from a file in this repository.
- Project-specific knowledge belongs in the project's own repository, as a
  project skill, not here.
- Skill frontmatter holds only `name` and `description`, so that other agents
  read it too. A skill that relies on a Claude Code tool says what to do
  without it, in the skill or in `references/<agent>-tools.md`.
- Raise a plugin's `version` in both `plugin.json` and `marketplace.json`
  when its content changes.

## Checks

    scripts/check-public.sh
    claude plugin validate .
    claude plugin validate plugins/<name>
