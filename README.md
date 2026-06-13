# Solution Architecture Diagram Skill

**Author:** Arvind Radhakrishnen  
**Primary output:** PNG architecture diagram  
**Editable outputs:** Draw.io XML (`.drawio`) and normalized JSON when appropriate  
**Primary renderer:** Agents365 Draw.io skill  
**Input modes:** Text-first, with optional supporting images  
**Use from:** VS Code, ChatGPT, Google Gemini, Claude, Cursor, or any agent interface that can read a skill folder and run local scripts.

---

## What this skill does

This skill helps a user describe a solution in **plain text** and optionally attach **supporting images** such as rough sketches, whiteboard photos, sample layouts, or reference architecture screenshots.

The skill then:

1. interprets the user's request
2. normalizes it into architecture JSON internally
3. selects the best layout family
4. uses the bundled reference architecture diagrams **internally** as layout guidance
5. generates a Draw.io-ready prompt
6. produces a **PNG architecture diagram**
7. produces editable **Draw.io XML / `.drawio`** and/or normalized JSON as appropriate
8. if needed, produces **additional level-2 diagrams** that expand the main capabilities and sub-capabilities from the first diagram

---

## Core behavior requirements

The skill must generate diagrams so that:
- **text is wrapped inside boxes**
- **labels do not overflow outside boxes**
- **text does not overlap other boxes**
- **boxes and connectors remain readable**
- **the main diagram stays executive-friendly**
- **additional deeper diagrams are generated when needed** to expand capability groups

If a requested architecture is too dense for a single page, the skill should:
1. generate a clean **Level 1** overview diagram
2. generate one or more **Level 2** expansion diagrams for major capabilities or domains
3. return all PNG and Draw.io files

---

## What users provide

### Preferred input
A simple text request describing what they want to build.

Example:

```text
Build a solution architecture diagram for a policy-as-spec governance platform.
Architects author YAML or JSON controls. A control plane resolves them.
CI/CD pipelines enforce them. Deployments target AWS, Azure, and GCP.
Include evidence ledger, drift detection, and waiver governance.
If needed, generate additional deeper diagrams for capabilities.
```

### Optional image input
Users may also attach images such as:
- hand-drawn sketches
- screenshots of rough architecture notes
- reference slides
- whiteboard diagrams
- component lists shown in an image

Images are **optional** and are treated as supporting context only.

---

## What the skill should do automatically

The skill should work with **text alone**, and use images only if provided.

It should:
- infer the best layout from the request
- use bundled reference architecture diagrams internally for layout style selection
- keep text wrapped inside containers
- avoid overlapping text and boxes
- split dense content into multiple diagrams when needed
- avoid asking the user for evaluation criteria or extra technical metadata
- ask follow-up questions only if the request is too incomplete to produce a meaningful diagram
- keep labels concise and presentation-ready
- return the generated files directly

---

## Reference layouts are internal

The bundled reference architecture diagrams are included to guide layout selection and information organization.

They are used **internally** by the skill to decide:
- how to arrange layers and boxes
- whether the best layout is a value chain, data platform, endpoint management map, cloud microservices map, or composite AI platform
- how to group inputs, outputs, central platform zones, and cross-cutting controls
- when to decompose the architecture into multiple pages

The skill should **not** ask the user to interpret those internal reference diagrams.

---

## Supported output pattern

A completed run may return one or more files:

### Minimum
- `solution_architecture_overview.png`
- `solution_architecture_overview.drawio`

### If deeper expansion is needed
- `solution_architecture_capability_01.png`
- `solution_architecture_capability_01.drawio`
- `solution_architecture_capability_02.png`
- `solution_architecture_capability_02.drawio`
- and so on

The first diagram should remain the **overview / Level 1** diagram.
Additional diagrams should expand key capabilities to **Level 2** detail.

---

## Supported layout types

| Template | Best for |
|---|---|
| `platform_value_chain` | Product overviews, AI platforms, capability chains, input → platform → output diagrams |
| `composite_ai_platform` | Agentic AI platforms, reusable solution maps, enterprise AI capability maps |
| `cloud_tenant_microservices` | SaaS platforms, tenant systems, APIs, cloud services, microservices |
| `enterprise_endpoint_management` | Endpoint, identity, compliance, policy, security, app management |
| `cloud_data_platform` | Data platforms, lakehouse, ingestion, governance, analytics, AI/ML delivery |

Reference layouts are documented in `docs/reference_layouts.md` and are for internal guidance.

---


## Single orchestration runner

This package now includes a **single orchestration runner**:

- `run_architecture_skill.py`

The runner coordinates sub-agents for:
- intake
- normalization
- layout selection
- decomposition planning
- overview prompt generation
- Level 2 expansion prompt generation
- packaging / reporting

### Parallel vs sequential execution
The runner supports sub-agent execution with a checkpointed fallback strategy:
- it first checks whether the execution engine can support parallel sub-agent execution
- if parallel execution is available and requested, compatible sub-agents run in parallel
- if parallel execution is not available, or if the probe/checkpoint detects failure, the runner falls back to **sequential execution**

### Shared memory across sub-agents
The runner maintains a shared context file:
- `outputs/<run_name>/run_context.json`

This shared memory is used to pass normalized state, selected layout, decomposition results, and prompt file locations across sub-agents.

### What the runner generates
For each run it creates a run folder such as:

```text
outputs/20250101_120000_solution_name/
├── raw_request.txt
├── draft_input.json
├── prepared_input.json
├── multilevel_plan.json
├── drawio_prompt_overview.md
├── expansion_specs/
├── drawio_prompts/
├── orchestration_report.json
└── run_context.json
```

### Example usage with text input

```bash
python run_architecture_skill.py   --text "Build a solution architecture diagram for a policy-as-spec governance platform with a control plane, CI/CD assurance, and multi-cloud targets."   --allow-parallel
```

### Example usage with a text file

```bash
python run_architecture_skill.py   --text-file examples/request.txt   --allow-parallel
```

### Example usage with JSON input

```bash
python run_architecture_skill.py   --json-input examples/sample_multilevel_input.json   --allow-parallel
```

### Force sequential execution

```bash
python run_architecture_skill.py   --json-input examples/sample_multilevel_input.json   --force-sequential
```

The runner produces the normalized JSON, the multi-level plan, the overview draw.io prompt, and prompt files for any deeper capability expansion diagrams.
It then tells the rendering engine what PNG and `.drawio` outputs should be created.

---

## Quick start from ChatGPT or Gemini

Use a prompt like this:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for:
[describe the solution]

If I attach images, use them as optional supporting context.
Use internal reference architecture layouts automatically.
Ensure all text is wrapped inside boxes and does not overlap with other boxes.
If needed, generate one or more additional level-2 diagrams that expand capabilities and sub-capabilities from the overview.
Return the final PNG diagram(s) and editable Draw.io XML / .drawio file(s) if available.
```

---

## Quick start from VS Code

```bash
unzip architecture_diagram_skill_v5.zip
cd architecture_diagram_skill_v5
```

If using JSON input:

```bash
python prepare_architecture_input.py   --input examples/my_architecture.json   --output outputs/prepared_input.json
python build_drawio_prompt.py   --input outputs/prepared_input.json   --output outputs/drawio_prompt.md
```

Then feed `outputs/drawio_prompt.md` into drawio-skill.

---

## Output files

A completed run should normally produce:

| File | Purpose |
|---|---|
| `outputs/prepared_input.json` | Clean normalized architecture input |
| `outputs/drawio_prompt.md` | Prompt to send to drawio-skill |
| `outputs/solution_architecture_overview.drawio` | Editable Draw.io XML source for Level 1 |
| `outputs/solution_architecture_overview.png` | Level 1 overview diagram |
| `outputs/solution_architecture_capability_*.drawio` | Editable Draw.io XML source for Level 2 expansions |
| `outputs/solution_architecture_capability_*.png` | Level 2 expansion diagrams |

If Draw.io rendering is unavailable, the skill should still return the normalized JSON and drawio prompt so the diagram can be rendered later.

---

## Notes

- The skill is **text-first**.
- Images are **optional**.
- Reference architecture diagrams are used **internally**.
- The skill should **not ask the user for evaluation instructions or extra internal metadata**.
- Labels should remain short, business-readable, and presentation-ready.
- Text must be wrapped within boxes and must not overlap other boxes.
- When the overview would be too dense, generate deeper expansion diagrams automatically.

**Author:** Arvind Radhakrishnen


## Renderer adapter

This package now includes a renderer adapter:
- `render_with_drawio_adapter.py`

It can be used standalone or through `run_architecture_skill.py --render`.

### What it does
- reads the overview and Level 2 prompt files produced by the orchestration runner
- invokes a configurable drawio-skill render command
- writes final `.png` and `.drawio` files into the same run folder
- supports parallel rendering when available, with fallback to sequential mode

### Example standalone usage
```bash
python render_with_drawio_adapter.py   --run-dir outputs/<run_name>   --config examples/renderer_config.json   --dry-run
```

### Example integrated usage
```bash
python run_architecture_skill.py   --json-input examples/sample_multilevel_input.json   --allow-parallel   --render   --renderer-config examples/renderer_config.json
```

### What you may need to approve in your environment
To enable end-to-end rendering, you may need to approve or provide:
1. **installation / availability of the Agents365 drawio-skill**
2. **installation / availability of draw.io desktop / CLI** used by the renderer
3. **the exact local command template** that should invoke rendering in your environment
4. **permission to execute local subprocess commands** from the runner
5. **permission for parallel render jobs** if you want rendering to fan out in parallel

If you do not yet want live rendering, you can still run the adapter in `--dry-run` mode to verify the render plan.


## Enhanced reference asset library

The skill now includes an expanded internal reference asset library with richer metadata.

It captures for each reference:
- layout family
- visual placement primitives
- architectural communication intent
- box placement model
- selection signals
- color palette cues
- recommended use cases

Key files:
- `data/reference_asset_library.json`
- `data/reference_architecture_patterns.json`
- `docs/reference_layouts.md`
- `docs/layout_semantics.md`

The renderer should use these assets internally to pick a layout and a similar color scheme, while keeping the final diagram original.


## Primary layout and palette recommendations

Each run now generates 1-2 recommendations so the user can choose the preferred visual direction.

Each recommendation includes:
- primary layout template
- secondary palette donor
- rationale for the recommendation
- communication intent
- guardrails for text wrapping, spelling, and technology placement

Generated file:
- `layout_recommendations.json`

If the user does not select a recommendation, the runner uses recommendation 1 by default.

## Quality guardrails

The skill includes guardrails to ensure:
- word spelling checks are in place
- canonical technology capitalization is preserved
- technology components are placed in the right architecture zones
- boxes and text are cleanly displayed
- long content is decomposed into Level 2 diagrams when needed

Generated guardrail files include:
- `technology_placement_report.json`
- `layout_recommendations.json`
- optional PNG evaluation report after rendering


## v10 guardrail and output behavior

This version adds stricter visual quality guardrails and a three-variant output pattern.

### Readability and ADA-oriented rendering
The generated diagram prompts require:
- body text at 14 pt or larger
- section headers at 16 pt or larger
- title at 26 pt or larger
- high-contrast text/background combinations
- wrapped text inside boxes
- 8-12 px internal padding so text does not touch borders
- box resizing or Level 2 decomposition instead of shrinking text too far

### Connector guardrails
The diagram prompts require:
- horizontal / vertical orthogonal connectors only
- no diagonal connectors by default
- connectors routed around boxes, not through boxes
- connector labels separated from box labels
- no connector overlap with text, icons, or container interiors

### CIO-ready outcome narrative
Each Level 1 diagram includes a short executive description explaining how the capabilities and sub-capabilities connect to deliver the business outcome.

### Three output variants
Each run prepares three variants:
1. `solution_architecture_variant_01.png` and `.drawio` - recommended enterprise view
2. `solution_architecture_variant_02.png` and `.drawio` - alternate style / palette view
3. `solution_architecture_variant_03.png` and `.drawio` - executive simplified view

### Output policy
User-facing generated outputs should be PNG and Draw.io files only. Evaluation and JSON files are internal/debug artifacts and should not be returned as final outputs. In live rendering mode, the runner can clean internal JSON/report files after rendering unless debug mode is enabled.
