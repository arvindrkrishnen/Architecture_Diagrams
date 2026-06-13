#!/usr/bin/env python3
import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_style(style):
    out = {}
    for part in (style or '').split(';'):
        if '=' in part:
            k, v = part.split('=', 1)
            out[k] = v
        elif part:
            out[part] = True
    return out

def main():
    ap = argparse.ArgumentParser(description='Validate rendered Draw.io file for readability, text wrapping, padding, and orthogonal connectors. No eval file is generated.')
    ap.add_argument('--drawio', required=True)
    ap.add_argument('--png', default='')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    path = Path(args.drawio)
    if not path.exists():
        if not args.quiet:
            print(f'Skipping rendered guardrail validation; missing drawio file: {path}')
        return

    issues = []
    try:
        root = ET.parse(path).getroot()
    except Exception as e:
        if not args.quiet:
            print(f'Could not parse Draw.io XML: {e}')
        if args.strict:
            sys.exit(1)
        return

    for cell in root.iter('mxCell'):
        style = parse_style(cell.attrib.get('style', ''))
        value = cell.attrib.get('value', '') or ''
        is_edge = cell.attrib.get('edge') == '1'
        is_vertex = cell.attrib.get('vertex') == '1'
        if is_vertex and value.strip():
            fs = style.get('fontSize')
            try:
                fs_val = int(float(fs)) if fs else None
            except Exception:
                fs_val = None
            if fs_val is not None and fs_val < 14:
                issues.append(f'Font below 14 pt for label: {value[:60]}')
            if style.get('whiteSpace') != 'wrap':
                issues.append(f'Missing whiteSpace=wrap for label: {value[:60]}')
            spacing_vals = [style.get(k) for k in ['spacing', 'spacingLeft', 'spacingRight', 'spacingTop', 'spacingBottom']]
            if not any(v is not None for v in spacing_vals):
                issues.append(f'Missing internal spacing/padding for label: {value[:60]}')
        if is_edge:
            st = cell.attrib.get('style','')
            if 'orthogonalEdgeStyle' not in st and 'edgeStyle=orthogonal' not in st and 'elbowEdgeStyle' not in st:
                issues.append('Connector may not be orthogonal / elbow routed.')

    if not args.quiet:
        if issues:
            print('Rendered guardrail warnings:')
            for i in issues[:50]:
                print('-', i)
        else:
            print('Rendered guardrails passed.')
    if args.strict and issues:
        sys.exit(1)

if __name__ == '__main__':
    main()
