"""
scanner.py: Walk the project directory, skip junk, return readable file contents.
"""

import os

# Directories to completely skip
SKIP_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "eggs",
    ".eggs",
    "htmlcov",
    ".cache",
    "target",
    "vendor",
    ".idea",
    ".vscode",
    "tmp",
    "temp",
    "logs",
    ".terraform",
    ".serverless",
    "site-packages",
}

# File extensions to read
ALLOWED_EXTENSIONS = {
    # Code
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".go",
    ".rs",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".sh",
    ".bash",
    ".zsh",
    # Config / infra
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".env.example",
    ".dockerfile",
    ".tf",
    ".hcl",
    # Docs
    ".md",
    ".txt",
    ".rst",
    # Web
    ".html",
    ".css",
    ".scss",
    # Data
    ".sql",
}

# Files to always skip regardless of extension
SKIP_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "package-lock.json",
    "yarn.lock",
    "poetry.lock",
    "Pipfile.lock",
    ".DS_Store",
    "Thumbs.db",
}

MAX_FILE_SIZE_BYTES = 50_000  # skip files > 50KB (too large, likely generated)
MAX_TOTAL_CHARS = 120_000  # cap total context sent to Gemini


def scan_project(root_path: str) -> list[dict]:
    """
    Walk root_path, collect readable files.
    Returns list of {"path": relative_path, "content": str}
    """
    collected = []
    total_chars = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Prune skip dirs in-place (prevents os.walk from descending)
        dirnames[:] = [
            d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
        ]

        for filename in filenames:
            if filename in SKIP_FILES:
                continue

            _, ext = os.path.splitext(filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                # Also allow files with no extension if they look like config
                if filename not in {"Makefile", "Dockerfile", "Procfile", "Gemfile"}:
                    continue

            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_path)

            # Skip large files
            try:
                size = os.path.getsize(full_path)
                if size > MAX_FILE_SIZE_BYTES:
                    continue
            except OSError:
                continue

            # Read content
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except (OSError, PermissionError):
                continue

            if not content.strip():
                continue

            collected.append({"path": rel_path, "content": content})
            total_chars += len(content)

            if total_chars >= MAX_TOTAL_CHARS:
                print(
                    f"⚠️  Large project — capped at {len(collected)} files to fit Gemini context."
                )
                return collected

    return collected
