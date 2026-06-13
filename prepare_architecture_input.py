#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ALLOWED_TEMPLATES = {
    "platform_value_chain",
    "composite_ai_platform",
    "cloud_tenant_microservices",
    "enterprise_endpoint_management",
    "cloud_data_platform",
}


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def clean_text(s, max_len=None):
    if s is None:
        return ""
    s = str(s)
    s = re.sub(r'\s+', ' ', s).strip()
    if max_len and len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def dedupe_preserve(items):
    seen = set()
    out = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def normalize(data):
    out = dict(data)
    out['title'] = clean_text(out.get('title', ''), 120)
    out['subtitle'] = clean_text(out.get('subtitle', ''), 220)

    template = clean_text(out.get('template', 'platform_value_chain'))
    if template not in ALLOWED_TEMPLATES:
        raise ValueError(f'Invalid template: {template}')
    out['template'] = template

    lanes = []
    for lane in out.get('lanes', []):
        items = [clean_text(x, 50) for x in lane.get('items', []) if clean_text(x, 50)]
        items = dedupe_preserve(items)[:12]
        lanes.append({
            'side': clean_text(lane.get('side', 'left')),
            'title': clean_text(lane.get('title', 'Lane'), 60),
            'items': items,
        })
    out['lanes'] = lanes

    zones = []
    for zone in out.get('zones', []):
        zid = clean_text(zone.get('id', ''))
        title = clean_text(zone.get('title', ''), 80)
        subtitle = clean_text(zone.get('subtitle', ''), 120)
        items = [clean_text(x, 60) for x in zone.get('items', []) if clean_text(x, 60)]
        items = dedupe_preserve(items)[:12]
        if not zid or not title or not items:
            raise ValueError('Each zone must have id, title, and at least one item')
        zones.append({
            'id': zid,
            'title': title,
            'subtitle': subtitle,
            'items': items,
            'columns': int(zone.get('columns', 1) or 1)
        })
    if len(zones) < 2:
        raise ValueError('At least two zones are required')
    out['zones'] = zones
    valid_ids = {z['id'] for z in zones}

    flows = []
    for flow in out.get('flows', []):
        src = clean_text(flow.get('from', ''), 40)
        dst = clean_text(flow.get('to', ''), 40)
        lbl = clean_text(flow.get('label', ''), 60)
        if not src or not dst:
            continue
        if src not in valid_ids or dst not in valid_ids:
            raise ValueError(f'Flow references unknown zone id: {src} -> {dst}')
        item = {'from': src, 'to': dst}
        if lbl:
            item['label'] = lbl
        flows.append(item)
    out['flows'] = flows[:30]

    ops = [clean_text(x, 60) for x in out.get('operations', []) if clean_text(x, 60)]
    out['operations'] = dedupe_preserve(ops)[:12]
    out['footer'] = clean_text(out.get('footer', ''), 180)
    out['rendering_preferences'] = out.get('rendering_preferences', {
        'backend': 'drawio-skill', 'format': 'png', 'embed_xml': True
    })
    return out


def main():
    ap = argparse.ArgumentParser(description='Normalize and validate architecture JSON input')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    raw = load_json(args.input)
    normalized = normalize(raw)
    save_json(args.output, normalized)
    print(f'Wrote normalized input to {args.output}')


if __name__ == '__main__':
    main()
