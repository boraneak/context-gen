"""
summarizer.py: Send scanned files to Gemini Flash and get a CONTEXT.md back.
"""

import json
import urllib.request
import urllib.error

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-lite:generateContent"
)

SYSTEM_PROMPT = """You are a senior software engineer. 
Given a set of project files, generate a concise CONTEXT.md file.

The CONTEXT.md must follow this EXACT structure (keep the headers):

# Project Context

## What This App Does
(2-3 sentences. What problem does it solve? Who is it for?)

## Tech Stack
(Bullet list: language, framework, database, infra tools detected)

## Project Structure
(Key files/folders and what they do — only the important ones)

## What's Already Built
(Checklist of features/components that clearly exist in the code)

## Currently In Progress
(Any TODOs, half-finished files, or incomplete features you can detect)

## Next Task
⬅️ FILL THIS IN MANUALLY — what are you working on right now?

## How to Run
(Commands to install deps and run the project, inferred from config files)

---
Be concise. This file will be pasted to AI agents to resume work instantly.
Do NOT add any explanation outside the markdown structure above.
"""


def build_prompt(file_contents: list[dict]) -> str:
    parts = []
    for f in file_contents:
        parts.append(f"### FILE: {f['path']}\n```\n{f['content']}\n```")
    return "\n\n".join(parts)


def summarize_with_gemini(file_contents: list[dict], api_key: str) -> str:
    user_prompt = build_prompt(file_contents)

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048,
        },
    }

    url = GEMINI_API_URL
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")

    try:
        return body["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response format: {body}")
