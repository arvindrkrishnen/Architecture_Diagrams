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
- Policy-as-Spec Architecture Control Platform

## Diagram subtitle
- Overview plus capability expansion diagrams

## Structural content

### Lanes
### Left lane — Lifecycle
- Author
- Resolve
- Enforce
- Deploy
- Assure

### Right lane — Interfaces
- REST API
- GraphQL
- MCP Server

### Capability zones
### Zone: Authorship Layer
Subtitle: Architect-owned specs
- Enterprise Architects
- LOB Architects
- YAML / JSON Specs

### Zone: Architecture Control Plane
Subtitle: Single source of truth
- Spec Repository
- REST API
- GraphQL
- MCP Server
- Spec Resolution
Expansion hint: This zone may be expanded into a Level 2 diagram.

### Zone: Architecture Assurance Fabric
Subtitle: Pipeline enforcement
- arch-ctl CLI
- Build Stage
- Deploy Stage
- OPA Checks
- Topology Verification
Expansion hint: This zone may be expanded into a Level 2 diagram.

### Zone: Multi-Cloud Targets
Subtitle: Deployment endpoints
- AWS EKS
- AKS
- GCP
- Harness Delegates
Expansion hint: This zone may be expanded into a Level 2 diagram.

### Zone: Cross-Cutting Components
Subtitle: Governance and evidence
- Evidence Ledger
- Drift Detector
- Waiver Governance
Expansion hint: This zone may be expanded into a Level 2 diagram.

### Flows
- authoring -> control_plane (publish specs)
- control_plane -> assurance (resolved controls)
- assurance -> targets (policy enforcement)
- targets -> controls (evidence and drift)

### Operations / cross-cutting layer
- Audit Trail
- Governance
- Security Controls

### Footer
- Generate overview and Level 2 expansion diagrams where useful

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
- Respect decomposition preferences: auto_expand=True, max_overview_zones=6, max_items_per_zone_overview=5, create_capability_children=True.

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
