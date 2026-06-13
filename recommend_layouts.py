#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in re.findall(r'[A-Za-z0-9+/#.-]+', text or '') if len(t) > 1]


def flatten_spec(spec: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in ['title', 'subtitle', 'template', 'footer']:
        if spec.get(key):
            parts.append(str(spec[key]))
    for lane in spec.get('lanes', []):
        parts.append(lane.get('title', ''))
        parts.extend(lane.get('items', []))
    for zone in spec.get('zones', []):
        parts.append(zone.get('title', ''))
        parts.append(zone.get('subtitle', ''))
        parts.extend(zone.get('items', []))
        for child in zone.get('children', []):
            parts.append(child.get('title', ''))
            parts.extend(child.get('items', []))
    parts.extend(spec.get('operations', []))
    for flow in spec.get('flows', []):
        parts.append(flow.get('label', ''))
    return ' '.join([p for p in parts if p])


def score_template(template: Dict[str, Any], asset_map: Dict[str, Dict[str, Any]], text_tokens: set, original_template: str) -> Tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []
    if template['id'] == original_template:
        score += 8
        reasons.append('matches initial normalized template')
    for kw in template.get('best_for', []):
        words = tokenize(kw)
        hits = sum(1 for w in words if w in text_tokens)
        if hits:
            score += 2 * hits
            reasons.append(f'best-for match: {kw}')
    for rule in template.get('visual_rules', []):
        hits = sum(1 for w in tokenize(rule) if w in text_tokens)
        if hits:
            score += hits
    for aid in template.get('reference_assets', []):
        a = asset_map.get(aid, {})
        for sig in a.get('selection_signals', []):
            sig_tokens = tokenize(sig)
            hits = sum(1 for w in sig_tokens if w in text_tokens)
            if hits:
                score += 3 * hits
                reasons.append(f'selection signal: {sig}')
        for use in a.get('use_cases', []):
            hits = sum(1 for w in tokenize(use) if w in text_tokens)
            if hits:
                score += 2 * hits
    return score, reasons[:5]


def choose_palette_donor(primary_template: Dict[str, Any], templates: List[Dict[str, Any]], asset_map: Dict[str, Dict[str, Any]], text_tokens: set) -> Dict[str, Any]:
    # Prefer a style donor from the same primary template; fall back to another relevant style asset.
    candidates = []
    for template in templates:
        for aid in template.get('reference_assets', []):
            asset = asset_map.get(aid, {})
            if not asset:
                continue
            score = 0
            if template['id'] == primary_template['id']:
                score += 10
            for sig in asset.get('selection_signals', []) + asset.get('use_cases', []):
                score += sum(1 for w in tokenize(sig) if w in text_tokens)
            candidates.append((score, template, asset))
    candidates.sort(key=lambda x: x[0], reverse=True)
    score, template, asset = candidates[0]
    return {
        'asset_id': asset.get('id'),
        'asset_title': asset.get('title'),
        'layout_family': asset.get('layout_family'),
        'palette': asset.get('palette', []),
        'style_cues': asset.get('style_cues', {}),
        'why': 'best palette donor for selected primary layout' if template['id'] == primary_template['id'] else 'secondary style donor selected by content match'
    }


def main() -> None:
    ap = argparse.ArgumentParser(description='Recommend primary layout and secondary palette donor for an architecture diagram')
    ap.add_argument('--input', required=True)
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json')
    ap.add_argument('--assets', default='data/reference_asset_library.json')
    ap.add_argument('--output', required=True)
    ap.add_argument('--topn', type=int, default=2)
    args = ap.parse_args()

    spec = load_json(Path(args.input))
    patterns = load_json(ROOT / args.patterns if not Path(args.patterns).is_absolute() else Path(args.patterns))
    assets = load_json(ROOT / args.assets if not Path(args.assets).is_absolute() else Path(args.assets))
    asset_map = {a['id']: a for a in assets.get('assets', [])}
    text_tokens = set(tokenize(flatten_spec(spec)))

    scored = []
    for template in patterns.get('templates', []):
        score, reasons = score_template(template, asset_map, text_tokens, spec.get('template', ''))
        scored.append((score, template, reasons))
    scored.sort(key=lambda x: x[0], reverse=True)

    recommendations = []
    for idx, (score, template, reasons) in enumerate(scored[:max(1, args.topn)], start=1):
        palette = choose_palette_donor(template, patterns.get('templates', []), asset_map, text_tokens)
        recommendations.append({
            'rank': idx,
            'score': score,
            'primary_layout_template': template['id'],
            'primary_layout_name': template.get('name'),
            'style_profile': template.get('style_profile'),
            'secondary_palette_donor': palette,
            'why_this_layout': reasons or ['closest general-purpose match'],
            'communication_intent': template.get('placement_semantics', []),
            'guardrails': [
                'wrap text inside boxes',
                'do not overlap text or connectors',
                'place technology components in semantically correct zones',
                'run spelling and label quality checks after rendering'
            ]
        })

    report = {
        'input_title': spec.get('title'),
        'recommendations': recommendations,
        'default_selected_recommendation': recommendations[0] if recommendations else None,
        'user_selection_guidance': 'Offer recommendation 1 and 2 to the user when interactive selection is possible; otherwise use recommendation 1 as the default.'
    }
    save_json(Path(args.output), report)
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
