# How to Use This Skill

**Author:** Arvind Radhakrishnen

## One-line instruction

```text
Use the Solution Architecture Diagram Skill to create a PNG and editable Draw.io architecture diagram for the solution I describe.
```

## From VS Code

1. Open the skill folder in VS Code.
2. Copy `examples/input_template.json` to `examples/my_architecture.json`.
3. Fill in the title, template, lanes, zones, flows, and operations.
4. Run:

```bash
python prepare_architecture_input.py --input examples/my_architecture.json --output outputs/prepared_input.json
python build_drawio_prompt.py --input outputs/prepared_input.json --output outputs/drawio_prompt.md
```

5. Send `outputs/drawio_prompt.md` to drawio-skill.
6. Export:
   - `outputs/solution_architecture.png`
   - `outputs/solution_architecture.drawio`
7. Evaluate:

```bash
python evaluate_architecture_png.py --png outputs/solution_architecture.png --expected-json outputs/prepared_input.json --report outputs/diagram_eval_report.json
```

## From ChatGPT

Paste:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for:
[describe your solution]

Return PNG, Draw.io XML, normalized JSON, and PNG evaluation report.
```

## From Google Gemini

Paste:

```text
Read SKILL.md from the Solution Architecture Diagram Skill folder.

Create a PNG and editable Draw.io architecture diagram for:
[describe your solution]

Follow the workflow: normalize input, select layout, build drawio prompt, render PNG/.drawio, evaluate spelling and label quality.
```

## Expected outputs

- PNG file
- Draw.io XML / `.drawio` source file
- Normalized JSON input
- Evaluation report JSON
