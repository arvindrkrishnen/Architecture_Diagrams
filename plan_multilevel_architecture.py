#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    ap = argparse.ArgumentParser(description='Create a multi-level plan for overview and expansion architecture diagrams')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    spec = load_json(args.input)
    decomp = spec.get('decomposition', {})
    max_items = decomp.get('max_items_per_zone_overview', 5)
    auto_expand = decomp.get('auto_expand', True)
    create_children = decomp.get('create_capability_children', True)

    overview = {
        'title': spec.get('title', ''),
        'subtitle': spec.get('subtitle', ''),
        'template': spec.get('template', ''),
        'output_basename': 'solution_architecture_overview',
        'zones': [],
        'notes': 'Level 1 overview diagram'
    }
    expansions = []

    for z in spec.get('zones', []):
        overview_zone = dict(z)
        overview_zone['items'] = z.get('items', [])[:max_items]
        overview['zones'].append(overview_zone)

        need_expand = z.get('expand', False) or (auto_expand and len(z.get('items', [])) > max_items)
        if create_children and need_expand:
            expansions.append({
                'parent_zone_id': z.get('id'),
                'parent_zone_title': z.get('title'),
                'title': f"{z.get('title')} — Level 2 Expansion",
                'subtitle': f"Detailed expansion of {z.get('title')}",
                'output_basename': f"solution_architecture_capability_{len(expansions)+1:02d}",
                'template': 'platform_value_chain',
                'items': z.get('items', []),
                'children': z.get('children', [])
            })

    plan = {
        'overview': overview,
        'expansions': expansions,
        'summary': {
            'has_expansions': len(expansions) > 0,
            'expansion_count': len(expansions)
        }
    }
    save_json(args.output, plan)
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
