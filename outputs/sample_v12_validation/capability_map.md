# Capability Map

| Capability | Owner | Outcomes | Value streams |
| --- | --- | --- | --- |
| Authorship Layer | Business / Platform Owner | REST API | Policy-as-Spec Architecture Control Platform |
| Architecture Control Plane | Business / Platform Owner | GraphQL | Policy-as-Spec Architecture Control Platform |
| Architecture Assurance Fabric | Business / Platform Owner | MCP Server | Policy-as-Spec Architecture Control Platform |
| Multi-Cloud Targets | Business / Platform Owner | MCP Server | Policy-as-Spec Architecture Control Platform |
| Cross-Cutting Components | Business / Platform Owner | MCP Server | Policy-as-Spec Architecture Control Platform |

## Business-to-technical mapping

### Authorship Layer
- YAML / JSON Specs (compute)
- Enterprise Architects (platform_control_plane)
- LOB Architects (platform_control_plane)

### Architecture Control Plane
- REST API (integration_apis)
- GraphQL (integration_apis)
- MCP Server (integration_apis)
- Spec Repository (platform_control_plane)
- Spec Resolution (platform_control_plane)

### Architecture Assurance Fabric
- Topology Verification (observability_governance)
- arch-ctl CLI (platform_control_plane)
- Deploy Stage (platform_control_plane)
- OPA Checks (platform_control_plane)
- Build Stage (cicd_devex)

### Multi-Cloud Targets
- AWS EKS (compute)
- AKS (compute)
- GCP (platform_control_plane)
- Harness Delegates (platform_control_plane)

### Cross-Cutting Components
- Evidence Ledger (observability_governance)
- Drift Detector (observability_governance)
- Waiver Governance (observability_governance)
