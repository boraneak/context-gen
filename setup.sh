#!/usr/bin/env bash
# setup.sh — Install context-gen as a global CLI command
# Usage: bash setup.sh

set -e

INSTALL_DIR="$HOME/.local/bin"
TOOL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📦 Installing context-gen..."

# Make sure ~/.local/bin exists
mkdir -p "$INSTALL_DIR"

# Create the wrapper script
cat > "$INSTALL_DIR/context-gen" << EOF
#!/usr/bin/env bash
python3 "$TOOL_DIR/context_gen.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/context-gen"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  Add this to your ~/.zshrc or ~/.bashrc:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "   Then run: source ~/.zshrc"
fi

echo ""
echo "✅ Installed! Now set your Gemini API key:"
echo "   export GEMINI_API_KEY=your_key_here"
echo ""
echo "   Add that line to ~/.zshrc to make it permanent."
echo ""
echo "🚀 Usage:"
echo "   cd your-project"
echo "   context-gen"
echo ""
echo "   Or point to a specific project:"
echo "   context-gen /path/to/your/project"
