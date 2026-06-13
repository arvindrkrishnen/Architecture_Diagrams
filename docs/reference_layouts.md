# Reference Layout Gallery for Solution Architecture Diagrams

> These examples are **layout references only**. They are not to be copied literally.
> The purpose of this gallery is to help the skill choose **how to organize information** before the diagram is rendered using drawio-skill.

## How to use this gallery
For any architecture request:
1. Pick the closest layout family.
2. Follow the layout grammar, not the exact artwork.
3. Use the selected family to build a drawio-skill prompt.
4. Render the final diagram as original work.

---

## 1. Platform value chain layout
**Template id:** `platform_value_chain`

**Use when:**
- you need a product overview
- you want a low-code / AI / analytics capability map
- you have clear upstream inputs and downstream outputs

**Visual grammar:**
- left rail for data sources / applications / real-time feeds
- large central platform boundary
- 4-6 capability tiles inside the platform
- right rail for outputs such as dashboards, apps, automation
- bottom cross-cutting operations band

**What the skill should learn from this reference:**
- the composition is outside-in and left-to-right
- grouping is more important than dense interconnectivity
- the center platform boundary is the primary visual anchor

![Platform value chain reference](../assets/reference_layouts/mastercraft_platform_overview.png)

---

## 2. Composite AI platform layout
**Template id:** `composite_ai_platform`

**Use when:**
- you need to show AI capabilities for business, IT, and agentic ecosystems
- you want a central capability map with supporting sectors
- you need a bottom band of reusable offerings or solutions

**Visual grammar:**
- central large grouped platform canvas
- multiple vertical capability columns
- left outer column for business sectors or industries
- right outer column for transformation outcomes / service lines
- bottom tile row for reusable solution assets

**What the skill should learn from this reference:**
- this layout behaves like a portfolio map rather than a strict data-flow diagram
- containment and categorization matter more than arrows
- side pillars communicate context, not core processing

![Composite AI platform reference](../assets/reference_layouts/tcs_cap_ai_overview.png)

---

## 3. Cloud tenant microservices layout
**Template id:** `cloud_tenant_microservices`

**Use when:**
- you need a SaaS or cloud migration view
- you want to show peripheral systems, mobile apps, APIs, microservices, and cloud services
- you need a clear system boundary from edge to tenant to cloud

**Visual grammar:**
- far-left actor/peripheral stack
- middle tenant/client system block
- right cloud platform block
- security / API / IAM rail inside cloud area
- microservices in the center of the cloud area
- portal / admin / onboarding block at the bottom

**What the skill should learn from this reference:**
- the diagram is structured as a left-to-right journey
- the cloud area can itself contain subzones
- top rows are useful for storage / platform utilities

![Cloud tenant microservices reference](../assets/reference_layouts/cloud_tenant_microservices.png)

---

## 4. Enterprise endpoint management layout
**Template id:** `enterprise_endpoint_management`

**Use when:**
- you need endpoint management or security architecture
- you want to show device policy, compliance, identity, apps, and managed endpoints
- you need external dependencies around a large service boundary

**Visual grammar:**
- one large central service boundary
- grouped internal blocks for protection, apps, policy, configuration, compliance
- identity and external systems on the right and left edges
- grouped device populations across the bottom

**What the skill should learn from this reference:**
- the central boundary dominates the page
- external systems form a surrounding ecosystem
- bottom grouped device blocks help show management coverage

![Endpoint management reference](../assets/reference_layouts/endpoint_management.png)

---

## 5. Cloud data platform layout
**Template id:** `cloud_data_platform`

**Use when:**
- you need a data platform, lakehouse, or governance architecture
- you want to show ingestion, core platform, and access layers
- you need multiple shared services and consumers

**Visual grammar:**
- four macro-columns: sources, ingestion, core platform, delivery
- the core platform is the largest region
- use stacked layers or bands for storage, compute, governance, metadata, and shared services
- rightmost area shows business consumption, analytics, apps, or AI/ML

**What the skill should learn from this reference:**
- this is a structured enterprise platform view
- layering inside the core platform is important
- consumption patterns should remain visually separate from platform internals

**Public reference URL:**
- https://d2908q01vomqb2.cloudfront.net/77de68daecd823babbb58edb1c8e14d7106e83bb/2024/04/26/PwC-Unified-Sustainability-Hub-2.1.png

---

## Prompting rules shared across all layouts
- Use the reference only for **layout family**.
- Do not recreate exact proprietary diagrams.
- Prefer short labels and clean grouping.
- Use drawio-skill for the final rendering.
- Export to PNG, and preserve `.drawio` source whenever possible.
