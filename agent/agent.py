#!/usr/bin/env python3
"""
Daily Reflection Tree - CLI Agent

Walks through a deterministic reflection tree, loading structure from JSON
and guiding the user through questions, decisions, and reflections.

No external dependencies. Python 3.7+ stdlib only.
"""

import json
import os
import sys
from pathlib import Path


class ReflectionState:
    """Tracks user answers and axis signal tallies."""

    def __init__(self):
        self.answers = {}  # node_id -> selected option (1-indexed)
        self.answer_texts = {}  # node_id -> option text
        self.axis_scores = {
            "locus": 0,
            "orientation": 0,
            "radius": 0
        }

    def record_answer(self, node_id: str, option_index: int, option_text: str):
        """Record a user's answer for a question node."""
        self.answers[node_id] = option_index
        self.answer_texts[node_id] = option_text

    def add_signal(self, axis: str, magnitude: int):
        """Add to an axis score. Positive = victor/contribution/altrocentric."""
        if axis in self.axis_scores:
            self.axis_scores[axis] += magnitude

    def get_score(self, axis: str) -> int:
        """Get current score for an axis."""
        return self.axis_scores.get(axis, 0)

    def interpolate(self, text: str) -> str:
        """Replace {nodeId.answer} placeholders with actual answers."""
        result = text
        for node_id, answer_text in self.answer_texts.items():
            placeholder = f"{{{node_id}.answer}}"
            if placeholder in result:
                result = result.replace(placeholder, answer_text)

        # Also interpolate signal results for summary
        for axis, score in self.axis_scores.items():
            # Determine which reflection node was taken
            if axis == "locus":
                victim_key = "{axis1_reflection_victim.signal.result}"
                victor_key = "{axis1_reflection_victor.signal.result}"
                if victim_key in result:
                    result = result.replace(victim_key, "victim" if score < 0 else "victor")
                if victor_key in result:
                    result = result.replace(victor_key, "victor" if score >= 0 else "victim")
            elif axis == "orientation":
                ent_key = "{axis2_reflection_entitlement.signal.result}"
                con_key = "{axis2_reflection_contribution.signal.result}"
                if ent_key in result:
                    result = result.replace(ent_key, "entitlement" if score >= 0 else "contribution")
                if con_key in result:
                    result = result.replace(con_key, "contribution" if score < 0 else "entitlement")
            elif axis == "radius":
                self_key = "{axis3_reflection_self.signal.result}"
                alt_key = "{axis3_reflection_altrocentric.signal.result}"
                if self_key in result:
                    result = result.replace(self_key, "self" if score >= 0 else "altrocentric")
                if alt_key in result:
                    result = result.replace(alt_key, "altrocentric" if score < 0 else "self")

        return result


class ReflectionTree:
    """Loads and navigates a reflection tree from JSON."""

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.nodes = {}  # id -> node dict
        self.start_node = None
        self._load()

    def _load(self):
        """Load tree from JSON file."""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for node in data.get("nodes", []):
            node_id = node.get("id")
            if node_id:
                self.nodes[node_id] = node
                if node.get("type") == "start":
                    self.start_node = node_id

        if not self.start_node:
            raise ValueError("No start node found in tree")

    def get_node(self, node_id: str) -> dict:
        """Get a node by ID."""
        return self.nodes.get(node_id, {})

    def evaluate_decision(self, node: dict, state: ReflectionState) -> str:
        """Evaluate a decision node's condition and return target node."""
        routing = node.get("routing", {})
        condition = routing.get("condition", "")

        # Parse conditions like "locus_score >= 0"
        if ">=" in condition:
            parts = condition.split(">=")
            axis = parts[0].strip().replace("_score", "")
            threshold = int(parts[1].strip())
            score = state.get_score(axis)
            if score >= threshold:
                return routing.get("true", "")
            else:
                return routing.get("false", "")
        elif "<=" in condition:
            parts = condition.split("<=")
            axis = parts[0].strip().replace("_score", "")
            threshold = int(parts[1].strip())
            score = state.get_score(axis)
            if score <= threshold:
                return routing.get("true", "")
            else:
                return routing.get("false", "")
        elif ">" in condition:
            parts = condition.split(">")
            axis = parts[0].strip().replace("_score", "")
            threshold = int(parts[1].strip())
            score = state.get_score(axis)
            if score > threshold:
                return routing.get("true", "")
            else:
                return routing.get("false", "")
        elif "<" in condition:
            parts = condition.split("<")
            axis = parts[0].strip().replace("_score", "")
            threshold = int(parts[1].strip())
            score = state.get_score(axis)
            if score < threshold:
                return routing.get("true", "")
            else:
                return routing.get("false", "")

        # Default: use target
        return node.get("target", "")


def print_markdown(text: str):
    """Print text, preserving markdown-like formatting for console."""
    # Simple markdown rendering for console
    lines = text.split('\n')
    for line in lines:
        # Bold: **text** -> just print as-is (terminal may not support)
        # Headers: # text -> print with emphasis
        stripped = line.lstrip('#').strip()
        if line.startswith('###'):
            print(f"\n  {stripped}")
        elif line.startswith('##'):
            print(f"\n {stripped}")
        elif line.startswith('#'):
            print(f"\n{stripped}")
        elif stripped.startswith('---'):
            print("\n" + "=" * 50)
        else:
            print(line)


def run_reflection(tree: ReflectionTree, state: ReflectionState):
    """Main reflection loop."""
    current_id = tree.start_node

    while current_id:
        node = tree.get_node(current_id)
        node_type = node.get("type", "unknown")
        text = node.get("text", "")
        options = node.get("options", [])
        routing = node.get("routing", {})
        signal = node.get("signal")

        # Clear screen for each step (optional, comment out if unwanted)
        # os.system('cls' if os.name == 'nt' else 'clear')

        print("\n" + "=" * 60 + "\n")

        # Interpolate any placeholders in the text
        display_text = state.interpolate(text)

        if node_type == "start":
            print_markdown(display_text)
            input()  # Wait for Enter
            current_id = node.get("target", "")

        elif node_type == "question":
            print_markdown(display_text)
            print()

            # Display options
            for i, opt in enumerate(options, 1):
                print(f"  [{i}] {opt}")

            print()

            # Get valid input
            while True:
                try:
                    user_input = input("Your choice (1-{}): ".format(len(options))).strip()
                    choice = int(user_input)
                    if 1 <= choice <= len(options):
                        break
                    print(f"Please enter a number between 1 and {len(options)}.")
                except ValueError:
                    print("Please enter a valid number.")

            # Record answer
            selected_option = options[choice - 1]
            state.record_answer(current_id, choice, selected_option)

            # Add signal if present
            if signal:
                axis = signal.get("axis")
                magnitude = signal.get("magnitude", 1)
                if axis:
                    state.add_signal(axis, magnitude)

            # Follow routing
            key = str(choice)
            if key in routing:
                current_id = routing[key]
            else:
                current_id = node.get("target", "")

        elif node_type == "decision":
            # Decision nodes auto-advance based on conditions
            next_id = tree.evaluate_decision(node, state)
            current_id = next_id

        elif node_type in ("reflection", "bridge"):
            print_markdown(display_text)
            print()
            input("Press Enter to continue...")

            # Use routing or target
            if routing:
                # Take first routing option (usually "1")
                current_id = routing.get("1", node.get("target", ""))
            else:
                current_id = node.get("target", "")

        elif node_type == "summary":
            print_markdown(display_text)
            print()
            input("Press Enter to finish...")
            current_id = node.get("target", "")

        elif node_type == "end":
            print_markdown(display_text)
            print()
            break

        else:
            # Unknown node type, try to use target
            current_id = node.get("target", "")

    return state


def main():
    """Entry point."""
    # Find tree JSON - check relative paths then default
    tree_path = None

    # Check command line arg
    if len(sys.argv) > 1:
        tree_path = sys.argv[1]
    else:
        # Try common locations
        candidates = [
            Path(__file__).parent.parent / "tree" / "reflection-tree.json",
            Path(__file__).parent / "tree" / "reflection-tree.json",
            Path("tree") / "reflection-tree.json",
            Path("../tree") / "reflection-tree.json",
        ]
        for candidate in candidates:
            if candidate.exists():
                tree_path = str(candidate)
                break

    if not tree_path or not Path(tree_path).exists():
        print("Error: Could not find reflection-tree.json")
        print("Usage: python agent.py <path-to-tree-json>")
        sys.exit(1)

    print()
    print("=" * 60)
    print("  DAILY REFLECTION TREE")
    print("=" * 60)
    print(f"  Loading tree from: {tree_path}")
    print("=" * 60)

    try:
        tree = ReflectionTree(tree_path)
        state = ReflectionState()
        run_reflection(tree, state)

        print("\n" + "=" * 60)
        print("Session complete.")
        print("=" * 60 + "\n")

    except json.JSONDecodeError as e:
        print(f"Error parsing tree JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running reflection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
