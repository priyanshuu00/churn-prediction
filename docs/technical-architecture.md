# Technical Architecture

## 1. System Overview
This project simulates a batch-processed data and AI pipeline. It takes raw telecom data, processes it through SQL and Python, generates ML predictions, augments them with Generative AI, and prepares the final flat file for Tableau consumption.

## 2. Component Stack
- **Database:** MySQL (Structured storage, data cleaning, cohort aggregation)
- **Data Engineering / EDA:** Python, Pandas, NumPy
- **Machine Learning:** Scikit-Learn (Logistic Regression, ROC-AUC evaluation)
- **Generative AI:** Google Gemini API (Strictly prompted for Next-Best-Action generation)
- **Visualization:** Tableau Desktop/Public

## 3. Data Flow
1. **Ingestion:** `RAW DATA.xlsx` is loaded into MySQL `stg_raw_data`.
2. **Transformation:** SQL scripts clean missing values, normalize the schema, and create `vw_customer_churn_analytics`.
3. **ML Prediction:** `src/model/churn_classifier.py` pulls the view, trains the Logistic Regression model, and scores active customers with a `churn_probability`.
4. **AI Enrichment:** High-risk customers (`churn_probability > 0.65`) are passed to `src/ai/recommendation_engine.py`. Gemini maps the customer's features to one of the 5 approved business interventions and generates plain-English reasoning.
5. **Output Delivery:** The final enriched dataset (Features + Probabilities + AI Recommendations) is exported to a `.csv` or directly connected to Tableau for the CSM dashboard.
