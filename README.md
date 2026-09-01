# 📊 AI-Powered Customer Churn & Retention Intelligence

## 1. Project Overview
This project is an end-to-end, decision-support analytics product designed to help businesses proactively manage customer churn. By combining **MySQL analytics, Python-based Machine Learning (Logistic Regression), Generative AI (Gemini), and Tableau**, this platform identifies customers at high risk of churning, explains the underlying drivers of that risk, and provides actionable, AI-generated retention recommendations.

## 2. Business Problem
Customer churn directly erodes Monthly Recurring Revenue (MRR). Traditional reporting is reactive; businesses usually find out a customer is unhappy only *after* they cancel. Customer Success Managers (CSMs) need a forward-looking system that bridges the gap between raw data and actionable retention strategies to protect monthly revenue exposure.

## 3. Product Solution
We built a pipeline that transitions from data cleaning to advanced modeling, and finally to business intervention:
1. **Data Layer (MySQL):** Cleans raw telco data and engineers features (e.g., cohort tenure, ticket volume).
2. **Machine Learning (Python/Scikit-Learn):** A balanced Logistic Regression model predicts individual churn probability.
3. **Generative AI (Gemini):** Evaluates high-risk profiles and maps them to a strictly approved matrix of retention actions (e.g., *Contract Upgrade Incentive*, *Proactive Tech Outreach*).
4. **Business Intelligence (Tableau):** A user-friendly dashboard enabling CSMs to sort at-risk customers by financial impact and apply the AI-recommended interventions.

## 4. Product Decision Flow
**The model is not treated as the product. The product converts model predictions into explainable, prioritized retention decisions for business users.**

The flow is strictly designed around human-in-the-loop decision-making:
Customer Data → Churn Risk Model → Risk Probability → Risk Drivers → Revenue at Risk → AI Next-Best-Action → CSM Intervention → Retention Outcome

## 5. Architecture & Technologies Used
- **SQL / MySQL:** Schema normalization, window functions, and data cleaning.
- **Python / Pandas / NumPy:** Exploratory Data Analysis (EDA) and feature engineering.
- **Scikit-Learn:** Logistic Regression, class-weight balancing, ROC-AUC metrics.
- **Google Gemini API:** Generative AI-powered recommendation engine translating structured risk drivers into human-readable text.
- **Tableau:** Executive and operational dashboard design specification.

## 6. Key Analytical Findings
- **High Friction Proxy:** Customers on Month-to-Month contracts who have submitted 3 or more technical support tickets are at the absolute highest risk of churn.
- **Service Synergy:** Customers lacking supplementary services (like Online Security) show a relationship with higher churn compared to those fully integrated into the product ecosystem.
- **Payment Method Risk:** Electronic check payments are associated with higher churn compared to credit card auto-pay.

## 7. AI & Explainability Features
- **Model Card:** We prioritize **Recall** over Precision, intentionally accepting some False Positives to ensure we do not miss high-value customers who are secretly at risk.
- **Constrained GenAI:** Gemini is not allowed to hallucinate offers. It is strictly constrained by a system prompt to select from 5 approved business interventions, ensuring the output is actually viable for a CSM to execute.

## 8. Business Impact & ROI Measurement
The system explicitly separates historical metrics from predictive metrics:
- **Historical Revenue Lost:** Actual revenue lost from canceled accounts.
- **Monthly Revenue Exposure from High-Risk Customers:** Total monthly charges from active accounts currently flagged by the ML model as `High Risk`.
- **Estimated Revenue Protected:** A scenario estimate projecting potential savings if a given percentage of high-risk customers are successfully retained.

## 9. Setup Instructions & How to Run
1. Clone the repository and install dependencies: `pip install -r requirements.txt`.
2. Ensure you have a local MySQL instance running. Run the SQL scripts in the `sql/` directory sequentially.
3. Copy `.env.example` to `.env` and insert your Gemini API Key.
4. Run `python build_project.py` to train the model, evaluate it, and generate the final `data/processed/` output files.
5. Review the `dashboard/dashboard_spec.md` to build the Tableau views.

## 10. Limitations & Future Improvements
- **Data Snapshot:** The dataset is currently a static snapshot. 
- **Intervention Feedback Loop:** To measure true "Retention Conversion Rate," we would need to integrate the output with a CRM to track intervention outcomes over time.
- **Tableau Mockup:** Currently, the Tableau UI exists as a specification document designed around the generated `tableau_dashboard_feed.csv`.
