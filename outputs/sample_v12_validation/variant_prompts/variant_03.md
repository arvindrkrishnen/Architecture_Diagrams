# Draw.io Renderer Prompt

## Overall communication goal
Policy-as-Spec Architecture Control Platform connects business capabilities, platform services, integrations, and cross-cutting controls to deliver governed, resilient, and measurable outcomes for CIO stakeholders.

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
| Component | Domain | Icon / shape instruction | Color family | Purpose |
| --- | --- | --- | --- | --- |
| Authorship Layer | business_capability | Business capability / value stream box | #EAF4FF | Business / Platform Owner |
| Architecture Control Plane | business_capability | Business capability / value stream box | #EAF4FF | Business / Platform Owner |
| Architecture Assurance Fabric | business_capability | Business capability / value stream box | #EAF4FF | Business / Platform Owner |
| Multi-Cloud Targets | business_capability | Business capability / value stream box | #EAF4FF | Business / Platform Owner |
| Cross-Cutting Components | business_capability | Business capability / value stream box | #EAF4FF | Business / Platform Owner |
| YAML / JSON Specs | compute | Generic draw.io / rounded rectangle with short descriptive symbol | #EAF7EA | Supports Authorship Layer |
| AWS EKS | compute | AWS Architecture Icons / Amazon EKS | #EAF7EA | Supports Multi-Cloud Targets |
| AKS | compute | Azure Icons / Azure Kubernetes Service | #EAF7EA | Supports Multi-Cloud Targets |
| Amazon EKS or ECS | compute | AWS Architecture Icons / Amazon EKS | #EAF7EA | Architecture enrichment |
| Containerized services | compute | Generic draw.io / rounded rectangle with short descriptive symbol | #EAF7EA | Architecture enrichment |
| Serverless workers | compute | Generic draw.io / rounded rectangle with short descriptive symbol | #EAF7EA | Architecture enrichment |
| REST API | integration_apis | Generic Networking / API / API endpoint | #F1ECFF | Supports Architecture Control Plane |
| GraphQL | integration_apis | Generic API / GraphQL endpoint | #F1ECFF | Supports Architecture Control Plane |
| MCP Server | integration_apis | Generic AI / server / MCP server | #F1ECFF | Supports Architecture Control Plane |
| Amazon API Gateway | integration_apis | AWS Architecture Icons / Amazon API Gateway | #F1ECFF | Architecture enrichment |
| EventBridge or Kafka | integration_apis | Kafka / generic streaming / event streaming topic | #F1ECFF | Architecture enrichment |
| Service-to-service APIs | integration_apis | Generic Networking / API / API endpoint | #F1ECFF | Architecture enrichment |
| AWS IAM | security_identity | AWS Architecture Icons / AWS IAM | #FFF1F2 | Architecture enrichment |
| AWS Secrets Manager | security_identity | AWS Architecture Icons / AWS Secrets Manager | #FFF1F2 | Architecture enrichment |
| WAF / ingress controls | security_identity | Security / firewall | #FFF1F2 | Architecture enrichment |
| Identity provider | security_identity | Generic draw.io / rounded rectangle with short descriptive symbol | #FFF1F2 | Architecture enrichment |
| Conditional access | security_identity | Generic draw.io / rounded rectangle with short descriptive symbol | #FFF1F2 | Architecture enrichment |
| Privileged access management | security_identity | Generic draw.io / rounded rectangle with short descriptive symbol | #FFF1F2 | Architecture enrichment |
| Topology Verification | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Supports Architecture Assurance Fabric |
| Evidence Ledger | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Supports Cross-Cutting Components |
| Drift Detector | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Supports Cross-Cutting Components |
| Waiver Governance | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Supports Cross-Cutting Components |
| CloudWatch metrics | observability_governance | AWS Architecture Icons / Amazon CloudWatch | #F0FDFA | Architecture enrichment |
| Centralized logs | observability_governance | AWS Architecture Icons / Amazon CloudWatch | #F0FDFA | Architecture enrichment |
| Distributed tracing | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Architecture enrichment |
| Access audit logs | observability_governance | AWS Architecture Icons / Amazon CloudWatch | #F0FDFA | Architecture enrichment |
| Compliance dashboard | observability_governance | Analytics / BI / dashboard chart | #F0FDFA | Architecture enrichment |
| Continuous trust evaluation | observability_governance | Generic draw.io / rounded rectangle with short descriptive symbol | #F0FDFA | Architecture enrichment |
| Enterprise Architects | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Authorship Layer |
| LOB Architects | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Authorship Layer |
| Spec Repository | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Architecture Control Plane |
| Spec Resolution | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Architecture Control Plane |
| arch-ctl CLI | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Architecture Assurance Fabric |
| Deploy Stage | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Architecture Assurance Fabric |
| OPA Checks | platform_control_plane | Security / governance / policy shield | #EEF2FF | Supports Architecture Assurance Fabric |
| GCP | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Multi-Cloud Targets |
| Harness Delegates | platform_control_plane | Generic draw.io / rounded rectangle with short descriptive symbol | #EEF2FF | Supports Multi-Cloud Targets |
| Central identity control plane | platform_control_plane | Azure Icons / Microsoft Entra ID | #EEF2FF | Architecture enrichment |
| Policy guardrails | platform_control_plane | Security / governance / policy shield | #EEF2FF | Architecture enrichment |
| Landing zone standards | platform_control_plane | AWS Architecture Icons / Amazon RDS | #EEF2FF | Architecture enrichment |
| Load balancer | networking | Networking / load balancer | #F8FAFC | Architecture enrichment |
| Private subnets | networking | Generic draw.io / rounded rectangle with short descriptive symbol | #F8FAFC | Architecture enrichment |
| Service mesh considerations | networking | Kubernetes / Networking / service mesh | #F8FAFC | Architecture enrichment |
| Secure access path | networking | Generic draw.io / rounded rectangle with short descriptive symbol | #F8FAFC | Architecture enrichment |
| Private connectivity | networking | Generic draw.io / rounded rectangle with short descriptive symbol | #F8FAFC | Architecture enrichment |
| Segmentation boundaries | networking | Generic draw.io / rounded rectangle with short descriptive symbol | #F8FAFC | Architecture enrichment |
| Build Stage | cicd_devex | Generic draw.io / rounded rectangle with short descriptive symbol | #ECFEFF | Supports Architecture Assurance Fabric |
| CI/CD pipeline | cicd_devex | DevOps / CI-CD / pipeline | #ECFEFF | Architecture enrichment |
| Policy-as-code checks | cicd_devex | Security / governance / policy shield | #ECFEFF | Architecture enrichment |
| Infrastructure as Code | cicd_devex | Generic draw.io / rounded rectangle with short descriptive symbol | #ECFEFF | Architecture enrichment |
| Multi-AZ deployment | resilience_dr | Generic draw.io / rounded rectangle with short descriptive symbol | #FDF2F8 | Architecture enrichment |
| Automated rollback | resilience_dr | Networking / load balancer | #FDF2F8 | Architecture enrichment |
| Backup / recovery plan | resilience_dr | Generic draw.io / rounded rectangle with short descriptive symbol | #FDF2F8 | Architecture enrichment |
| Break-glass access | resilience_dr | Generic draw.io / rounded rectangle with short descriptive symbol | #FDF2F8 | Architecture enrichment |
| Regional failover controls | resilience_dr | Generic draw.io / rounded rectangle with short descriptive symbol | #FDF2F8 | Architecture enrichment |
| Business users | actor_persona | Actor/person icon or muted persona card | #F3F4F6 | Use delivered insights and workflows |
| Author | external_system | External system container / muted rectangle | #F3F4F6 | Provides input or event data |
| Resolve | external_system | External system container / muted rectangle | #F3F4F6 | Provides input or event data |
| Enforce | external_system | External system container / muted rectangle | #F3F4F6 | Provides input or event data |
| Deploy | external_system | External system container / muted rectangle | #F3F4F6 | Provides input or event data |
| Assure | external_system | External system container / muted rectangle | #F3F4F6 | Provides input or event data |
| REST API | external_system | External system container / muted rectangle | #F3F4F6 | Receives outcomes or insights |
| GraphQL | external_system | External system container / muted rectangle | #F3F4F6 | Receives outcomes or insights |
| MCP Server | external_system | External system container / muted rectangle | #F3F4F6 | Receives outcomes or insights |

Icon priority rule: For every technical component, use the most semantically accurate official icon from available draw.io libraries such as AWS Architecture Icons, Azure, GCP, Kubernetes, database, security, networking, DevOps, and analytics shapes. Prefer official shapes over generic rectangles. For custom or abstract services, use rounded rectangles with consistent internal styling and a short descriptive icon or symbol.

## Business-to-technical mapping
| Business capability | Outcome | Realized by technical services |
| --- | --- | --- |
| Authorship Layer | REST API | YAML / JSON Specs (compute), Enterprise Architects (platform_control_plane), LOB Architects (platform_control_plane) |
| Architecture Control Plane | GraphQL | REST API (integration_apis), GraphQL (integration_apis), MCP Server (integration_apis), Spec Repository (platform_control_plane), Spec Resolution (platform_control_plane) |
| Architecture Assurance Fabric | MCP Server | Topology Verification (observability_governance), arch-ctl CLI (platform_control_plane), Deploy Stage (platform_control_plane), OPA Checks (platform_control_plane), Build Stage (cicd_devex) |
| Multi-Cloud Targets | MCP Server | AWS EKS (compute), AKS (compute), GCP (platform_control_plane), Harness Delegates (platform_control_plane) |
| Cross-Cutting Components | MCP Server | Evidence Ledger (observability_governance), Drift Detector (observability_governance), Waiver Governance (observability_governance) |

Explicitly show how major business capabilities are realized by technical services. Do not leave capabilities disconnected from the platform services that enable them.

## Relationship and flow instructions
| From | To | Label | Protocol/style | Payload | Direction |
| --- | --- | --- | --- | --- | --- |
| authoring | control_plane | publish specs | logical | business / technical payload | source_to_target |
| control_plane | assurance | resolved controls | logical | business / technical payload | source_to_target |
| assurance | targets | policy enforcement | logical | business / technical payload | source_to_target |
| targets | controls | evidence and drift | logical | business / technical payload | source_to_target |
| external_systems | integration_apis | API requests | sync | JSON / HTTP | inbound |
| core_services | event_processing | events | event | event envelope | publish_subscribe |
| authoring | control_plane | publish specs | logical | architecture payload | source_to_target |
| control_plane | assurance | resolved controls | logical | architecture payload | source_to_target |
| assurance | targets | policy enforcement | logical | architecture payload | source_to_target |
| targets | controls | evidence and drift | logical | architecture payload | source_to_target |

Connector rules:
- use meaningful labels such as “events (Kafka)”, “policy evaluation”, “state sync”, “API request”, “audit evidence”, or “data sync” where appropriate
- use orthogonal horizontal/vertical connectors only
- avoid diagonal lines
- route connectors around boxes and avoid crossing container interiors
- separate connector labels from box labels

## Structural content from normalized input

### Diagram title
- Policy-as-Spec Architecture Control Platform

### Diagram subtitle
- Overview plus capability expansion diagrams

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
### Zone: Architecture Assurance Fabric
Subtitle: Pipeline enforcement
- arch-ctl CLI
- Build Stage
- Deploy Stage
### Zone: Multi-Cloud Targets
Subtitle: Deployment endpoints
- AWS EKS
- AKS
- GCP
### Zone: Cross-Cutting Components
Subtitle: Governance and evidence
- Evidence Ledger
- Drift Detector
- Waiver Governance

### Cross-cutting concerns
- **Security**: Security Controls, AWS IAM, AWS Secrets Manager, WAF / ingress controls, Identity provider
- **Compliance**: Audit Trail, Governance
- **Observability**: Topology Verification, Evidence Ledger, Drift Detector, Waiver Governance
- **Cost**: Cost allocation and usage visibility
- **Sustainability**: Efficient managed services and right-sized capacity

### Operations / cross-cutting layer
- Audit Trail
- Governance
- Security Controls

### Footer
- Generate overview and Level 2 expansion diagrams where useful

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


## Variant profile
- Variant: Executive simplified view
- Intent: More whitespace, fewer boxes, larger fonts, stronger business outcome narrative.
- Density: low
- Font bias: larger ADA-readable
- Detail guidance: Show only the most important capabilities and move detail to Level 2 if needed.

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
