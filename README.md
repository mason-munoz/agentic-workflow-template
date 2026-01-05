# Client Template - 3-Layer Agent Architecture

This is a template workspace for deploying AI-powered workflows using a 3-layer architecture that separates probabilistic LLM decisions from deterministic code execution.

## Quick Start

1. **Clone this template for each new client:**
   ```bash
   git clone <this-repo> client_name
   cd client_name
   ```

2. **Set up environment:**
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies as needed
   pip install -r requirements.txt  # Create this file as you add dependencies
   ```

3. **Configure credentials:**
   - Edit `.env` with your API keys
   - Add `credentials.json` and `token.json` for Google OAuth (if needed)
   - These files are gitignored for security

4. **Start building:**
   - Create directives in `directives/` to define workflows
   - Create Python scripts in `execution/` for deterministic operations
   - Let your AI agent (Claude, Gemini, etc.) orchestrate between them

## Architecture Overview

### 3 Layers

1. **Directives** (`directives/`) - SOPs in Markdown defining what to do
2. **Orchestration** - AI agents make decisions, route tasks, handle errors
3. **Execution** (`execution/`) - Deterministic Python scripts do the work

### Directory Structure

```
.
├── CLAUDE.md          # Agent instructions for Claude
├── GEMINI.md          # Agent instructions for Gemini
├── AGENTS.md          # Agent instructions for other AI systems
├── .env               # Environment variables (gitignored)
├── .gitignore         # Excludes secrets and temp files
├── directives/        # Workflow SOPs in Markdown
├── execution/         # Deterministic Python scripts
└── .tmp/              # Temporary/intermediate files (gitignored)
```

### File Organization Principles

- **Deliverables** live in cloud services (Google Sheets, Slides, etc.)
- **Intermediates** go in `.tmp/` and can be regenerated
- **Secrets** stay in `.env`, `credentials.json`, `token.json` (all gitignored)
- **Instructions** are in directive files (version controlled)
- **Tools** are Python scripts in `execution/` (version controlled)

## Workflow

1. **Define** the workflow in a directive (`directives/workflow_name.md`)
2. **Build** deterministic tools in Python (`execution/workflow_name.py`)
3. **Test** locally until it works reliably
4. **Deploy** to Modal for webhooks or cron jobs (optional)

## Deployment to Modal (Optional)

For production workflows that need to run on a schedule or be triggered via webhooks:

```bash
# One-time setup
pip install modal
modal token new

# Deploy a script
modal deploy execution/workflow_name.py
```

See [CLAUDE.md](CLAUDE.md) for detailed Modal deployment instructions.

## Operating Principles

1. **Check for existing tools** before creating new scripts
2. **Self-anneal when things break** - fix, test, update directives
3. **Keep directives updated** as you learn about API limits, edge cases, etc.

## Getting Help

- Read [CLAUDE.md](CLAUDE.md), [GEMINI.md](GEMINI.md), or [AGENTS.md](AGENTS.md) for full agent instructions
- Review existing directives in `directives/` for workflow examples
- Check `execution/` scripts to see how tools are structured

## License

Configure for your needs.
