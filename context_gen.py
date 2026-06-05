#!/usr/bin/env python3
"""
context-gen: Auto-generate CONTEXT.md for any project.
Uses Gemini Flash (free tier) to summarize your codebase.
"""

import os
import sys
import argparse
from scanner import scan_project
from summarizer import summarize_with_gemini
from writer import preview_and_write


def main():
    parser = argparse.ArgumentParser(
        description="Generate CONTEXT.md for your project using Gemini AI (free)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to project directory (default: current directory)",
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)

    if not os.path.isdir(project_path):
        print(f"❌ Not a directory: {project_path}")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set.")
        print("   Export it: export GEMINI_API_KEY=your_key_here")
        sys.exit(1)

    print(f"📁 Scanning: {project_path}")
    file_contents = scan_project(project_path)

    if not file_contents:
        print("❌ No readable files found.")
        sys.exit(1)

    print(f"✅ Scanned {len(file_contents)} files. Sending to Gemini...")
    context_md = summarize_with_gemini(file_contents, api_key)

    output_path = os.path.join(project_path, "CONTEXT.md")
    preview_and_write(context_md, output_path)


if __name__ == "__main__":
    main()
