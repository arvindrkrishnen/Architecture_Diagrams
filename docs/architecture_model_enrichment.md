# Architecture Model Enrichment and Multi-View Planning

## Purpose
This version expands the skill from diagram prompt generation into an architecture modeling workflow. The skill now enriches user input into a canonical architecture model and uses that model to generate diagrams, companion artifacts, and traceability.

## Enriched model sections
The canonical model captures:
- Business capabilities / services with owners, outcomes, and value streams
- Technical services categorized into compute, data/storage, integration & APIs, security & identity, observability & governance, platform/control plane, networking, CI/CD & DevEx, and resilience & DR
- Actors, users, personas, and external systems
- Key integrations and data flows with direction, protocol/style, and payload type
- Cross-cutting concerns for security, compliance, observability, cost, and sustainability
- Assumptions, constraints, and architectural decisions
- Business-to-technical mapping

## Enrichment behavior
`enrich_architecture_model.py` uses hybrid rules and architecture best practices. For example, if the input mentions microservices on AWS, the model can add API Gateway, service mesh considerations, observability, secrets management, CI/CD with policy-as-code, networking, and resilience services.

## Multi-view planning
`plan_architecture_views.py` creates a view plan:
1. Executive / Business Capability View
2. Logical / Solution Architecture View
3. Technical Services & Infrastructure Detail
4. Integration & Data Flow View
5. Optional overlays for Security & Compliance, Observability, Cost / FinOps, and Sustainability

## Companion artifacts
`generate_companion_artifacts.py` writes:
- `executive_summary.md`
- `architecture_decisions.md`
- `component_inventory.json`
- `capability_map.md`

These artifacts are intended to make the diagram package CIO-ready and traceable.
