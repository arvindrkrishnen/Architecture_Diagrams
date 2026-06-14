#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def clean(s: str) -> str:
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def outputs(spec: Dict[str, Any]) -> List[str]:
    out=[]
    for lane in spec.get('lanes', []):
        if lane.get('side') == 'right' or lane.get('title','').lower() in {'outputs','outcomes','business outcomes'}:
            out.extend(lane.get('items', []))
    return out[:4]


def caps(spec: Dict[str, Any]) -> List[str]:
    am = spec.get('architecture_model', {})
    c = [x.get('name','') for x in am.get('business_capabilities', []) if x.get('name')]
    if c:
        return c[:4]
    return [z.get('title','') for z in spec.get('zones', []) if z.get('title')][:4]


def infer_problem(text: str, spec: Dict[str, Any]) -> str:
    t = text.lower()
    if any(k in t for k in ['compliance','regulatory','audit','governance','policy']):
        return 'improve governance, compliance assurance, and audit readiness'
    if any(k in t for k in ['data','analytics','insight','reporting']):
        return 'convert fragmented data into trusted, actionable insight'
    if any(k in t for k in ['microservice','platform','cloud','kubernetes','modernization']):
        return 'modernize delivery while improving reliability and operational control'
    if any(k in t for k in ['agent','ai','llm','genai']):
        return 'scale AI-enabled decision support with governance and traceability'
    return 'deliver the target business capability with stronger execution discipline'


def generate(spec: Dict[str, Any], raw_text: str = '') -> Dict[str, Any]:
    title = spec.get('title','The solution')
    capability_names = caps(spec)
    outcome_names = outputs(spec)
    stakeholders = 'CIO stakeholders, business owners, architects, and delivery teams'
    if any('architect' in (x or '').lower() for x in capability_names + [raw_text]):
        stakeholders = 'enterprise architects, platform teams, CIO stakeholders, and delivery pipelines'
    problem = infer_problem(raw_text, spec)
    cap_phrase = ', '.join(capability_names[:3]) or 'the core platform capabilities'
    outcome_phrase = ', '.join(outcome_names[:3]) or 'measurable business outcomes'
    narrative = (
        f"{title} addresses the need to {problem} by organizing {cap_phrase} into a governed operating model. "
        f"The architecture gives {stakeholders} a shared view of how capabilities, services, integrations, and controls work together. "
        f"By connecting business outcomes to technical services and evidence-producing controls, the solution improves delivery speed, resilience, risk management, and executive visibility."
    )
    return {
        'business_narrative': narrative,
        'subtitle_candidate': narrative[:220],
        'capabilities_referenced': capability_names,
        'outcomes_referenced': outcome_names,
        'stakeholders': stakeholders
    }


def main() -> None:
    ap = argparse.ArgumentParser(description='Generate a CIO-ready business narrative for architecture diagrams')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--raw-text', default='')
    ap.add_argument('--raw-text-file', default='')
    args = ap.parse_args()
    spec = load_json(Path(args.input))
    raw = args.raw_text or (Path(args.raw_text_file).read_text(encoding='utf-8') if args.raw_text_file and Path(args.raw_text_file).exists() else '')
    result = generate(spec, raw)
    # Also update the architecture spec with narrative fields for downstream prompt generation.
    spec['business_outcome_description'] = result['business_narrative']
    spec.setdefault('architecture_model', {})
    spec['architecture_model']['communication_goal'] = result['business_narrative']
    result['updated_spec'] = spec
    save_json(Path(args.output), result)
    print(f'Wrote narrative to {args.output}')


if __name__ == '__main__':
    main()
