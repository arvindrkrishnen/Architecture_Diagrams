# Domain Vocabulary Packs

Domain vocabulary packs improve executive credibility by mapping domain-specific terms to canonical architecture components and correct placement zones.

## Available packs
- financial_services
- healthcare
- retail_ecommerce
- cloud_platform
- ai_ml_platform
- manufacturing_iot
- government_public_sector

## Usage

```bash
python run_architecture_skill.py \
  --text-file examples/request.txt \
  --domain financial_services \
  --allow-parallel
```

Or during normalization:

```bash
python prepare_architecture_input.py \
  --input examples/my_architecture.json \
  --output outputs/prepared_input.json \
  --domain financial_services
```

## What packs do
- identify matched domain terms
- add canonical services into the model
- add cross-cutting concerns such as compliance and audit controls
- influence icon selection, placement, and template affinity
- improve technology placement validation
