# context-gen

Auto-generate `CONTEXT.md` for any project using **Gemini Flash (free tier)**.

Paste `CONTEXT.md` to any AI agent (Claude, ChatGPT, Gemini, Mistral) to resume work instantly — no re-explaining, no lost context.

## Why

- Claude, ChatGPT, Gemini all have token/daily limits
- When you hit a limit, you lose context and waste time re-explaining
- This tool generates a single file any AI can read to get up to speed in seconds

## Requirements

- Python 3.8+
- A free Gemini API key → https://aistudio.google.com/app/apikey

## Install

```bash
git clone https://github.com/boraneak/context-gen.git
cd context-gen
bash setup.sh
```

Then add your API key permanently:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GEMINI_API_KEY=your_key_here
export PATH="$HOME/.local/bin:$PATH"
```

```bash
source ~/.zshrc
```

## Usage

```bash
# Inside any project
cd my-project
context-gen

# Or point to a project
context-gen /path/to/project
```

It will:
1. Scan all your code files (skips node_modules, .git, venv, etc.)
2. Send to Gemini Flash (free)
3. Show you a preview
4. Ask to confirm before writing `CONTEXT.md`
5. Ask what you're working on — injects it as `## Next Task` automatically

## When to use

- Before switching to another AI agent
- After a long session — update the context
- When onboarding a new AI to your project

## The only manual step

When you run `context-gen`, it will ask:

```
📝 What are you working on right now? (press Enter to skip):
```

Type your current task — it gets injected into `CONTEXT.md` automatically.
This is the one thing Gemini can't know — your intention.

## Multi-agent rotation strategy

| Agent | Free Tier | Best For |
|---|---|---|
| Claude.ai | Daily limit | Architecture, complex reasoning |
| ChatGPT (GPT-4o) | Limited/day | Code generation |
| Gemini | Very generous | Long context, big files |
| Mistral Le Chat | Very generous | Fast code, no daily limit feel |
| Phind | Free | Dev-focused search + code |

When one cuts you off → run `context-gen` → paste `CONTEXT.md` to the next agent → keep building.
