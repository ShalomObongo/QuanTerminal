#!/usr/bin/env python3

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ContextAnalyzer:
    """Analyzes the current directory context for better command generation."""

    def __init__(self, directory: str = "."):
        self.directory = Path(directory).resolve()
        self.context_cache = {}

    def get_project_type(self) -> Dict[str, float]:
        """
        Detect project type based on files and return confidence scores.
        Example: {"nodejs": 0.9, "python": 0.2}
        """
        if "project_type" in self.context_cache:
            return self.context_cache["project_type"]

        scores = {}
        
        # Node.js indicators
        if (self.directory / "package.json").exists():
            scores["nodejs"] = 0.9
            if (self.directory / "node_modules").exists():
                scores["nodejs"] = 1.0
        
        # Python indicators
        if list(self.directory.glob("*.py")) or (self.directory / "requirements.txt").exists():
            scores["python"] = 0.8
            if (self.directory / "venv").exists() or (self.directory / ".venv").exists():
                scores["python"] = 1.0
        
        # Docker indicators
        if (self.directory / "Dockerfile").exists() or list(self.directory.glob("docker-compose*.yml")):
            scores["docker"] = 0.9
        
        # Rust indicators
        if (self.directory / "Cargo.toml").exists():
            scores["rust"] = 1.0
        
        # Go indicators
        if (self.directory / "go.mod").exists():
            scores["go"] = 1.0
        
        self.context_cache["project_type"] = scores
        return scores

    def get_git_context(self) -> Optional[Dict[str, str]]:
        """
        Get Git repository status and context.
        Returns None if not a Git repository.
        """
        if "git_context" in self.context_cache:
            return self.context_cache["git_context"]

        try:
            # Check if it's a git repository
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                cwd=self.directory
            )
            if result.returncode != 0:
                return None

            context = {}
            
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.directory
            )
            context["branch"] = result.stdout.strip()
            
            # Get status summary
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.directory
            )
            status_output = result.stdout.strip().split("\n")
            
            # Parse status
            context["modified"] = len([l for l in status_output if l.startswith(" M") or l.startswith("M ")])
            context["untracked"] = len([l for l in status_output if l.startswith("??")])
            context["staged"] = len([l for l in status_output if l.startswith("A ") or l.startswith("M ")])
            
            # Get remote information
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                cwd=self.directory
            )
            context["has_remote"] = bool(result.stdout.strip())

            self.context_cache["git_context"] = context
            return context

        except subprocess.SubprocessError:
            return None

    def get_shell_context(self) -> Dict[str, str]:
        """Get relevant environment variables and aliases."""
        if "shell_context" in self.context_cache:
            return self.context_cache["shell_context"]

        context = {
            "shell": os.environ.get("SHELL", ""),
            "path": os.environ.get("PATH", ""),
            "home": os.environ.get("HOME", ""),
            "user": os.environ.get("USER", ""),
            "term": os.environ.get("TERM", ""),
        }

        # Get aliases (if possible)
        try:
            if context["shell"].endswith("zsh"):
                result = subprocess.run(
                    ["zsh", "-ic", "alias"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    context["aliases"] = result.stdout.strip()
            elif context["shell"].endswith("bash"):
                result = subprocess.run(
                    ["bash", "-ic", "alias"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    context["aliases"] = result.stdout.strip()
        except subprocess.SubprocessError:
            context["aliases"] = ""

        self.context_cache["shell_context"] = context
        return context

    def get_compact_context(self) -> str:
        """
        Get a compact context string suitable for AI prompt without exceeding token limits.
        Returns a concise string with the most relevant context information.
        """
        context_parts = []
        
        # Project type context
        project_types = self.get_project_type()
        if project_types:
            main_type = max(project_types.items(), key=lambda x: x[1])
            if main_type[1] > 0.7:  # Only include if confidence is high
                context_parts.append(f"Project type: {main_type[0]}")
        
        # Git context
        git_context = self.get_git_context()
        if git_context:
            git_status = []
            if git_context["modified"]:
                git_status.append(f"{git_context['modified']} modified")
            if git_context["untracked"]:
                git_status.append(f"{git_context['untracked']} untracked")
            if git_context["staged"]:
                git_status.append(f"{git_context['staged']} staged")
            if git_status:
                context_parts.append(f"Git: {', '.join(git_status)} files")
            context_parts.append(f"Branch: {git_context['branch']}")
        
        # Shell context (minimal)
        shell_context = self.get_shell_context()
        shell_name = os.path.basename(shell_context["shell"])
        context_parts.append(f"Shell: {shell_name}")
        
        return " | ".join(context_parts)

def main():
    """CLI interface for testing the context analyzer."""
    analyzer = ContextAnalyzer()
    
    print("\n=== Project Type ===")
    print(json.dumps(analyzer.get_project_type(), indent=2))
    
    print("\n=== Git Context ===")
    git_context = analyzer.get_git_context()
    print(json.dumps(git_context, indent=2) if git_context else "Not a Git repository")
    
    print("\n=== Shell Context ===")
    print(json.dumps(analyzer.get_shell_context(), indent=2))
    
    print("\n=== Compact Context ===")
    print(analyzer.get_compact_context())

if __name__ == "__main__":
    main() 