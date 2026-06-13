#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

VARIANT_PROFILES = [
    {
        'id': 'variant_01',
        'name': 'Recommended enterprise view',
        'intent': 'Balanced CIO-ready architecture view using the top-ranked layout and palette recommendation.',
        'density': 'medium',
        'font_bias': 'standard ADA-readable',
        'detail_guidance': 'Show key capabilities, cross-cutting controls, and major flows.'
    },
    {
        'id': 'variant_02',
        'name': 'Alternate style view',
        'intent': 'Alternative palette or second recommended layout for visual preference selection.',
        'density': 'medium',
        'font_bias': 'standard ADA-readable',
        'detail_guidance': 'Preserve the same architecture content but vary layout/palette treatment.'
    },
    {
        'id': 'variant_03',
        'name': 'Executive simplified view',
        'intent': 'More whitespace, fewer boxes, larger fonts, stronger business outcome narrative.',
        'density': 'low',
        'font_bias': 'larger ADA-readable',
        'detail_guidance': 'Show only the most important capabilities and move detail to Level 2 if needed.'
    }
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def business_outcome_description(spec):
    if spec.get('business_outcome_description'):
        return spec['business_outcome_description']
    capabilities = ', '.join([z.get('title','') for z in spec.get('zones', [])[:3] if z.get('title')])
    outputs = []
    for lane in spec.get('lanes', []):
        if lane.get('side') == 'right':
            outputs.extend(lane.get('items', [])[:3])
    outcome = ', '.join(outputs) or 'measurable business outcomes'
    return f"The architecture connects {capabilities or 'core capabilities'} through governed flows and shared controls to deliver {outcome} with speed, resilience, and executive visibility."

def append_variant_guardrails(prompt_path, profile):
    extra = f'''

## Variant profile
- Variant: {profile['name']}
- Intent: {profile['intent']}
- Density: {profile['density']}
- Font bias: {profile['font_bias']}
- Detail guidance: {profile['detail_guidance']}

## ADA and readability guardrails for this variant
- Body text must be at least 14 pt.
- Section headers must be at least 16 pt.
- The main title must be at least 26 pt.
- Use high contrast text and fills that approximate WCAG AA readability.
- Text must be wrapped and must not touch box borders.
- Use 8-12 px minimum internal padding inside boxes.
- If a label does not fit, enlarge the box, wrap the label, shorten it, or move detail to a Level 2 diagram.
- Connectors must be orthogonal using only horizontal and vertical segments.
- Connectors must route around boxes and must not pass through boxes or over text.
- Use waypoints/elbows to avoid crossing major containers.
- Do not generate evaluation files or JSON files as final user-facing outputs; final outputs are PNG and Draw.io only.
'''
    with open(prompt_path, 'a', encoding='utf-8') as f:
        f.write(extra)

def main():
    ap = argparse.ArgumentParser(description='Generate three drawio prompt variants from normalized architecture input and layout recommendations')
    ap.add_argument('--input', required=True)
    ap.add_argument('--recommendations', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json')
    ap.add_argument('--count', type=int, default=3)
    args = ap.parse_args()

    spec = load_json(Path(args.input))
    rec = load_json(Path(args.recommendations)) if Path(args.recommendations).exists() else {}
    recommendations = rec.get('recommendations', [])
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    specs_dir = out_dir.parent / 'variant_specs'
    specs_dir.mkdir(parents=True, exist_ok=True)

    variant_outputs = []
    for idx, profile in enumerate(VARIANT_PROFILES[:args.count], start=1):
        variant_spec = dict(spec)
        variant_spec['business_outcome_description'] = business_outcome_description(spec)
        chosen = recommendations[0] if recommendations else spec.get('style_selection', {})
        if idx == 2 and len(recommendations) > 1:
            chosen = recommendations[1]
        if idx == 3:
            variant_spec['zones'] = []
            for z in spec.get('zones', [])[:6]:
                nz = dict(z)
                nz['items'] = z.get('items', [])[:3]
                nz['expand'] = True if len(z.get('items', [])) > 3 else z.get('expand', False)
                variant_spec['zones'].append(nz)
        if chosen:
            variant_spec['template'] = chosen.get('primary_layout_template', variant_spec.get('template'))
            variant_spec['style_selection'] = chosen
        variant_spec['variant_profile'] = profile

        spec_path = specs_dir / f"variant_{idx:02d}.json"
        prompt_path = out_dir / f"variant_{idx:02d}.md"
        save_json(spec_path, variant_spec)
        subprocess.run([
            sys.executable, str(ROOT / 'build_drawio_prompt.py'),
            '--input', str(spec_path),
            '--patterns', str(ROOT / args.patterns if not Path(args.patterns).is_absolute() else Path(args.patterns)),
            '--output', str(prompt_path)
        ], check=True)
        append_variant_guardrails(prompt_path, profile)
        variant_outputs.append({'variant': profile['id'], 'name': profile['name'], 'prompt_path': str(prompt_path), 'spec_path': str(spec_path)})

    save_json(out_dir.parent / 'variant_prompt_manifest.json', {'variants': variant_outputs})
    print(f'Wrote {len(variant_outputs)} variant prompts to {out_dir}')

if __name__ == '__main__':
    main()
