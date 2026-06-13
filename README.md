# Solution Architecture Diagram Skill

**Author:** Arvind Radhakrishnen  
**Primary output:** PNG architecture diagram  
**Editable outputs:** Draw.io XML (`.drawio`) and normalized JSON  
**Primary renderer:** Agents365 Draw.io skill  
**Use from:** VS Code, ChatGPT, Google Gemini, Claude, Cursor, or any agent interface that can read a skill folder and run local scripts.

---

## What this skill does

This skill helps anyone describe a solution in natural language and generate a professional solution architecture diagram.

You can provide a short request such as:

> Build a solution architecture diagram for a policy-as-spec governance platform where architects author YAML/JSON controls, a control plane resolves specs, CI/CD pipelines enforce them, and AWS/Azure/GCP targets receive deployments.

The skill converts that request into:

1. **Normalized architecture JSON**
2. **A Draw.io-ready generation prompt**
3. **A generated PNG architecture diagram**
4. **Editable Draw.io XML / `.drawio` output when rendered through drawio-skill**
5. **An optional evaluation report to catch spelling, missing label, or text quality issues**

---

## Who should use it

Use this skill if you are:

- an enterprise architect creating solution diagrams
- a product owner describing a new platform
- a solution architect documenting cloud, AI, data, security, or integration architecture
- a consultant preparing executive-ready architecture slides
- a developer who wants architecture diagrams generated from requirements
- a student or founder who wants to explain a technical solution visually

---

## What users need to provide

Users can provide either a simple natural-language description or structured JSON.

### Option 1 — Natural-language input

Example:

```text
Create a solution architecture diagram for an Article Summary Platform.
The system ingests articles, extracts metadata, summarizes content using LLMs,
stores evidence and citations, exposes dashboards and APIs, and uses audit,
security, and monitoring as cross-cutting controls.
```

The skill should convert this into the required JSON structure automatically.

### Option 2 — Structured JSON input

Use `examples/input_template.json` as a starting point.

```json
{
  "title": "Article Summary Platform",
  "subtitle": "Ingestion, summarization, evidence management, and business delivery",
  "template": "platform_value_chain",
  "lanes": [
    {
      "side": "left",
      "title": "Inputs",
      "items": ["Articles", "URLs", "PDFs", "Feeds", "APIs"]
    },
    {
      "side": "right",
      "title": "Outputs",
      "items": ["Summary dashboard", "Citation report", "Insight API", "Alerts"]
    }
  ],
  "zones": [
    {
      "id": "ingestion",
      "title": "Content Ingestion",
      "subtitle": "Collect and normalize",
      "items": ["URL crawler", "Document parser", "Metadata extraction", "Deduplication"]
    },
    {
      "id": "knowledge",
      "title": "Evidence Store",
      "subtitle": "Searchable source of truth",
      "items": ["Raw content", "Embeddings", "Citation index", "Version history"]
    },
    {
      "id": "ai",
      "title": "AI Summarization",
      "subtitle": "Generate and validate",
      "items": ["LLM summarizer", "Fact checker", "Topic classifier", "Question generator"]
    },
    {
      "id": "delivery",
      "title": "Delivery Layer",
      "subtitle": "Consume insights",
      "items": ["Dashboard", "API gateway", "Report generator", "Notification service"]
    }
  ],
  "flows": [
    {"from": "ingestion", "to": "knowledge", "label": "curated content"},
    {"from": "knowledge", "to": "ai", "label": "grounded context"},
    {"from": "ai", "to": "delivery", "label": "approved summaries"}
  ],
  "operations": ["SSO", "Audit trail", "Observability", "Data governance", "Model monitoring"],
  "footer": "Deployable on AWS, Azure, GCP, or private cloud",
  "rendering_preferences": {
    "backend": "drawio-skill",
    "format": "png",
    "embed_xml": true
  }
}
```

---

## Supported layout types

Choose one of these templates, or let the skill select one automatically.

| Template | Best for |
|---|---|
| `platform_value_chain` | Product overviews, AI platforms, capability chains, input → platform → output diagrams |
| `composite_ai_platform` | Agentic AI platforms, reusable solution maps, enterprise AI capability maps |
| `cloud_tenant_microservices` | SaaS platforms, tenant systems, APIs, cloud services, microservices |
| `enterprise_endpoint_management` | Endpoint, identity, compliance, policy, security, app management |
| `cloud_data_platform` | Data platforms, lakehouse, ingestion, governance, analytics, AI/ML delivery |

Reference layouts are documented in `docs/reference_layouts.md`.

---

## Quick start from VS Code

### 1. Download and unzip this skill

Unzip the package into a local folder, for example:

```bash
unzip architecture_diagram_skill_v3.zip
cd architecture_diagram_skill_v3
```

### 2. Prepare your input

Copy the blank template:

```bash
cp examples/input_template.json examples/my_architecture.json
```

Edit `examples/my_architecture.json` in VS Code.

### 3. Normalize and validate the input

```bash
python prepare_architecture_input.py   --input examples/my_architecture.json   --output outputs/prepared_input.json
```

### 4. Build the Draw.io prompt

```bash
python build_drawio_prompt.py   --input outputs/prepared_input.json   --output outputs/drawio_prompt.md
```

### 5. Render with drawio-skill

Feed `outputs/drawio_prompt.md` into the imported Agents365 drawio-skill.

Expected generated files:

```text
outputs/solution_architecture.drawio
outputs/solution_architecture.png
outputs/prepared_input.json
```

### 6. Evaluate the PNG for spelling and label quality

```bash
python evaluate_architecture_png.py   --png outputs/solution_architecture.png   --expected-json outputs/prepared_input.json   --report outputs/diagram_eval_report.json
```

If issues are found, refine the input labels or prompt and regenerate.

---

## Quick start from ChatGPT

Use this prompt pattern:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for:
[describe the solution]

Use a clean enterprise architecture style.
Return:
1. PNG diagram
2. Draw.io XML / .drawio source if available
3. Normalized JSON used to generate the diagram
4. Evaluation report for spelling and label quality
```

Example:

```text
Use the Solution Architecture Diagram Skill.

Build a solution architecture diagram for a Policy-as-Spec Architecture Control Platform.
Architects author YAML/JSON specs. A control plane resolves specs through REST,
GraphQL, and MCP. CI/CD pipelines enforce controls using arch-ctl and OPA.
Deployments target AWS EKS, AKS, and GCP. Cross-cutting components include
evidence ledger, drift detector, and waiver governance.

Return PNG, draw.io source, normalized JSON, and spelling evaluation report.
```

The assistant or agent should:
1. Normalize the request into architecture JSON
2. Select the layout
3. Build a drawio-skill prompt
4. Render PNG + `.drawio`
5. Evaluate the PNG output

---

## Quick start from Google Gemini

Use this prompt pattern in Gemini:

```text
You have access to a Solution Architecture Diagram Skill folder.
Read SKILL.md first.

Create a PNG solution architecture diagram for:
[describe the solution]

Use the skill workflow:
- normalize the request into JSON
- select the best reference layout
- generate a draw.io prompt
- render PNG and .drawio XML if possible
- run the PNG evaluation workflow for spelling and text quality
```

Gemini can use the same normalized JSON contract in `examples/input_template.json`.

---

## Quick start from any agent interface

Any AI coding or assistant tool can use this skill if it can:

1. Read files in this folder
2. Execute Python scripts
3. Invoke drawio-skill or render Draw.io XML
4. Return generated files

Generic instruction:

```text
Read SKILL.md in this folder.
Ask me what solution architecture I want to build.
Convert my response into the normalized JSON schema.
Generate a drawio-skill prompt.
Render a PNG and editable .drawio XML.
Run the PNG evaluation workflow and fix spelling or label issues.
Return the PNG, .drawio file, normalized JSON, and evaluation report.
```

---

## Output files

A completed run should produce:

| File | Purpose |
|---|---|
| `outputs/prepared_input.json` | Clean normalized architecture input |
| `outputs/drawio_prompt.md` | Prompt to send to drawio-skill |
| `outputs/solution_architecture.drawio` | Editable Draw.io XML source |
| `outputs/solution_architecture.png` | Final PNG diagram |
| `outputs/diagram_eval_report.json` | Quality and spelling evaluation report |

If drawio-skill is unavailable, the skill should still return:

- normalized JSON
- generated drawio prompt
- a note explaining that rendering requires drawio-skill / draw.io CLI

---

## Input quality tips

Good architecture diagrams come from clean inputs.

Use this structure:

```text
1. What is the solution?
2. Who are the users or actors?
3. What are the major layers?
4. What systems are on the left as inputs?
5. What systems are on the right as outputs?
6. What are the central platform capabilities?
7. What are the key flows?
8. What security, audit, governance, or operations controls are cross-cutting?
9. What cloud or deployment targets should appear?
```

Keep labels short:

- Good: `Spec Repository`
- Avoid: `A centralized repository that stores all enterprise and LOB specifications and version history`

Use notes or subtitles for longer explanations.

---

## PNG evaluation

The skill includes a post-render evaluation workflow.

It checks for:

- spelling mistakes
- missing labels
- suspicious OCR mismatches
- truncated text
- label readability issues

Run:

```bash
python evaluate_architecture_png.py   --png outputs/solution_architecture.png   --expected-json outputs/prepared_input.json   --report outputs/diagram_eval_report.json
```

For best results, combine the OCR-based script with a **vision-capable evaluator model** that visually checks the PNG.

---

## Companion dependency

This skill is designed to work with the open-source Agents365 drawio-skill repository:

```text
https://github.com/Agents365-ai/drawio-skill
```

Typical install patterns include:

```bash
npx skills add Agents365-ai/365-skills -g
```

or manual clone into a local skills directory.

---

## Package structure

```text
architecture_diagram_skill_v3/
├── SKILL.md
├── README.md
├── prepare_architecture_input.py
├── build_drawio_prompt.py
├── evaluate_architecture_png.py
├── render_architecture.py
├── skill_manifest.json
├── data/
│   ├── architecture_input_schema.json
│   └── reference_architecture_patterns.json
├── docs/
│   ├── USAGE.md
│   ├── input_formatting_guide.md
│   ├── png_eval_workflow.md
│   └── reference_layouts.md
├── examples/
│   ├── input_template.json
│   ├── invoke_skill_prompt.txt
│   ├── sample_input.json
│   └── sample_drawio_prompt.md
└── outputs/
```

---

## License and usage

This skill is provided as an architecture-generation helper. The included sample reference diagrams are used only to describe layout archetypes and should not be copied literally.

**Author:** Arvind Radhakrishnen
