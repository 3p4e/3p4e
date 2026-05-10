# Development Environment

> Code-server-based polyglot development environment with 14+ MCP integrations, Kilo AI agent orchestration, and automated ecosystem backup.

## Environment

| Component | Detail |
|-----------|--------|
| **Platform** | code-server (VS Code Server) on KVM4 VPS |
| **Shell** | Bash 5.x / Zsh |
| **Node.js** | via `/config/nodejs/bin/node` |
| **Python** | 3.12+ with uv/pip |
| **AI CLI** | Kilo v7.2.49 / DeepSeek TUI v0.8.25 |

## AI Agent Configuration

### Models
- **Primary**: DeepSeek V4 Pro (`kilo/deepseek/deepseek-v4-pro`)
- **Fallbacks**: Anthropic Claude, OpenAI GPT-4o, Gemini, MiniMax, Kimi

### 6 Specialized Agents

| Agent | Role | Write Access |
|-------|------|-------------|
| `frontend-specialist` | React, TypeScript, CSS | `.tsx?`, `.jsx?`, `.css`, `.scss` |
| `code-reviewer` | Security, quality, performance | Read-only |
| `code-simplifier` | Refactoring, DRY, clarity | Full access |
| `code-skeptic` | Critical review, validation | `.md` only |
| `docs-specialist` | Technical documentation | `.md`, `.txt`, `.rst` |
| `test-engineer` | Test coverage, edge cases | `.test.*`, `.spec.*` |

## MCP Server Ecosystem (14 servers)

| Server | Type | Purpose |
|--------|------|---------|
| **brave-search** | Search | Web & local search |
| **context7** | Docs | Library documentation lookup |
| **filesystem** | FS | Full filesystem access (`/`) |
| **github** | VCS | Repository & PR management |
| **supabase** | DB | Open Brain knowledge storage |
| **sequentialthinking** | Reasoning | Structured thought chains |
| **puppeteer** | Browser | Headless browser automation |
| **playwright** | Browser | Web testing & automation |
| **figma-dev-mode** | Design | Figma design integration |
| **google-workspace** | GSuite | Docs, Sheets, Drive |
| **gdrive** | Storage | Google Drive access |
| **firebase** | Platform | Firebase services |
| **time** | Utility | Timezone-aware time operations |

## Skills Inventory (49 skills)

### Kilo Global (46)
`adding-dbt-unit-test` `agent-md-refactor` `angular-component` `angular-di` `angular-directives` `angular-forms` `angular-http` `angular-routing` `angular-signals` `angular-ssr` `angular-testing` `angular-tooling` `answering-natural-language-questions-with-dbt` `building-dbt-semantic-layer` `changelog-generator` `competitive-ads-extractor` `configuring-dbt-mcp-server` `create-pull-request` `dbt` `dbt-migration` `domain-name-brainstormer` `fetching-dbt-docs` `figma-implement-design` `file-organizer` `grill-me` `image-enhancer` `internal-comms` `langsmith-fetch` `lead-research-assistant` `mcp-builder` `meeting-insights-analyzer` `migrating-dbt-core-to-fusion` `migrating-dbt-project-across-platforms` `running-dbt-commands` `skill-creator` `skill-share` `slack-gif-creator` `theme-factory` `troubleshooting-dbt-job-errors` `using-dbt-for-analytics-engineering` `vercel-composition-patterns` `vercel-deploy` `vercel-react-best-practices` `web-design-guidelines` `webapp-testing` `youtube-downloader`

### KiloCode IDE (3)
`artifacts-builder` `canvas-design` `content-research-writer`

## VS Code Extensions (105)

`angular-essentials` `angular-developer-std` `angular.ng-template` `antigravity-cockpit` `antigravity-plus` `better-comments` `bookmarks` `builder.builder` `claude-code` `claude-dev` `code-runner` `color-highlight` `copy-paste-tracker` `css-peek` `diff-ui` `docker` `easy-codesnap` `emojisense` `errorlens` `eslint` `eyecons` `firefox-debug` `gemini-cli` `geminicodeassist` `git-extension-pack` `git-graph` `git-project-manager` `github-actions` `github-pull-request` `githistory` `gitignore` `gitlens` `google-drive-vscode` `google-translate` `gutter-preview` `hermes-ai-agent` `hostinger-connector` `html-css` `html-essentials` `html-validate` `indent-rainbow` `javascript-essentials` `javascriptsnippets` `java` `jupyter` `kilo-code` `kimi-code` `live-server-speed-edition` `magicpython` `markdown-all-in-one` `markdownlint` `material-product-icons` `n8n-as-code` `n8n-mcp-vscode` `npm-intellisense` `obsidian-dark` `obsidianpreview` `output-colorizer` `path-intellisense` `peacock` `prettier-vscode` `pretty-ts-errors` `pyrefly` `python` `python-debugpy` `python-envs` `pythonsnippets3` `qt-core` `qt-ui` `rainbow-csv` `reactive-theme-settings` `rust-analyzer` `sftp` `skills-sh-vscode` `skills-wizard` `sonarlint` `sqltools` `status-bar-format-toggle` `stylelint` `svg` `svgreact` `todo-tree` `ts-error-translator` `typescript-essentials` `uitranslator` `vsc-essentials` `vsc-essentials-core` `vscode-clangd` `vscode-color` `vscode-containers` `vtp-voice-prompt` `workspace-mcp` `xml` `yaml` `zen-icon-theme`

## Ecosystem Backup

Automated dual-destination backup preserving the entire development environment:

- **GitHub**: [`3p4e/dev-env-config`](https://github.com/3p4e/dev-env-config) — sanitized, version-controlled configs
- **Open Brain**: Supabase `thoughts` table — searchable metadata
- **Local**: `/tmp/ecosystem-backup/` — AES-256-CBC encrypted secrets bundle

```bash
# Run backup
ecosystem-backup.sh
# Restore from GitHub
ecosystem-restore.sh --from-github
```

## Active Projects

- **[CoA Tracker](https://github.com/3p4e/CoA_TRACK)** — Certificate of Analysis tracking system with AI-powered compliance analysis
- **[Weekly SUMA](https://github.com/3p4e/WEEKLY_SUMA)** — ISO 17025 compliant lab management system
- **Purely Plant QMS** — Quality Management System for plant-based products

---

*Last updated: 2026-05-10 · Environment: KVM4 code-server container*
