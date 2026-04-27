# Daily Reflection Tree

A deterministic, non-LLM reflection tool for DeepThought. Guides users through three psychological dimensions via a structured decision tree.

## Quick Start

```bash
python agent/agent.py tree/reflection-tree.json
```

No external dependencies. Python 3.7+ stdlib only.

## Project Structure

```
.
├── README.md                    # This file
├── write-up.md                  # 2-page design rationale
├── tree/
│   ├── reflection-tree.json     # Decision tree (28 nodes)
│   └── tree-diagram.md          # Mermaid visualization
├── agent/
│   └── agent.py                 # CLI runner
└── transcripts/
    ├── persona-1-transcript.md  # Victim/Entitled/Self path
    └── persona-2-transcript.md  # Victor/Contributing/Altrocentric path
```

## The Three Axes

| Axis | Pole A | Pole B | Psychology |
|------|--------|--------|------------|
| **Locus** | Victim (external) | Victor (internal) | Rotter 1954, Dweck 2006 |
| **Orientation** | Entitlement (deserving) | Contribution (gratitude) | Campbell 2004, Organ 1988 |
| **Radius** | Self-centric | Altrocentric | Maslow 1969, Batson 2011 |

## How It Works

1. **Start node** sets tone, invites entry
2. **Question nodes** present 3-5 fixed options, record answers
3. **Decision nodes** evaluate accumulated signals, auto-route
4. **Reflection nodes** mirror patterns using user's own words
5. **Bridge node** transitions to synthesis
6. **Summary node** interpolates full profile
7. **End node** closes session

## Tree Statistics

- **28 nodes** total
- **13 questions** (4+ per axis)
- **3 decision nodes** (one per axis)
- **6 reflection nodes** (2 per axis)
- **1 bridge**, **1 summary**, **2 terminal** nodes
- **64 unique paths** from start to end

## JSON Schema

```json
{
  "id": "unique_node_id",
  "parentId": null,
  "type": "start|question|decision|reflection|bridge|summary|end",
  "text": "Display text with optional {nodeId.answer} interpolation",
  "options": ["Option 1", "Option 2", ...],
  "routing": {
    "1": "next_node_id",
    "condition": "axis_score >= 0",
    "true": "target_if_true",
    "false": "target_if_false"
  },
  "signal": {
    "axis": "locus|orientation|radius",
    "direction": "internal|external",
    "magnitude": 1
  },
  "target": "fallback_node_id"
}
```

## Running Transcripts

To generate a transcript without interaction:

```bash
# Persona 1 path (victim/entitled/self)
python agent/agent.py tree/reflection-tree.json < inputs/persona1.txt

# Persona 2 path (victor/contribution/altrocentric)
python agent/agent.py tree/reflection-tree.json < inputs/persona2.txt
```

## Design Principles

1. **No LLM at runtime** - All paths predetermined, fully auditable
2. **No free text** - Fixed options enable deterministic routing
3. **Wise colleague tone** - No moralizing, shaming, or diagnosis
4. **Interpolation over generation** - Personalization via `{nodeId.answer}` syntax
5. **Signal accumulation** - Decisions based on tallied responses, not single answers

## License

MIT
