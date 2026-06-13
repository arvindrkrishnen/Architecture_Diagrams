# ADA, Readability, Connector, and Business Outcome Guardrails

These guardrails are mandatory during execution and must be revalidated after rendering.

## Text readability and ADA-oriented rules
Generated diagrams must be readable in an executive presentation setting.

### Font size
- Body labels: minimum 14 pt.
- Section headers: minimum 16 pt.
- Main title: minimum 26 pt.
- Subtitle and executive outcome description: minimum 14 pt.
- Do not shrink text below these limits to fit dense content.
- If text does not fit, enlarge the box, shorten the label, or create a Level 2 diagram.

### Contrast
- Use high-contrast text and background combinations.
- Prefer dark navy, black, or charcoal text on white or pale fills.
- Avoid low-contrast gray text on gray backgrounds.
- Approximate WCAG AA contrast target: at least 4.5:1 for normal text.

### Padding and borders
- Text must remain inside its box.
- Text must not touch box borders.
- Use at least 8-12 px internal padding.
- Use 14-18 px padding for large containers and description panels.
- Leave breathing room between icons and labels.

### Text length
- Keep labels short and business-readable.
- Prefer 1-5 words for primary labels.
- Use wrapped multi-line labels for longer text.
- Do not place paragraph-length content inside small boxes.

## Connector routing rules
Connectors must communicate flow without obscuring the architecture.

- Use orthogonal connectors only: horizontal and vertical segments.
- Avoid diagonal connectors unless explicitly requested.
- Route connectors around boxes, not through boxes.
- Do not overlap text, labels, icons, or box interiors.
- Use waypoints / elbow connectors to avoid crossing major containers.
- Keep connector labels short.
- Use arrowheads consistently.
- If the diagram becomes connector-heavy, simplify the overview and move detail to Level 2.

## Box placement rules
- Use consistent box widths within a row or lane.
- Align boxes to a clean grid.
- Maintain visible gutters between boxes.
- Do not let boxes overlap.
- Use container boundaries to clarify scope.
- Cross-cutting controls should appear in bands, not scattered randomly.

## Executive CIO-ready business outcome description
Every Level 1 diagram must include a short description explaining how capabilities connect to deliver the business outcome.

### Placement
Place it near the title, below the title, or in a clearly labeled callout.

### Length
- 1-2 sentences.
- 20-45 words total.
- Written for a CIO / senior technology executive.

### Content pattern
Use this pattern when possible:

> The platform connects [inputs/actors] through [core capabilities] and [governance/operations] to deliver [business outcome] with measurable control, speed, resilience, or insight.

## Three output variants
Every run should prepare three variants:

1. **Variant 1 - Recommended enterprise view**
   - Uses the top-ranked primary layout.
   - Balanced executive and technical detail.

2. **Variant 2 - Alternate style / palette view**
   - Uses the second layout recommendation when available, or the same layout with a different palette donor.
   - Useful for visual preference selection.

3. **Variant 3 - Executive simplified view**
   - Same architecture content, fewer boxes, stronger whitespace, larger font, and clearer business outcome narrative.

## Output policy
User-facing outputs should be:
- `.png`
- `.drawio`

Do not create user-facing evaluation files or JSON files. Internal JSON may be used transiently by the orchestration engine, but final artifacts returned to the user should be the three PNG files and three Draw.io files.
