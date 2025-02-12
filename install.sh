#!/bin/bash

# Create necessary directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/lib/ai-cli

# Copy files to their locations
cp command_generator.py ~/.local/lib/ai-cli/
cp requirements.txt ~/.local/lib/ai-cli/
cp .env ~/.local/lib/ai-cli/ 2>/dev/null || true

# Create virtual environment if it doesn't exist
if [ ! -d ~/.local/lib/ai-cli/venv ]; then
    echo "Setting up virtual environment..."
    cd ~/.local/lib/ai-cli
    python -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# Create the ai command script
cat > ~/.local/bin/ai << 'EOL'
#!/bin/bash

ai() {
    # Get the directory where the AI CLI is installed
    AI_DIR="$HOME/.local/lib/ai-cli"
    
    if [ $# -eq 0 ]; then
        echo "Usage: ai 'your natural language command description'"
        echo "Example: ai 'install python requirements'"
        return 1
    fi
    
    # Generate the command
    cd "$AI_DIR"  # Change to AI directory to ensure .env is found
    generated_cmd=$("$AI_DIR/venv/bin/python" "$AI_DIR/command_generator.py" "$@")
    cd - > /dev/null  # Return to previous directory
    
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Detect shell type and use appropriate method
    if [ -n "$ZSH_VERSION" ]; then
        # For Zsh
        print -z "$generated_cmd"
    else
        # For Bash
        history -s "$generated_cmd"
        bind '"\e[A": history-search-backward'
        echo "Press Up Arrow to get the command"
    fi
}

# Export the function so it can be used in subshells
export -f ai
EOL

# Make the script executable
chmod +x ~/.local/bin/ai

# Add to shell config if not already there
for config in ~/.zshrc ~/.bashrc; do
    if [ -f "$config" ]; then
        if ! grep -q "source ~/.local/bin/ai" "$config"; then
            echo -e "\n# AI CLI\nsource ~/.local/bin/ai" >> "$config"
        fi
    fi
done

echo "Installation complete! Please restart your terminal or run:"
echo "source ~/.local/bin/ai" 