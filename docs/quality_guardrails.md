# Quality Guardrails

## Per-run recommendations
Each run should produce 1-2 layout recommendations in:
- `layout_recommendations.json`

Each recommendation includes:
- primary layout template
- secondary palette donor
- why the layout was selected
- communication intent
- guardrails to preserve readability

When the user is present and an interactive selection is useful, show the top 1-2 recommendations and let the user choose. If no choice is provided, use recommendation 1.

## Spelling and label guardrails
- Preserve canonical capitalization for technology names.
- Use `data/technology_terms_allowlist.txt` as the spelling allowlist.
- Run spelling / OCR quality checks after the PNG is rendered when possible.
- Keep labels short and wrap inside boxes.

## Technology placement guardrails
Each run should produce:
- `technology_placement_report.json`

This report checks whether technology components are placed in semantically appropriate zones.

Examples:
- REST, GraphQL, MCP → interface / control plane / access layer
- EKS, AKS, GCP, Kubernetes → cloud target / compute / landing-zone layer
- dashboards and analytics → access / delivery / reporting layer
- policy, waiver, evidence, audit → governance / assurance / operations layer
- data stores → storage / data platform / metadata layer

Warnings are heuristic, but should be reviewed before final rendering.

## Clean display guardrails
- Text must be wrapped inside boxes.
- Boxes should have enough padding for wrapped labels.
- Connectors should not cross labels where possible.
- If a diagram becomes crowded, create Level 2 expansion diagrams.
