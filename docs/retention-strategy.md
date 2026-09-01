# Retention Strategy Mapping

This document outlines the business logic used by our AI and rule-based systems to determine the Next-Best-Action for a high-risk customer.

## The Matrix: Risk Signal → Business Action

| Risk Signal (Evidence) | Recommended Action (Intervention) | Business Rationale |
| :--- | :--- | :--- |
| **High Tech Tickets (> 2)** | Proactive Tech Support Outreach | High technical friction is a massive churn driver. A VIP tech check-in resolves the root cause. |
| **Month-to-Month Contract** | Contract Upgrade Incentive | M2M customers have zero exit barriers. Offering a 10% discount to lock in an annual plan secures MRR. |
| **Electronic Check Payment** | Auto-Pay Migration Campaign | Manual payments lead to passive churn (forgetting to pay). We assist them in setting up Credit Card auto-pay. |
| **Missing Security Add-ons** | Free 1-Month Security Trial | Customers with more integrated services ("sticky" products) churn less. The trial builds reliance on our ecosystem. |
| **High Tenure + Elevated Risk** | VIP Loyalty Check-in | Loyal customers rarely churn unless a major life event or massive service failure occurs. Requires a personalized, high-touch call. |

## Execution Guidelines
- **Budget Caps:** Interventions involving discounts (Contract Upgrade) cannot exceed 10% of the customer's Annual Recurring Revenue (ARR).
- **Frequency Capping:** A customer should not receive more than one retention outreach every 6 months to avoid fatigue.
