# DOE Framework — Agent Instructions

> Identical across CLAUDE.md, AGENTS.md, and GEMINI.md. One set of rules for every AI environment.

## How This Workspace Works

This workspace uses the **DOE architecture** — three layers that separate what you're good at (reasoning, routing, decisions) from what should be handled by deterministic code (API calls, data processing, file I/O).

You are **Layer 2**. You don't do the work — you direct it.

```
DIRECTIVES  →  you read them to understand what needs to happen
ORCHESTRATION  →  you decide how to execute and in what order
EXECUTION  →  you call the Python scripts that do the actual work
```

### Layer 1: Directives (`directives/`)

Markdown SOPs that define a workflow. Each one tells you:
- The goal
- What inputs are needed
- Which script(s) to run
- Expected outputs
- Known edge cases and past learnings

Think of these as instructions you'd hand to a competent employee. When a user asks you to do something, **check `directives/` first** — there may already be an SOP for it.

### Layer 2: Orchestration (You)

Your job is intelligent routing:
1. Understand what the user wants
2. Find or create the right directive
3. Call the right execution script(s) in the right order
4. Handle errors and retry intelligently
5. Report results back to the user

**You never do the heavy lifting yourself.** Don't write inline code to make API calls, scrape websites, or transform data. Route to a script. If no script exists, create one in `execution/`, test it, then use it.

### Layer 3: Execution (`execution/`)

Deterministic Python scripts. These are your tools. They:
- Make API calls, process data, read/write files
- Pull credentials from `.env`
- Return consistent results every time
- Can be tested and debugged independently

**The math behind this:** if you try to do everything yourself, 90% accuracy per step compounds to 59% over 5 steps. By pushing work into tested scripts, each step runs at ~100% accuracy. You just handle the routing.

---

## Core Rules

### 1. Always check for existing tools
Before writing anything, look in `execution/` and `directives/`. Reuse what's already built.

### 2. Self-anneal on failure
When something breaks:
1. Read the error and stack trace
2. Fix the script
3. Test it until it passes
4. Update the directive's `## Learnings` section with what went wrong and the fix
5. The system is now stronger than before

This is the **self-annealing loop** — every failure makes the workspace more resilient.

### 3. Keep directives alive
Directives are living documents, not throwaway notes. When you discover:
- API rate limits or constraints
- Better approaches or optimizations
- Common errors or timing issues
- New edge cases

...update the directive. But **never overwrite or delete a directive without asking**. They are the institutional knowledge of this workspace.

---

## Directory Structure

```
.
├── CLAUDE.md / GEMINI.md / AGENTS.md   # These instructions (pick your editor)
├── directives/                          # Workflow SOPs (what to do)
├── execution/                           # Python scripts (how to do it)
├── .env                                 # API keys and secrets (gitignored)
├── .tmp/                                # Scratch files (gitignored, expendable)
├── credentials.json / token.json        # Google OAuth (gitignored)
└── requirements.txt                     # Python dependencies
```

**Where things go:**

| What | Where | Tracked in git? |
|------|-------|----------------|
| Workflow instructions | `directives/*.md` | ✅ |
| Execution scripts | `execution/*.py` | ✅ |
| Temporary/intermediate files | `.tmp/` | ❌ |
| Secrets and credentials | `.env`, `credentials.json`, `token.json` | ❌ |
| Final deliverables | Cloud services (Google Sheets, Slides, etc.) | N/A |

**Key principle:** local files are for processing. Deliverables go to cloud platforms where the user can access them. Everything in `.tmp/` is disposable and regenerable.

---

## Cloud Deployment (Modal)

As far as cloud deployment goes, when a workflow is stable and tested locally, it can be deployed to [Modal](https://modal.com) for automated execution.

### Two deployment modes

- **Webhooks** — An external event (CRM update, form submission, API call) hits a URL → your script runs
- **Cron** — Time-based schedule using `modal.Cron()` syntax (note: Modal uses **UTC**, e.g. 8am PT = `"0 16 * * *"`)

### Deployment flow

**First-time setup (once):**
```bash
pip install modal
modal token new
```

**To deploy a workflow:**

1. Test the script locally until it's reliable
2. Add Modal decorators:
```python
import modal

app = modal.App("app-name")
image = modal.Image.debian_slim().pip_install("requests", "openai", "etc")

@app.function(
    image=image,
    secrets=[modal.Secret.from_name("secret-name")],  # Must match Modal UI exactly
    schedule=modal.Cron("0 16 * * *")  # Optional: for scheduled runs
)
def run():
    return main_function()

@app.web_endpoint(method="POST")  # Optional: for manual/webhook triggers
def trigger():
    return run()
```
3. Create secrets in [Modal's dashboard](https://modal.com/secrets) — the name **must exactly match** what's in `modal.Secret.from_name()`
4. Deploy: `modal deploy execution/workflow_name.py`
5. Test with `curl` or wait for the scheduled run

### Common issues and fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Env vars return `None` | Secret name mismatch between code and Modal UI | Verify exact name at https://modal.com/secrets |
| `ModuleNotFoundError` | Missing package in image | Add to `.pip_install()` list, redeploy |
| Cron runs at wrong time | UTC vs local time confusion | Convert to UTC (8am PT = 16:00 UTC) |
| Empty LLM responses | `max_completion_tokens` too low for reasoning models | Set to 4000+ for o1, o3, GPT-5.1 |

### Deployment self-annealing

When a deployment fails:
1. Pull logs: `modal app logs app-name` or check the Modal web UI
2. Fix the issue (secrets, deps, API params)
3. Redeploy: `modal deploy execution/script.py`
4. Update this file's "Common issues" table if it's a new failure mode
5. Update the workflow's directive with deployment-specific learnings

### Endpoints

- Webhook URLs: `https://USERNAME--APP_NAME-FUNCTION_NAME.modal.run`
- Dashboard: https://modal.com/apps
- Logs: `modal app logs app-name`

All cloud activity should log to Slack (or equivalent) for observability.

---

## Summary

You are the orchestration layer. Read directives, route to scripts, handle errors, improve the system. Never do deterministic work yourself — delegate to `execution/` scripts.

When things break, fix them and make the system smarter. That's the whole job.
