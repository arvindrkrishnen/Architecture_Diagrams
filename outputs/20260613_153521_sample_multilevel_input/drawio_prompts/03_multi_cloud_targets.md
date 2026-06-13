# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `platform_value_chain`
- Template name: Connected intelligence / low-code AI platform overview
- Markdown reference: ``
- Draw.io preset: `architecture`

## Layout intent


### Layout grammar


### Shape hints


### Connector style
- orthogonal

## Diagram title
- Multi-Cloud Targets — Level 2 Expansion

## Diagram subtitle
- Detailed expansion of Multi-Cloud Targets

## Structural content

### Lanes
- No lanes provided

### Capability zones
### Zone: AWS EKS
- Primary Cluster
- Delegate
- Policy Results

### Zone: AKS / GCP
- Secondary Cluster
- Optional Cluster
- Delegate Routing

### Flows
- child_1 -> child_2 (detail flow)

### Operations / cross-cutting layer
- Audit Trail
- Governance
- Security Controls

### Footer
- Level 2 expansion of Multi-Cloud Targets

## Mandatory layout quality rules
- Wrap all text inside boxes and containers.
- Do not allow text to overflow box boundaries.
- Do not overlap text with adjacent boxes, connectors, icons, or arrows.
- Increase box size or spacing when wrapping is needed.
- Prefer shorter labels over tiny unreadable fonts.
- Keep the overview diagram clean and presentation-ready.

## Multi-level decomposition rules
- This diagram should be treated as the Level 1 overview unless otherwise specified.
- If content is dense, reduce detail in the overview and create additional Level 2 expansion diagrams.
- Use consistent naming between the overview and expansion diagrams.
- Respect decomposition preferences: auto_expand=False, max_overview_zones=6, max_items_per_zone_overview=5, create_capability_children=False.

## Styling guidance
- Make the diagram presentation-ready and business-readable.
- Use clean grouping containers and consistent spacing.
- Keep labels short.
- Use orthogonal connectors and avoid line crossings where possible.
- Use color sparingly for major grouping, not decoration.
- Keep the work original. Do not copy the proprietary reference diagrams literally.

## Final rendering instructions
- Use drawio-skill to generate the diagram.
- Export PNG.
- Preserve editable source if supported.
