#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def bullets(items, indent=0):
    pad = ' ' * indent
    return "\n".join(f"{pad}- {item}" for item in items)


def md_table(rows, headers):
    out=['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |']
    for r in rows:
        out.append('| ' + ' | '.join(str(x).replace('|','/') for x in r) + ' |')
    return '\n'.join(out)


def find_icon_hint(name: str, registry: Dict[str, Any]) -> Dict[str, str]:
    t=name.lower()
    for canonical, meta in registry.get('components', {}).items():
        if any(k.lower() in t for k in meta.get('keywords', [])):
            return {'canonical': canonical, 'library': meta.get('library',''), 'shape_hint': meta.get('shape_hint',''), 'domain': meta.get('domain','')}
    return {'canonical': name, 'library': 'Generic draw.io', 'shape_hint': 'rounded rectangle with short descriptive symbol', 'domain': 'platform_control_plane'}


def component_catalog(architecture: Dict[str, Any], registry: Dict[str, Any], style: Dict[str, Any]) -> str:
    am = architecture.get('architecture_model', {})
    rows=[]
    for cap in am.get('business_capabilities', []):
        rows.append([cap.get('name',''), 'business_capability', 'Business capability / value stream box', style.get('domains',{}).get('business_capability',{}).get('color',''), cap.get('owner','')])
    for cat, svcs in am.get('technical_services', {}).items():
        for svc in svcs:
            hint = find_icon_hint(svc.get('name',''), registry)
            rows.append([svc.get('name',''), cat, f"{hint['library']} / {hint['shape_hint']}", style.get('domains',{}).get(cat,{}).get('color',''), svc.get('purpose','')])
    for actor in am.get('actors_users_personas', []):
        rows.append([actor.get('name',''), 'actor_persona', 'Actor/person icon or muted persona card', '#F3F4F6', actor.get('interaction','')])
    for ext in am.get('external_systems', []):
        rows.append([ext.get('name',''), 'external_system', 'External system container / muted rectangle', style.get('domains',{}).get('external_system',{}).get('color','#F3F4F6'), ext.get('interaction','')])
    return md_table(rows[:80], ['Component','Domain','Icon / shape instruction','Color family','Purpose']) if rows else '- Use the provided zones and lane labels as the component catalog.'


def flows_md(architecture: Dict[str, Any]) -> str:
    am=architecture.get('architecture_model', {})
    flows=am.get('key_integrations_data_flows', [])
    rows=[]
    for f in flows:
        rows.append([f.get('from',''), f.get('to',''), f.get('label',''), f.get('protocol_style',''), f.get('payload_type',''), f.get('direction','')])
    for f in architecture.get('flows', []):
        rows.append([f.get('from',''), f.get('to',''), f.get('label',''), 'logical', 'architecture payload', 'source_to_target'])
    return md_table(rows[:60], ['From','To','Label','Protocol/style','Payload','Direction']) if rows else '- No explicit flows specified; infer simple orthogonal flows based on layout.'


def mapping_md(architecture: Dict[str, Any]) -> str:
    rows=[]
    for m in architecture.get('architecture_model', {}).get('business_to_technical_mapping', []):
        realized=', '.join(f"{x.get('technical_service')} ({x.get('category')})" for x in m.get('realized_by', [])[:6])
        rows.append([m.get('business_capability',''), ', '.join(m.get('outcomes', [])), realized])
    return md_table(rows, ['Business capability','Outcome','Realized by technical services']) if rows else '- Map each capability zone to the technical components shown within or adjacent to it.'


def main():
    ap = argparse.ArgumentParser(description='Build a prescriptive drawio-skill prompt from enriched architecture JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json')
    ap.add_argument('--output', required=True)
    ap.add_argument('--view-plan', default='')
    ap.add_argument('--view-id', default='')
    ap.add_argument('--icon-registry', default='data/icon_registry.json')
    ap.add_argument('--style-guide', default='data/style_guide.json')
    args = ap.parse_args()

    architecture = load_json(Path(args.input))
    patterns = load_json(Path(args.patterns))
    assets_lib = load_json(Path(args.patterns).parent / 'reference_asset_library.json') if (Path(args.patterns).parent / 'reference_asset_library.json').exists() else {'assets': []}
    registry = load_json(Path(args.icon_registry)) if Path(args.icon_registry).exists() else {'components': {}}
    style_guide = load_json(Path(args.style_guide)) if Path(args.style_guide).exists() else {'domains': {}}
    view_plan = load_json(Path(args.view_plan)) if args.view_plan and Path(args.view_plan).exists() else {}
    selected_view = None
    if args.view_id:
        selected_view = next((v for v in view_plan.get('recommended_views', []) if v.get('id') == args.view_id), None)
    if selected_view and selected_view.get('recommended_template'):
        template_id = selected_view['recommended_template']
    else:
        template_id = architecture.get('template', 'platform_value_chain')
    template = next((t for t in patterns.get('templates', []) if t.get('id') == template_id), None) or next((t for t in patterns.get('templates', []) if t.get('id') == architecture.get('template')), {})

    style_profiles = patterns.get('style_profiles', {})
    style_profile = style_profiles.get(template.get('style_profile', ''), {})
    asset_map = {a['id']: a for a in assets_lib.get('assets', [])}
    asset_notes=[]
    for aid in template.get('reference_assets', []):
        a=asset_map.get(aid)
        if a:
            asset_notes.append(f"- {a.get('title')} | family={a.get('layout_family')} | intent={a.get('architecture_communication_intent')} | placement={a.get('box_placement_model')} | palette={', '.join(a.get('palette', [])[:5])}")

    lanes_md=[]
    for lane in architecture.get('lanes', []):
        lanes_md.append(f"### {lane.get('side','').title()} lane — {lane.get('title','Lane')}\n" + bullets(lane.get('items', [])))
    zones_md=[]
    for zone in architecture.get('zones', []):
        lines=[f"### Zone: {zone.get('title')}"]
        if zone.get('subtitle'): lines.append(f"Subtitle: {zone.get('subtitle')}")
        lines.append(bullets(zone.get('items', [])))
        zones_md.append('\n'.join(lines))
    ops_md=bullets(architecture.get('operations', [])) if architecture.get('operations') else '- Use cross-cutting concerns from the enriched model.'
    am=architecture.get('architecture_model', {})
    concerns=am.get('cross_cutting_concerns', {})
    concerns_md='\n'.join(f"- **{k.title()}**: {', '.join(v)}" for k,v in concerns.items() if v) or '- None specified'
    view_name=selected_view.get('name') if selected_view else 'Logical / Solution Architecture View'
    view_strategy=selected_view.get('layout_strategy') if selected_view else 'Use the selected primary architecture layout family.'

    md=f"""# Draw.io Renderer Prompt

## Overall communication goal
{am.get('communication_goal') or architecture.get('business_outcome_description') or 'Show how the architecture connects capabilities, services, integrations, and controls to deliver the business outcome.'}

## View type and layout strategy
- **View:** {view_name}
- **View ID:** {selected_view.get('id','default_logical_view') if selected_view else 'default_logical_view'}
- **Layout strategy:** {view_strategy}
- **Primary layout template:** `{template.get('id', template_id)}`
- **Template name:** {template.get('name','')}
- **Draw.io preset:** architecture

## Executive polish requirement
Design this as an executive-ready architecture artifact: strong visual hierarchy, clear focal point, generous but not wasteful whitespace, minimal cognitive load on Level 1, and clean separation between business capabilities, technical services, integrations, and controls.

## Style profile and palette
- Style profile: {template.get('style_profile','')}
- Primary: {style_profile.get('primary','')}
- Secondary: {style_profile.get('secondary','')}
- Accent: {style_profile.get('accent','')}
- Container: {style_profile.get('container','')}
- Border: {style_profile.get('border','')}
- Guidance: {style_profile.get('note','')}

## Internal reference assets to learn from
{chr(10).join(asset_notes) if asset_notes else '- Use the selected template metadata and style guide.'}

## Component catalog with icon and shape instructions
{component_catalog(architecture, registry, style_guide)}

Icon priority rule: For every technical component, use the most semantically accurate official icon from available draw.io libraries such as AWS Architecture Icons, Azure, GCP, Kubernetes, database, security, networking, DevOps, and analytics shapes. Prefer official shapes over generic rectangles. For custom or abstract services, use rounded rectangles with consistent internal styling and a short descriptive icon or symbol.

## Business-to-technical mapping
{mapping_md(architecture)}

Explicitly show how major business capabilities are realized by technical services. Do not leave capabilities disconnected from the platform services that enable them.

## Relationship and flow instructions
{flows_md(architecture)}

Connector rules:
- use meaningful labels such as “events (Kafka)”, “policy evaluation”, “state sync”, “API request”, “audit evidence”, or “data sync” where appropriate
- use orthogonal horizontal/vertical connectors only
- avoid diagonal lines
- route connectors around boxes and avoid crossing container interiors
- separate connector labels from box labels

## Structural content from normalized input

### Diagram title
- {architecture.get('title','')}

### Diagram subtitle
- {architecture.get('subtitle','')}

### Lanes
{chr(10).join(lanes_md) if lanes_md else '- No lanes provided'}

### Capability zones
{chr(10).join(zones_md)}

### Cross-cutting concerns
{concerns_md}

### Operations / cross-cutting layer
{ops_md}

### Footer
- {architecture.get('footer', '')}

## Visual style guide
- Use rounded containers with subtle grouping.
- Use major section header bars.
- Use dashed or dotted borders for VPCs, clusters, trust zones, environments, or external boundaries.
- Include a legend when more than four domains, multiple connector types, trust zones, or overlays are shown.
- Maintain 8–12 px internal padding so text never touches box borders.
- Body text minimum 14 pt, section headers minimum 16 pt, title minimum 26 pt.
- Keep labels concise and wrapped inside boxes.
- Use domain color families from the style guide.

## Completeness and guardrail checklist
Before finalizing the diagram, ensure:
- business capabilities are visible and mapped to enabling services
- technical services are in the correct domain groups
- actors/personas and external systems are positioned outside or at the edges of the solution boundary
- integrations are labeled with direction and protocol/style
- security, compliance, observability, cost, and sustainability concerns appear as overlays or cross-cutting bands when relevant
- all technology names preserve canonical spelling and capitalization
- all text is readable, wrapped, padded, and non-overlapping
- connectors are orthogonal and avoid overlapping boxes
- the diagram has a clear focal point and executive-ready finish

## Final rendering instructions
- Generate the final PNG and editable `.drawio` XML.
- Use this prompt as a precise specification, not as loose inspiration.
- Keep the final artifact original; do not copy internal reference diagrams literally.
"""
    Path(args.output).write_text(md, encoding='utf-8')
    print(f'Wrote {args.output}')

if __name__ == '__main__':
    main()
