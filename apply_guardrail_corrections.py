#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def collect_issues(report: Dict[str, Any]) -> List[str]:
    issues=[]
    for key in ['issues','warnings','errors']:
        val = report.get(key, [])
        if isinstance(val, list):
            issues.extend([str(x) for x in val])
    for result in report.get('results', []) if isinstance(report.get('results'), list) else []:
        if result.get('status') == 'failed':
            issues.append(f"Render job failed: {result.get('job',{}).get('name')} {result.get('error','')}")
    return issues[:50]


def main() -> None:
    ap=argparse.ArgumentParser(description='Convert guardrail validation failures into prompt correction instructions')
    ap.add_argument('--report', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    report=load_json(Path(args.report))
    issues=collect_issues(report)
    correction={
        'issues': issues,
        'correction_policy': [
            'Increase box size instead of shrinking font below 14pt.',
            'Add 10-12px padding so text does not touch borders.',
            'Use orthogonal connectors routed around boxes.',
            'Shorten long labels and move details to Level 2 diagrams.',
            'Preserve canonical technology capitalization.'
        ],
        'max_correction_cycles': 2
    }
    save_json(Path(args.output), correction)
    print(f'Wrote correction instructions to {args.output}')


if __name__ == '__main__':
    main()
