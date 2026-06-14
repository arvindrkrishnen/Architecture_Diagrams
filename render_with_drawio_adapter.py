#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
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


def load_config(path: str) -> Dict[str, Any]:
    if not path:
        return {}
    return load_json(Path(path))


def build_jobs(run_dir: Path) -> List[Dict[str, Any]]:
    jobs: List[Dict[str, Any]] = []
    variant_dir = run_dir / 'variant_prompts'
    if variant_dir.exists():
        for prompt in sorted(variant_dir.glob('variant_*.md')):
            stem = prompt.stem
            suffix = stem.split('_', 1)[1] if '_' in stem else stem
            jobs.append({
                'name': stem,
                'prompt': str(prompt),
                'png': str(run_dir / f'solution_architecture_variant_{suffix}.png'),
                'drawio': str(run_dir / f'solution_architecture_variant_{suffix}.drawio')
            })
        if jobs:
            return jobs

    overview_prompt = run_dir / 'drawio_prompt_overview.md'
    if overview_prompt.exists():
        jobs.append({
            'name': 'overview',
            'prompt': str(overview_prompt),
            'png': str(run_dir / 'solution_architecture_overview.png'),
            'drawio': str(run_dir / 'solution_architecture_overview.drawio')
        })

    prompts_dir = run_dir / 'drawio_prompts'
    if prompts_dir.exists():
        for prompt in sorted(prompts_dir.glob('*.md')):
            stem = prompt.stem
            prefix = stem.split('_', 1)[0]
            jobs.append({
                'name': stem,
                'prompt': str(prompt),
                'png': str(run_dir / f'solution_architecture_capability_{prefix}.png'),
                'drawio': str(run_dir / f'solution_architecture_capability_{prefix}.drawio')
            })
    return jobs


def render_one(job: Dict[str, Any], command_template: str, dry_run: bool) -> Dict[str, Any]:
    cmd = command_template.format(
        prompt=job['prompt'],
        png=job['png'],
        drawio=job['drawio'],
        name=job['name'],
        run_dir=str(Path(job['png']).parent)
    )
    result = {
        'job': job,
        'command': cmd,
        'status': 'dry_run' if dry_run else 'pending'
    }
    if dry_run:
        return result
    try:
        subprocess.run(cmd, shell=True, check=True, executable='/bin/bash')
        # Revalidate rendered artifact guardrails without writing eval files.
        drawio_path = Path(job['drawio'])
        if drawio_path.exists():
            subprocess.run([
                'python', str(ROOT / 'validate_rendered_guardrails.py'),
                '--drawio', str(drawio_path),
                '--png', str(job['png']),
                '--quiet'
            ], check=False)
        result['status'] = 'success'
    except subprocess.CalledProcessError as e:
        result['status'] = 'failed'
        result['error'] = str(e)
    return result



def claude_native_render_one(job: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
    """Create a Claude-native rendering instruction artifact when drawio-skill CLI is unavailable.
    This does not call Claude; it emits a self-contained prompt that can be pasted into Claude
    to produce inline SVG and draw.io-compatible mxGraphModel XML.
    """
    prompt_text = Path(job['prompt']).read_text(encoding='utf-8')
    out_path = Path(job['drawio']).with_suffix('.claude_native_render.md')
    instruction = f"""# Claude-Native Architecture Rendering Instruction

Use the following Draw.io renderer prompt to produce a complete architecture diagram without the drawio-skill CLI.

## Required output
1. An inline SVG preview of the diagram.
2. A draw.io-compatible XML block wrapped in `<mxGraphModel>`.
3. The diagram must follow ADA readability, text wrapping, orthogonal connectors, padding, non-overlap, and color rules from the prompt.

## Target artifact names
- PNG target: `{job['png']}`
- Draw.io XML target: `{job['drawio']}`

## Renderer prompt

{prompt_text}
"""
    if not dry_run:
        out_path.write_text(instruction, encoding='utf-8')
    return {'job': job, 'command': 'claude-native prompt generation', 'status': 'dry_run' if dry_run else 'claude_native_instruction_written', 'claude_native_instruction': str(out_path)}

def main() -> None:
    ap = argparse.ArgumentParser(description='Renderer adapter for drawio-skill output generation')
    ap.add_argument('--run-dir', required=True, help='Run directory created by run_architecture_skill.py')
    ap.add_argument('--config', default='', help='Optional renderer config JSON file')
    ap.add_argument('--command-template', default='', help='Shell command template to invoke the renderer')
    ap.add_argument('--allow-parallel', action='store_true', help='Allow parallel render jobs when supported')
    ap.add_argument('--force-sequential', action='store_true', help='Force sequential rendering')
    ap.add_argument('--dry-run', action='store_true', help='Do not execute commands; only emit the render plan')
    ap.add_argument('--render-mode', choices=['drawio-skill','claude-native','dry-run'], default='drawio-skill', help='Renderer mode. claude-native emits inline SVG/XML instructions instead of invoking a CLI.')
    ap.add_argument('--debug-report', action='store_true', help='Write render_report.json for debugging. Disabled by default to avoid user-facing JSON outputs.')
    args = ap.parse_args()

    cfg = load_config(args.config)
    command_template = args.command_template or cfg.get('command_template', '')
    dry_run = args.dry_run or bool(cfg.get('dry_run', False))
    if not command_template and args.render_mode == 'drawio-skill':
        raise SystemExit('No command template provided. Use --command-template or --config.')

    run_dir = Path(args.run_dir)
    jobs = build_jobs(run_dir)
    if not jobs:
        raise SystemExit(f'No prompt files found in {run_dir}')

    parallel_ok, probe_msg = probe_parallel_execution()
    parallel_requested = args.allow_parallel or bool(cfg.get('allow_parallel', False))
    if args.force_sequential:
        execution_mode = 'sequential'
        parallel_enabled = False
    elif parallel_requested and parallel_ok:
        execution_mode = 'parallel'
        parallel_enabled = True
    else:
        execution_mode = 'sequential'
        parallel_enabled = False

    render_func = claude_native_render_one if args.render_mode in ('claude-native','dry-run') else render_one
    if args.render_mode == 'dry-run':
        dry_run = True
    results: List[Dict[str, Any]] = []
    if parallel_enabled:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(jobs))) as ex:
                futures = [ex.submit(render_func, job, command_template, dry_run) if args.render_mode == 'drawio-skill' else ex.submit(render_func, job, dry_run) for job in jobs]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
        except Exception as e:
            execution_mode = 'sequential'
            parallel_enabled = False
            results = []
            for job in jobs:
                results.append(render_func(job, command_template, dry_run) if args.render_mode == 'drawio-skill' else render_func(job, dry_run))
            fallback_reason = str(e)
        else:
            fallback_reason = ''
    else:
        for job in jobs:
            results.append(render_func(job, command_template, dry_run) if args.render_mode == 'drawio-skill' else render_func(job, dry_run))
        fallback_reason = ''

    results = sorted(results, key=lambda x: x['job']['name'])
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'run_dir': str(run_dir),
        'render_mode': args.render_mode,
        'execution': {
            'mode': execution_mode,
            'parallel_supported': parallel_ok,
            'parallel_requested': parallel_requested,
            'probe_message': probe_msg,
            'fallback_reason': fallback_reason
        },
        'job_count': len(results),
        'results': results
    }
    if args.debug_report:
        report_path = run_dir / 'render_report.json'
        save_json(report_path, report)
        print(f'Render report: {report_path}')
    else:
        print('Render completed. No render JSON report written.')
    for item in results:
        print(f"[{item['status']}] {item['job']['name']} -> {item['job']['png']} | {item['job']['drawio']}")


if __name__ == '__main__':
    main()
