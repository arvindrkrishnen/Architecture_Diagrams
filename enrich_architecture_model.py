#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

TECH_CATEGORIES = [
    'compute', 'data_storage', 'integration_apis', 'security_identity',
    'observability_governance', 'platform_control_plane', 'networking',
    'cicd_devex', 'resilience_dr'
]

CATEGORY_LABELS = {
    'compute': 'Compute',
    'data_storage': 'Data / Storage',
    'integration_apis': 'Integration & APIs',
    'security_identity': 'Security & Identity',
    'observability_governance': 'Observability & Governance',
    'platform_control_plane': 'Platform / Control Plane',
    'networking': 'Networking',
    'cicd_devex': 'CI/CD & DevEx',
    'resilience_dr': 'Resilience & DR'
}

ARCH_DEFAULTS = {
    'microservices_aws': {
        'triggers': ['microservices', 'microservice', 'aws', 'eks', 'ecs', 'lambda'],
        'technical_services': {
            'compute': ['Amazon EKS or ECS', 'Containerized services', 'Serverless workers'],
            'integration_apis': ['Amazon API Gateway', 'EventBridge or Kafka', 'Service-to-service APIs'],
            'security_identity': ['AWS IAM', 'AWS Secrets Manager', 'WAF / ingress controls'],
            'observability_governance': ['CloudWatch metrics', 'Centralized logs', 'Distributed tracing'],
            'cicd_devex': ['CI/CD pipeline', 'Policy-as-code checks', 'Infrastructure as Code'],
            'networking': ['Load balancer', 'Private subnets', 'Service mesh considerations'],
            'resilience_dr': ['Multi-AZ deployment', 'Automated rollback', 'Backup / recovery plan']
        },
        'decisions': ['Use managed cloud services where they reduce operational burden.', 'Apply policy-as-code in CI/CD to enforce architectural controls before deployment.']
    },
    'data_platform': {
        'triggers': ['data platform', 'lakehouse', 'analytics', 'warehouse', 'ingestion', 'etl'],
        'technical_services': {
            'data_storage': ['Object storage / data lake', 'Curated data zones', 'Metadata catalog'],
            'integration_apis': ['Batch ingestion', 'Streaming ingestion', 'API ingestion'],
            'observability_governance': ['Data quality checks', 'Lineage tracking', 'Catalog governance'],
            'security_identity': ['Role-based access', 'Encryption and key management', 'Data classification'],
            'compute': ['Transformation engine', 'Query engine', 'ML / analytics compute']
        },
        'decisions': ['Separate raw, curated, and business-aligned data layers.', 'Use governance and metadata services as cross-cutting controls.']
    },
    'identity_multicloud': {
        'triggers': ['identity', 'landing zone', 'multi-cloud', 'entra', 'iam'],
        'technical_services': {
            'security_identity': ['Identity provider', 'Conditional access', 'Privileged access management'],
            'platform_control_plane': ['Central identity control plane', 'Policy guardrails', 'Landing zone standards'],
            'observability_governance': ['Access audit logs', 'Compliance dashboard', 'Continuous trust evaluation'],
            'networking': ['Secure access path', 'Private connectivity', 'Segmentation boundaries'],
            'resilience_dr': ['Break-glass access', 'Regional failover controls']
        },
        'decisions': ['Centralize identity and policy governance while allowing cloud-local execution.', 'Use separate landing zones to enforce blast-radius control.']
    },
    'ai_agentic': {
        'triggers': ['llm', 'agent', 'agentic', 'genai', 'copilot', 'rag'],
        'technical_services': {
            'platform_control_plane': ['Agent orchestration', 'Prompt registry', 'Tool gateway'],
            'data_storage': ['Vector store', 'Evidence store', 'Prompt / response logs'],
            'integration_apis': ['Model API', 'Tool APIs', 'Event callbacks'],
            'security_identity': ['PII filtering', 'Access policy checks', 'Secrets management'],
            'observability_governance': ['Evaluation traces', 'Model monitoring', 'Audit trail'],
            'cicd_devex': ['Prompt versioning', 'Agent test pipeline', 'Deployment gates']
        },
        'decisions': ['Separate orchestration, knowledge retrieval, and model execution for traceability.', 'Preserve evidence and citations to support explainability.']
    }
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_') or 'item'


def all_text(spec: Dict[str, Any]) -> str:
    parts = [spec.get('title',''), spec.get('subtitle',''), spec.get('footer','')]
    for lane in spec.get('lanes', []):
        parts.append(lane.get('title',''))
        parts.extend(lane.get('items', []))
    for zone in spec.get('zones', []):
        parts.append(zone.get('title',''))
        parts.append(zone.get('subtitle',''))
        parts.extend(zone.get('items', []))
    parts.extend(spec.get('operations', []))
    return ' '.join(parts).lower()


def dedupe(items: List[str]) -> List[str]:
    out=[]; seen=set()
    for item in items:
        item=norm(item)
        if item and item.lower() not in seen:
            seen.add(item.lower()); out.append(item)
    return out


def infer_business_capabilities(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    caps=[]
    outputs=[]
    for lane in spec.get('lanes', []):
        if lane.get('side') in ('right','bottom') or lane.get('title','').lower() in ('outputs','outcomes','business outcomes'):
            outputs.extend(lane.get('items', []))
    if not outputs:
        outputs=['Improved business visibility','Operational efficiency','Governed delivery']
    for idx, zone in enumerate(spec.get('zones', [])[:8], start=1):
        outcome = outputs[min(idx-1, len(outputs)-1)] if outputs else 'Business outcome'
        caps.append({
            'id': f'bc_{idx}',
            'name': zone.get('title', f'Capability {idx}'),
            'owner': 'Business / Platform Owner',
            'outcomes': [outcome],
            'value_streams': [spec.get('title','Solution Value Stream')],
            'realized_by_zone_id': zone.get('id')
        })
    return caps


def infer_actors_and_external_systems(spec: Dict[str, Any]) -> Dict[str, Any]:
    actors=[]; external=[]
    for lane in spec.get('lanes', []):
        title = lane.get('title','').lower()
        for item in lane.get('items', []):
            if any(k in item.lower() for k in ['user','admin','analyst','architect','engineer','operator','auditor','persona']):
                actors.append({'name': item, 'role': 'User / Persona', 'interaction': 'Consumes or governs the solution'})
            elif lane.get('side') == 'left' or 'input' in title or 'source' in title:
                external.append({'name': item, 'type': 'External source/system', 'interaction': 'Provides input or event data'})
            elif lane.get('side') == 'right' or 'output' in title:
                external.append({'name': item, 'type': 'Downstream consumer/system', 'interaction': 'Receives outcomes or insights'})
    if not actors:
        actors=[{'name':'Business users','role':'Consumer','interaction':'Use delivered insights and workflows'}]
    return {'actors': dedupe_obj(actors, 'name'), 'external_systems': dedupe_obj(external, 'name')}


def dedupe_obj(items: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    out=[]; seen=set()
    for item in items:
        val=str(item.get(key,''))
        if val and val.lower() not in seen:
            seen.add(val.lower()); out.append(item)
    return out


def classify_service(name: str) -> str:
    t=name.lower()
    if any(k in t for k in ['eks','ecs','lambda','compute','container','kubernetes','gke','aks','ec2','worker','runtime']): return 'compute'
    if any(k in t for k in ['s3','database','db','rds','dynamodb','storage','lake','warehouse','catalog','vector','metadata','redshift']): return 'data_storage'
    if any(k in t for k in ['api','rest','graphql','mcp','event','queue','kafka','integration','gateway','message','pub/sub']): return 'integration_apis'
    if any(k in t for k in ['iam','identity','security','secret','waf','auth','policy','compliance','access','encryption','key']): return 'security_identity'
    if any(k in t for k in ['audit','log','metric','trace','monitor','observability','governance','ledger','evidence','drift']): return 'observability_governance'
    if any(k in t for k in ['control plane','orchestration','platform','registry','repository']): return 'platform_control_plane'
    if any(k in t for k in ['network','load balancer','lb','vpc','subnet','mesh','ingress','egress','routing']): return 'networking'
    if any(k in t for k in ['ci/cd','pipeline','devex','iac','terraform','deployment','build']): return 'cicd_devex'
    if any(k in t for k in ['dr','resilience','backup','restore','failover','bcp','recovery']): return 'resilience_dr'
    return 'platform_control_plane'


def infer_technical_services(spec: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    buckets={c: [] for c in TECH_CATEGORIES}
    for zone in spec.get('zones', []):
        for item in zone.get('items', []):
            cat = classify_service(item)
            buckets[cat].append({'name': item, 'source_zone_id': zone.get('id'), 'source_zone_title': zone.get('title'), 'purpose': f"Supports {zone.get('title','capability')}"})
    txt = all_text(spec)
    for rule in ARCH_DEFAULTS.values():
        if any(trigger in txt for trigger in rule['triggers']):
            for cat, services in rule.get('technical_services', {}).items():
                for svc in services:
                    buckets[cat].append({'name': svc, 'source_zone_id': '', 'source_zone_title': 'Recommended best-practice service', 'purpose': 'Architecture enrichment'})
    for cat in list(buckets):
        seen=set(); clean=[]
        for svc in buckets[cat]:
            k=svc['name'].lower()
            if k not in seen:
                seen.add(k); clean.append(svc)
        buckets[cat]=clean
    return buckets


def infer_integrations(spec: Dict[str, Any], tech: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    flows=[]
    for f in spec.get('flows', []):
        label = f.get('label','flow')
        style = 'event' if any(k in label.lower() for k in ['event','stream','queue','async']) else 'sync' if any(k in label.lower() for k in ['api','request','query']) else 'logical'
        flows.append({'from': f.get('from'), 'to': f.get('to'), 'label': label, 'direction': 'source_to_target', 'protocol_style': style, 'payload_type': 'business / technical payload'})
    names = [svc['name'] for svcs in tech.values() for svc in svcs]
    if any('API Gateway' in n or 'REST' in n for n in names):
        flows.append({'from':'external_systems','to':'integration_apis','label':'API requests', 'direction':'inbound', 'protocol_style':'sync', 'payload_type':'JSON / HTTP'})
    if any('Kafka' in n or 'EventBridge' in n or 'Queue' in n for n in names):
        flows.append({'from':'core_services','to':'event_processing','label':'events', 'direction':'publish_subscribe', 'protocol_style':'event', 'payload_type':'event envelope'})
    return flows


def infer_cross_cutting(spec: Dict[str, Any], tech: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    base = {
        'security': [], 'compliance': [], 'observability': [], 'cost': [], 'sustainability': []
    }
    ops = ' '.join(spec.get('operations', [])).lower()
    for op in spec.get('operations', []):
        lo=op.lower()
        if any(k in lo for k in ['security','sso','identity','access','secret','policy']): base['security'].append(op)
        elif any(k in lo for k in ['audit','compliance','governance']): base['compliance'].append(op)
        elif any(k in lo for k in ['monitor','observability','log','metric','trace']): base['observability'].append(op)
        elif any(k in lo for k in ['cost','finops']): base['cost'].append(op)
        elif any(k in lo for k in ['sustainability','carbon','energy']): base['sustainability'].append(op)
    if tech.get('security_identity'): base['security'].extend([x['name'] for x in tech['security_identity'][:4]])
    if tech.get('observability_governance'): base['observability'].extend([x['name'] for x in tech['observability_governance'][:4]])
    base['cost'].append('Cost allocation and usage visibility')
    base['sustainability'].append('Efficient managed services and right-sized capacity')
    return {k: dedupe(v) for k,v in base.items()}


def infer_decisions(text: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    txt = all_text(spec) + ' ' + text.lower()
    decisions=[]
    for rule in ARCH_DEFAULTS.values():
        if any(trigger in txt for trigger in rule['triggers']):
            decisions.extend(rule.get('decisions', []))
    if not decisions:
        decisions=['Use a layered architecture to separate business capabilities, platform services, integrations, and cross-cutting controls.']
    assumptions=['The target environment has access to standard cloud, integration, and observability services.', 'Security, audit, and operational controls are required for production readiness.']
    constraints=['Keep executive overview diagrams readable and decompose detailed services into companion views.', 'Use official draw.io icons where available and fallback to styled rounded rectangles for abstract capabilities.']
    return {'assumptions': assumptions, 'constraints': constraints, 'architectural_decisions': dedupe(decisions)}


def map_capabilities_to_technical(caps: List[Dict[str, Any]], tech: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    mapping=[]
    for cap in caps:
        zone_id = cap.get('realized_by_zone_id')
        realized=[]
        for cat, svcs in tech.items():
            for svc in svcs:
                if svc.get('source_zone_id') == zone_id:
                    realized.append({'technical_service': svc['name'], 'category': cat})
        if not realized:
            # Add small default support mapping
            for cat in ['platform_control_plane','integration_apis','observability_governance']:
                for svc in tech.get(cat, [])[:1]:
                    realized.append({'technical_service': svc['name'], 'category': cat})
        mapping.append({'business_capability': cap['name'], 'business_owner': cap['owner'], 'outcomes': cap['outcomes'], 'realized_by': realized[:8]})
    return mapping


def build_component_inventory(spec: Dict[str, Any], tech: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    inv=[]
    for cat, svcs in tech.items():
        for svc in svcs:
            inv.append({'name': svc['name'], 'category': cat, 'category_label': CATEGORY_LABELS.get(cat, cat), 'group': svc.get('source_zone_title',''), 'purpose': svc.get('purpose','')})
    return inv


def enrich(spec: Dict[str, Any], raw_text: str = '') -> Dict[str, Any]:
    enriched = dict(spec)
    business_capabilities = infer_business_capabilities(spec)
    actors_systems = infer_actors_and_external_systems(spec)
    technical_services = infer_technical_services(spec)
    integrations = infer_integrations(spec, technical_services)
    concerns = infer_cross_cutting(spec, technical_services)
    decisions = infer_decisions(raw_text, spec)
    mapping = map_capabilities_to_technical(business_capabilities, technical_services)
    inventory = build_component_inventory(spec, technical_services)

    outcome_text = spec.get('business_outcome_description') or (
        f"{spec.get('title','The solution')} connects business capabilities, platform services, integrations, and cross-cutting controls to deliver governed, resilient, and measurable outcomes for CIO stakeholders."
    )
    enriched['architecture_model'] = {
        'business_capabilities': business_capabilities,
        'technical_services': technical_services,
        'actors_users_personas': actors_systems.get('actors', []),
        'external_systems': actors_systems.get('external_systems', []),
        'key_integrations_data_flows': integrations,
        'cross_cutting_concerns': concerns,
        'assumptions': decisions['assumptions'],
        'constraints': decisions['constraints'],
        'architectural_decisions': decisions['architectural_decisions'],
        'business_to_technical_mapping': mapping,
        'component_inventory': inventory,
        'communication_goal': outcome_text
    }
    enriched['business_outcome_description'] = outcome_text
    return enriched


def main() -> None:
    ap = argparse.ArgumentParser(description='Enrich normalized architecture JSON with business, technical, integration, and decision metadata.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--raw-text', default='')
    ap.add_argument('--raw-text-file', default='')
    args = ap.parse_args()
    spec = load_json(Path(args.input))
    raw = args.raw_text or (Path(args.raw_text_file).read_text(encoding='utf-8') if args.raw_text_file and Path(args.raw_text_file).exists() else '')
    save_json(Path(args.output), enrich(spec, raw))
    print(f'Wrote enriched architecture model to {args.output}')

if __name__ == '__main__':
    main()
