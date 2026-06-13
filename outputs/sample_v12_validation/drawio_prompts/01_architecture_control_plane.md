# Draw.io Renderer Prompt

## Overall communication goal
Show how the architecture connects capabilities, services, integrations, and controls to deliver the business outcome.

## View type and layout strategy
- **View:** Logical / Solution Architecture View
- **View ID:** default_logical_view
- **Layout strategy:** Use the selected primary architecture layout family.
- **Primary layout template:** `identity_multicloud_control_plane`
- **Template name:** Identity-centric multi-cloud control plane and landing zones
- **Draw.io preset:** architecture

## Executive polish requirement
Design this as an executive-ready architecture artifact: strong visual hierarchy, clear focal point, generous but not wasteful whitespace, minimal cognitive load on Level 1, and clean separation between business capabilities, technical services, integrations, and controls.

## Style profile and palette
- Style profile: identity_green_blue
- Primary: #2D6CDF
- Secondary: #47A55A
- Accent: #7C3AED
- Container: #F9FBFF
- Border: #6E8EDC
- Guidance: Use for identity control plane and multi-cloud landing zone layouts.

## Internal reference assets to learn from
- Identity-centric multi-cloud landing zone architecture | family=identity_multicloud_control_plane | intent=Show how a central identity control plane governs access, lifecycle, workloads, landing zones, and monitoring across multi-cloud environments. | placement=strong central control plane with right-side landing zones and applications, supported by layered governance and monitoring bands | palette=#F0F0F0, #E0E0E0, #E0E0F0, #C0C0C0, #F0F0E0

## Component catalog with icon and shape instructions
- Use the provided zones and lane labels as the component catalog.

Icon priority rule: For every technical component, use the most semantically accurate official icon from available draw.io libraries such as AWS Architecture Icons, Azure, GCP, Kubernetes, database, security, networking, DevOps, and analytics shapes. Prefer official shapes over generic rectangles. For custom or abstract services, use rounded rectangles with consistent internal styling and a short descriptive icon or symbol.

## Business-to-technical mapping
- Map each capability zone to the technical components shown within or adjacent to it.

Explicitly show how major business capabilities are realized by technical services. Do not leave capabilities disconnected from the platform services that enable them.

## Relationship and flow instructions
| From | To | Label | Protocol/style | Payload | Direction |
| --- | --- | --- | --- | --- | --- |
| child_1 | child_2 | detail flow | logical | architecture payload | source_to_target |

Connector rules:
- use meaningful labels such as “events (Kafka)”, “policy evaluation”, “state sync”, “API request”, “audit evidence”, or “data sync” where appropriate
- use orthogonal horizontal/vertical connectors only
- avoid diagonal lines
- route connectors around boxes and avoid crossing container interiors
- separate connector labels from box labels

## Structural content from normalized input

### Diagram title
- Architecture Control Plane — Level 2 Expansion

### Diagram subtitle
- Detailed expansion of Architecture Control Plane

### Lanes
- No lanes provided

### Capability zones
### Zone: Spec Repository
- Versioning
- Hashing
- Promotion
- Rollback
### Zone: Interfaces
- GET /specs/resolve
- Dashboard queries
- MCP tools

### Cross-cutting concerns
- None specified

### Operations / cross-cutting layer
- Audit Trail
- Governance
- Security Controls

### Footer
- Level 2 expansion of Architecture Control Plane

## Visual style guide
- Use rounded containers with subtle grouping.
- Use major section header bars.
- Use dashed or dotted borders for VPCs, clusters, trust zones, environments, or external boundaries.
- Include a legend when more than four domains, multiple connector types, trust zones, or overlays are shown.
- Maintain 8–12 px internal padding so text never touches box borders.
- Body text minimum 14 pt, section headers minimum 16 pt, title minimum 26 pt.
- Keep labels concise and wrapped inside boxes.
- Use domain color families from the style guide.

## Completeness and guardrail checklist
Before finalizing the diagram, ensure:
- business capabilities are visible and mapped to enabling services
- technical services are in the correct domain groups
- actors/personas and external systems are positioned outside or at the edges of the solution boundary
- integrations are labeled with direction and protocol/style
- security, compliance, observability, cost, and sustainability concerns appear as overlays or cross-cutting bands when relevant
- all technology names preserve canonical spelling and capitalization
- all text is readable, wrapped, padded, and non-overlapping
- connectors are orthogonal and avoid overlapping boxes
- the diagram has a clear focal point and executive-ready finish

## Final rendering instructions
- Generate the final PNG and editable `.drawio` XML.
- Use this prompt as a precise specification, not as loose inspiration.
- Keep the final artifact original; do not copy internal reference diagrams literally.
