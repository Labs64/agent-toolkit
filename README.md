![agent-toolkit: Labs64 tools for coding agents](assets/social-preview.png)

Tools for coding agents from [Labs64](https://www.labs64.com).

| Plugin | Contents |
|---|---|
| [review](plugins/review) | `branch-review-tracker`: reviews a branch or pull request and tracks its issues across fix rounds |
| [writing](plugins/writing) | `mr-description`: drafts merge and pull request titles and descriptions |

The skills follow the [Agent Skills](https://agentskills.io) format, so agents
other than Claude Code can use them too.

## Install

Claude Code:

    claude plugin marketplace add Labs64/agent-toolkit
    claude plugin install review@labs64
    claude plugin install writing@labs64

Other agents that read Agent Skills: copy or link a skill folder, such as
`plugins/review/skills/branch-review-tracker`, into the agent's skills
directory.

## License

[Apache-2.0](LICENSE)
