# Solution Architecture Diagram PNG Skill

## What this skill does
This skill converts a user's architecture description into a polished PNG solution architecture diagram. It uses a JSON-persisted reference set of architecture slide patterns inspired by common enterprise diagrams: AI platform overview, composite AI platform, cloud tenant microservices, endpoint management, and cloud data platform.

## Inputs to collect from the user
Ask for, infer, or generate the following fields:

- `title`: architecture title.
- `subtitle`: short positioning line.
- `template`: one of `platform_value_chain`, `composite_ai_platform`, `cloud_tenant_microservices`, `enterprise_endpoint_management`, `cloud_data_platform`.
- `lanes`: side inputs and outputs, such as data sources, channels, users, downstream apps, or external systems.
- `zones`: main platform capability blocks. Each zone should have an `id`, `title`, `subtitle`, and 3-8 `items`.
- `flows`: directed relationships between zones or components.
- `operations`: cross-cutting capabilities such as SSO, observability, audit, governance, DataOps, MLOps, FinOps, SecOps.
- `footer`: deployment note, such as “Any public or private cloud.”

## Generation process
1. Choose the closest template from `data/reference_architecture_patterns.json`.
2. Convert the user's narrative into the JSON input contract.
3. Keep component labels short and action-oriented.
4. Render the JSON using `render_architecture.py`.
5. Return the PNG and, when useful, the input JSON used to generate it.

## Template selection guidance
- Use `platform_value_chain` for product overview diagrams with data inputs, AI/analytics/orchestration capabilities, and business outputs.
- Use `composite_ai_platform` for maps of AI for business, AI for IT, agent studios, prompt studios, agentic RAG, and reusable core solutions.
- Use `cloud_tenant_microservices` for AWS/Azure/GCP tenant systems, APIs, microservices, portal, security, storage, and external peripherals.
- Use `enterprise_endpoint_management` for endpoint, device, policy, identity, compliance, mobile threat defense, and SaaS/on-prem integration diagrams.
- Use `cloud_data_platform` for lakehouse, ingestion, governance, metadata, analytics, AI/ML, and data delivery diagrams.

## Rendering command
```bash
python render_architecture.py --input examples/sample_input.json --output outputs/sample_architecture.png
```

## Diagram quality rules
- Prefer 20-45 total boxes.
- Group capabilities into 4-6 primary zones.
- Use left-to-right or outside-in flow depending on the template.
- Put security, governance, observability, audit, and operations in cross-cutting bands.
- Do not copy proprietary diagrams exactly; use reference patterns only for layout and information architecture.
