# Agent Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- Basically just SOPs written in Markdown, live in `directives/`
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases
- Natural language instructions, like you'd give a mid-level employee

**Layer 2: Orchestration (Decision making)**
- This is you. Your job: intelligent routing.
- Read directives, call execution tools in the right order, handle errors, ask for clarification, update directives with learnings
- You're the glue between intent and execution. E.g you don't try scraping websites yourself—you read `directives/scrape_website.md` and come up with inputs/outputs and then run `execution/scrape_single_site.py`

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Environment variables, api tokens, etc are stored in `.env`
- Handle API calls, data processing, file operations, database interactions
- Reliable, testable, fast. Use scripts instead of manual work.

**Why this works:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. The solution is push complexity into deterministic code. That way you just focus on decision-making.

## Operating Principles

**1. Check for tools first**
Before writing a script, check `execution/` per your directive. Only create new scripts if none exist.

**2. Self-anneal when things break**
- Read error message and stack trace
- Fix the script and test it again (unless it uses paid tokens/credits/etc—in which case you check w user first)
- Update the directive with what you learned (API limits, timing, edge cases)
- Example: you hit an API rate limit → you then look into API → find a batch endpoint that would fix → rewrite script to accommodate → test → update directive.

**3. Update directives as you learn**
Directives are living documents. When you discover API constraints, better approaches, common errors, or timing expectations—update the directive. But don't create or overwrite directives without asking unless explicitly told to. Directives are your instruction set and must be preserved (and improved upon over time, not extemporaneously used and then discarded).

## Self-annealing loop

Errors are learning opportunities. When something breaks:
1. Fix it
2. Update the tool
3. Test tool, make sure it works
4. Update directive to include new flow
5. System is now stronger

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets, Google Slides, or other cloud-based outputs that the user can access
- **Intermediates**: Temporary files needed during processing

**Directory structure:**
- `.tmp/` - All intermediate files (dossiers, scraped data, temp exports). Never commit, always regenerated.
- `execution/` - Python scripts (the deterministic tools)
- `directives/` - SOPs in Markdown (the instruction set)
- `.env` - Environment variables and API keys
- `credentials.json`, `token.json` - Google OAuth credentials (required files, in `.gitignore`)

**Key principle:** Local files are only for processing. Deliverables live in cloud services (Google Sheets, Slides, etc.) where the user can access them. Everything in `.tmp/` can be deleted and regenerated.

## Cloud Webhooks (Modal)

Once a workflow is battle-tested locally, deploy ONLY the deterministic Python scripts to Modal. 

### Deployment Types

**Event-Driven (Webhooks)**: External trigger (CRM, form, API) hits URL → script executes immediately

**Schedule-Driven (Cron)**: Time-based triggers. Use `modal.Cron()` with cron syntax:
- Ex. Daily at 8am PT: `modal.Cron("0 16 * * *")` (remember: Modal uses UTC, so 8am PT = 16:00 UTC)

### Deploying an Existing Workflow as a Webhook

When user says "Deploy [workflow_name] as a webhook using Modal":

**First-Time Setup (one time only)**:
1. Install Modal: `pip install modal`
2. Authenticate: `modal token new` (opens browser to authenticate your Modal account)

**Deployment Steps**:
1. **Test locally first** - Always run the Python script locally to verify it works
2. Agent adds Modal decorators to `execution/workflow_name.py`:
   ```python
   import modal

   app = modal.App("app-name")
   image = modal.Image.debian_slim().pip_install("requests", "openai", "etc")

   @app.function(
       image=image,
       secrets=[modal.Secret.from_name("secret-name")],  # MUST match Modal UI name exactly
       schedule=modal.Cron("0 16 * * *")  # Optional: for cron jobs
   )
   def scheduled_function():
       return main_workflow_function()

   @app.web_endpoint(method="POST")  # Optional: for manual triggers
   def manual_trigger():
       return scheduled_function()
   ```
3. **Create secrets in Modal UI** (https://modal.com/secrets):
   - Click "Create Secret"
   - Add environment variables (e.g., `OPENAI_API_KEY`, `SLACK_WEBHOOK`)
   - **CRITICAL**: Note the exact secret name shown in the UI
   - Use that exact name in `modal.Secret.from_name("exact-name")`
4. Deploy: `modal deploy execution/workflow_name.py`
5. Agent provides webhook URL and/or confirms cron schedule
6. Test the deployment with curl or wait for scheduled run

**Common Deployment Issues**:

1. **Secrets not loading** (environment variables return `None`):
   - **Cause**: Secret name in code doesn't match Modal UI
   - **Fix**: Check https://modal.com/secrets for exact name, update `modal.Secret.from_name("exact-name")`
   - **Debug**: Add `print(f"KEY present: {bool(os.getenv('KEY'))}")` temporarily

2. **Missing dependencies**:
   - **Cause**: Forgot to add package to `modal.Image.debian_slim().pip_install(...)`
   - **Fix**: Add all imports to pip_install list, redeploy

3. **Timezone confusion**:
   - **Cause**: Modal cron uses UTC, user thinks in local time
   - **Fix**: Convert local time to UTC (e.g., 8am PT = 16:00 UTC)

4. **Empty responses from reasoning models (GPT-5.1, o1, o3)**:
   - **Cause**: Reasoning models use tokens for internal thinking + output. Low `max_completion_tokens` = all tokens consumed by reasoning
   - **Fix**: Set `max_completion_tokens=4000+` for reasoning models
   - **Debug**: Check `reasoning_tokens` in response object

### Key Files

- `execution/modal_*.py` - Individual Modal deployment scripts with decorators
- Modal secrets stored at https://modal.com/secrets (encrypted, never in code)

### Your Endpoints

Once deployed, your Modal endpoints will look like:
- Webhooks: `https://USERNAME--APP_NAME-FUNCTION_NAME.modal.run`
- View deployments: `https://modal.com/apps`
- View logs: `modal app logs app-name` (or via Modal web UI)

**Observability**: All cloud activity should log to Slack for monitoring. Agent adds logging code automatically.

### Self-Annealing for Modal Deployments

When deployments fail:
1. Check Modal logs for exact error (via CLI or web UI)
2. Fix the issue in code (secrets, dependencies, API parameters)
3. Redeploy with `modal deploy execution/script.py`
4. Update this CLAUDE.md file with the fix in the "Common Deployment Issues" section
5. Update the specific workflow directive (e.g., `directives/daily_ai_news.md`) with workflow-specific learnings

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.

Also, use Opus-4.5 for everything while building. It came out a few days ago and is an order of magnitude better than Sonnet and other models. If you can't find it, look it up first.