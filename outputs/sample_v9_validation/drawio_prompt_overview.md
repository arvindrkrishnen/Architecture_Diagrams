# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `identity_multicloud_control_plane`
- Template name: Identity-centric multi-cloud control plane and landing zones
- Markdown reference: ``
- Draw.io preset: `architecture`

## Layout intent


## Style profile
- Style profile: identity_green_blue
- Primary: #2D6CDF
- Secondary: #47A55A
- Accent: #7C3AED
- Container: #F9FBFF
- Border: #6E8EDC
- Guidance: Use for identity control plane and multi-cloud landing zone layouts.

## Selected recommendation
- Primary layout: identity_multicloud_control_plane
- Palette donor: Identity-centric multi-cloud landing zone architecture
- Selection rationale: best-for match: identity architecture, best-for match: multi-cloud security, best-for match: governance and monitoring, selection signal: central control plane, selection signal: multi-cloud panels

## Internal reference assets to learn from
- Identity-centric multi-cloud landing zone architecture | family=identity_multicloud_control_plane | intent=Show how a central identity control plane governs access, lifecycle, workloads, landing zones, and monitoring across multi-cloud environments. | placement=strong central control plane with right-side landing zones and applications, supported by layered governance and monitoring bands | palette=#F0F0F0, #E0E0E0, #E0E0F0, #C0C0C0, #F0F0E0

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
- Use the template style profile and internal reference asset palette mood for macro segmentation.
- Borrow color schemes similarly to the internal references, but keep the diagram original.
- Use header bars, panels, and cross-cutting bands when the reference family indicates them.
- Keep the work original. Do not copy the proprietary reference diagrams literally.

## Final rendering instructions
- Use drawio-skill to generate the diagram.
- Export PNG.
- Preserve editable source if supported.
