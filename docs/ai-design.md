# AI Design Document

## 1. Goal
Translate the output of our predictive churn model (a probability score) into actionable, plain-English Next-Best-Action (NBA) recommendations for Customer Success Managers (CSMs).

## 2. Constraints & Safety
- **No Hallucinations:** The LLM is restricted via system prompt to ONLY choose from a pre-defined list of 5 approved business interventions. It cannot invent discounts, promise refunds, or claim non-existent policies.
- **Deterministic Triggering:** The model only generates text; it does not trigger emails or API calls directly to the customer. A human (the CSM) always remains in the loop.
- **Batch Processing:** Recommendations are generated offline/batch for all customers scoring above the `High Risk` threshold (e.g., > 65% probability) and are then displayed in Tableau.

## 3. Data Pipeline
1. **Input:** Python `dict` containing the customer's tenure, contract type, payment method, support tickets, and calculated churn probability.
2. **System Prompt:** Instructs Gemini to act as a Retention AI Agent.
3. **Execution:** Gemini evaluates the features and maps them to the approved intervention list.
4. **Output:** A strict JSON block containing `recommended_action`, `reasoning`, and `communication_tone`.

## 4. Fallback Mechanism
If the Gemini API is down, rate-limited, or keys are missing, the system gracefully falls back to a deterministic, rule-based Python function `_fallback_recommendation()`, ensuring the dashboard always has data to display.
