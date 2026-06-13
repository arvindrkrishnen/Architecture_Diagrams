# Sub-Agent Orchestration Model

## Overview
The single runner `run_architecture_skill.py` coordinates multiple sub-agents.

## Sub-agents
1. **intake_agent**
   - accepts text or JSON
   - creates a draft working specification

2. **normalization_agent**
   - validates and normalizes the working specification
   - writes `prepared_input.json`

3. **layout_agent**
   - records the selected template and summary counts

4. **decomposition_agent**
   - creates a multi-level plan for overview and expansion diagrams

5. **overview_prompt_agent**
   - generates the Level 1 overview draw.io prompt

6. **expansion_prompt_agent**
   - generates one prompt per Level 2 expansion diagram

7. **packaging_agent**
   - writes the orchestration report

## Memory sharing
Shared state is stored in a common context object and checkpointed into:
- `outputs/<run_name>/run_context.json`

This provides durable memory across sub-agents and makes fallback from parallel to sequential execution safe.

## Parallel execution strategy
Parallelizable stages:
- layout selection
- decomposition planning
- overview prompt generation
- expansion prompt generation

The runner performs a parallel execution probe first.
If the engine does not support reliable parallel execution, the runner switches to sequential mode.

## Fallback checkpoint
A checkpoint is written before and after the middle orchestration stage.
If the parallel stage fails, the runner records the reason and reruns the remaining tasks sequentially.
