#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def bullets(items, indent=0):
    pad = ' ' * indent
    return "\n".join(f"{pad}- {item}" for item in items)


def main():
    ap = argparse.ArgumentParser(description='Build a drawio-skill prompt from normalized architecture JSON.')
    ap.add_argument('--input', required=True, help='Path to normalized architecture input JSON')
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json', help='Path to reference patterns JSON')
    ap.add_argument('--output', required=True, help='Output markdown prompt path')
    args = ap.parse_args()

    architecture = load_json(Path(args.input))
    patterns = load_json(Path(args.patterns))
    template_id = architecture['template']
    template = next((t for t in patterns['templates'] if t['id'] == template_id), None)
    if not template:
        raise SystemExit(f'Template not found: {template_id}')

    lanes_md = []
    for lane in architecture.get('lanes', []):
        lanes_md.append(f"### {lane['side'].title()} lane — {lane.get('title','Lane')}\n" + bullets(lane.get('items', [])))

    zones_md = []
    for zone in architecture.get('zones', []):
        zone_lines = [f"### Zone: {zone['title']}"]
        if zone.get('subtitle'):
            zone_lines.append(f"Subtitle: {zone['subtitle']}")
        zone_lines.append(bullets(zone.get('items', [])))
        if zone.get('expand'):
            zone_lines.append('Expansion hint: This zone may be expanded into a Level 2 diagram.')
        zones_md.append("\n".join(zone_lines))

    flows_md = bullets([
        f"{flow.get('from')} -> {flow.get('to')}" + (f" ({flow.get('label')})" if flow.get('label') else '')
        for flow in architecture.get('flows', [])
    ]) if architecture.get('flows') else '- None specified'

    ops_md = bullets(architecture.get('operations', [])) if architecture.get('operations') else '- None specified'
    decomp = architecture.get('decomposition', {})

    md = f"""# Draw.io Skill Prompt

## Objective
Create a polished **solution architecture diagram** and export it as **PNG**. Preserve the diagram as editable draw.io source if supported.

## Output format
- Primary export: PNG
- Preserve source: .drawio
- If supported, export as embedded PNG using a `.drawio.png` filename

## Selected layout archetype
- Template id: `{template['id']}`
- Template name: {template['name']}
- Markdown reference: `{template.get('markdown_reference','')}`
- Draw.io preset: `{template.get('drawio',{}).get('preset','architecture')}`

## Layout intent
{template.get('prompt_scaffold','')}

### Layout grammar
{bullets(template.get('layout',{}).get('information_grammar', []))}

### Shape hints
{bullets(template.get('drawio',{}).get('shape_hints', []))}

### Connector style
- {template.get('drawio',{}).get('connector_style','orthogonal')}

## Diagram title
- {architecture.get('title','')}

## Diagram subtitle
- {architecture.get('subtitle','')}

## Structural content

### Lanes
{"\n\n".join(lanes_md) if lanes_md else '- No lanes provided'}

### Capability zones
{"\n\n".join(zones_md)}

### Flows
{flows_md}

### Operations / cross-cutting layer
{ops_md}

### Footer
- {architecture.get('footer', '')}

## Mandatory layout quality rules
- Wrap all text inside boxes and containers.
- Do not allow text to overflow box boundaries.
- Do not overlap text with adjacent boxes, connectors, icons, or arrows.
- Increase box size or spacing when wrapping is needed.
- Prefer shorter labels over tiny unreadable fonts.
- Keep the overview diagram clean and presentation-ready.

## Multi-level decomposition rules
- This diagram should be treated as the Level 1 overview unless otherwise specified.
- If content is dense, reduce detail in the overview and create additional Level 2 expansion diagrams.
- Use consistent naming between the overview and expansion diagrams.
- Respect decomposition preferences: auto_expand={decomp.get('auto_expand', True)}, max_overview_zones={decomp.get('max_overview_zones', 6)}, max_items_per_zone_overview={decomp.get('max_items_per_zone_overview', 5)}, create_capability_children={decomp.get('create_capability_children', True)}.

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
"""

    Path(args.output).write_text(md, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
