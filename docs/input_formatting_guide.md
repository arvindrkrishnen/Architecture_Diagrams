# Input Formatting Guide for Architecture Diagram Requests

This guide helps convert raw narrative into structured JSON that can reliably generate high-quality architecture diagrams.

## Core principle
A good diagram input should capture:
- **what the solution is**
- **which layout family fits best**
- **what the major capability blocks are**
- **how information or control flows**
- **which controls are cross-cutting**

## Recommended authoring sequence
1. **Title** — short, executive-friendly
2. **Subtitle** — one sentence only
3. **Template** — choose exactly one layout family
4. **Lanes** — inputs, outputs, actors, channels, or external systems
5. **Zones** — main grouped capability blocks
6. **Flows** — only the most important directional relationships
7. **Operations** — security, audit, SSO, governance, observability, etc.
8. **Footer** — deployment note or platform note

## Good formatting rules
- Prefer 1-5 word labels for node text.
- Use subtitles only when needed.
- Avoid paragraphs inside boxes.
- Use nouns or short action phrases.
- Keep zone count to roughly 4-6 for most diagrams.
- Keep lane items to the most important 4-8 items.
- Keep flows to the critical path.

## Anti-patterns to avoid
- Long prose in zone items
- Repeating the same concept in multiple places
- Too many arrows
- Too many tiny zones
- Using paragraphs instead of short labels
- Combining layout selection and detailed content in one free-form sentence

## Template selection cheat sheet
- `platform_value_chain` → product/platform overview with inputs and outputs
- `composite_ai_platform` → AI platform capability map or agent ecosystem
- `cloud_tenant_microservices` → cloud platform with tenant system and services
- `enterprise_endpoint_management` → endpoint/compliance/identity/security management
- `cloud_data_platform` → data ingestion, governance, core platform, delivery

## Minimal strong input example
```json
{
  "title": "Policy-as-Spec Architecture Control Platform",
  "subtitle": "Declarative YAML/JSON controls authored by architects and enforced in CI/CD and multi-cloud deployments.",
  "template": "platform_value_chain",
  "lanes": [
    {"side": "left", "title": "Lifecycle", "items": ["Author", "Resolve", "Enforce", "Deploy", "Assure"]},
    {"side": "right", "title": "Interfaces", "items": ["REST API", "GraphQL", "MCP Server"]}
  ],
  "zones": [
    {"id": "authoring", "title": "Authorship Layer", "items": ["Enterprise Architects", "LOB Architects", "YAML / JSON specs"]},
    {"id": "control_plane", "title": "Architecture Control Plane", "items": ["Spec repository", "REST API", "GraphQL", "MCP Server"]},
    {"id": "assurance", "title": "Architecture Assurance Fabric", "items": ["arch-ctl CLI", "Build stage", "Deploy stage"]}
  ],
  "flows": [
    {"from": "authoring", "to": "control_plane", "label": "publish specs"},
    {"from": "control_plane", "to": "assurance", "label": "resolved controls"}
  ],
  "operations": ["Evidence ledger", "Drift detector", "Waiver governance"],
  "footer": "Primary export: PNG"
}
```

## Multi-level decomposition guidance
- Keep the Level 1 overview focused on major capabilities.
- Mark a zone for expansion when it contains many sub-capabilities or deeper service detail.
- Prefer generating Level 2 child diagrams rather than overcrowding the overview.
- When in doubt, keep 4-6 zones in the overview and expand detailed areas separately.
