#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def has_any(text: str, words: List[str]) -> bool:
    t = text.lower()
    return any(w.lower() in t for w in words)


def all_text(spec: Dict[str, Any]) -> str:
    parts=[spec.get('title',''), spec.get('subtitle','')]
    am=spec.get('architecture_model', {})
    for cap in am.get('business_capabilities', []):
        parts.append(cap.get('name','')); parts.extend(cap.get('outcomes', []))
    for cat, svcs in am.get('technical_services', {}).items():
        parts.extend([x.get('name','') for x in svcs])
    for f in am.get('key_integrations_data_flows', []):
        parts.append(f.get('label','')); parts.append(f.get('protocol_style',''))
    return ' '.join(parts)


def choose_logical_layout(spec: Dict[str, Any]) -> str:
    text = all_text(spec)
    existing = spec.get('template', 'platform_value_chain')
    if has_any(text, ['bronze', 'silver', 'gold', 'lakehouse', 'databricks']): return 'modern_data_lakehouse'
    if has_any(text, ['landing zone', 'entra', 'identity control plane', 'conditional access']): return 'identity_multicloud_control_plane'
    if has_any(text, ['iot', 'ot', 'industrial', 'risk matrix', 'threat']): return 'iot_ot_security_layers'
    if has_any(text, ['service catalog', 'orchestration', 'billing', 'provisioning']): return 'service_orchestration_workflow'
    if has_any(text, ['microservices', 'eks', 'aks', 'gke', 'kubernetes', 'api gateway']): return 'cloud_tenant_microservices'
    return existing


def plan_views(spec: Dict[str, Any]) -> Dict[str, Any]:
    am = spec.get('architecture_model', {})
    text = all_text(spec)
    logical_layout = choose_logical_layout(spec)
    views = [
        {
            'id': 'view_01_executive_business_capability',
            'name': 'Executive / Business Capability View',
            'view_type': 'executive_business_capability',
            'layout_strategy': 'value chain or capability map with key enablers, business outcomes, and a CIO-ready outcome statement',
            'recommended_template': 'platform_value_chain' if len(am.get('business_capabilities', [])) <= 6 else 'composite_ai_platform',
            'audience': 'CIO, executive sponsors, business stakeholders',
            'focus': ['business capabilities', 'owners', 'outcomes', 'value streams', 'key enablers'],
            'artifact_basename': 'view_01_executive_business_capability'
        },
        {
            'id': 'view_02_logical_solution_architecture',
            'name': 'Logical / Solution Architecture View',
            'view_type': 'logical_solution_architecture',
            'layout_strategy': 'primary chosen reference layout with central platform boundary, capability groups, actors, systems, and cross-cutting bands',
            'recommended_template': logical_layout,
            'audience': 'enterprise architects, solution architects, platform owners',
            'focus': ['logical components', 'platform capabilities', 'external systems', 'cross-cutting concerns'],
            'artifact_basename': 'view_02_logical_solution_architecture'
        },
        {
            'id': 'view_03_technical_services_infrastructure',
            'name': 'Technical Services & Infrastructure Detail',
            'view_type': 'technical_services_infrastructure',
            'layout_strategy': 'runtime and deployment view grouped by compute, storage, networking, security, CI/CD, resilience, and observability',
            'recommended_template': 'cloud_tenant_microservices' if has_any(text, ['kubernetes','eks','aks','gke','microservice']) else 'identity_multicloud_control_plane',
            'audience': 'engineering leads, platform teams, cloud/security teams',
            'focus': ['technical services', 'runtime boundaries', 'networking', 'security', 'CI/CD', 'DR'],
            'artifact_basename': 'view_03_technical_services_infrastructure'
        },
        {
            'id': 'view_04_integration_data_flow',
            'name': 'Integration & Data Flow View',
            'view_type': 'integration_data_flow',
            'layout_strategy': 'orthogonal flow view emphasizing APIs, events, sync/async integrations, payload types, and system boundaries',
            'recommended_template': 'service_orchestration_workflow' if len(am.get('key_integrations_data_flows', [])) > 4 else 'platform_value_chain',
            'audience': 'integration architects, data architects, engineering teams',
            'focus': ['APIs', 'events', 'payloads', 'protocol style', 'source-to-target flows'],
            'artifact_basename': 'view_04_integration_data_flow'
        }
    ]
    overlays=[]
    concerns=am.get('cross_cutting_concerns', {})
    if concerns.get('security') or concerns.get('compliance'):
        overlays.append({'id':'overlay_security_compliance','name':'Security & Compliance Overlay','focus':['identity','policy','audit','controls','trust zones']})
    if concerns.get('observability'):
        overlays.append({'id':'overlay_observability','name':'Observability Overlay','focus':['metrics','logs','traces','audit evidence','alerting']})
    if concerns.get('cost'):
        overlays.append({'id':'overlay_cost_finops','name':'Cost / FinOps Overlay','focus':['cost allocation','usage visibility','capacity optimization']})
    if concerns.get('sustainability'):
        overlays.append({'id':'overlay_sustainability','name':'Sustainability Overlay','focus':['right sizing','managed services','efficiency']})

    return {
        'version': '1.0.0',
        'primary_view': views[1]['id'],
        'recommended_views': views,
        'optional_overlays': overlays,
        'hybrid_layout_guidance': [
            'Use central platform plus value-chain flows when the solution has a dominant control plane and clear inputs/outputs.',
            'Add horizontal governance bands when cross-cutting controls are central to the architecture.',
            'Use swimlanes when operational sequence or ownership is the primary message.',
            'Use progression stacks when data or maturity moves through staged zones.'
        ],
        'selection_summary': {
            'logical_layout': logical_layout,
            'secondary_views': [views[0]['id'], views[2]['id'], views[3]['id']],
            'overlay_count': len(overlays)
        }
    }


def main() -> None:
    ap=argparse.ArgumentParser(description='Plan multi-view architecture outputs from an enriched architecture model.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    spec=load_json(Path(args.input))
    save_json(Path(args.output), plan_views(spec))
    print(f'Wrote architecture view plan to {args.output}')

if __name__ == '__main__':
    main()
