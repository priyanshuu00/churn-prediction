# Product Metrics

The following metrics define how we will measure the health of the customer base and the success of the AI-Powered Customer Churn & Retention Intelligence product.

## 1. Churn Rate
- **Definition:** The percentage of total customers who have canceled their service over a specific time period.
- **Calculation Concept:** (Number of Churned Customers / Total Customers at the start of the period) * 100
- **Purpose:** The primary north star metric for the retention team.

## 2. Retention Rate
- **Definition:** The percentage of customers retained over a specific time period.
- **Calculation Concept:** 100% - Churn Rate.
- **Purpose:** A positive framing of business health, often used in executive reporting.

## 3. Revenue at Risk
- **Definition:** The total monthly or annual recurring revenue tied to customers who are currently flagged as high-risk by the model.
- **Calculation Concept:** Sum of (MonthlyCharges) for all customers where `Risk Level = High`.
- **Purpose:** Helps CSMs prioritize outreach based on financial impact rather than just customer volume.

## 4. High-Risk Customer Count
- **Definition:** The absolute number of customers identified by the analytics/ML pipeline as having a high probability of churning.
- **Calculation Concept:** Count of customers where `Churn Probability > Threshold`.
- **Purpose:** Defines the backlog of work for the Customer Success team.

## 5. Average Tenure
- **Definition:** The average length of time a customer stays with the company.
- **Calculation Concept:** Mean of the `tenure` column across active customers.
- **Purpose:** Helps identify at what lifecycle stage customers are most likely to drop off.

## 6. Estimated Revenue Protected
- **Definition:** The amount of revenue saved from customers who were flagged as high-risk, received an intervention, and subsequently did *not* churn.
- **Calculation Concept:** Sum of (MonthlyCharges) for customers who were high-risk, received a retention action, and remained active past their risk window.
- **Purpose:** Quantifies the ROI of the AI product and the retention team's efforts.

## 7. Retention Conversion Rate
- **Definition:** The success rate of the Next-Best-Action interventions.
- **Calculation Concept:** (Number of High-Risk Customers Retained / Total Number of High-Risk Customers Contacted) * 100
- **Purpose:** Evaluates the quality and effectiveness of the AI-generated recommendations.
