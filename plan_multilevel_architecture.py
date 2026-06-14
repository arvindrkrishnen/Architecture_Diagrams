#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_template_defaults(spec: Dict[str, Any], patterns_path: Path) -> Dict[str, Any]:
    default = {
        'max_overview_zones': 6,
        'max_items_per_zone_overview': 5,
        'preferred_canvas': 'landscape',
        'l2_trigger_strategy': 'zone_item_count'
    }
    if not patterns_path.exists():
        return default
    patterns = load_json(patterns_path)
    tid = spec.get('template', 'platform_value_chain')
    template = next((t for t in patterns.get('templates', []) if t.get('id') == tid), None)
    if not template:
        return default
    default.update(template.get('decomposition_defaults', {}))
    return default


def effective_decomposition(spec: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    user = spec.get('decomposition', {}) or {}
    eff = dict(defaults)
    # User can override upward/downward intentionally, but defaults set template-aware starting point.
    for key in ['max_overview_zones', 'max_items_per_zone_overview']:
        if key in user:
            eff[key] = int(user.get(key) or eff[key])
    eff['auto_expand'] = bool(user.get('auto_expand', True))
    eff['create_capability_children'] = bool(user.get('create_capability_children', True))
    eff['strategy_source'] = 'template_defaults_with_user_overrides'
    return eff


def should_expand_zone(zone: Dict[str, Any], eff: Dict[str, Any]) -> bool:
    if zone.get('expand', False):
        return True
    if not eff.get('auto_expand', True):
        return False
    items = zone.get('items', [])
    children = zone.get('children', [])
    max_items = int(eff.get('max_items_per_zone_overview', 5))
    strategy = eff.get('l2_trigger_strategy', 'zone_item_count')
    if len(items) > max_items:
        return True
    if children:
        return True
    if strategy in {'flow_count', 'runtime_complexity', 'data_lifecycle_complexity', 'control_plane_complexity'} and len(items) >= max(4, max_items - 1):
        return True
    return False


def plan(spec: Dict[str, Any], patterns_path: Path) -> Dict[str, Any]:
    defaults = get_template_defaults(spec, patterns_path)
    eff = effective_decomposition(spec, defaults)
    max_items = int(eff.get('max_items_per_zone_overview', 5))
    max_zones = int(eff.get('max_overview_zones', 6))
    create_children = bool(eff.get('create_capability_children', True))

    overview = {
        'title': spec.get('title', ''),
        'subtitle': spec.get('subtitle', ''),
        'template': spec.get('template', ''),
        'output_basename': 'solution_architecture_overview',
        'zones': [],
        'notes': 'Level 1 overview diagram optimized for executive readability',
        'decomposition_defaults': eff
    }
    expansions = []
    zones = spec.get('zones', [])
    for z in zones[:max_zones]:
        overview_zone = dict(z)
        overview_zone['items'] = z.get('items', [])[:max_items]
        overview['zones'].append(overview_zone)

        if create_children and should_expand_zone(z, eff):
            expansions.append({
                'parent_zone_id': z.get('id'),
                'parent_zone_title': z.get('title'),
                'title': f"{z.get('title')} — Level 2 Expansion",
                'subtitle': f"Detailed expansion of {z.get('title')}",
                'output_basename': f"solution_architecture_capability_{len(expansions)+1:02d}",
                'template': spec.get('template', 'platform_value_chain'),
                'items': z.get('items', []),
                'children': z.get('children', [])
            })

    # Overflow zones get their own appendix expansion instead of crowding L1.
    if len(zones) > max_zones and create_children:
        overflow = zones[max_zones:]
        expansions.append({
            'parent_zone_id': 'additional_capabilities',
            'parent_zone_title': 'Additional Capabilities',
            'title': 'Additional Capabilities — Level 2 Expansion',
            'subtitle': 'Capabilities intentionally moved out of the Level 1 overview to preserve executive readability',
            'output_basename': f"solution_architecture_capability_{len(expansions)+1:02d}",
            'template': spec.get('template', 'platform_value_chain'),
            'items': [z.get('title', '') for z in overflow],
            'children': [{'title': z.get('title',''), 'items': z.get('items', [])} for z in overflow]
        })

    return {
        'overview': overview,
        'expansions': expansions,
        'summary': {
            'has_expansions': bool(expansions),
            'expansion_count': len(expansions),
            'template_aware_decomposition': eff,
            'overview_zone_count': len(overview['zones']),
            'moved_to_expansion_count': max(0, len(zones) - max_zones)
        }
    }


def main() -> None:
    ap = argparse.ArgumentParser(description='Create a template-aware multi-level plan for overview and expansion architecture diagrams')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--patterns', default='data/reference_architecture_patterns.json')
    args = ap.parse_args()
    spec = load_json(Path(args.input))
    patterns_path = Path(args.patterns) if Path(args.patterns).is_absolute() else ROOT / args.patterns
    save_json(Path(args.output), plan(spec, patterns_path))
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
