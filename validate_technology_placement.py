#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

TECH_RULES = [
    {'keywords': ['aws', 'eks', 'ec2', 'lambda', 's3', 'glue', 'redshift', 'kinesis', 'eventbridge', 'dynamodb', 'cloudwatch', 'cloudtrail', 'iam'], 'expected_zone_terms': ['cloud', 'target', 'platform', 'compute', 'storage', 'common', 'multi-cloud', 'ingestion', 'metadata']},
    {'keywords': ['azure', 'aks', 'entra', 'sentinel', 'pim', 'rbac'], 'expected_zone_terms': ['cloud', 'identity', 'landing', 'target', 'control', 'security']},
    {'keywords': ['gcp', 'google cloud', 'gke'], 'expected_zone_terms': ['cloud', 'target', 'landing']},
    {'keywords': ['rest', 'api', 'graphql', 'mcp', 'gateway'], 'expected_zone_terms': ['interface', 'access', 'delivery', 'control', 'plane', 'api']},
    {'keywords': ['dashboard', 'analytics', 'reporting', 'bi', 'quicksight', 'athena', 'powerbi'], 'expected_zone_terms': ['access', 'delivery', 'output', 'analytics', 'consumption', 'reporting']},
    {'keywords': ['llm', 'ai', 'ml', 'bedrock', 'sagemaker', 'mlops', 'model'], 'expected_zone_terms': ['ai', 'ml', 'analytics', 'compute', 'platform', 'intelligence']},
    {'keywords': ['audit', 'governance', 'compliance', 'evidence', 'ledger', 'waiver', 'policy'], 'expected_zone_terms': ['governance', 'control', 'cross', 'operations', 'assurance', 'audit', 'policy']},
    {'keywords': ['source', 'database', 'files', 'applications', 'iot', 'sensor', 'logs'], 'expected_zone_terms': ['source', 'input', 'ingestion', 'data']},
]


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def contains_kw(text: str, keywords: List[str]) -> bool:
    t = text.lower()
    return any(k.lower() in t for k in keywords)


def zone_context(zone: Dict[str, Any]) -> str:
    return ' '.join([zone.get('id',''), zone.get('title',''), zone.get('subtitle','')] + zone.get('items', [])).lower()


def main() -> None:
    ap = argparse.ArgumentParser(description='Validate likely technology component placement in normalized architecture spec')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--domain-vocab-dir', default='data/domain_vocabularies')
    args = ap.parse_args()

    spec = load_json(Path(args.input))
    domain = spec.get('domain', '') or spec.get('architecture_model', {}).get('domain_context', {}).get('domain', '')
    vocab_rules = []
    vocab_dir = Path(args.domain_vocab_dir) if Path(args.domain_vocab_dir).is_absolute() else Path(__file__).resolve().parent / args.domain_vocab_dir
    vocab_path = vocab_dir / f'{domain}.json' if domain else None
    if vocab_path and vocab_path.exists():
        vocab = load_json(vocab_path)
        for term, meta in vocab.get('terms', {}).items():
            vocab_rules.append({'canonical': meta.get('canonical'), 'expected_zone_terms': [meta.get('zone','').replace('_',' '), meta.get('category','').replace('_',' '), 'governance', 'control']})
    warnings = []
    confirmations = []
    for zone in spec.get('zones', []):
        ctx = zone_context(zone)
        for item in zone.get('items', []):
            item_l = item.lower()
            for rule in TECH_RULES:
                if contains_kw(item_l, rule['keywords']):
                    expected = rule['expected_zone_terms']
                    if any(term in ctx for term in expected):
                        confirmations.append({'component': item, 'zone': zone.get('title'), 'status': 'likely_correct'})
                    else:
                        warnings.append({
                            'component': item,
                            'zone': zone.get('title'),
                            'issue': 'component may be in a semantically weak zone',
                            'expected_zone_terms': expected
                        })
    # Domain vocabulary placement checks.
    for zone in spec.get('zones', []):
        ctx = zone_context(zone)
        for item in zone.get('items', []):
            for rule in vocab_rules:
                canonical = rule.get('canonical') or ''
                if canonical and canonical.lower() in item.lower():
                    if any(term and term in ctx for term in rule.get('expected_zone_terms', [])):
                        confirmations.append({'component': item, 'zone': zone.get('title'), 'status': 'domain_vocab_correct'})
                    else:
                        warnings.append({'component': item, 'zone': zone.get('title'), 'issue': 'domain vocabulary component may be misplaced', 'expected_zone_terms': rule.get('expected_zone_terms')})
    report = {
        'title': spec.get('title'),
        'warning_count': len(warnings),
        'warnings': warnings,
        'confirmation_count': len(confirmations),
        'confirmations': confirmations[:50],
        'guidance': 'Warnings are heuristics. Use them to adjust the normalized JSON before rendering when needed.'
    }
    save_json(Path(args.output), report)
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
