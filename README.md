<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/social-preview-dark.png">
  <img src="assets/social-preview.png" alt="agent-toolkit: Labs64 tools for coding agents">
</picture>

Tools for coding agents from [Labs64](https://www.labs64.com).

The [labs64-dev](plugins/labs64-dev) plugin holds these skills:

| Skill | What it does |
|---|---|
| `branch-review-tracker` | Reviews a branch or pull request and tracks its issues across fix rounds |
| `mr-description` | Drafts merge and pull request titles and descriptions |

The skills follow the [Agent Skills](https://agentskills.io) format, so agents
other than Claude Code can use them too.

## Install

Claude Code:

    claude plugin marketplace add Labs64/agent-toolkit
    claude plugin install labs64-dev@labs64

Other agents that read Agent Skills: copy or link a skill folder, such as
`plugins/labs64-dev/skills/branch-review-tracker`, into the agent's skills
directory.

## Updates

Claude Code updates the plugin when you ask:

    claude plugin update labs64-dev@labs64

To get updates automatically, run `/plugin`, open the Marketplaces tab,
select `labs64` and choose Enable auto-update. A new version then loads in
your next session.

The `review` and `writing` plugins are now one plugin, `labs64-dev`. If you
installed them, replace them:

    claude plugin uninstall review@labs64
    claude plugin uninstall writing@labs64
    claude plugin install labs64-dev@labs64

## License

[Apache-2.0](LICENSE)
