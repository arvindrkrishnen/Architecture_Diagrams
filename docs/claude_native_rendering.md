# Claude-Native Rendering Path

Use this path when Agents365 drawio-skill CLI or draw.io desktop is not available.

## Runner usage

```bash
python run_architecture_skill.py \
  --text-file examples/request.txt \
  --render \
  --render-mode claude-native
```

## What happens
The renderer adapter writes a Claude-native render instruction file for each output variant. The file asks Claude to generate:
1. inline SVG preview
2. draw.io-compatible XML inside an `mxGraphModel` block
3. ADA-compliant text sizing, wrapping, padding, and orthogonal connectors

## Manual use
Paste the generated `.claude_native_render.md` content into Claude and ask it to render the inline SVG and draw.io XML.
