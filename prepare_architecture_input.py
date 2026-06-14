#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent

ALLOWED_TEMPLATES = {
    "platform_value_chain", "composite_ai_platform", "cloud_tenant_microservices",
    "enterprise_endpoint_management", "cloud_data_platform", "cloud_service_operating_model",
    "service_orchestration_workflow", "iot_ot_security_layers", "modern_data_lakehouse",
    "identity_multicloud_control_plane",
}

CONNECTOR_PATTERNS = {
    'sync_api','async_event','batch_etl','streaming','webhook','pub_sub','grpc','file_transfer','database_replication','logical'
}


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def clean_text(s: Any, max_len: int | None = None) -> str:
    if s is None:
        return ""
    s = re.sub(r'\s+', ' ', str(s)).strip()
    if max_len and len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def dedupe_preserve(items: List[str]) -> List[str]:
    seen = set(); out = []
    for item in items:
        item = clean_text(item)
        if item and item.lower() not in seen:
            seen.add(item.lower()); out.append(item)
    return out


def load_domain_vocab(domain: str, vocab_dir: Path) -> Dict[str, Any]:
    if not domain:
        return {}
    path = vocab_dir / f'{domain}.json'
    if path.exists():
        return load_json(path)
    return {}


def flatten_text(data: Dict[str, Any]) -> str:
    parts=[]
    for k in ['title','subtitle','footer','business_outcome_description']:
        parts.append(str(data.get(k,'')))
    for lane in data.get('lanes', []):
        parts.append(str(lane.get('title',''))); parts.extend(map(str, lane.get('items', [])))
    for zone in data.get('zones', []):
        parts.append(str(zone.get('title',''))); parts.append(str(zone.get('subtitle',''))); parts.extend(map(str, zone.get('items', [])))
    parts.extend(map(str, data.get('operations', [])))
    return ' '.join(parts).lower()


def apply_domain_vocabulary(data: Dict[str, Any], domain: str, vocab_dir: Path) -> Dict[str, Any]:
    vocab = load_domain_vocab(domain, vocab_dir)
    if not vocab:
        return data
    text = flatten_text(data)
    matches=[]
    for term, meta in vocab.get('terms', {}).items():
        if term.lower() in text:
            matches.append({'term': term, **meta})
    if not matches:
        return data

    data['domain'] = vocab.get('domain', domain)
    data.setdefault('domain_context', {})
    data['domain_context']['matched_terms'] = matches

    # Add cross-cutting defaults if not already present.
    ops = list(data.get('operations', []))
    ops.extend(vocab.get('cross_cutting_defaults', []))
    data['operations'] = dedupe_preserve([clean_text(x, 60) for x in ops])[:16]

    # Add inferred canonical domain terms to a domain-specific zone so diagrams do not miss important regulated services.
    canonicals = dedupe_preserve([m.get('canonical','') for m in matches if m.get('canonical')])
    if canonicals:
        target_id = 'domain_controls'
        existing = next((z for z in data.get('zones', []) if z.get('id') == target_id), None)
        if existing:
            existing['items'] = dedupe_preserve(existing.get('items', []) + canonicals)[:12]
            existing['expand'] = True
        else:
            data.setdefault('zones', []).append({
                'id': target_id,
                'title': 'Domain Controls',
                'subtitle': f"{vocab.get('domain', domain).replace('_',' ').title()} context",
                'items': canonicals[:12],
                'expand': True,
                'children': []
            })
    if vocab.get('annotation_defaults'):
        data.setdefault('annotations', [])
        data['annotations'].extend(vocab.get('annotation_defaults', []))
    return data


def normalize_child(child: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'title': clean_text(child.get('title', ''), 80),
        'subtitle': clean_text(child.get('subtitle', ''), 120),
        'items': dedupe_preserve([clean_text(x, 60) for x in child.get('items', []) if clean_text(x, 60)])[:12]
    }


def normalize(data: Dict[str, Any], domain: str = '', vocab_dir: Path | None = None) -> Dict[str, Any]:
    out = dict(data)
    if domain:
        out['domain'] = domain
    if vocab_dir:
        out = apply_domain_vocabulary(out, out.get('domain',''), vocab_dir)

    out['title'] = clean_text(out.get('title', ''), 120) or 'Solution Architecture'
    out['subtitle'] = clean_text(out.get('subtitle', ''), 220)
    out['business_outcome_description'] = clean_text(out.get('business_outcome_description',''), 500)

    template = clean_text(out.get('template', 'platform_value_chain'))
    if template not in ALLOWED_TEMPLATES:
        raise ValueError(f'Invalid template: {template}')
    out['template'] = template

    lanes=[]
    for lane in out.get('lanes', []):
        side = clean_text(lane.get('side', 'left')) or 'left'
        if side not in {'left','right','top','bottom'}:
            side = 'left'
        lanes.append({
            'side': side,
            'title': clean_text(lane.get('title','Lane'), 60),
            'items': dedupe_preserve([clean_text(x, 50) for x in lane.get('items', []) if clean_text(x, 50)])[:12]
        })
    out['lanes'] = lanes

    zones=[]
    for zone in out.get('zones', []):
        zid = clean_text(zone.get('id',''))
        title = clean_text(zone.get('title',''), 80)
        subtitle = clean_text(zone.get('subtitle',''), 120)
        items = dedupe_preserve([clean_text(x, 60) for x in zone.get('items', []) if clean_text(x, 60)])[:12]
        if not zid or not title or not items:
            continue
        zout = {
            'id': re.sub(r'[^a-z0-9_-]+','_', zid.lower())[:40],
            'title': title,
            'subtitle': subtitle,
            'items': items,
            'columns': int(zone.get('columns', 1) or 1),
            'expand': bool(zone.get('expand', False))
        }
        if zone.get('color'):
            zout['color'] = clean_text(zone.get('color'), 7)
        children = [normalize_child(c) for c in zone.get('children', [])]
        children = [c for c in children if c.get('title') or c.get('items')]
        if children:
            zout['children'] = children
        zones.append(zout)
    if len(zones) < 2:
        raise ValueError('At least two valid zones are required')
    out['zones'] = zones
    valid_ids = {z['id'] for z in zones}

    flows=[]
    for flow in out.get('flows', []):
        src = clean_text(flow.get('from',''), 40)
        dst = clean_text(flow.get('to',''), 40)
        if not src or not dst:
            continue
        if src not in valid_ids or dst not in valid_ids:
            raise ValueError(f'Flow references unknown zone id: {src} -> {dst}')
        pattern = clean_text(flow.get('pattern') or flow.get('protocol_style') or 'logical')
        if pattern not in CONNECTOR_PATTERNS:
            # infer common patterns from label
            label_l = clean_text(flow.get('label','')).lower()
            if any(x in label_l for x in ['event','kafka','stream']): pattern = 'async_event'
            elif any(x in label_l for x in ['batch','etl','file']): pattern = 'batch_etl'
            elif 'webhook' in label_l: pattern = 'webhook'
            else: pattern = 'sync_api' if any(x in label_l for x in ['api','rest','graphql','request']) else 'logical'
        item = {'from': src, 'to': dst, 'pattern': pattern, 'direction': clean_text(flow.get('direction','source_to_target')) or 'source_to_target'}
        if flow.get('label'): item['label'] = clean_text(flow.get('label'), 60)
        if flow.get('payload_type'): item['payload_type'] = clean_text(flow.get('payload_type'), 100)
        if flow.get('protocol_style'): item['protocol_style'] = clean_text(flow.get('protocol_style'), 100)
        if flow.get('timing'): item['timing'] = clean_text(flow.get('timing'), 40)
        flows.append(item)
    out['flows'] = flows[:30]

    ops = [clean_text(x, 60) for x in out.get('operations', []) if clean_text(x, 60)]
    out['operations'] = dedupe_preserve(ops)[:16]
    out['footer'] = clean_text(out.get('footer',''), 180)

    annotations=[]
    for ann in out.get('annotations', []):
        if ann.get('label'):
            annotations.append({
                'type': clean_text(ann.get('type','callout'), 40),
                'target_zone_id': clean_text(ann.get('target_zone_id',''), 40),
                'label': clean_text(ann.get('label',''), 120),
                'color_role': clean_text(ann.get('color_role','accent_highlight'), 40)
            })
    if annotations:
        out['annotations'] = annotations[:12]

    d = out.get('decomposition', {}) or {}
    out['decomposition'] = {
        'auto_expand': bool(d.get('auto_expand', True)),
        'max_overview_zones': int(d.get('max_overview_zones', 6) or 6),
        'max_items_per_zone_overview': int(d.get('max_items_per_zone_overview', 5) or 5),
        'create_capability_children': bool(d.get('create_capability_children', True))
    }
    out['rendering_preferences'] = out.get('rendering_preferences', {'backend':'drawio-skill','format':'png','embed_xml':True})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description='Normalize and validate architecture JSON input with optional domain vocabulary enrichment')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--domain', default='')
    ap.add_argument('--domain-vocab-dir', default='data/domain_vocabularies')
    args = ap.parse_args()
    raw = load_json(Path(args.input))
    vocab_dir = Path(args.domain_vocab_dir) if Path(args.domain_vocab_dir).is_absolute() else ROOT / args.domain_vocab_dir
    normalized = normalize(raw, domain=args.domain, vocab_dir=vocab_dir)
    save_json(Path(args.output), normalized)
    print(f'Wrote normalized input to {args.output}')


if __name__ == '__main__':
    main()
