# Layout Semantics and Visual Communication Guide

This guide explains how the skill should interpret reference architecture diagrams.

## 1. Read the diagram as an architecture communication artifact
Every good architecture slide does more than list components. It uses placement to communicate:
- **scope** — what is inside the solution versus outside it
- **hierarchy** — what is core versus supporting
- **flow** — what moves left-to-right, top-to-bottom, or across bands
- **governance** — what is cross-cutting or controlling
- **actors and consumers** — who interacts with the platform

## 2. Common placement patterns
### Side rails
Use side rails for:
- inputs / sources
- users / personas
- downstream outputs
- external systems
- risks or technologies

### Dominant central boundary
Use a large central boundary when one platform, control plane, or managed service is the main subject.

### Horizontal bands
Use horizontal bands when you need to show:
- operations
- governance
- lifecycle
- monitoring
- security
- metadata
- shared services

### Nested boxes
Use nested boxes when one major platform contains sub-platforms or service groups.

### Swimlanes
Use swimlanes when sequence or operational ownership matters.

### Progression stacks
Use progression stacks when data or maturity moves through stages such as bronze → silver → gold.

## 3. Color semantics
The skill should use color for meaning, not decoration.
- Use **one primary family** for the main platform or control plane.
- Use **one or two secondary colors** to distinguish major domains.
- Use **neutral grays or pale fills** for support services or background grouping.
- Use **bold header bars** when macro-columns or macro-lanes need strong segmentation.

## 4. Selection heuristic
Pick the layout that best matches the user's communication need:
- data lifecycle → `cloud_data_platform` or `modern_data_lakehouse`
- portfolio / ecosystem → `composite_ai_platform`
- platform to outcomes → `platform_value_chain`
- cloud operating model → `cloud_service_operating_model`
- workflow / portal → `service_orchestration_workflow`
- control plane / landing zone → `identity_multicloud_control_plane`
- endpoint / service boundary → `enterprise_endpoint_management`
- OT / risk view → `iot_ot_security_layers`
- tenant + cloud runtime → `cloud_tenant_microservices`
