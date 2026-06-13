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
