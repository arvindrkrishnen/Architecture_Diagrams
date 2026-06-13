#!/usr/bin/env python3
import argparse
import concurrent.futures
import copy
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / 'outputs'
OUTPUTS.mkdir(exist_ok=True)


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def slugify(value: str) -> str:
    value = re.sub(r'[^A-Za-z0-9]+', '_', value).strip('_').lower()
    return value or 'architecture_run'


def clean_text(value: str) -> str:
    return re.sub(r'\s+', ' ', (value or '')).strip()


def checkpoint(memory: Dict[str, Any], run_dir: Path, stage: str) -> Path:
    memory.setdefault('checkpoints', []).append({
        'stage': stage,
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    })
    path = run_dir / 'run_context.json'
    save_json(path, memory)
    return path


def probe_parallel_execution() -> Tuple[bool, str]:
    try:
        def work(x: int) -> int:
            return x + 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            futs = [ex.submit(work, i) for i in (1, 2)]
            results = [f.result(timeout=2) for f in futs]
        if results == [2, 3]:
            return True, 'parallel execution probe passed'
        return False, 'parallel execution probe returned unexpected results'
    except Exception as e:
        return False, f'parallel execution probe failed: {e}'


def choose_template(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ['bronze', 'silver', 'gold', 'databricks', 'self-service analytics', 'lakehouse']):
        return 'modern_data_lakehouse'
    if any(k in t for k in ['landing zone', 'entra', 'multi-cloud landing', 'identity control plane']):
        return 'identity_multicloud_control_plane'
    if any(k in t for k in ['iot', 'ot', 'industrial', 'threat', 'risk matrix']):
        return 'iot_ot_security_layers'
    if any(k in t for k in ['service catalog', 'order orchestration', 'billing', 'provisioning', 'workflow']):
        return 'service_orchestration_workflow'
    if any(k in t for k in ['saas', 'paas', 'iaas', 'broker model', 'cloud carrier']):
        return 'cloud_service_operating_model'
    if any(k in t for k in ['data platform', 'ingestion', 'governance', 'analytics', 'warehouse']):
        return 'cloud_data_platform'
    if any(k in t for k in ['endpoint', 'device', 'intune', 'identity', 'conditional access', 'compliance']):
        return 'enterprise_endpoint_management'
    if any(k in t for k in ['microservice', 'tenant', 'kubernetes', 'eks', 'aks', 'gcp', 'api gateway', 'saas']):
        return 'cloud_tenant_microservices'
    if any(k in t for k in ['agent', 'genai', 'llm', 'copilot', 'ai platform', 'agentic']):
        return 'composite_ai_platform'
    return 'platform_value_chain'


def infer_title(text: str) -> str:
    first = clean_text(text.splitlines()[0] if text.strip() else 'Solution Architecture')
    patterns = [
        r'build a solution architecture diagram for (?:an?|the)?\s*(.+)',
        r'create a solution architecture diagram for (?:an?|the)?\s*(.+)',
        r'architecture diagram for (?:an?|the)?\s*(.+)',
        r'for (?:an?|the)?\s*(.+)'
    ]
    low = first.lower()
    for p in patterns:
        m = re.search(p, low)
        if m:
            candidate = first[m.start(1):].strip(' .:-')
            return candidate[:120].title()
    if len(first) <= 120:
        return first.rstrip('. ')
    return 'Solution Architecture'


def split_items(blob: str) -> List[str]:
    parts = re.split(r'[;,]|\n|\u2022|- ', blob)
    items = []
    for p in parts:
        p = clean_text(p)
        if p:
            items.append(p[:60])
    deduped = []
    seen = set()
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def parse_structured_sections(text: str) -> Dict[str, Any]:
    lines = [line.rstrip() for line in text.splitlines()]
    sections: Dict[str, List[str]] = {}
    current = 'description'
    sections[current] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m = re.match(r'^(title|subtitle|template|inputs|outputs|capabilities|zones|operations|flows|footer)\s*:\s*(.*)$', line, re.I)
        if m:
            current = m.group(1).lower()
            sections.setdefault(current, [])
            if m.group(2).strip():
                sections[current].append(m.group(2).strip())
        else:
            sections.setdefault(current, []).append(line)
    return sections


def draft_spec_from_text(text: str) -> Dict[str, Any]:
    sections = parse_structured_sections(text)
    title = clean_text(' '.join(sections.get('title', []))) or infer_title(text)
    subtitle = clean_text(' '.join(sections.get('subtitle', [])))
    template = clean_text(' '.join(sections.get('template', []))) or choose_template(text)

    inputs = split_items(' '.join(sections.get('inputs', [])))
    outputs = split_items(' '.join(sections.get('outputs', [])))
    operations = split_items(' '.join(sections.get('operations', [])))
    footer = clean_text(' '.join(sections.get('footer', [])))

    zone_lines = sections.get('zones', []) + sections.get('capabilities', [])
    zones = []
    for idx, line in enumerate(zone_lines, start=1):
        if '|' in line:
            parts = [clean_text(x) for x in line.split('|')]
            ztitle = parts[0] or f'Capability {idx}'
            zsubtitle = parts[1] if len(parts) > 1 else ''
            zitems = split_items(parts[2] if len(parts) > 2 else '')
        elif ':' in line:
            left, right = line.split(':', 1)
            ztitle = clean_text(left)
            zsubtitle = ''
            zitems = split_items(right)
        else:
            ztitle = f'Capability {idx}'
            zsubtitle = ''
            zitems = split_items(line)
        if not zitems:
            zitems = [ztitle]
        zones.append({
            'id': f'zone_{idx}',
            'title': ztitle[:80],
            'subtitle': zsubtitle[:120],
            'items': zitems[:8],
            'expand': len(zitems) > 4,
            'children': []
        })

    if not zones:
        # heuristic fallback from sentences
        clauses = [clean_text(x) for x in re.split(r'[\.;]', text) if clean_text(x)]
        grouped = []
        for c in clauses:
            if len(grouped) < 5:
                grouped.append(c)
        if not grouped:
            grouped = ['Core capabilities']
        for idx, clause in enumerate(grouped[:5], start=1):
            words = clause.split()
            ztitle = ' '.join(words[:4]).title() if words else f'Capability {idx}'
            zones.append({
                'id': f'zone_{idx}',
                'title': ztitle[:80],
                'subtitle': '',
                'items': [clause[:60]],
                'expand': False,
                'children': []
            })

    flows = []
    for i in range(len(zones) - 1):
        flows.append({'from': zones[i]['id'], 'to': zones[i+1]['id'], 'label': 'flow'})

    spec = {
        'title': title or 'Solution Architecture',
        'subtitle': subtitle,
        'template': template if template in {
            'platform_value_chain', 'composite_ai_platform', 'cloud_tenant_microservices',
            'enterprise_endpoint_management', 'cloud_data_platform', 'cloud_service_operating_model',
            'service_orchestration_workflow', 'iot_ot_security_layers', 'modern_data_lakehouse',
            'identity_multicloud_control_plane'
        } else choose_template(text),
        'lanes': [],
        'zones': zones,
        'flows': flows,
        'operations': operations,
        'footer': footer,
        'decomposition': {
            'auto_expand': True,
            'max_overview_zones': 6,
            'max_items_per_zone_overview': 5,
            'create_capability_children': True
        },
        'rendering_preferences': {'backend': 'drawio-skill', 'format': 'png', 'embed_xml': True}
    }
    if inputs:
        spec['lanes'].append({'side': 'left', 'title': 'Inputs', 'items': inputs[:12]})
    if outputs:
        spec['lanes'].append({'side': 'right', 'title': 'Outputs', 'items': outputs[:12]})
    return spec


def run_cmd(cmd: List[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


class AgentResult:
    def __init__(self, name: str, payload: Dict[str, Any]):
        self.name = name
        self.payload = payload


def intake_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    spec_source = memory['inputs']['source_type']
    if spec_source == 'json':
        spec = load_json(Path(memory['inputs']['json_input']))
        payload = {'draft_spec': spec, 'input_mode': 'json'}
    else:
        text = memory['inputs']['text']
        save_text(run_dir / 'raw_request.txt', text)
        payload = {'draft_spec': draft_spec_from_text(text), 'input_mode': 'text'}
    return AgentResult('intake_agent', payload)


def normalization_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    draft_path = run_dir / 'draft_input.json'
    prepared_path = run_dir / 'prepared_input.json'
    save_json(draft_path, memory['working']['draft_spec'])
    run_cmd([
        sys.executable, 'prepare_architecture_input.py',
        '--input', str(draft_path),
        '--output', str(prepared_path)
    ], ROOT)
    payload = {
        'prepared_input_path': str(prepared_path),
        'prepared_input': load_json(prepared_path)
    }
    return AgentResult('normalization_agent', payload)




def recommendation_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    prepared_path = Path(memory['working']['prepared_input_path'])
    rec_path = run_dir / 'layout_recommendations.json'
    run_cmd([
        sys.executable, 'recommend_layouts.py',
        '--input', str(prepared_path),
        '--patterns', str(ROOT / 'data' / 'reference_architecture_patterns.json'),
        '--assets', str(ROOT / 'data' / 'reference_asset_library.json'),
        '--output', str(rec_path),
        '--topn', '2'
    ], ROOT)
    rec = load_json(rec_path)
    # Apply default selected recommendation to the prepared input for downstream prompt generation.
    default = rec.get('default_selected_recommendation') or {}
    if default.get('primary_layout_template'):
        spec = load_json(prepared_path)
        spec['template'] = default['primary_layout_template']
        spec['style_selection'] = default
        save_json(prepared_path, spec)
    return AgentResult('recommendation_agent', {
        'layout_recommendations_path': str(rec_path),
        'layout_recommendations': rec,
        'selected_recommendation': rec.get('default_selected_recommendation')
    })


def technology_placement_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    prepared_path = Path(memory['working']['prepared_input_path'])
    report_path = run_dir / 'technology_placement_report.json'
    run_cmd([
        sys.executable, 'validate_technology_placement.py',
        '--input', str(prepared_path),
        '--output', str(report_path)
    ], ROOT)
    return AgentResult('technology_placement_agent', {
        'technology_placement_report_path': str(report_path),
        'technology_placement_report': load_json(report_path)
    })

def layout_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    spec = memory['working']['prepared_input']
    payload = {
        'selected_template': spec.get('template'),
        'layout_summary': {
            'zone_count': len(spec.get('zones', [])),
            'lane_count': len(spec.get('lanes', [])),
            'operations_count': len(spec.get('operations', []))
        }
    }
    return AgentResult('layout_agent', payload)


def decomposition_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    prepared_path = Path(memory['working']['prepared_input_path'])
    multilevel_path = run_dir / 'multilevel_plan.json'
    run_cmd([
        sys.executable, 'plan_multilevel_architecture.py',
        '--input', str(prepared_path),
        '--output', str(multilevel_path)
    ], ROOT)
    payload = {
        'multilevel_plan_path': str(multilevel_path),
        'multilevel_plan': load_json(multilevel_path)
    }
    return AgentResult('decomposition_agent', payload)


def overview_prompt_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    prepared_path = Path(memory['working']['prepared_input_path'])
    prompt_path = run_dir / 'drawio_prompt_overview.md'
    run_cmd([
        sys.executable, 'build_drawio_prompt.py',
        '--input', str(prepared_path),
        '--patterns', str(ROOT / 'data' / 'reference_architecture_patterns.json'),
        '--output', str(prompt_path)
    ], ROOT)
    return AgentResult('overview_prompt_agent', {'overview_prompt_path': str(prompt_path)})


def build_expansion_spec(base_spec: Dict[str, Any], expansion: Dict[str, Any]) -> Dict[str, Any]:
    zones = []
    children = expansion.get('children') or []
    if children:
        for idx, child in enumerate(children, start=1):
            zones.append({
                'id': f'child_{idx}',
                'title': child.get('title', f'Sub-capability {idx}')[:80],
                'subtitle': child.get('subtitle', '')[:120],
                'items': child.get('items', [])[:10],
                'expand': False,
                'children': []
            })
    else:
        items = expansion.get('items', [])
        chunks = [items[i:i+4] for i in range(0, len(items), 4)] or [[expansion.get('parent_zone_title', 'Capability')]]
        for idx, chunk in enumerate(chunks, start=1):
            zones.append({
                'id': f'child_{idx}',
                'title': f'Capability Group {idx}',
                'subtitle': '',
                'items': chunk,
                'expand': False,
                'children': []
            })
    flows = []
    for i in range(len(zones)-1):
        flows.append({'from': zones[i]['id'], 'to': zones[i+1]['id'], 'label': 'detail flow'})
    return {
        'title': expansion.get('title', 'Level 2 Expansion'),
        'subtitle': expansion.get('subtitle', ''),
        'template': base_spec.get('template', 'platform_value_chain'),
        'lanes': [],
        'zones': zones,
        'flows': flows,
        'operations': base_spec.get('operations', [])[:8],
        'footer': f"Level 2 expansion of {expansion.get('parent_zone_title','capability')}",
        'decomposition': {
            'auto_expand': False,
            'max_overview_zones': 6,
            'max_items_per_zone_overview': 5,
            'create_capability_children': False
        },
        'rendering_preferences': base_spec.get('rendering_preferences', {'backend':'drawio-skill','format':'png','embed_xml':True})
    }


def expansion_prompt_agent(memory: Dict[str, Any], run_dir: Path, expansion: Dict[str, Any], index: int) -> AgentResult:
    base_spec = memory['working']['prepared_input']
    specs_dir = run_dir / 'expansion_specs'
    prompts_dir = run_dir / 'drawio_prompts'
    specs_dir.mkdir(exist_ok=True)
    prompts_dir.mkdir(exist_ok=True)

    spec = build_expansion_spec(base_spec, expansion)
    spec_path = specs_dir / f"{index:02d}_{slugify(expansion.get('parent_zone_title', 'capability'))}.json"
    prompt_path = prompts_dir / f"{index:02d}_{slugify(expansion.get('parent_zone_title', 'capability'))}.md"
    save_json(spec_path, spec)
    run_cmd([
        sys.executable, 'build_drawio_prompt.py',
        '--input', str(spec_path),
        '--patterns', str(ROOT / 'data' / 'reference_architecture_patterns.json'),
        '--output', str(prompt_path)
    ], ROOT)
    return AgentResult('expansion_prompt_agent', {
        'index': index,
        'parent_zone_title': expansion.get('parent_zone_title'),
        'expansion_spec_path': str(spec_path),
        'expansion_prompt_path': str(prompt_path)
    })


def merge_agent_results(memory: Dict[str, Any], result: AgentResult) -> None:
    memory.setdefault('agent_results', {})[result.name] = result.payload
    memory.setdefault('working', {}).update(result.payload)


def run_sequential_post_normalization(memory: Dict[str, Any], run_dir: Path) -> None:
    for agent in [layout_agent, decomposition_agent, overview_prompt_agent]:
        result = agent(memory, run_dir)
        merge_agent_results(memory, result)
        checkpoint(memory, run_dir, result.name)


def run_parallel_post_normalization(memory: Dict[str, Any], run_dir: Path) -> None:
    agents = [layout_agent, decomposition_agent, overview_prompt_agent]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        future_map = {ex.submit(agent, copy.deepcopy(memory), run_dir): agent.__name__ for agent in agents}
        for future in concurrent.futures.as_completed(future_map):
            result = future.result()
            merge_agent_results(memory, result)
            checkpoint(memory, run_dir, result.name)


def run_expansion_agents(memory: Dict[str, Any], run_dir: Path, parallel_enabled: bool) -> None:
    expansions = memory.get('working', {}).get('multilevel_plan', {}).get('expansions', [])
    memory['working']['expansion_outputs'] = []
    if not expansions:
        return
    if parallel_enabled:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(expansions))) as ex:
                futures = [
                    ex.submit(expansion_prompt_agent, copy.deepcopy(memory), run_dir, exp, idx)
                    for idx, exp in enumerate(expansions, start=1)
                ]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    memory['working']['expansion_outputs'].append(result.payload)
                    checkpoint(memory, run_dir, f"expansion_prompt_agent_{result.payload['index']:02d}")
        except Exception:
            # fallback to sequential
            parallel_enabled = False
    if not parallel_enabled:
        for idx, exp in enumerate(expansions, start=1):
            result = expansion_prompt_agent(memory, run_dir, exp, idx)
            memory['working']['expansion_outputs'].append(result.payload)
            checkpoint(memory, run_dir, f"expansion_prompt_agent_{idx:02d}")
    memory['working']['expansion_outputs'] = sorted(memory['working']['expansion_outputs'], key=lambda x: x['index'])




def render_adapter_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    cmd = [sys.executable, 'render_with_drawio_adapter.py', '--run-dir', str(run_dir)]
    if memory['execution'].get('mode') == 'parallel':
        cmd.append('--allow-parallel')
    else:
        cmd.append('--force-sequential')
    if memory['rendering'].get('renderer_config'):
        cmd.extend(['--config', memory['rendering']['renderer_config']])
    if memory['rendering'].get('renderer_command_template'):
        cmd.extend(['--command-template', memory['rendering']['renderer_command_template']])
    if memory['rendering'].get('renderer_dry_run'):
        cmd.append('--dry-run')
    run_cmd(cmd, ROOT)
    report_path = run_dir / 'render_report.json'
    payload = {'render_report_path': str(report_path)}
    if report_path.exists():
        payload['render_report'] = load_json(report_path)
    return AgentResult('render_adapter_agent', payload)

def packaging_agent(memory: Dict[str, Any], run_dir: Path) -> AgentResult:
    summary = {
        'run_id': memory['run_id'],
        'execution_mode': memory['execution']['mode'],
        'parallel_probe': memory['execution']['parallel_probe'],
        'input_mode': memory['inputs']['source_type'],
        'prepared_input_path': memory['working'].get('prepared_input_path'),
        'overview_prompt_path': memory['working'].get('overview_prompt_path'),
        'multilevel_plan_path': memory['working'].get('multilevel_plan_path'),
        'layout_recommendations_path': memory['working'].get('layout_recommendations_path'),
        'technology_placement_report_path': memory['working'].get('technology_placement_report_path'),
        'expansion_prompts': memory['working'].get('expansion_outputs', []),
        'expected_render_outputs': {
            'overview_png': 'outputs/solution_architecture_overview.png',
            'overview_drawio': 'outputs/solution_architecture_overview.drawio',
            'expansion_png_pattern': 'outputs/solution_architecture_capability_*.png',
            'expansion_drawio_pattern': 'outputs/solution_architecture_capability_*.drawio'
        },
        'next_step': 'Feed the generated overview and expansion prompt markdown files into drawio-skill to render PNG and .drawio outputs.'
    }
    report_path = run_dir / 'orchestration_report.json'
    save_json(report_path, summary)
    return AgentResult('packaging_agent', {'orchestration_report_path': str(report_path), 'orchestration_report': summary})


def main() -> None:
    parser = argparse.ArgumentParser(description='Single orchestration runner for the Solution Architecture Diagram Skill')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--text', help='Raw text request describing the architecture to build')
    src.add_argument('--text-file', help='Path to a text file containing the request')
    src.add_argument('--json-input', help='Path to a structured JSON input file')
    parser.add_argument('--run-name', default='', help='Optional run name')
    parser.add_argument('--output-dir', default='', help='Optional output directory for this run')
    parser.add_argument('--allow-parallel', action='store_true', help='Allow sub-agents to run in parallel when the execution engine supports it')
    parser.add_argument('--force-sequential', action='store_true', help='Force sequential orchestration even if parallel execution is available')
    parser.add_argument('--render', action='store_true', help='Invoke the renderer adapter after orchestration')
    parser.add_argument('--renderer-config', default='', help='Optional renderer config JSON file for render_with_drawio_adapter.py')
    parser.add_argument('--renderer-command-template', default='', help='Optional renderer command template')
    parser.add_argument('--renderer-dry-run', action='store_true', help='Dry run the renderer adapter without executing the render command')
    args = parser.parse_args()

    if args.force_sequential and args.allow_parallel:
        parser.error('Use either --allow-parallel or --force-sequential, not both.')

    if args.json_input:
        input_name = Path(args.json_input).stem
        raw_text = ''
        source_type = 'json'
    else:
        raw_text = Path(args.text_file).read_text(encoding='utf-8') if args.text_file else args.text
        input_name = slugify(infer_title(raw_text))
        source_type = 'text'

    run_name = args.run_name or f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{input_name}"
    run_dir = Path(args.output_dir) if args.output_dir else OUTPUTS / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    parallel_ok, probe_msg = probe_parallel_execution()
    if args.force_sequential:
        execution_mode = 'sequential'
        parallel_enabled = False
    elif args.allow_parallel and parallel_ok:
        execution_mode = 'parallel'
        parallel_enabled = True
    else:
        execution_mode = 'sequential'
        parallel_enabled = False

    memory: Dict[str, Any] = {
        'run_id': run_name,
        'author': 'Arvind Radhakrishnen',
        'inputs': {
            'source_type': source_type,
            'text': raw_text,
            'json_input': args.json_input or ''
        },
        'execution': {
            'mode': execution_mode,
            'parallel_probe': {'supported': parallel_ok, 'message': probe_msg},
            'parallel_requested': bool(args.allow_parallel),
            'forced_sequential': bool(args.force_sequential)
        },
        'working': {},
        'rendering': {
            'enabled': bool(args.render),
            'renderer_config': args.renderer_config,
            'renderer_command_template': args.renderer_command_template,
            'renderer_dry_run': bool(args.renderer_dry_run)
        }
    }
    checkpoint(memory, run_dir, 'start')

    # intake
    result = intake_agent(memory, run_dir)
    merge_agent_results(memory, result)
    checkpoint(memory, run_dir, result.name)

    # normalization
    result = normalization_agent(memory, run_dir)
    merge_agent_results(memory, result)
    checkpoint(memory, run_dir, result.name)

    # recommendation and placement guardrails must run before prompt generation
    for pre_agent in [recommendation_agent, technology_placement_agent]:
        result = pre_agent(memory, run_dir)
        merge_agent_results(memory, result)
        checkpoint(memory, run_dir, result.name)

    # parallelizable middle stage with checkpoint-based fallback strategy
    if parallel_enabled:
        try:
            run_parallel_post_normalization(memory, run_dir)
        except Exception as e:
            memory['execution']['mode'] = 'sequential'
            memory['execution']['parallel_fallback_reason'] = f'parallel stage failed: {e}'
            checkpoint(memory, run_dir, 'parallel_fallback_to_sequential')
            run_sequential_post_normalization(memory, run_dir)
    else:
        run_sequential_post_normalization(memory, run_dir)

    # expansion agents: parallel if supported, else sequential
    run_expansion_agents(memory, run_dir, parallel_enabled=memory['execution']['mode'] == 'parallel')

    if memory['rendering'].get('enabled'):
        result = render_adapter_agent(memory, run_dir)
        merge_agent_results(memory, result)
        checkpoint(memory, run_dir, result.name)

    result = packaging_agent(memory, run_dir)
    merge_agent_results(memory, result)
    checkpoint(memory, run_dir, result.name)

    print(f'Run directory: {run_dir}')
    print(f"Prepared input: {memory['working'].get('prepared_input_path')}")
    print(f"Overview prompt: {memory['working'].get('overview_prompt_path')}")
    print(f"Multilevel plan: {memory['working'].get('multilevel_plan_path')}")
    print(f"Layout recommendations: {memory['working'].get('layout_recommendations_path')}")
    print(f"Technology placement report: {memory['working'].get('technology_placement_report_path')}")
    print(f"Expansion prompt count: {len(memory['working'].get('expansion_outputs', []))}")
    print(f"Report: {memory['working'].get('orchestration_report_path')}")
    if memory['working'].get('render_report_path'):
        print(f"Render report: {memory['working'].get('render_report_path')}")


if __name__ == '__main__':
    main()
