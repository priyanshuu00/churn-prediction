# Tableau Dashboard Specification

## Purpose
Provide a clean, business-user friendly interface for the Customer Success Manager to view overall churn health and prioritize outreach based on AI-driven risk scores.

## Data Source
The Tableau dashboard will connect to a flattened, enriched dataset: `vw_tableau_dashboard_feed`.
This feed includes:
- Historical Data (Tenure, Contract, Monthly Charges)
- Machine Learning Output (Churn Probability, Risk Tier, Top 3 Drivers)
- AI Output (Next-Best-Action Recommendation)

---

## VIEW 1: Executive Overview (Top Level)
**Goal:** Answer "How bad is churn?"

**Visuals:**
1. **KPI BANs (Big A** Numbers):** 
   - Total Customers (e.g., 7,043)
   - Overall Churn Rate (e.g., 26.5%)
   - Historical Revenue Lost (Sum of churned Monthly Charges)
   - **Monthly Revenue Exposure from High-Risk Customers** (Sum of Monthly Charges for Active customers where Risk = High)
2. **Trend Chart:** Monthly Charges distribution (Area Chart) showing Active vs. Churned.

---

## VIEW 2: Churn Drivers (Diagnostic)
**Goal:** Answer "Where is churn concentrated?"

**Visuals:**
1. **Bar Chart:** Churn Rate by Contract Type (Month-to-month vs. Annual).
2. **Stacked Bar Chart:** Churn Volume by Internet Service Type.
3. **Scatter Plot / Matrix:** Tech Support Tickets (X-axis) vs. Churn Rate (Y-axis), sized by Customer Count.

---

## VIEW 3: Customer Risk & Prioritization
**Goal:** Answer "Which customers should I prioritize?"

**Visuals:**
1. **Risk Tier Distribution (Donut or Bar):** Low, Medium, High, Critical.
2. **Detail Table (Interactive List):**
   - Customer ID
   - Monthly Charges (Revenue)
   - Churn Probability %
   - Risk Tier
   - *Sorted descending by Monthly Charges to prioritize VIPs.*

---

## VIEW 4: Retention Intelligence (Action)
**Goal:** Answer "What should I do to save them?"

**Visuals:**
1. **Action Panel (Linked to View 3 Table):**
   When a user clicks a specific customer in View 3, this panel updates to show:
   - **Top Risk Drivers:** (e.g., "Month-to-Month, 4 Tech Tickets")
   - **AI Recommended Action:** (e.g., "Proactive Tech Support Outreach")
   - **AI Reasoning:** (e.g., "High technical friction detected; resolve underlying network issue to prevent cancellation.")

## User Experience Flow
1. CSM logs in and checks the **Monthly Revenue Exposure from High-Risk Customers** in View 1.
2. Navigates to **View 3** and filters for `Risk Tier = High`.
3. Sorts the list by `Monthly Charges` to find the most valuable accounts.
4. Clicks the top account.
5. Reads the **AI Recommended Action** in View 4 and executes the playbook (e.g., calls the customer with a targeted offer).
