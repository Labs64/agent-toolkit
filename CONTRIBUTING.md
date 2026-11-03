# Contributing

## Adding a skill

1. Put it in the plugin it fits, under `plugins/<plugin>/skills/<skill>/`, or
   create a new plugin folder and list it in `.claude-plugin/marketplace.json`.
2. Keep the frontmatter to `name` and `description`. The description says when
   to use the skill; agents decide from it alone whether to load it.
3. Describe the skill in the plugin's `README.md`, with what it needs to run.
4. Run the checks listed in `AGENTS.md`.

## Releasing a plugin

1. Raise `version` in the plugin's `plugin.json` and in its
   `marketplace.json` entry.
2. Tag the release, which also checks that both versions agree:

       claude plugin tag plugins/<plugin>

   The tag reads `<plugin>--v<version>`.
3. Push the commit and the tag.
