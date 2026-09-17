# System Design: Guardrails & Hallucination Elimination

## 1. The Financial Hallucination Problem
LLMs naturally interpolate numbers when predicting the next token. In accounting, an interpolated 0.5% difference can lead to compliance violations.

## 2. Mitigation Strategy
- **Strict Grounding Prompting**: System prompts prohibit extrapolation beyond provided context.
- **Post-Inference RegEx Audit**: A regex layer extracts every number in the LLM output and validates its exact presence in the retrieved source text chunk.
- **Automatic Retry Trigger**: If any ungrounded numerical token is detected, the query is rejected or re-run with zero temperature.
