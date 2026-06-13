#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from difflib import get_close_matches

try:
    from PIL import Image
except Exception:
    Image = None

try:
    import pytesseract
except Exception:
    pytesseract = None

STOPWORDS = {
    'the','and','for','with','from','into','layer','stage','service','services','system','systems',
    'data','platform','architecture','control','controls','of','to','in','on','or','a','an'
}


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def extract_expected_strings(spec):
    strings = []
    for key in ('title', 'subtitle', 'footer'):
        val = spec.get(key)
        if val:
            strings.append(val)
    for lane in spec.get('lanes', []):
        strings.append(lane.get('title', ''))
        strings.extend(lane.get('items', []))
    for zone in spec.get('zones', []):
        strings.append(zone.get('title', ''))
        if zone.get('subtitle'):
            strings.append(zone.get('subtitle'))
        strings.extend(zone.get('items', []))
    strings.extend(spec.get('operations', []))
    for flow in spec.get('flows', []):
        if flow.get('label'):
            strings.append(flow['label'])
    return [s for s in strings if s]


def tokenize(text):
    return [t for t in re.findall(r"[A-Za-z0-9+/.-]+", text) if len(t) > 2]


def extract_expected_keywords(strings):
    toks = []
    for s in strings:
        toks.extend(tokenize(s))
    uniq = []
    seen = set()
    for t in toks:
        key = t.lower()
        if key not in seen and key not in STOPWORDS:
            seen.add(key)
            uniq.append(t)
    return uniq


def ocr_png(path):
    if Image is None or pytesseract is None:
        return None, 'OCR dependencies not installed. Install pillow and pytesseract, plus Tesseract OCR.'
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text, None


def evaluate(spec, ocr_text):
    expected_strings = extract_expected_strings(spec)
    expected_keywords = extract_expected_keywords(expected_strings)
    ocr_tokens = tokenize(ocr_text)
    ocr_lower = {t.lower() for t in ocr_tokens}

    missing_keywords = []
    suspicious_matches = []
    for word in expected_keywords:
        if word.lower() not in ocr_lower:
            close = get_close_matches(word.lower(), list(ocr_lower), n=1, cutoff=0.72)
            if close:
                suspicious_matches.append({'expected': word, 'ocr_near_match': close[0]})
            else:
                missing_keywords.append(word)

    title_present = spec.get('title', '').lower() in ocr_text.lower() if spec.get('title') else None
    report = {
        'summary': {
            'title_present_exact': title_present,
            'expected_keyword_count': len(expected_keywords),
            'missing_keyword_count': len(missing_keywords),
            'suspicious_match_count': len(suspicious_matches)
        },
        'missing_keywords': missing_keywords,
        'suspicious_matches': suspicious_matches,
        'ocr_excerpt': ocr_text[:4000]
    }
    return report


def main():
    ap = argparse.ArgumentParser(description='Evaluate generated architecture PNG for spelling/label issues')
    ap.add_argument('--png', required=True)
    ap.add_argument('--expected-json', required=True)
    ap.add_argument('--report', required=True)
    args = ap.parse_args()

    spec = load_json(args.expected_json)
    ocr_text, err = ocr_png(args.png)
    if err:
        report = {
            'status': 'warning',
            'message': err,
            'recommendation': 'Use a vision-capable evaluator model or install OCR dependencies.'
        }
    else:
        report = {'status': 'ok', 'evaluation': evaluate(spec, ocr_text)}
    save_json(args.report, report)
    print(f'Wrote evaluation report to {args.report}')


if __name__ == '__main__':
    main()
