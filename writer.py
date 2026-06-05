"""
writer.py: Show preview of generated CONTEXT.md and confirm before writing.
"""

import os


def preview_and_write(content: str, output_path: str):
    print("\n" + "=" * 60)
    print("📄 PREVIEW — CONTEXT.md")
    print("=" * 60)
    print(content)
    print("=" * 60)

    existing = os.path.exists(output_path)
    if existing:
        prompt = "\n⚠️  CONTEXT.md already exists. Overwrite? [y/N]: "
    else:
        prompt = "\n✅ Write CONTEXT.md to project? [y/N]: "

    answer = input(prompt).strip().lower()

    if answer == "y":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Written: {output_path}")

        next_task = input(
            "\n📝 What are you working on right now? (press Enter to skip): "
        ).strip()
        if next_task:
            with open(output_path, "r", encoding="utf-8") as f:
                md = f.read()
            md = md.replace(
                "## Next Task\n⬅️ FILL THIS IN MANUALLY — what are you working on right now?",
                f"## Next Task\n{next_task}",
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)
            print("✅ Next Task updated.")
        else:
            print(
                "💡 Tip: Fill in '## Next Task' in CONTEXT.md before switching AI agents."
            )
    else:
        print("❌ Cancelled. Nothing written.")
