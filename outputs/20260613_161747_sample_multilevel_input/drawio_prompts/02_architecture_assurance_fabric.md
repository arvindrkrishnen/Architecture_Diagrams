# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `platform_value_chain`
- Template name: Connected intelligence / capability value chain
- Markdown reference: ``
- Draw.io preset: `architecture`

## Layout intent


## Style profile
- Style profile: clean_enterprise_blue
- Primary: #2F73D8
- Secondary: #8FB8F3
- Accent: #1F3B73
- Container: #F7FAFF
- Border: #4B6FA9
- Guidance: Use for control planes, operating models, or identity-centric enterprise diagrams.

## Selected recommendation
- Primary layout: platform_value_chain
- Palette donor: template default
- Selection rationale: template default

## Internal reference assets to learn from
- Connected intelligence platform overview | family=platform_value_chain | intent=Show how upstream data and applications enter a platform, how central capabilities are grouped, and how outputs are delivered to business users. | placement=left-right journey with single dominant middle boundary and bottom operations strip | palette=#F0F0F0, #E0E0F0, #E0E0E0, #C0C0C0, #A0A0A0

### Layout grammar


### Shape hints


### Connector style
- orthogonal

## Diagram title
- Architecture Assurance Fabric — Level 2 Expansion

## Diagram subtitle
- Detailed expansion of Architecture Assurance Fabric

## CIO-ready business outcome description
- Create a brief CIO-ready statement explaining how the capabilities and sub-capabilities connect through governed flows to deliver the stated business outcome.

Instruction: include this as a short, readable callout near the title or in a clearly labeled executive outcome panel. Keep it to 1-2 sentences and 20-45 words.

## Structural content

### Lanes
- No lanes provided

### Capability zones
### Zone: Build Stage
- Dependency Scan
- IaC Plan
- Container Image Check

### Zone: Deploy Stage
- BCP / DR Gates
- LB Spec
- Topology Verification

### Flows
- child_1 -> child_2 (detail flow)

### Operations / cross-cutting layer
- Audit Trail
- Governance
- Security Controls

### Footer
- Level 2 expansion of Architecture Assurance Fabric

## Mandatory semantic placement rules
- Place technology components in semantically correct areas.
- Data stores and databases belong in storage, data platform, persistence, or metadata zones.
- APIs, REST, GraphQL, and MCP belong in interface, control plane, access, or delivery zones.
- Cloud runtimes such as EKS, AKS, GCP, EC2, Lambda, and Kubernetes belong in cloud target, compute, platform, or landing-zone areas.
- Analytics tools belong in access, delivery, reporting, analytics, or consumption areas.
- Governance, audit, waiver, evidence, and policy components belong in governance, control, operations, or assurance bands.

## Mandatory spelling and label rules
- Preserve canonical capitalization for technology names such as GraphQL, Kubernetes, AWS, Azure, GCP, EKS, AKS, REST API, MCP, YAML, JSON, CI/CD, IaC, MLOps, OPA, and Terraform.
- Use the technology terms allowlist when checking labels.
- Avoid invented misspellings or compressed labels.
- Use short labels and wrap text rather than reducing font size excessively.

## Mandatory ADA/readability layout quality rules
- Wrap all text inside boxes and containers.
- Do not allow text to overflow box boundaries.
- Do not let text touch box borders. Maintain at least 8-12 px internal padding.
- Body text must be at least 14 pt. Section headers must be at least 16 pt. Main title must be at least 26 pt.
- Use high-contrast colors that approximate WCAG AA readability.
- Do not overlap text with adjacent boxes, connectors, icons, or arrows.
- Increase box size or spacing when wrapping is needed.
- Prefer shorter labels over tiny unreadable fonts.
- Keep the overview diagram clean and presentation-ready.

## Mandatory connector rules
- Use only orthogonal connectors with horizontal and vertical segments.
- Do not use diagonal connectors.
- Route connectors around boxes, not through boxes.
- Do not let connectors overlap text or pass over box interiors.
- Use waypoints or elbow connectors to avoid crossing major containers.
- Keep connector labels short and clearly separated from box labels.

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
- Use the template style profile and internal reference asset palette mood for macro segmentation.
- Borrow color schemes similarly to the internal references, but keep the diagram original.
- Use header bars, panels, and cross-cutting bands when the reference family indicates them.
- Keep the work original. Do not copy the proprietary reference diagrams literally.

## Final rendering instructions
- Use drawio-skill to generate the diagram.
- Export PNG.
- Preserve editable .drawio source if supported.
- Produce user-facing artifacts only as PNG and Draw.io files. Do not produce user-facing eval files or JSON files.
