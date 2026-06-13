#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def table(rows, headers):
    out=['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |']
    for row in rows:
        out.append('| ' + ' | '.join(str(x).replace('|','/') for x in row) + ' |')
    return '\n'.join(out)


def main() -> None:
    ap=argparse.ArgumentParser(description='Generate companion architecture artifacts from enriched model.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--view-plan', required=False, default='')
    ap.add_argument('--output-dir', required=True)
    args=ap.parse_args()
    spec=load_json(Path(args.input))
    view_plan=load_json(Path(args.view_plan)) if args.view_plan and Path(args.view_plan).exists() else {}
    out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    am=spec.get('architecture_model', {})

    caps=am.get('business_capabilities', [])
    decisions=am.get('architectural_decisions', [])
    concerns=am.get('cross_cutting_concerns', {})
    inv=am.get('component_inventory', [])

    # executive summary
    cap_names=', '.join(c.get('name','') for c in caps[:5]) or 'core capabilities'
    summary=f"""# Executive Summary

## Architecture outcome
{am.get('communication_goal') or spec.get('business_outcome_description','The architecture connects capabilities and services to deliver the target business outcome.')}

## How the architecture delivers value
The solution organizes {cap_names} into a governed architecture where business capabilities map to technical services, integrations, data flows, and cross-cutting controls. This gives CIO stakeholders a clear path from strategy to execution: capabilities are owned, services are categorized, integrations are explicit, and decisions are traceable.

## Key value delivered
- Clear business-to-technology traceability
- More complete architecture coverage through enrichment of platform, security, observability, CI/CD, and resilience concerns
- Reusable multi-view outputs for executive, logical, technical, and integration discussions
- Stronger governance through assumptions, constraints, and ADR-style decisions

## Recommended views
"""
    for v in view_plan.get('recommended_views', []):
        summary += f"- **{v.get('name')}** — {v.get('layout_strategy')}\n"
    write(out/'executive_summary.md', summary.strip()+'\n')

    # decisions
    adr="# Architecture Decisions\n\n"
    for idx,d in enumerate(decisions, start=1):
        adr += f"## ADR-{idx:03d}: {d}\n\n- **Status:** Proposed\n- **Context:** Derived from the user request and architecture enrichment rules.\n- **Decision:** {d}\n- **Consequence:** Improves completeness, governance, and operational readiness of the generated architecture.\n\n"
    adr += "## Assumptions\n" + ''.join(f"- {x}\n" for x in am.get('assumptions', [])) + "\n## Constraints\n" + ''.join(f"- {x}\n" for x in am.get('constraints', []))
    write(out/'architecture_decisions.md', adr.strip()+'\n')

    # capability map
    rows=[]
    for c in caps:
        rows.append([c.get('name',''), c.get('owner',''), ', '.join(c.get('outcomes', [])), ', '.join(c.get('value_streams', []))])
    cap_md="# Capability Map\n\n" + table(rows, ['Capability','Owner','Outcomes','Value streams']) + "\n\n## Business-to-technical mapping\n"
    for m in am.get('business_to_technical_mapping', []):
        cap_md += f"\n### {m.get('business_capability')}\n"
        cap_md += ''.join(f"- {x.get('technical_service')} ({x.get('category')})\n" for x in m.get('realized_by', []))
    write(out/'capability_map.md', cap_md.strip()+'\n')

    # component inventory JSON
    (out/'component_inventory.json').write_text(json.dumps({'components': inv, 'cross_cutting_concerns': concerns}, indent=2), encoding='utf-8')
    print(f'Wrote companion artifacts to {out}')

if __name__ == '__main__':
    main()
