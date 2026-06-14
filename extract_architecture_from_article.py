#!/usr/bin/env python3
"""architecture-blog-to-diagram extractor.

Transforms prose-first architecture content into a structured architecture model
and a normalized diagram-generation payload.
"""
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def clean(s: str) -> str:
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def bullets(text: str) -> List[str]:
    items = []
    for line in text.splitlines():
        line = line.strip(' -•\t')
        if line:
            items.append(clean(line))
    return items


def title_from_text(text: str) -> str:
    for line in text.splitlines():
        line = clean(line.strip('# '))
        if line and len(line) < 140:
            return line
    return 'Architecture from Article'


def infer_style(text: str) -> str:
    t = text.lower()
    if 'control plane' in t: return 'control-plane'
    if any(k in t for k in ['event', 'kafka', 'pub/sub', 'stream']): return 'event-driven'
    if any(k in t for k in ['pipeline', 'ci/cd', 'build', 'deploy']): return 'pipeline-centric'
    if any(k in t for k in ['agent', 'mcp', 'llm', 'copilot']): return 'agentic-platform'
    if any(k in t for k in ['lakehouse', 'data platform', 'ingestion']): return 'layered-data-platform'
    return 'layered-architecture'


def extract_actors(text: str) -> List[str]:
    candidates = ['Architects','Developers','Pipelines','Agents','Operators','Auditors','End users','Cloud platforms','External services','Compliance teams','LOB architects','Enterprise architects']
    t=text.lower(); out=[]
    for c in candidates:
        if any(tok in t for tok in c.lower().split()):
            out.append(c)
    return out or ['Users','Operators','External systems']


def find_components(text: str) -> List[Dict[str, Any]]:
    keywords = {
        'Spec Repository':'datastore', 'Repository':'datastore', 'REST API':'api', 'GraphQL':'api', 'MCP Server':'agent_interface',
        'CLI':'cli', 'Dashboard':'ui', 'Evidence Ledger':'evidence_store', 'Drift Detector':'controller', 'Waiver Governance':'workflow',
        'Pipeline':'pipeline_stage', 'CI/CD':'pipeline', 'Policy Engine':'controller', 'OPA':'policy_engine', 'Kafka':'event_bus', 'EventBridge':'event_bus',
        'API Gateway':'gateway', 'Kubernetes':'runtime', 'EKS':'runtime', 'AKS':'runtime', 'GCP':'cloud_runtime', 'Data Lake':'datastore',
        'Catalog':'metadata', 'Secrets Manager':'security', 'IAM':'security', 'Observability':'monitoring', 'Metrics':'monitoring', 'Logs':'monitoring', 'Traces':'monitoring'
    }
    found=[]; t=text.lower()
    for name, typ in keywords.items():
        if name.lower() in t:
            found.append({'name': name, 'type': typ, 'role': f'{name} capability identified or implied in source content', 'interfaces': [], 'artifacts': []})
    return found


def infer_layers(text: str, comps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    style=infer_style(text)
    if style == 'control-plane':
        names=['Authorship Layer','Architecture Control Plane','Enforcement Layer','Runtime Platform','Evidence & Governance Layer']
    elif style == 'pipeline-centric':
        names=['Developer Experience Layer','CI/CD Enforcement Layer','Policy & Control Layer','Runtime Platform','Observability & Governance Layer']
    elif style == 'layered-data-platform':
        names=['Source Layer','Ingestion Layer','Data Platform Layer','Governance Layer','Consumption Layer']
    elif style == 'agentic-platform':
        names=['Experience Layer','Agent Orchestration Layer','Knowledge & Tool Layer','Model Execution Layer','Governance & Evaluation Layer']
    else:
        names=['Experience Layer','API / Integration Layer','Core Platform Layer','Data Layer','Governance & Operations Layer']
    layers=[]
    for n in names:
        layers.append({'layer_name': n, 'purpose': f'{n} responsibilities', 'components': [], 'inbound_from': [], 'outbound_to': []})
    for c in comps:
        lname = 'Core Platform Layer'
        typ = c.get('type','')
        if typ in ['api','gateway','event_bus','agent_interface','cli']: lname='API / Integration Layer'
        if typ in ['datastore','evidence_store','metadata']: lname='Data Layer'
        if typ in ['policy_engine','controller','workflow','monitoring','security']: lname='Governance & Operations Layer'
        if typ in ['pipeline','pipeline_stage']: lname='CI/CD Enforcement Layer'
        if typ in ['runtime','cloud_runtime']: lname='Runtime Platform'
        target = next((l for l in layers if l['layer_name'] == lname), layers[2])
        target['components'].append(c['name'])
    return layers


def extract_interfaces(comps: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
    interfaces=[]
    mapping=[('REST API','REST','request/response'),('GraphQL','GraphQL','query/read model'),('MCP Server','MCP','tool invocation'),('CLI','CLI','pipeline command'),('Kafka','event','publish/subscribe'),('Webhook','webhook','callback')]
    names=[c['name'] for c in comps]
    for name, proto, purpose in mapping:
        if any(name.lower() in n.lower() for n in names) or name.lower() in text.lower():
            interfaces.append({'interface': name, 'protocol': proto, 'source':'consumer / caller', 'target': name, 'purpose': purpose, 'timing': 'sync' if proto in ['REST','GraphQL','CLI','MCP'] else 'async'})
    return interfaces


def flows(comps: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
    names=[c['name'] for c in comps]
    flow_defs=[]
    if 'Spec Repository' in names or 'Repository' in names:
        flow_defs.append({'name':'Authoring and resolution flow','trigger':'architecture change or pipeline run','ordered_path':['Architect publishes specification','Repository versions the specification','Pipeline or agent resolves applicable controls','Control plane returns resolved policy set'],'decisions':['spec applicable?','policy pass/fail?'],'outputs':['resolved controls','version hash','evidence record']})
    if any('Pipeline' in n or 'CI/CD' in n for n in names):
        flow_defs.append({'name':'Build and deploy enforcement flow','trigger':'CI/CD execution','ordered_path':['Pipeline calls CLI or API','Policy engine evaluates artifacts','Decision blocks, warns, or requires waiver','Evidence is written to ledger'],'decisions':['block/warn/waiver-required'],'outputs':['deployment decision','audit evidence']})
    if any('Drift' in n for n in names):
        flow_defs.append({'name':'Drift and feedback loop','trigger':'scheduled or event-driven drift signal','ordered_path':['Detector observes expiry or vulnerability signal','Alert is sent to architecture owner','Spec update is proposed','Updated controls are republished'],'decisions':['drift accepted or remediated?'],'outputs':['alert','spec evolution']})
    if not flow_defs:
        flow_defs.append({'name':'Primary solution flow','trigger':'user or system request','ordered_path':['Actor initiates request','Integration layer routes request','Core platform processes request','Data or evidence is stored','Consumer receives outcome'],'decisions':['valid request?'],'outputs':['business outcome']})
    return flow_defs


def sequence_models(flow_defs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out=[]
    for f in flow_defs:
        steps=[]
        for i, step in enumerate(f.get('ordered_path', []), 1):
            steps.append(f'{i}. {step}')
        out.append({'flow': f['name'], 'steps': steps})
    return out


def normalized_payload(text: str, title: str, style: str, layers: List[Dict[str, Any]], comps: List[Dict[str, Any]], interfaces: List[Dict[str, Any]], flow_defs: List[Dict[str, Any]], actors: List[str]) -> Dict[str, Any]:
    zones=[]
    for i,l in enumerate(layers,1):
        items=l.get('components') or [l['purpose']]
        zones.append({'id': f'layer_{i}', 'title': l['layer_name'], 'subtitle': l['purpose'], 'items': items[:8], 'expand': len(items)>5})
    flow_edges=[]
    for i in range(len(zones)-1):
        flow_edges.append({'from': zones[i]['id'], 'to': zones[i+1]['id'], 'label':'interaction', 'pattern':'sync_api', 'direction':'source_to_target'})
    return {
        'system_name': title,
        'architecture_style': style,
        'primary_diagram_type': 'layered-control-plane' if style == 'control-plane' else 'layered-architecture',
        'title': title,
        'subtitle': 'Extracted architecture model from prose source',
        'template': 'platform_value_chain' if style not in ['event-driven','pipeline-centric'] else 'service_orchestration_workflow',
        'layers': layers,
        'components': comps,
        'interfaces': interfaces,
        'flows': flow_edges,
        'interaction_flows': flow_defs,
        'feedback_loops': [f for f in flow_defs if 'loop' in f['name'].lower() or 'feedback' in f['name'].lower()],
        'external_actors': actors,
        'zones': zones,
        'lanes': [{'side':'left','title':'Actors','items':actors[:8]}, {'side':'right','title':'Interfaces','items':[i['interface'] for i in interfaces][:8]}],
        'operations': ['Security','Compliance','Observability','Governance'],
        'assumptions': ['Sequencing is inferred from prose when not explicitly specified.'],
        'ambiguities': ['Validate exact ownership and deployment topology if not stated in the source.']
    }


def transform(text: str) -> Dict[str, Any]:
    title = title_from_text(text)
    style = infer_style(text)
    actors = extract_actors(text)
    comps = find_components(text)
    layers = infer_layers(text, comps)
    interfaces = extract_interfaces(comps, text)
    flow_defs = flows(comps, text)
    payload = normalized_payload(text, title, style, layers, comps, interfaces, flow_defs, actors)
    return {
        'executive_abstraction': f'{title} is represented as a {style} architecture that separates actors, interfaces, core platform responsibilities, runtime services, and governance feedback loops.',
        'architecture_layers': layers,
        'key_components': comps,
        'interfaces': interfaces,
        'interaction_flows': flow_defs,
        'sequence_models': sequence_models(flow_defs),
        'diagram_payload': payload,
        'ambiguities_and_assumptions': payload['ambiguities'] + payload['assumptions']
    }


def main() -> None:
    ap=argparse.ArgumentParser(description='Transform an architecture blog/article/whitepaper into diagram-ready architecture payload')
    ap.add_argument('--input-text', default='')
    ap.add_argument('--input-file', default='')
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    text=args.input_text or (Path(args.input_file).read_text(encoding='utf-8') if args.input_file else '')
    result=transform(text)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f'Wrote extracted architecture model to {args.output}')


if __name__ == '__main__':
    main()
