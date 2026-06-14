# Assessment, Gaps, and Recommendations Applied

This version applies the assessment and recommendations provided for the Architecture Diagram Skill.

## Implemented improvements

### 1. Claude-native rendering path
- Added `--render-mode claude-native` to the runner/renderer path.
- Added Claude-native rendering instructions that emit a self-contained SVG / draw.io XML prompt when drawio-skill CLI is not available.
- Added Claude-specific usage guidance in `SKILL.md`.

### 2. Domain vocabulary packs
Added `data/domain_vocabularies/` with starter packs:
- `financial_services.json`
- `healthcare.json`
- `retail_ecommerce.json`
- `cloud_platform.json`
- `ai_ml_platform.json`
- `manufacturing_iot.json`
- `government_public_sector.json`

These packs map domain terms to canonical architecture services, technical categories, flow patterns, and template affinities.

### 3. Ranked icon resolution
`build_drawio_prompt.py` now uses ranked icon matching:
1. exact canonical match
2. alias match
3. keyword overlap score
4. domain hint boost
5. generic fallback

It returns primary and fallback icon guidance.

### 4. Template-aware decomposition
`plan_multilevel_architecture.py` now reads `decomposition_defaults` from `data/reference_architecture_patterns.json`, then applies user overrides.

### 5. Business narrative generator
Added `generate_narrative.py`, producing a CIO-ready 3-sentence narrative that is injected into downstream prompts as the communication goal.

### 6. Hex-precise color palette
`data/style_guide.json` now contains explicit hex palettes:
- `enterprise_light`
- `enterprise_dark`
- `boardroom_blue`

The prompt builder emits exact hex values rather than abstract color labels.

### 7. Connector semantic layer
Flow schema and prompt generation now support:
- `sync_api`
- `async_event`
- `batch_etl`
- `streaming`
- `webhook`
- `pub_sub`
- `grpc`
- `file_transfer`
- `database_replication`
- `logical`

Each maps to distinct connector styling.

### 8. Guardrail feedback hooks
`build_drawio_prompt.py` accepts `--correction-report` and injects guardrail correction instructions into the renderer prompt. Runner supports `--auto-correct` metadata for correction cycles.

### 9. Claude-specific usage section
`SKILL.md` includes Claude / Claude API guidance and a Claude self-evaluation checklist.

### 10. Annotation / callout schema
`architecture_input_schema.json` supports `annotations` for highlights, risk flags, callouts, decision points, and investment markers.

### 11. Article/blog-to-diagram extraction
Added `extract_architecture_from_article.py`, implementing the `architecture-blog-to-diagram` transformation pattern for prose-first inputs.

## Key runtime files
- `run_architecture_skill.py`
- `prepare_architecture_input.py`
- `enrich_architecture_model.py`
- `generate_narrative.py`
- `plan_architecture_views.py`
- `plan_multilevel_architecture.py`
- `build_drawio_prompt.py`
- `extract_architecture_from_article.py`
- `render_with_drawio_adapter.py`

### 12. Guardrail correction addendum
Added `apply_guardrail_corrections.py` to convert validation/report issues into correction instructions that `build_drawio_prompt.py` can inject via `--correction-report`.
