# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `cloud_data_platform`
- Template name: Cloud data platform with ingestion, governance, processing, and access layers
- Markdown reference: ``
- Draw.io preset: `architecture`

## Layout intent


## Style profile
- Style profile: aws_red_orange
- Primary: #D92D20
- Secondary: #E99B00
- Accent: #4B5563
- Container: #F4F4F5
- Border: #C94632
- Guidance: Use for data platforms with strong ingestion/core/delivery segmentation.

## Selected recommendation
- Primary layout: cloud_data_platform
- Palette donor: Large cloud data platform reference
- Selection rationale: best-for match: data governance, best-for match: ESG data platform, best-for match: analytics and ML delivery, best-for match: AWS data architecture, selection signal: high density data platform

## Internal reference assets to learn from
- Unified sustainability hub data platform | family=cloud_data_platform | intent=Show how many data sources are ingested, governed, processed, and delivered to analytics, AI/ML, users, and downstream applications. | placement=four macro-columns with a large center core and bottom supporting bands | palette=#F0F0F0, #E0E0E0, #C0C0C0, #F0E0E0, #A0A0A0
- Large cloud data platform reference | family=cloud_data_platform | intent=Show a detailed enterprise lakehouse with governance and core data processing engine plus access and users. | placement=same as unified sustainability hub but with richer sub-zones and denser component layout | palette=#F0F0F0, #E0E0E0, #C0C0C0, #E0C0C0, #A0A0A0

### Layout grammar


### Shape hints


### Connector style
- orthogonal

## Diagram title
- Policy-as-Spec Architecture Control Platform

## Diagram subtitle
- Overview plus capability expansion diagrams

## CIO-ready business outcome description
- The architecture connects Authorship Layer, Architecture Control Plane, Architecture Assurance Fabric through governed flows and shared controls to deliver REST API, GraphQL, MCP Server with speed, resilience, and executive visibility.

Instruction: include this as a short, readable callout near the title or in a clearly labeled executive outcome panel. Keep it to 1-2 sentences and 20-45 words.

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
- Preserve editable .drawio source if supported.
- Produce user-facing artifacts only as PNG and Draw.io files. Do not produce user-facing eval files or JSON files.


## Variant profile
- Variant: Alternate style view
- Intent: Alternative palette or second recommended layout for visual preference selection.
- Density: medium
- Font bias: standard ADA-readable
- Detail guidance: Preserve the same architecture content but vary layout/palette treatment.

## ADA and readability guardrails for this variant
- Body text must be at least 14 pt.
- Section headers must be at least 16 pt.
- The main title must be at least 26 pt.
- Use high contrast text and fills that approximate WCAG AA readability.
- Text must be wrapped and must not touch box borders.
- Use 8-12 px minimum internal padding inside boxes.
- If a label does not fit, enlarge the box, wrap the label, shorten it, or move detail to a Level 2 diagram.
- Connectors must be orthogonal using only horizontal and vertical segments.
- Connectors must route around boxes and must not pass through boxes or over text.
- Use waypoints/elbows to avoid crossing major containers.
- Do not generate evaluation files or JSON files as final user-facing outputs; final outputs are PNG and Draw.io only.
