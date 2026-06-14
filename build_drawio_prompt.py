#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def bullets(items: List[Any], indent: int = 0) -> str:
    pad=' ' * indent
    return '\n'.join(f"{pad}- {item}" for item in items)


def md_table(rows: List[List[Any]], headers: List[str]) -> str:
    if not rows:
        return '- None specified'
    out=['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |']
    for row in rows:
        out.append('| ' + ' | '.join(str(x).replace('|','/') for x in row) + ' |')
    return '\n'.join(out)


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in re.findall(r'[A-Za-z0-9+/#.-]+', str(text or '')) if len(t) > 1]


def find_icon_hint(name: str, registry: Dict[str, Any], domain_hint: str = '') -> Dict[str, Any]:
    """Ranked icon resolution: exact -> alias -> keyword score -> domain fallback."""
    t = str(name or '').lower().strip()
    scores: Dict[str, int] = {}
    for canonical, meta in registry.get('components', {}).items():
        kws = [k.lower() for k in meta.get('keywords', [])]
        aliases = [a.lower() for a in meta.get('aliases', [])]
        score = 0
        if t == canonical.lower(): score += 100
        if t in aliases: score += 80
        if canonical.lower() in t: score += 40
        score += sum(4 for a in aliases if a and a in t)
        score += sum(2 for k in kws if k and k in t)
        score += sum(1 for k in kws if t and t in k)
        if domain_hint and meta.get('domain') == domain_hint: score += 5
        if score > 0:
            scores[canonical] = score
    if not scores:
        return {'canonical': name, 'library': 'Generic draw.io', 'shape_hint': 'rounded rectangle with short descriptive symbol', 'domain': domain_hint or 'platform_control_plane', 'fallback_canonical': None}
    ranked = sorted(scores, key=scores.get, reverse=True)
    best = registry['components'][ranked[0]]
    fallback = ranked[1] if len(ranked) > 1 else None
    return {'canonical': ranked[0], 'library': best.get('library',''), 'shape_hint': best.get('shape_hint',''), 'domain': best.get('domain',''), 'fallback_canonical': fallback, 'score': scores[ranked[0]]}


def style_for_domain(style: Dict[str, Any], domain: str) -> Dict[str, Any]:
    domains = style.get('domains', {})
    return domains.get(domain) or domains.get(domain.replace('integration_apis','integration')) or domains.get('platform_control_plane', {})


def component_catalog(architecture: Dict[str, Any], registry: Dict[str, Any], style: Dict[str, Any]) -> str:
    am = architecture.get('architecture_model', {})
    rows=[]
    for cap in am.get('business_capabilities', []):
        dom = style_for_domain(style, 'business_capability')
        rows.append([cap.get('name',''), 'business_capability', 'Business capability / value stream card', f"header {dom.get('header','')} body {dom.get('body', dom.get('color',''))}", cap.get('owner','')])
    for cat, svcs in am.get('technical_services', {}).items():
        for svc in svcs:
            hint = find_icon_hint(svc.get('name',''), registry, cat)
            dom = style_for_domain(style, cat)
            rows.append([svc.get('name',''), cat, f"Primary: {hint['library']} / {hint['shape_hint']}; fallback: {hint.get('fallback_canonical') or 'styled rounded rectangle'}", f"header {dom.get('header','')} body {dom.get('body', dom.get('color',''))} border {dom.get('border','')}", svc.get('purpose','')])
    for actor in am.get('actors_users_personas', []):
        rows.append([actor.get('name',''), 'actor_persona', 'Actor/person icon or muted persona card', '#F3F4F6 / #6B7280', actor.get('interaction','')])
    for ext in am.get('external_systems', []):
        dom = style_for_domain(style, 'external_system')
        rows.append([ext.get('name',''), 'external_system', 'External system container / muted rectangle', f"header {dom.get('header','')} body {dom.get('body', dom.get('color',''))}", ext.get('interaction','')])
    if not rows:
        # fallback from zones
        for zone in architecture.get('zones', []):
            rows.append([zone.get('title',''), 'capability_zone', 'rounded capability container', 'template domain color', zone.get('subtitle','')])
    return md_table(rows[:100], ['Component','Domain','Icon / shape instruction','Exact colors','Purpose'])


def flow_rows(architecture: Dict[str, Any], style: Dict[str, Any]) -> List[List[Any]]:
    am=architecture.get('architecture_model', {})
    connector_styles = style.get('connector_styles', {})
    rows=[]
    for f in am.get('key_integrations_data_flows', []):
        pattern = f.get('pattern') or f.get('protocol_style') or 'sync_api'
        cstyle = connector_styles.get(pattern, connector_styles.get('sync_api', {}))
        rows.append([f.get('from',''), f.get('to',''), f.get('label',''), pattern, f.get('payload_type',''), f.get('direction','source_to_target'), f"{cstyle.get('style','solid')} {cstyle.get('line_width',2)}px {cstyle.get('color','')}"])
    for f in architecture.get('flows', []):
        pattern = f.get('pattern') or 'logical'
        cstyle = connector_styles.get(pattern, connector_styles.get('sync_api', {}))
        rows.append([f.get('from',''), f.get('to',''), f.get('label',''), pattern, f.get('payload_type','architecture payload'), f.get('direction','source_to_target'), f"{cstyle.get('style','solid')} {cstyle.get('line_width',2)}px {cstyle.get('color','')}"])
    return rows[:80]


def mapping_md(architecture: Dict[str, Any]) -> str:
    rows=[]
    for m in architecture.get('architecture_model', {}).get('business_to_technical_mapping', []):
        realized=', '.join(f"{x.get('technical_service')} ({x.get('category')})" for x in m.get('realized_by', [])[:8])
        rows.append([m.get('business_capability',''), m.get('business_owner',''), ', '.join(m.get('outcomes', [])), realized])
    return md_table(rows, ['Business capability','Owner','Outcome','Realized by technical services']) if rows else '- Map each capability zone to enabling technical services.'


def annotations_md(architecture: Dict[str, Any], style: Dict[str, Any]) -> str:
    rows=[]
    ann_rules = style.get('visual_rules', {}).get('annotation_rules', {})
    for a in architecture.get('annotations', []):
        rows.append([a.get('type','callout'), a.get('target_zone_id',''), a.get('label',''), a.get('color_role','accent_highlight'), ann_rules.get(a.get('type','callout'), 'small callout anchored to target')])
    return md_table(rows, ['Type','Target','Label','Color role','Rendering instruction']) if rows else '- No annotations provided. Add no decorative callouts unless needed for clarity.'


def domain_guidance(architecture: Dict[str, Any]) -> str:
    domain = architecture.get('domain') or architecture.get('architecture_model', {}).get('domain_context', {}).get('domain','')
    txt = ' '.join([architecture.get('title',''), architecture.get('subtitle',''), domain]).lower()
    if domain == 'financial_services' or any(k in txt for k in ['bank','capital markets','risk','regulatory','ccar','aml','kyc','basel']):
        return """## Financial services architecture intelligence
- Map CCAR/DFAST, Basel/RWA, CECL, AML/KYC, SOX, BCBS 239, MiFID II, regulatory reporting, and model risk controls into the correct governance, compliance, risk, data, and integration zones.
- Always include a Regulatory & Compliance cross-cutting band when financial regulation is present.
- Add Model Risk Management for AI/ML or decisioning architectures in financial services.
- Label sensitive data flows with data classification when known, such as PII, NPI, or MNPI.
- Use secure enclave / trusted execution boundary styling for sensitive compute zones.
"""
    return ''


def main():
    ap = argparse.ArgumentParser(description='Build a prescriptive drawio-skill prompt from enriched architecture JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json')
    ap.add_argument('--output', required=True)
    ap.add_argument('--view-plan', default='')
    ap.add_argument('--view-id', default='')
    ap.add_argument('--icon-registry', default='data/icon_registry.json')
    ap.add_argument('--style-guide', default='data/style_guide.json')
    ap.add_argument('--correction-report', default='')
    args = ap.parse_args()

    architecture = load_json(Path(args.input))
    patterns = load_json(Path(args.patterns))
    assets_path = Path(args.patterns).parent / 'reference_asset_library.json'
    assets_lib = load_json(assets_path) if assets_path.exists() else {'assets': []}
    registry = load_json(Path(args.icon_registry) if Path(args.icon_registry).is_absolute() else ROOT / args.icon_registry) if (Path(args.icon_registry).is_absolute() or (ROOT / args.icon_registry).exists()) else {'components': {}}
    style_guide = load_json(Path(args.style_guide) if Path(args.style_guide).is_absolute() else ROOT / args.style_guide) if (Path(args.style_guide).is_absolute() or (ROOT / args.style_guide).exists()) else {'domains': {}}
    view_plan = load_json(Path(args.view_plan)) if args.view_plan and Path(args.view_plan).exists() else {}
    corrections = load_json(Path(args.correction_report)) if args.correction_report and Path(args.correction_report).exists() else {}

    selected_view = None
    if args.view_id:
        selected_view = next((v for v in view_plan.get('recommended_views', []) if v.get('id') == args.view_id), None)
    template_id = selected_view.get('recommended_template') if selected_view and selected_view.get('recommended_template') else architecture.get('template','platform_value_chain')
    template = next((t for t in patterns.get('templates', []) if t.get('id') == template_id), None) or {}
    style_profiles = patterns.get('style_profiles', {})
    style_profile = style_profiles.get(template.get('style_profile',''), {})
    selected_palette = architecture.get('style_selection', {}).get('secondary_palette_donor', {}).get('palette', [])
    palette_name = architecture.get('rendering_preferences', {}).get('palette', 'enterprise_light')
    palette = style_guide.get('palettes', {}).get(palette_name, style_guide.get('palettes', {}).get('enterprise_light', {}))
    asset_map={a['id']: a for a in assets_lib.get('assets', [])}
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
    concerns_text='\n'.join(f"- **{k.title()}**: {', '.join(v)}" for k,v in concerns.items() if v) or '- None specified'
    view_name=selected_view.get('name') if selected_view else 'Logical / Solution Architecture View'
    view_strategy=selected_view.get('layout_strategy') if selected_view else 'Use the selected primary architecture layout family.'
    correction_text=''
    if corrections.get('issues'):
        correction_text = '\n## Correction instructions from guardrail pass\nThe following issues were detected and MUST be fixed:\n' + '\n'.join(f"- {x}" for x in corrections.get('issues', [])) + '\n'

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

## Overall communication goal and executive polish
Design this as an executive-ready architecture artifact. The Level-1 view must tell a clear business story in under 10 seconds: what business capability is enabled, how the technical platform realizes it, which controls make it safe, and what measurable outcome it delivers. Use generous but not wasteful whitespace, strong visual hierarchy, and a clear focal point, usually the core platform or control plane.

## Style profile and exact palette
- Requested palette family: `{palette_name}`
- Canvas background: {palette.get('canvas_bg','')}
- Zone header background: {palette.get('zone_header_bg','')}
- Zone body background: {palette.get('zone_body_bg','')}
- Default connector: {palette.get('connector_default','')}
- Async/event connector: {palette.get('connector_async','')}
- Primary text: {palette.get('text_primary','')}
- Secondary text: {palette.get('text_secondary','')}
- Accent highlight: {palette.get('accent_highlight','')}
- Subtle border: {palette.get('border_subtle','')}
- Template style profile: {template.get('style_profile','')}
- Template primary/secondary/accent: {style_profile.get('primary','')} / {style_profile.get('secondary','')} / {style_profile.get('accent','')}
- Palette donor colors from reference assets: {', '.join(selected_palette[:6]) if selected_palette else 'Use exact palette above and template style profile.'}

## Internal reference assets to learn from
{chr(10).join(asset_notes) if asset_notes else '- Use the selected template metadata and style guide.'}

## Component catalog with icon and shape instructions
{component_catalog(architecture, registry, style_guide)}

Icon priority rule: For every technical component, use the most semantically accurate official icon from available draw.io libraries such as AWS Architecture Icons, Azure, GCP, Kubernetes, database, security, networking, DevOps, and analytics shapes. Prefer official shapes over generic rectangles. If multiple icon candidates exist, use the primary canonical icon and keep the fallback as a styled rounded rectangle. For abstract services, use rounded rectangles with consistent internal styling and a short descriptive symbol.

## Business-to-technical mapping
{mapping_md(architecture)}

Explicitly show how major business capabilities are realized by technical services. Do not leave capabilities disconnected from the platform services that enable them.

## Relationship and flow instructions
{md_table(flow_rows(architecture, style_guide), ['From','To','Label','Pattern','Payload','Direction','Connector style'])}

Connector rules:
- Use orthogonal horizontal/vertical connectors only.
- Avoid diagonal lines.
- Route connectors around boxes and avoid crossing box interiors.
- Differentiate connector patterns visually: solid for sync API, dashed for async/event, dotted for batch/file, heavier line for streaming.
- Use meaningful labels such as “events (Kafka)”, “policy evaluation”, “state sync”, “REST / JSON”, “audit evidence”, or “batch file”.
- Separate connector labels from box labels.

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
{concerns_text}

### Operations / cross-cutting layer
{ops_md}

### Annotations and callouts
{annotations_md(architecture, style_guide)}

### Footer
- {architecture.get('footer', '')}

{domain_guidance(architecture)}
## Visual style guide and ADA readability
- Use rounded containers with subtle grouping.
- Use major section header bars.
- Use dashed or dotted borders for VPCs, clusters, trust zones, environments, and external boundaries.
- Include a legend when more than four domains, multiple connector types, trust zones, or overlays are shown.
- Maintain 10–12 px internal padding so text never touches box borders.
- Body text minimum 14 pt; preferred 15–16 pt for executive views.
- Section headers minimum 16 pt; preferred 18–20 pt for executive views.
- Title minimum 26 pt; preferred 30–32 pt for executive views.
- Keep labels concise and wrapped inside boxes.
- Use high contrast: WCAG-friendly contrast between text and container fills.
- Do not shrink text below readable size; expand the box or split the content instead.

## Completeness and guardrail checklist
Before finalizing the diagram, ensure:
- business capabilities are visible and mapped to enabling services
- technical services are in the correct domain groups
- actors/personas and external systems are positioned outside or at the edges of the solution boundary
- integrations are labeled with direction and integration pattern
- security, compliance, observability, cost, and sustainability concerns appear as overlays or cross-cutting bands when relevant
- all technology names preserve canonical spelling and capitalization
- all text is readable, wrapped, padded, and non-overlapping
- connectors are orthogonal and avoid overlapping boxes
- the diagram has a clear focal point and executive-ready finish
- if more than 3 connector styles or 4 domain colors are used, include a legend

## Claude self-evaluation checklist
If rendered in Claude-native mode, self-check before returning output:
- Does the L1 diagram tell a clear business story in under 10 seconds?
- Are capability zones business-friendly and not overly technical?
- Is every flow labeled with direction and integration pattern?
- Are cross-cutting concerns shown as bands or overlays, not scattered boxes?
- Is the color palette consistent and hex-precise?
- Is title ≥26 pt, section text ≥16 pt, body text ≥14 pt?
- Does the subtitle contain a CIO-ready narrative?
- Are external systems and actors positioned at diagram boundaries?
- Does regulated-industry content include a compliance band?
- Is there a legend when multiple connector types or domain colors are used?
{correction_text}
## Final rendering instructions
- Generate the final PNG and editable `.drawio` XML.
- Use this prompt as a precise specification, not as loose inspiration.
- Keep the final artifact original; do not copy internal reference diagrams literally.
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(md, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
