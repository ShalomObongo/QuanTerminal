#!/bin/bash

ai() {
    if [ $# -eq 0 ]; then
        echo "Usage: ai 'your natural language command description'"
        echo "Example: ai 'install python requirements'"
        return 1
    fi

    # Get the directory where this script is located
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    # Check if virtual environment exists
    if [ ! -d "$SCRIPT_DIR/venv" ]; then
        echo "⚠️  Virtual environment not found. Setting up..."
        cd "$SCRIPT_DIR"  # Change to script directory before creating venv
        python -m venv venv
        ./venv/bin/pip install -r requirements.txt
        cd - > /dev/null  # Return to previous directory
    fi
    
    # Generate the command
    cd "$SCRIPT_DIR"  # Change to script directory to ensure .env is found
    generated_cmd=$("$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/command_generator.py" "$@")
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