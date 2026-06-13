# Solution Architecture Diagram Skill (Text + Optional Images + Multi-Level Output)

**Author:** Arvind Radhakrishnen

## Purpose
This skill converts a user's architecture request into polished **solution architecture diagrams in PNG format**, using the **Agents365 drawio-skill** as the primary rendering backend.

The skill is designed to receive:
- **text input** as the main source of requirements
- **optional images** as supporting context only

The skill should not require the user to provide evaluation criteria, schema knowledge, or extra internal metadata.

## Easy invocation pattern
A user should be able to invoke this skill directly from VS Code, ChatGPT, Google Gemini, Claude, Cursor, or any compatible agent interface by saying:

```text
Use the Solution Architecture Diagram Skill.
Build a solution architecture diagram for:
[describe the solution]

If I attach images, use them as optional supporting context.
Use internal reference architecture layouts automatically.
Ensure text is wrapped inside boxes and does not overlap with other boxes.
If needed, generate additional deeper diagrams to expand capabilities.
Return the final PNG diagram(s) and editable Draw.io XML / .drawio file(s) if available.
```

The skill must then:
1. Accept the user's text request.
2. Use attached images only if they are provided.
3. Normalize the input into the internal JSON schema.
4. Select the best internal reference layout automatically.
5. Build a drawio-skill prompt.
6. Render a clean **Level 1 overview** PNG and Draw.io XML.
7. If the overview is dense, render one or more **Level 2 expansion** PNG and Draw.io XML files.
8. Return the generated files.


## Single orchestration runner
This skill includes `run_architecture_skill.py` as the top-level orchestrator.

It uses coordinated sub-agents for:
- intake
- normalization
- layout selection
- decomposition planning
- overview prompt generation
- Level 2 expansion prompt generation
- packaging and reporting

### Parallel execution checkpoint rule
The runner must:
1. check whether the execution engine supports parallel sub-agent execution
2. run compatible sub-agents in parallel only when support exists and parallel execution is requested
3. create checkpoints in shared memory before and after major stages
4. fall back to sequential execution if the engine cannot run sub-agents in parallel or if the parallel stage fails

### Shared memory rule
The runner uses a shared in-memory context persisted to:
- `outputs/<run_name>/run_context.json`

This memory carries forward:
- draft input
- normalized input
- selected template
- multilevel plan
- overview prompt location
- expansion prompt locations
- orchestration report metadata

### Runner examples
```bash
python run_architecture_skill.py --text "Build a solution architecture diagram for a multi-cloud policy-as-spec platform." --allow-parallel
python run_architecture_skill.py --json-input examples/sample_multilevel_input.json --force-sequential
```

## Required companion skill
Import and use the Draw.io skill from:
- `https://github.com/Agents365-ai/drawio-skill`

This solution-architecture skill acts as a **planner + input normalizer + layout selector + prompt builder + multi-level decomposition guide**.

## Local knowledge sources for this skill
Consult these files before generating a diagram:
1. `data/reference_architecture_patterns.json` — layout archetypes, selection rules, draw.io mapping, prompt scaffolds.
2. `data/architecture_input_schema.json` — strict input schema for normalized architecture requests.
3. `docs/input_formatting_guide.md` — guidance for converting raw user narrative into clean architecture JSON.
4. `docs/reference_layouts.md` — embedded markdown gallery describing sample layout families.
5. `docs/layout_and_wrapping_rules.md` — text wrapping, spacing, overlap, and multi-page decomposition rules.
6. `examples/sample_input.json` — example normalized input contract.
7. `examples/sample_drawio_prompt.md` — example prompt to feed into drawio-skill.
8. `examples/sample_multilevel_input.json` — example that triggers overview plus expansion diagrams.

## Input handling rules
- Treat **text** as the primary input.
- Treat **images** as optional support.
- If images are provided, use them to infer layout, grouping, labels, or rough composition.
- Do not require the user to explain the internal reference diagrams.
- Do not ask the user for evaluation instructions or extra data unless the original request is too incomplete to build a useful diagram.
- Ask follow-up questions only when absolutely necessary.

## Deliverables
The final deliverable should normally be:
- a **Level 1 overview `.png`** architecture diagram
- a **Level 1 overview `.drawio`** source file when rendering supports it
- one or more **Level 2 expansion `.png`** diagrams when needed
- one or more **Level 2 expansion `.drawio`** source files when needed
- normalized JSON when appropriate

## Text wrapping and non-overlap rules
These are mandatory.

### Box and text rules
- All text must be **wrapped inside its box or container**.
- Labels must not overflow outside box boundaries.
- Text must not overlap neighboring boxes, connectors, or icons.
- Prefer shorter labels over tiny font sizes.
- Use multi-line wrapping when a label is longer than the box width.
- Increase box height when needed so wrapped text remains readable.
- Increase white space and spacing between containers if overlap risk exists.
- Keep connector labels short.

### Density rules
If the architecture is too dense for one page, do not shrink everything excessively.
Instead:
- reduce the number of boxes shown in the Level 1 overview
- keep the overview focused on major capabilities only
- create additional Level 2 diagrams for deeper detail

### Level 1 vs Level 2 rules
- **Level 1** should show the main capability groups, inputs, outputs, flows, and cross-cutting controls.
- **Level 2** should expand a major capability from Level 1 into sub-capabilities, components, services, controls, or workflows.
- Each Level 2 diagram should clearly reference the parent capability it expands.
- Use consistent naming across the overview and expansion diagrams.

## Strict input normalization requirement
Before building the prompt, convert the user request into the normalized JSON contract defined in:
- `data/architecture_input_schema.json`

Always do the following:
- choose one approved `template`
- keep titles short and executive-friendly
- keep each label concise (typically 1-5 words)
- avoid paragraphs inside boxes
- move long explanations to subtitle or notes, not to node labels
- ensure every `flow.from` and `flow.to` points to a valid zone id or component id
- ensure cross-cutting controls go in `operations`, not duplicated across boxes
- determine whether expansion diagrams are needed

## Recommended normalization workflow
1. Read the raw user text.
2. Inspect optional attached images if present.
3. Extract the business goal.
4. Identify the closest template.
5. Map inputs, outputs, zones, flows, and operations.
6. Decide whether the diagram requires only a Level 1 overview or also Level 2 expansions.
7. Validate against `data/architecture_input_schema.json`.
8. Run `prepare_architecture_input.py` to clean, shorten, and validate the JSON.
9. Use `build_drawio_prompt.py` to build the Level 1 drawio-skill prompt.
10. If expansion is needed, generate child prompts using `plan_multilevel_architecture.py`.
11. Render with drawio-skill.
12. Return all generated files.

## Internal reference layout usage
The reference architecture diagrams bundled with this skill are for **internal layout guidance only**.
They should be used to decide:
- information hierarchy
- group placement
- flow direction
- central vs side composition
- which layout archetype fits the request best
- whether the solution needs multi-page decomposition

Do **not** ask the user to interpret or choose from the internal reference diagrams unless they explicitly want to.

## Input contract summary
```json
{
  "title": "string",
  "subtitle": "string optional",
  "template": "platform_value_chain | composite_ai_platform | cloud_tenant_microservices | enterprise_endpoint_management | cloud_data_platform",
  "lanes": [{"side": "left|right|top|bottom", "title": "string", "items": ["..."]}],
  "zones": [{"id": "string", "title": "string", "subtitle": "string", "items": ["..."], "columns": 1, "color": "optional", "expand": true}],
  "flows": [{"from": "string", "to": "string", "label": "string optional"}],
  "operations": ["..."],
  "footer": "string optional",
  "decomposition": {
    "auto_expand": true,
    "max_overview_zones": 6,
    "max_items_per_zone_overview": 5,
    "create_capability_children": true
  },
  "rendering_preferences": {"backend": "drawio-skill", "format": "png", "embed_xml": true}
}
```

## Layout selection guidance
- `platform_value_chain` — product overviews, platform capability chains, input → platform → output maps.
- `composite_ai_platform` — AI platform capability maps, business vs IT vs agentic ecosystem, reusable core solutions.
- `cloud_tenant_microservices` — SaaS platform, cloud migration, peripheral integration, mobile apps, APIs, microservices, storage, security.
- `enterprise_endpoint_management` — endpoint, device, compliance, policy, app, identity, and security diagrams.
- `cloud_data_platform` — lakehouse/data platform, ingestion/governance/processing/access.

## Draw.io generation instructions
When handing off to drawio-skill, instruct it to:
- use the **architecture** preset unless a more specific preset is required
- generate an original layout based on the chosen archetype
- keep the diagram business-readable and presentation-ready
- prefer clean grouping containers, rounded rectangles, and orthogonal connectors
- **wrap all text within boxes**
- **increase box size rather than allowing overflow**
- **avoid overlapping boxes, text, icons, and connectors**
- keep labels short and multi-line where needed
- include a title and optional subtitle
- represent operations / governance / security as cross-cutting bands when relevant
- create a clean **Level 1 overview** first
- create **Level 2 expansion** diagrams when required
- export to PNG
- if available, export as `.drawio` with embedded diagram XML

## Rules for using the reference diagrams
The sample diagrams are **layout references only**.
Do **not** reproduce proprietary artwork, exact iconography, or exact arrangement one-for-one.
Use them only to determine:
- information hierarchy
- group placement
- center-vs-side composition
- bands, lanes, containers, and tile usage
- likely flow direction

## Helper commands
### Prepare / validate input
```bash
python prepare_architecture_input.py --input examples/sample_input.json --output outputs/prepared_input.json
```

### Build drawio prompt
```bash
python build_drawio_prompt.py --input outputs/prepared_input.json --output examples/sample_drawio_prompt.md
```

### Plan multi-level expansion
```bash
python plan_multilevel_architecture.py --input outputs/prepared_input.json --output outputs/multilevel_plan.json
```

## Compatibility note
If drawio-skill or the draw.io desktop CLI is unavailable, preserve the normalized JSON and prompt so the diagram can be rendered later in a compatible environment.


## Renderer adapter
This skill includes `render_with_drawio_adapter.py`.

### Behavior
- It reads the overview and Level 2 prompt files from a run directory.
- It invokes a configurable renderer command to produce `.png` and `.drawio` files.
- It supports parallel rendering when supported and requested.
- It falls back to sequential rendering if the execution engine cannot safely render in parallel.

### Integrated orchestration usage
The top-level runner may invoke it directly:
```bash
python run_architecture_skill.py --json-input examples/sample_multilevel_input.json --allow-parallel --render --renderer-config examples/renderer_config.json
```

### Approval dependencies
For live rendering, the environment may need:
- drawio-skill installed and reachable
- draw.io desktop / CLI installed and reachable
- a locally approved renderer command template
- permission to execute local subprocess commands


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
