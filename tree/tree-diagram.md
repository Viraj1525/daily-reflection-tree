# Daily Reflection Tree - Visual Diagram

## Flow Diagram

```mermaid
flowchart TD
    START([START]) --> A1Q1[axis1_q1: Locus Opening]
    
    %% Axis 1 Questions
    A1Q1 -->|"Option 1"| A1Q2a[axis1_q2a: Fantasy vs Reach]
    A1Q1 -->|"Option 2"| A1Q2b[axis1_q2b: External Pull]
    A1Q1 -->|"Option 3"| A1Q2c[axis1_q2c: Ratio in Arena]
    A1Q1 -->|"Option 4"| A1Q2d[axis1_q2d: Ripple Effects]
    
    %% All Axis 1 Q2s lead to decision
    A1Q2a --> D1[axis1_decision]
    A1Q2b --> D1
    A1Q2c --> D1
    A1Q2d --> D1
    
    %% Axis 1 Decision branches
    D1 -->|"locus_score < 0"| R1V[axis1_reflection_victim]
    D1 -->|"locus_score >= 0"| R1Vic[axis1_reflection_victor]
    
    %% Both reflections converge
    R1V --> A2Q3[axis2_q3: Orientation Opening]
    R1Vic --> A2Q3
    
    %% Axis 2 Questions
    A2Q3 -->|"Option 1"| A2Q4a[axis2_q4a: Earned It]
    A2Q3 -->|"Option 2"| A2Q4b[axis2_q4b: Doubt Deserving]
    A2Q3 -->|"Option 3"| A2Q4c[axis2_q4c: Guilt]
    A2Q3 -->|"Option 4"| A2Q4d[axis2_q4d: Pass Forward]
    
    %% All Axis 2 Q2s lead to decision
    A2Q4a --> D2[axis2_decision]
    A2Q4b --> D2
    A2Q4c --> D2
    A2Q4d --> D2
    
    %% Axis 2 Decision branches
    D2 -->|"orientation_score < 0"| R2C[axis2_reflection_contribution]
    D2 -->|"orientation_score >= 0"| R2E[axis2_reflection_entitlement]
    
    %% Both reflections converge
    R2C --> A3Q5[axis3_q5: Radius Opening]
    R2E --> A3Q5
    
    %% Axis 3 Questions
    A3Q5 -->|"Option 1"| A3Q6a[axis3_q6a: Self-First]
    A3Q5 -->|"Option 2"| A3Q6b[axis3_q6b: Bounded Circle]
    A3Q5 -->|"Option 3"| A3Q6c[axis3_q6c: Relational Us]
    A3Q5 -->|"Option 4"| A3Q6d[axis3_q6d: Wide Ripple]
    
    %% All Axis 3 Q2s lead to decision
    A3Q6a --> D3[axis3_decision]
    A3Q6b --> D3
    A3Q6c --> D3
    A3Q6d --> D3
    
    %% Axis 3 Decision branches
    D3 -->|"radius_score < 0"| R3A[axis3_reflection_altrocentric]
    D3 -->|"radius_score >= 0"| R3S[axis3_reflection_self]
    
    %% Both reflections converge
    R3A --> BR1[bridge1: Synthesis Bridge]
    R3S --> BR1
    
    %% Bridge to Summary to End
    BR1 --> SUM[summary: Profile Summary]
    SUM --> END([END])
    
    %% Styling
    classDef startEnd fill:#1a1a2e,color:#fff,stroke:#0f0f23
    classDef question fill:#16213e,color:#fff,stroke:#0f3460
    classDef decision fill:#533483,color:#fff,stroke:#2d1b4e
    classDef reflection fill:#0f3460,color:#fff,stroke:#16213e
    classDef bridge fill:#e94560,color:#fff,stroke:#c73e54
    classDef summary fill:#00b894,color:#fff,stroke:#00a884
    
    class START,END startEnd
    class A1Q1,A1Q2a,A1Q2b,A1Q2c,A1Q2d,A2Q3,A2Q4a,A2Q4b,A2Q4c,A2Q4d,A3Q5,A3Q6a,A3Q6b,A3Q6c,A3Q6d question
    class D1,D2,D3 decision
    class R1V,R1Vic,R2E,R2C,R3S,R3A reflection
    class BR1 bridge
    class SUM summary
```

## Node Inventory

| Node ID | Type | Axis | Description |
|---------|------|------|-------------|
| start | start | - | Entry point |
| axis1_q1 | question | Locus | Opening locus question |
| axis1_q2a | question | Locus | Follow-up for external option |
| axis1_q2b | question | Locus | Follow-up for mixed option |
| axis1_q2c | question | Locus | Follow-up for internal option |
| axis1_q2d | question | Locus | Follow-up for strong internal |
| axis1_decision | decision | Locus | Routes by locus_score |
| axis1_reflection_victim | reflection | Locus | External locus reflection |
| axis1_reflection_victor | reflection | Locus | Internal locus reflection |
| axis2_q3 | question | Orientation | Opening orientation question |
| axis2_q4a | question | Orientation | Follow-up for entitlement |
| axis2_q4b | question | Orientation | Follow-up for doubt |
| axis2_q4c | question | Orientation | Follow-up for guilt |
| axis2_q4d | question | Orientation | Follow-up for contribution |
| axis2_decision | decision | Orientation | Routes by orientation_score |
| axis2_reflection_entitlement | reflection | Orientation | Entitlement reflection |
| axis2_reflection_contribution | reflection | Orientation | Contribution reflection |
| axis3_q5 | question | Radius | Opening radius question |
| axis3_q6a | question | Radius | Follow-up for self-first |
| axis3_q6b | question | Radius | Follow-up for bounded circle |
| axis3_q6c | question | Radius | Follow-up for relational |
| axis3_q6d | question | Radius | Follow-up for expansive |
| axis3_decision | decision | Radius | Routes by radius_score |
| axis3_reflection_self | reflection | Radius | Self-centric reflection |
| axis3_reflection_altrocentric | reflection | Radius | Altrocentric reflection |
| bridge1 | bridge | - | Synthesis transition |
| summary | summary | - | Final profile with interpolation |
| end | end | - | Terminal node |

## Path Statistics

- **Total Nodes:** 28
- **Questions:** 13 (4+ per axis including opening)
- **Decision Nodes:** 3
- **Reflection Nodes:** 6
- **Bridge Nodes:** 1
- **Summary Nodes:** 1
- **Start/End Nodes:** 2

## Possible Paths

The tree supports 64 unique paths from start to end:
- 4 options at axis1_q1 × 4 options at each axis1_q2× = 16 paths to Axis 1 decision
- 2 branches from Axis 1 decision × 4 options at axis2_q3 × 4 options at each axis2_q4× = 32 paths to Axis 2 decision
- 2 branches from Axis 2 decision × 4 options at axis3_q5 × 4 options at each axis3_q6× = 64 total unique paths

Each path produces a unique combination of:
1. Locus orientation (victim/victor)
2. Orientation framing (entitlement/contribution)
3. Radius scope (self/altrocentric)

## Signal System

Each question node emits signals that accumulate:
- `axis`: Which axis (locus, orientation, radius)
- `direction`: Which pole (internal/external, entitlement/contribution, self/altrocentric)
- `magnitude`: Weight (-1, 0, 1, 2)

Decision nodes evaluate accumulated scores:
- `locus_score >= 0` → victor path
- `orientation_score >= 0` → entitlement path
- `radius_score >= 0` → self path
