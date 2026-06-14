# Article / Blog to Diagram Extraction

The skill includes `extract_architecture_from_article.py` to transform prose-first content into a diagram-ready architecture payload.

## When to use
Use it for:
- architecture blogs
- long-form articles
- whitepapers
- platform engineering writeups
- governance/control-plane narratives
- DevOps / CI-CD / observability articles

## Runner usage

```bash
python run_architecture_skill.py \
  --text-file article.md \
  --source-kind article
```

## Direct usage

```bash
python extract_architecture_from_article.py \
  --input-file article.md \
  --output outputs/article_extraction.json
```

## Extraction output
The extractor returns:
- executive abstraction
- architecture layers
- key components
- interfaces
- interaction flows
- sequence models
- normalized diagram payload
- ambiguities and assumptions
