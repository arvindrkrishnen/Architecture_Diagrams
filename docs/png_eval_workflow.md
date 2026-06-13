# PNG Evaluation Workflow

The purpose of this workflow is to catch errors **after** a diagram is rendered.

## Evaluation goals
1. Detect spelling mistakes
2. Detect missing or truncated labels
3. Detect suspicious OCR mismatches
4. Detect key expected labels that never appeared in the output
5. Flag low-confidence text for human or model review

## Recommended evaluation stack
### Preferred
- A **vision-capable evaluator model** that looks at the final PNG and checks:
  - title spelling
  - section headers
  - major box labels
  - arrow labels
  - cropped or overlapping text

### Optional automated support
- `evaluate_architecture_png.py`
  - OCRs the PNG
  - builds an expected vocabulary from the normalized JSON
  - compares OCR output to expected text
  - emits a JSON report of likely misses and suspicious labels

## Suggested evaluation loop
1. Generate PNG with drawio-skill
2. Run OCR evaluator
3. Run vision evaluator review
4. If issues exist:
   - shorten labels
   - reduce density
   - revise prompt wording
   - regenerate PNG
5. Re-run evaluation until issues are resolved

## Pass criteria
A diagram should pass when:
- title matches exactly
- no obvious spelling errors exist in primary labels
- expected critical labels are present
- OCR mismatch count is low and explainable
- labels are readable and not clipped

## Common remediation actions
- Replace long labels with shorter equivalents
- Split a crowded zone into two zones
- Increase whitespace in the prompt
- Ask drawio-skill to reduce text density
- Correct brand capitalization (e.g., GraphQL, Kubernetes, OpenAI, Azure)
