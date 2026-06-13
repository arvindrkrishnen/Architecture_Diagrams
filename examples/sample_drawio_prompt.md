# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `platform_value_chain`
- Template name: Connected intelligence / low-code AI platform overview
- Markdown reference: `docs/reference_layouts.md#1-platform-value-chain-layout`
- Draw.io preset: `architecture`

## Layout intent
Create a polished architecture overview diagram using a left-to-right product value chain layout. Include left input lanes, a central platform boundary with grouped capability blocks, right output lanes, and a bottom operations band. Keep it presentation-ready and original.

### Layout grammar
- Use 4-6 large central capability blocks.
- Place upstream data/application inputs on the left.
- Place reports/apps/automation outcomes on the right.
- Reserve a bottom operations band inside the main container.

### Shape hints
- rounded rectangles
- header ribbons
- side lanes
- operations band

### Connector style
- orthogonal

## Diagram title
- Agentic Vendor Intelligence Platform — Solution Architecture

## Diagram subtitle
- Unified ingestion, AI research orchestration, evidence store, and business delivery layer

## Structural content

### Lanes
### Left lane — Inputs
- Vendor websites
- Analyst reports
- RFP documents
- CRM notes
- Market news
- APIs

### Right lane — Outputs
- Vendor dashboards
- Comparison matrices
- Executive briefs
- RFP responses
- Alerts & tasks

### Capability zones
### Zone: Data integration
Subtitle: Normalize and enrich
- Web/API connectors
- Document parser
- Metadata extraction
- Source lineage

### Zone: Knowledge fabric
Subtitle: Searchable evidence
- Vector index
- Entity graph
- Taxonomy mapping
- Citation store

### Zone: Predictive & generative AI
Subtitle: Multi-agent research
- Research agent
- Comparator agent
- Risk summarizer
- Question generator

### Zone: Decision orchestration
Subtitle: Human-in-loop workflows
- Rules engine
- Review queues
- Approval workflow
- Audit trail

### Zone: Apps, APIs & analytics
Subtitle: Business consumption
- Dashboard builder
- Insight API
- Report generator
- Notification service

### Flows
- ingestion -> knowledge (curated data)
- knowledge -> ai (retrieval)
- ai -> orchestration (recommendations)
- orchestration -> delivery (approved outputs)

### Operations / cross-cutting layer
- User management & SSO
- Workflow automation
- ModelOps
- DataOps
- Audit & compliance

### Footer
- Deployable on AWS, Azure, GCP, or private cloud

## Styling guidance
- Make the diagram presentation-ready and business-readable.
- Use clean grouping containers and consistent spacing.
- Keep labels short.
- Use orthogonal connectors and avoid line crossings where possible.
- Use color sparingly for major grouping, not decoration.
- Keep the work original. Do not copy the proprietary reference diagrams literally.

## Final rendering instructions
- Use drawio-skill to generate the diagram.
- Export PNG.
- Preserve editable source if supported.
