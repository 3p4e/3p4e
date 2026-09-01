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

## Agency Agents Pack (258 agents)

Installed via [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) — a community roster of specialized AI agent personas, added to the Claude Code agent directory alongside the 6 project-specific agents above.

```bash
git clone https://github.com/msitarzewski/agency-agents.git
cd agency-agents
./scripts/install.sh --tool claude-code
```

### Divisions

| Division | Agents | Division | Agents |
|----------|-------:|----------|-------:|
| Engineering | 59 | Specialized | 58 |
| Marketing | 36 | GIS | 13 |
| Security | 12 | Design | 10 |
| Sales | 9 | Testing | 9 |
| Paid Media | 7 | Project Management | 7 |
| Academic | 6 | Game Development | 6 |
| Spatial Computing | 6 | Support | 6 |
| Finance | 5 | Product | 5 |
| Healthcare | 3 | Research | 1 |

Activate any agent in a Claude Code session with a prompt like *"Hey Claude, activate Frontend Developer mode and help me build a React component."*

## OpenMontage (agentic video production)

Installed via [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage) — an open-source, agentic video production system driven directly from AI coding assistants (Claude Code, Cursor, Copilot, Windsurf, Codex). It orchestrates research, scripting, asset generation, editing, and rendering through pipeline-driven skills, using free/local tools (Piper TTS, FFmpeg, Remotion/HyperFrames, Archive.org/NASA/Wikimedia footage) by default, with 60+ optional cloud provider integrations for paid generation.

```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
make setup
```

Prerequisites: Python 3.10+, FFmpeg, Node.js 18+. API keys for cloud image/video/voice/music providers are optional and go in `.env` (see `.env.example`).

Usage is prompt-driven from the coding assistant, e.g. *"Make a 60-second animated explainer about how neural networks learn."* Pipelines cover explainers, cinematic trailers, documentary montages, talking-head, avatar spokesperson, screen demos, localization/dub, and more — each following `research → proposal → script → scene_plan → assets → edit → compose`.

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
