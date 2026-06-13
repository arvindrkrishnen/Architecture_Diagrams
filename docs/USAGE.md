# How to Use This Skill

**Author:** Arvind Radhakrishnen

## One-line instruction

```text
Use the Solution Architecture Diagram Skill to create a PNG and editable Draw.io architecture diagram for the solution I describe.
```

## Accepted input
- text description of the solution
- optional supporting images such as sketches, screenshots, or architecture samples

## Important behavior
- text is the main input
- images are optional
- internal reference architecture diagrams are used automatically by the skill
- the skill should not ask for evaluation instructions or other internal metadata
- text must be wrapped inside boxes
- text must not overlap adjacent boxes
- if the overview is too dense, the skill should generate additional Level 2 expansion diagrams

## From ChatGPT or Gemini

Paste:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for:
[describe your solution]

If I attach images, use them as optional supporting context.
Use internal reference architecture layouts automatically.
Ensure text is wrapped inside boxes and does not overlap with other boxes.
If needed, generate one or more Level 2 expansion diagrams.
Return PNG and Draw.io XML / .drawio files if available.
```

## From VS Code

1. Open the folder.
2. Provide a text request through your AI assistant, or use `examples/input_template.json`.
3. If using JSON, run:

```bash
python prepare_architecture_input.py --input examples/my_architecture.json --output outputs/prepared_input.json
python build_drawio_prompt.py --input outputs/prepared_input.json --output outputs/drawio_prompt.md
python plan_multilevel_architecture.py --input outputs/prepared_input.json --output outputs/multilevel_plan.json
```

4. Send `outputs/drawio_prompt.md` to drawio-skill.
5. Save:
   - `outputs/solution_architecture_overview.png`
   - `outputs/solution_architecture_overview.drawio`
   - `outputs/solution_architecture_capability_*.png`
   - `outputs/solution_architecture_capability_*.drawio`

## Expected outputs
- PNG overview file
- Draw.io XML / `.drawio` overview file
- optional Level 2 PNG expansion files
- optional Level 2 Draw.io XML expansion files
- normalized JSON input when appropriate

## Single runner

Use the orchestration runner for a one-command workflow:

```bash
python run_architecture_skill.py --text "Build a solution architecture diagram for an article summary platform." --allow-parallel
```

Or force sequential mode:

```bash
python run_architecture_skill.py --json-input examples/sample_multilevel_input.json --force-sequential
```


## Renderer adapter
Use the renderer adapter after orchestration:

```bash
python render_with_drawio_adapter.py --run-dir outputs/<run_name> --config examples/renderer_config.json --dry-run
```

Or call it through the single runner:

```bash
python run_architecture_skill.py --text-file examples/request.txt --allow-parallel --render --renderer-config examples/renderer_config.json
```


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


## v12 architecture enrichment and multi-view planning
The skill now enriches each architecture request into a canonical architecture model before rendering. It captures business capabilities, technical services by domain, actors/personas, external systems, integrations/data flows, cross-cutting concerns, assumptions, constraints, and architectural decisions.

New scripts:
- `enrich_architecture_model.py`
- `plan_architecture_views.py`
- `generate_companion_artifacts.py`

New metadata:
- `data/canonical_architecture_model_schema.json`
- `data/icon_registry.json`
- `data/style_guide.json`

New companion artifacts generated per run:
- `executive_summary.md`
- `architecture_decisions.md`
- `component_inventory.json`
- `capability_map.md`

The renderer prompt is now more prescriptive and includes communication goal, view type, component catalog, icon guidance, relationship/flow instructions, visual style rules, guardrail checklist, and business-to-technical mapping.
