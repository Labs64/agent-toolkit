# Contributing

## Adding a skill

1. Put it in the plugin it fits, under `plugins/<plugin>/skills/<skill>/`, or
   create a new plugin folder. Add `.codex-plugin/plugin.json` and list the
   plugin in `.claude-plugin/marketplace.json` and
   `.agents/plugins/marketplace.json`.
2. Keep the frontmatter to `name` and `description`. The description says when
   to use the skill; agents decide from it alone whether to load it.
3. Describe the skill in the plugin's `README.md`, with what it needs to run.
4. Run the checks listed in `AGENTS.md`.

## Releasing a plugin

1. Raise `version` in both plugin manifests (`.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json`) and in the plugin's entry in
   `.claude-plugin/marketplace.json`. Codex marketplace entries resolve the
   plugin version from its manifest.
2. Tag the release, which also checks that both versions agree:

       claude plugin tag plugins/<plugin>

   The tag reads `<plugin>--v<version>`.
3. Push the commit and the tag.
