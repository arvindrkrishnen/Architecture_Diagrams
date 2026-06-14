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

## Claude-native rendering path

If the Agents365 drawio-skill CLI is not available, such as in claude.ai or Claude API environments, use the Claude-native rendering path.

```bash
python run_architecture_skill.py \
  --text-file examples/request.txt \
  --render \
  --render-mode claude-native
```

The renderer adapter emits a self-contained Claude-native instruction file asking Claude to generate:
1. an inline SVG preview
2. draw.io-compatible XML wrapped in an `mxGraphModel` block
3. ADA-compliant text, padding, wrapping, and orthogonal connector routing

## Quick start from Claude (claude.ai or Claude API)

Paste this prompt into Claude:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for:
[describe your solution in 2–10 sentences, including the business problem, users, key technical services, cloud platforms, and governance/security requirements]

Requirements:
- Select the most appropriate layout template automatically.
- Keep the Level 1 diagram executive-ready: no more than 6–8 capability zones.
- Generate Level 2 expansion diagrams if the architecture is dense.
- Use official cloud/platform icons where available.
- Apply the enterprise_light palette unless executive/board mode is requested.
- Include a 3-sentence CIO narrative in the subtitle or narrative block.
- Ensure all text is wrapped inside boxes with at least 10px padding.
- Use orthogonal connectors only.
- Differentiate sync API, async event, batch/file, streaming, and replication connectors visually.
- Return normalized JSON, drawio prompt markdown, and an inline SVG preview of the Level 1 diagram when drawio-skill is unavailable.
```

## Financial services architecture intelligence

When the request involves banking, capital markets, insurance, risk, or financial services:

- Map regulatory requirements to architecture zones automatically:
  - CCAR/DFAST → risk_and_compliance
  - Basel / RWA → risk_and_compliance
  - AML/KYC → compliance_controls
  - SOX → governance overlay
  - BCBS 239 → data_platform / lineage controls
  - MiFID II / RegReporting → integration and reporting zones
- Always include a Regulatory & Compliance cross-cutting band.
- Add Model Risk Management for AI/ML architectures in financial services.
- Label sensitive data flows with data classification when known, such as PII, NPI, or MNPI.
- Use Secure Enclave or Trusted Execution Environment boundary styling for sensitive compute zones.

## Executive presentation mode

When the user says “executive,” “CxO,” “board,” “investor,” or “steering committee”:

- Limit the Level 1 diagram to 5 capability zones maximum.
- Use business capability labels on Level 1 and move technology specifics to Level 2.
- Increase title font to 32pt, zone header to 20pt, and body text to 16pt.
- Add a Key Outcomes banner with 3–4 business outcomes.
- Prefer the enterprise_dark or boardroom_blue palette for projected presentations.
- Generate a Technical Appendix view set with full technology detail.

## Claude self-evaluation checklist

Before returning any diagram output, Claude or any LLM renderer must verify:

- [ ] Does the Level 1 diagram tell a clear business story in under 10 seconds?
- [ ] Are all capability zones labeled in business language, not technology jargon?
- [ ] Is every flow labeled with direction and integration pattern?
- [ ] Are all cross-cutting concerns shown as bands or overlays, not scattered boxes?
- [ ] Is the color palette consistent and hex-precise?
- [ ] Is the title at least 26pt, section text at least 16pt, and body text at least 14pt?
- [ ] Does the subtitle or description contain a CIO-ready narrative?
- [ ] Are external systems and actors positioned at the diagram boundary, not inside the platform?
- [ ] If the architecture is for a regulated industry, is there a compliance band?
- [ ] Does the diagram have a legend if more than 3 connector types or 4 domain colors are used?

If any item is unchecked, correct it before returning the output.

## Article / blog to diagram mode

When the source material is prose-first, use article mode:

```bash
python run_architecture_skill.py --text-file article.md --source-kind article
```

This invokes `extract_architecture_from_article.py` to infer layers, components, interfaces, flows, sequence models, feedback loops, and diagram-ready payloads before the normal architecture diagram pipeline runs.

## Domain vocabulary packs

Use `--domain` to activate a vocabulary pack:

```bash
python run_architecture_skill.py --text-file examples/request.txt --domain financial_services
```

Available packs include financial_services, healthcare, retail_ecommerce, cloud_platform, ai_ml_platform, manufacturing_iot, and government_public_sector.

## Connector semantic layer

Flows may include:

```json
{
  "from": "api_gateway",
  "to": "order_service",
  "label": "REST / JSON",
  "pattern": "sync_api",
  "direction": "source_to_target",
  "payload_type": "JSON",
  "timing": "runtime"
}
```

Supported patterns: sync_api, async_event, batch_etl, streaming, webhook, pub_sub, grpc, file_transfer, database_replication, logical.

## Annotation and callout layer

Use annotations to mark business-critical information:

```json
{
  "annotations": [
    {"type": "highlight", "target_zone_id": "ai_decisioning", "label": "FY26 Investment Priority", "color_role": "accent_highlight"},
    {"type": "risk_flag", "target_zone_id": "legacy_mainframe", "label": "Technical Debt — Retire by Q4", "color_role": "risk_red"}
  ]
}
```
