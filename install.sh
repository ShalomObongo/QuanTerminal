#!/bin/bash

# Create necessary directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/lib/ai-cli/functions

# Copy files to their locations
cp command_generator.py context_analyzer.py ~/.local/lib/ai-cli/
cp requirements.txt ~/.local/lib/ai-cli/
cp .env ~/.local/lib/ai-cli/ 2>/dev/null || true

# Create virtual environment if it doesn't exist
if [ ! -d ~/.local/lib/ai-cli/venv ]; then
    echo "Setting up virtual environment..."
    cd ~/.local/lib/ai-cli
    python -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# Create the ai function file for Zsh (name must match function name)
cat > ~/.local/lib/ai-cli/functions/ai << 'EOL'
# Get the directory where the AI CLI is installed
AI_DIR="$HOME/.local/lib/ai-cli"

if [ $# -eq 0 ]; then
    echo "Usage: ai 'your natural language command description'"
    echo "Example: ai 'install python requirements'"
    return 1
fi

# Store current directory to restore it later
CURRENT_DIR="$PWD"

# Generate the command (passing current directory as argument)
cd "$AI_DIR"  # Change to AI directory to ensure .env is found
generated_cmd=$("$AI_DIR/venv/bin/python" "$AI_DIR/command_generator.py" --dir "$CURRENT_DIR" "$@")
cd "$CURRENT_DIR"  # Return to original directory

if [ $? -ne 0 ]; then
    return 1
fi

# Use Zsh's print -z to put the command in the buffer
print -z "$generated_cmd"
EOL

# Create the ai command script for Bash
cat > ~/.local/lib/ai-cli/ai.bash << 'EOL'
# Define the function without displaying it
function ai {
    # Get the directory where the AI CLI is installed
    AI_DIR="$HOME/.local/lib/ai-cli"
    
    if [ $# -eq 0 ]; then
        echo "Usage: ai 'your natural language command description'"
        echo "Example: ai 'install python requirements'"
        return 1
    fi
    
    # Store current directory to restore it later
    CURRENT_DIR="$PWD"
    
    # Generate the command (passing current directory as argument)
    cd "$AI_DIR"  # Change to AI directory to ensure .env is found
    generated_cmd=$("$AI_DIR/venv/bin/python" "$AI_DIR/command_generator.py" --dir "$CURRENT_DIR" "$@")
    cd "$CURRENT_DIR"  # Return to original directory
    
    if [ $? -ne 0 ]; then
        return 1
    fi

    # For Bash
    history -s "$generated_cmd"
    bind '"\e[A": history-search-backward'
    echo "Press Up Arrow to get the command"
}
EOL

# Remove old configuration
for config in ~/.zshrc ~/.bashrc; do
    if [ -f "$config" ]; then
        sed -i.bak '/^# AI CLI$/d' "$config"
        sed -i.bak '/^source ~\/.local\/bin\/ai/d' "$config"
        sed -i.bak '/^source.*ai\.zsh/d' "$config"
        sed -i.bak '/^source.*ai\.bash/d' "$config"
        sed -i.bak '/^fpath=.*ai-cli/d' "$config"
        sed -i.bak '/^autoload.*ai/d' "$config"
        rm -f "${config}.bak"
    fi
done

# Add new configuration
if [ -f ~/.zshrc ]; then
    echo "# AI CLI" >> ~/.zshrc
    echo "fpath=(~/.local/lib/ai-cli/functions \$fpath)" >> ~/.zshrc
    echo "autoload -Uz ai" >> ~/.zshrc
fi

if [ -f ~/.bashrc ]; then
    echo "# AI CLI" >> ~/.bashrc
    echo "source ~/.local/lib/ai-cli/ai.bash" >> ~/.bashrc
fi

# Make the Zsh function file executable
chmod +x ~/.local/lib/ai-cli/functions/ai

echo "Installation complete! Please restart your terminal or run:"
if [ -n "$ZSH_VERSION" ]; then
    echo "fpath=(~/.local/lib/ai-cli/functions \$fpath) && autoload -Uz ai"
else
    echo "source ~/.local/lib/ai-cli/ai.bash"
fi 