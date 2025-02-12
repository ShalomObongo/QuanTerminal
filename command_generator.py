#!/usr/bin/env python3

import os
import sys
import argparse
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from context_analyzer import ContextAnalyzer

def load_environment():
    """Load environment variables from .env files"""
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    # First try the current directory
    for env_file in env_files:
        env_path = Path('.') / env_file
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            break
    
    # If not found, try the parent directory (workspace root)
    if not env_loaded:
        for env_file in env_files:
            env_path = Path('..') / env_file
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
                env_loaded = True
                break
    
    return env_loaded

def print_setup_instructions():
    """Print instructions for setting up the Groq API key"""
    print("\n❌ GROQ_API_KEY not found in environment variables!", file=sys.stderr)
    print("\nTo set up the Groq API key:", file=sys.stderr)
    print("1. Get your API key from https://console.groq.com", file=sys.stderr)
    print("2. Create a .env file in the project root:", file=sys.stderr)
    print("3. Add the following line to your .env file:", file=sys.stderr)
    print("\nGROQ_API_KEY=your_api_key_here\n", file=sys.stderr)
    print("Make sure to replace 'your_api_key_here' with your actual Groq API key.", file=sys.stderr)

def create_groq_client():
    """Create and return a Groq client"""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print_setup_instructions()
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return Groq(api_key=api_key)

def generate_command(prompt: str, directory: str = ".") -> str:
    """Generate a terminal command from natural language using Groq"""
    client = create_groq_client()
    
    # Get context information from the specified directory
    analyzer = ContextAnalyzer(directory)
    context = analyzer.get_compact_context()
    
    system_prompt = f"""You are a command line interface that converts natural language into terminal commands.
    Current Context: {context}

    Rules:
    1. Output ONLY the command itself - no explanations, no markdown, no backticks
    2. The command should be a single line that can be directly executed in a terminal
    3. Do not include any formatting or explanatory text
    4. Do not wrap the command in quotes or code blocks
    5. Do not include any newlines in the output
    6. Consider the current context when generating commands:
       - Use project-specific commands when appropriate (npm, pip, etc.)
       - Consider Git status for Git commands
       - Use appropriate paths and environment variables

    Example input: "list all files"
    Example output: ls -la"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert this to a terminal command: {prompt}"}
            ],
            temperature=0.1,  # Low temperature for more deterministic outputs
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n❌ Error generating command: {str(e)}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate terminal commands from natural language')
    parser.add_argument('prompt', nargs='+', help='The natural language command description')
    parser.add_argument('--dir', default=".", help='The directory to analyze for context')
    args = parser.parse_args()
    
    if not load_environment():
        print("⚠️  No .env files found. Looking for environment variables...", file=sys.stderr)
    
    prompt = " ".join(args.prompt)
    command = generate_command(prompt, args.dir)
    
    if command:
        print(command)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 