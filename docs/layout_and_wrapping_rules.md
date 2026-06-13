# Layout and Wrapping Rules

These rules are used internally by the skill to improve readability.

## Mandatory rules
- Wrap text inside all boxes and containers.
- Do not allow text to extend beyond box boundaries.
- Do not allow text to overlap adjacent boxes, icons, arrows, or connectors.
- Increase box height or width when wrapping is needed.
- Keep minimum padding inside boxes.
- Keep adequate spacing between boxes.
- Do not reduce font size excessively to fit more text.
- Prefer decomposition into multiple diagrams over dense overcrowded layouts.

## Overview page rules
- Use the overview to show only the highest-value capability groups.
- Limit the number of items shown per zone.
- Use short labels.
- Keep the overview presentation-ready.

## Expansion page rules
- Create one Level 2 diagram per major capability when expansion is necessary.
- Show sub-capabilities, key services, data stores, interfaces, and control points.
- Use the title format: `<Capability Name> — Level 2 Expansion`.
- Keep consistent naming between the overview and expansion diagrams.

## Trigger conditions for extra diagrams
Generate additional Level 2 diagrams when one or more of these are true:
- more than 6 major zones are needed
- any zone has more than 5 overview items
- labels would become too dense or unreadable
- significant sub-capability detail would clutter the overview
- the user explicitly asks for deeper expansion
