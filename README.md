# DOE Framework — A 3-Layer Architecture for Reliable AI Agent Workflows

> **Directives · Orchestration · Execution**
>
> A production-ready template for structuring AI agent workflows. Separates *what to do* (Directives), *decision-making* (Orchestration), and *deterministic code* (Execution) to eliminate error compounding. Works with Claude Code, Gemini, Cursor, Windsurf, and any LLM-powered agent.

---

## The Problem

LLMs are probabilistic. Business logic is deterministic. When you let an AI agent do everything — scraping, API calls, data transforms, file I/O — errors compound fast:

> **90% accuracy per step × 5 steps = 59% overall success rate.**

Most people using AI coding agents have zero structure. They vibe code and hope for the best. DOE fixes that by pushing deterministic work into reliable Python scripts, and letting the LLM focus on what it's actually good at: **decision-making and routing.**

---

## The 3 Layers

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: DIRECTIVES                                │
│  SOPs in Markdown — define goals, inputs, outputs   │
│  "What to do" — like instructions for an employee   │
│                         ↓                           │
│  Layer 2: ORCHESTRATION                             │
│  The AI agent — reads directives, makes decisions,  │
│  routes tasks, handles errors, updates learnings    │
│                         ↓                           │
│  Layer 3: EXECUTION                                 │
│  Deterministic Python scripts — API calls, data     │
│  processing, file ops. Reliable, testable, fast.    │
└─────────────────────────────────────────────────────┘
```

### Why this works

The LLM never touches unreliable operations directly. It reads the SOP, decides what to do, and calls a tested Python script. If the script fails, the agent reads the error, fixes the script, tests it, and **updates the directive with what it learned** — so the system gets stronger over time.

This is the **self-annealing loop**:

1. Error occurs →
2. Agent fixes the script →
3. Agent tests it →
4. Agent updates the directive with new knowledge →
5. System is now more resilient

---

## Quick Start

### 1. Clone this template

```bash
git clone https://github.com/YOUR_USERNAME/doe-framework.git my_project
cd my_project
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env with your API keys

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies for the example workflow
pip install requests beautifulsoup4 openai python-dotenv
```

### 3. Open in your AI editor

Open the project in Claude Code, Cursor, Windsurf, or any AI-assisted editor. The agent instructions are automatically loaded via `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md`.

### 4. Start building

```bash
# Try the included example workflow
python execution/summarize_url.py https://example.com
```

Then create your own workflows. Tell AI to build whatever workflow you want, and it will:
- Define a directive in `directives/your_workflow.md`
- Build a script in `execution/your_workflow.py`
- Use these to execute tasks in the future.
- Constantly improve the workflow as it learns from errors.

---

## Directory Structure

```
.
├── CLAUDE.md              # Agent instructions (Claude Code)
├── GEMINI.md              # Agent instructions (Gemini)
├── AGENTS.md              # Agent instructions (Cursor, Windsurf, etc.)
├── .env.example           # Environment variable template
├── .gitignore             # Excludes secrets and temp files
├── directives/            # Workflow SOPs in Markdown
│   └── summarize_url.md   # Example directive (can be deleted)
├── execution/             # Deterministic Python scripts
│   └── summarize_url.py   # Example execution script (can be deleted)
└── .tmp/                  # Temporary/intermediate files (gitignored)
```

### File Organization Principles

| Type | Location | Version Controlled? |
|------|----------|-------------------|
| **Directives** (SOPs) | `directives/` | ✅ Yes |
| **Execution scripts** | `execution/` | ✅ Yes |
| **Agent instructions** | `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` | ✅ Yes |
| **Secrets / API keys** | `.env` | ❌ Gitignored |
| **Intermediate files** | `.tmp/` | ❌ Gitignored |
| **Deliverables** | Cloud services (Google Sheets, etc.) | N/A |

---

## Example Workflow

The template includes a complete example: **Summarize URL**.

**Directive** (`directives/summarize_url.md`):
- Defines the goal, inputs, steps, outputs, and edge cases
- Includes a `## Learnings` section that the agent updates over time

**Execution Script** (`execution/summarize_url.py`):
- Fetches a webpage and extracts text
- Sends it to OpenAI for summarization
- Handles errors (timeouts, paywalls, rate limits)

This is the pattern for every workflow: **a Markdown SOP paired with a Python script**, with the AI agent orchestrating between them.

---

## Deployment (Optional)

For webhooks or cron jobs, once a workflow is battle-tested locally, deploy the execution scripts to [Modal](https://modal.com) or any other cloud platform:

```bash
# One-time setup
pip install modal
modal token new

# Deploy
modal deploy execution/workflow_name.py
```

Supports:
- **Event-driven** — External trigger hits a webhook URL → script executes
- **Schedule-driven** — Cron jobs (e.g., daily at 8am PT)

See the agent instruction files for detailed deployment patterns and common issue fixes.

---

## Agent-Agnostic

The same instructions are mirrored across three files so the framework works everywhere:

| File | Platform |
|------|----------|
| `CLAUDE.md` | Claude Code |
| `GEMINI.md` | Gemini / Google AI agents |
| `AGENTS.md` | Cursor, Windsurf, and other AI editors |

Your agent reads its respective file, understands the architecture, and follows the DOE pattern automatically.

---

## Operating Principles

1. **Check for existing tools first** — Before writing a new script, check `execution/`. Don't reinvent the wheel.
2. **Self-anneal when things break** — Fix the script, test it, then update the directive with what you learned.
3. **Keep directives alive** — Directives are living documents. API limits, edge cases, better approaches — all get captured over time.

---

## TLDR: Why DOE > Unstructured Agent Prompting

| | DOE Framework | Unstructured Prompting |
|---|---|---|
| **Reliability** | Deterministic scripts eliminate error compounding | Every step is probabilistic |
| **Institutional knowledge** | Directives accumulate learnings over time | Knowledge is lost between sessions |
| **Separation of concerns** | Clear split: intent → decisions → code | Everything mixed together |
| **Testability** | Scripts can be tested independently | Nothing is independently testable |
| **Agent-agnostic** | Works with any AI agent | Tied to one platform's conventions |
| **Deployment path** | Built-in Modal webhooks/cron | Manual and ad-hoc |

---

## License

MIT — use it however you want.
