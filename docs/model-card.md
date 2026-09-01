# Model Card: Customer Churn Predictor

## 1. Model Details
- **Model Type:** Logistic Regression (with class-weight balancing)
- **Use Case:** Predicting the probability (0-100%) that an active customer will cancel their telecom subscription.

## 2. Intended Use
- **Primary Use:** To flag high-risk customers for proactive retention outreach by the Customer Success team.
- **Out of Scope:** Should not be used to automatically deny services or alter billing without human review.

## 3. Data & Feature Engineering
- **Source:** Telecom Churn Dataset (7,043 rows)
- **Target Variable:** `Churn` (Yes/No)
- **Features Used:** 
  - Demographics (SeniorCitizen, Dependents)
  - Services (Internet, TechSupport)
  - Financials (Tenure, Contract type, MonthlyCharges)
  - Operations (Tech tickets, Admin tickets)
- **Handling Imbalance:** The target variable is imbalanced (~26% churn). We applied the `class_weight='balanced'` parameter to heavily penalize false negatives (missing a churner).

## 4. Evaluation Metrics
- **Chosen Threshold (0.4):** After evaluating the precision-recall trade-off, we selected a custom decision threshold of 0.4 (rather than the default 0.5). At this threshold, the model achieves a **Recall of 94%** and a **Precision of 57%** for the churn class.
- **Recall (Sensitivity):** We prioritize Recall over Precision. It is better to falsely flag a customer as "At Risk" and give them a check-in call (False Positive) than to completely miss a customer who is about to churn (False Negative).
- **ROC-AUC:** Used as the primary metric for overall model separability, scoring an excellent 0.925 (ROC-AUC is threshold-independent).

## 5. Limitations & Bias
- **Static Snapshot:** The dataset lacks time-series data for individual customers (e.g., we see total tenure, but not monthly changes in behavior).
- **False Positives:** Will result in some retention budget (discounts) being spent on customers who were not actually going to leave. Business rules must cap the discount availability.
