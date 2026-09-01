import os
import json
import pandas as pd
import numpy as np
import nbformat as nbf
from src.data.preprocessing import load_and_clean_data, feature_engineering
from src.model.churn_classifier import ChurnModel
from src.ai.recommendation_engine import RetentionAgent

def create_notebook(filename, title, markdown, code):
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(f"# {title}"),
        nbf.v4.new_markdown_cell(markdown),
        nbf.v4.new_code_cell(code)
    ]
    nb['cells'] = cells
    with open(filename, 'w') as f:
        nbf.write(nb, f)

def run():
    print("Running pipeline...")
    
    # 1. Data Cleaning
    raw_path = os.path.join('data', 'raw', 'RAW DATA.xlsx')
    if not os.path.exists(raw_path):
        print("Raw data not found at", raw_path)
        return
        
    df = load_and_clean_data(raw_path)
    df_engineered = feature_engineering(df)
    
    # Calculate historical metrics
    total_customers = len(df)
    churn_rate = len(df[df['Churn'] == 'Yes']) / total_customers
    hist_revenue_lost = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()
    
    # Save cleaned
    df_engineered.to_csv('data/processed/cleaned_customer_data.csv', index=False)
    
    # Apply Threshold prioritizing Recall
    threshold = 0.4 
    
    # 2. Model Training & Evaluation
    model = ChurnModel()
    X_train, X_test, y_train, y_test = model.prepare_data(df_engineered)
    model.train(X_train, y_train)
    report, auc = model.evaluate(X_test, y_test, threshold=threshold)
    
    # Generate risk scores for all ACTIVE customers
    active_mask = df_engineered['Churn_Target'] == 0
    active_df = df_engineered[active_mask].copy()
    
    # Use Sklearn Pipeline for predictions
    X_active = active_df[model.categorical_cols + model.numerical_cols]
    probs = model.model.predict_proba(X_active)[:, 1]
    active_df['ChurnProbability'] = probs
    
    # RiskTier uses the same threshold

    active_df['RiskTier'] = np.where(probs >= 0.7, 'Critical',
                            np.where(probs >= threshold, 'High', 'Low'))
                            
    active_df.to_csv('data/processed/customer_risk_scores.csv', index=False)
    
    # Calculate Predicted Revenue at Risk
    high_risk_mask = active_df['RiskTier'].isin(['High', 'Critical'])
    predicted_rev_risk = active_df[high_risk_mask]['MonthlyCharges'].sum()
    high_risk_count = high_risk_mask.sum()
    
    # 3. Tableau Dashboard Feed
    tableau_feed = active_df[['customerID', 'MonthlyCharges', 'tenure', 'Contract', 
                              'InternetService', 'PaymentMethod', 'numTechTickets', 'numAdminTickets',
                              'Churn', 'ChurnProbability', 'RiskTier']].copy()
                              
    # Initialize Retention Agent and extract model coefficients
    agent = RetentionAgent()
    coeffs = model.get_model_coefficients()
    coeff_dict = dict(zip(coeffs['Feature'], coeffs['Coefficient']))
    
    top_drivers = []
    nbas = []
    
    # Pre-encode features for local risk driver extraction
    preprocessor = model.model.named_steps['preprocessor']
    X_active_encoded = preprocessor.transform(X_active)
    X_active_encoded_df = pd.DataFrame(X_active_encoded, index=active_df.index, columns=model.feature_names)
    
    # We only process high-risk customers to save API calls and focus on actionable retention
    for idx, row in tableau_feed.iterrows():
        if row['RiskTier'] in ['High', 'Critical']:
            # Calculate dynamic risk driver based on LR coefficients * customer feature value
            customer_encoded_features = X_active_encoded_df.loc[idx]
            max_contribution = -np.inf
            top_driver = "Baseline Risk"
            
            for feat, val in customer_encoded_features.items():
                c = coeff_dict.get(feat, 0)
                contribution = c * val
                if contribution > max_contribution and contribution > 0:
                    max_contribution = contribution
                    top_driver = feat
            
            # Format top driver string
            top_driver = top_driver.replace('_', ' ').title()
            
            profile = {
                'tenure': row['tenure'],
                'MonthlyCharges': row['MonthlyCharges'],
                'Contract': row['Contract'],
                'PaymentMethod': row['PaymentMethod'],
                'numTechTickets': row['numTechTickets'],
                'ChurnProbability': f"{row['ChurnProbability']:.0%}",
                'TopRiskDriver': top_driver
            }
            rec = agent.get_recommendation(profile)
            action = rec.get('recommended_action', 'VIP Loyalty Check-in')
            
            top_drivers.append(top_driver)
            nbas.append(action)
        else:
            top_drivers.append("N/A")
            nbas.append("N/A")
            
    tableau_feed['TopRiskDriver1'] = top_drivers
    tableau_feed['NextBestAction'] = nbas
    tableau_feed.to_csv('data/processed/tableau_dashboard_feed.csv', index=False)
    
    # 4. Final Results Document
    results = f"""# Final Pipeline Results

## Business Analysis
- Total Customers: {total_customers}
- Churn Rate: {churn_rate:.2%}
- Historical Revenue Lost: ${hist_revenue_lost:,.2f}
- High-Risk Customer Count (Active): {high_risk_count}
- Predicted Revenue at Risk: ${predicted_rev_risk:,.2f}

## Model Evaluation
- Model: Logistic Regression (balanced class weight)
- Chosen Threshold: {threshold} (Prioritizing recall over precision)
- ROC-AUC: {auc:.3f}

### Classification Report (Threshold={threshold}):
```
{report}
```
"""
    with open('docs/final-results.md', 'w') as f:
        f.write(results)
        
    # 5. Generate Jupyter Notebooks templates
    setup = "import os, sys\nos.chdir('..')\nsys.path.append('..')\n"
    create_notebook("notebooks/01_data_quality.ipynb", "Data Quality & Cleaning", "Analyze missing values, whitespace in TotalCharges, and basic types.", setup + "import pandas as pd\nfrom src.data.preprocessing import load_and_clean_data\ndf = load_and_clean_data('data/raw/RAW DATA.xlsx')\ndisplay(df.head())")
    create_notebook("notebooks/02_eda.ipynb", "Exploratory Data Analysis", "Analyze churn by contract, tenure, and services.", setup + "import pandas as pd\nimport matplotlib.pyplot as plt\nfrom src.analytics.churn_analysis import get_overall_churn_rate, analyze_churn_by_dimension\ndf = pd.read_csv('data/processed/cleaned_customer_data.csv')\nprint(get_overall_churn_rate(df))\n\n# Churn by Contract Chart\ncontract_churn = analyze_churn_by_dimension(df, 'Contract')\ndisplay(contract_churn)\ncontract_churn.set_index('Contract')['churn_rate'].plot(kind='bar', color='skyblue', title='Churn Rate by Contract')\nplt.ylabel('Churn Rate')\nplt.show()")
    create_notebook("notebooks/03_customer_segmentation.ipynb", "Customer Segmentation", "Value segments and High Friction analysis.", setup + "import pandas as pd\nfrom src.analytics.segmentation import create_customer_segments, analyze_segment_risk\ndf = pd.read_csv('data/processed/cleaned_customer_data.csv')\ndf_seg = create_customer_segments(df)\ndisplay(analyze_segment_risk(df_seg, 'High_Friction'))")
    create_notebook("notebooks/04_churn_prediction.ipynb", "Churn Prediction Modeling", "Train LR, evaluate Precision/Recall, output metrics.", setup + "import pandas as pd\nimport matplotlib.pyplot as plt\nfrom src.model.churn_classifier import ChurnModel\ndf = pd.read_csv('data/processed/cleaned_customer_data.csv')\nmodel = ChurnModel()\nX_train, X_test, y_train, y_test = model.prepare_data(df)\nmodel.train(X_train, y_train)\nreport, auc = model.evaluate(X_test, y_test, threshold=0.4)\nprint(report)\nprint(f'AUC: {auc}')\n\n# Visualize predicted probabilities\nprobs = model.model.predict_proba(X_test)[:, 1]\nplt.hist(probs, bins=20, color='coral', edgecolor='black')\nplt.axvline(x=0.4, color='red', linestyle='--', label='Threshold=0.4')\nplt.title('Distribution of Churn Probabilities')\nplt.legend()\nplt.show()")
    create_notebook("notebooks/05_model_explainability.ipynb", "Explainability", "Extract LR coefficients to rank top drivers.", setup + "import pandas as pd\nimport matplotlib.pyplot as plt\nfrom src.model.churn_classifier import ChurnModel\ndf = pd.read_csv('data/processed/cleaned_customer_data.csv')\nmodel = ChurnModel()\nX_train, _, y_train, _ = model.prepare_data(df)\nmodel.train(X_train, y_train)\nimportance = model.get_model_coefficients()\ndisplay(importance)\n\n# Top 10 Features Chart\nimportance.head(10).set_index('Feature').plot(kind='barh', color='purple', title='Top Churn Drivers (LR Coefficients)')\nplt.gca().invert_yaxis()\nplt.show()")
    create_notebook("notebooks/06_ai_recommendations.ipynb", "AI Recommendation Engine", "Use Gemini to generate NBA from risk profiles.", setup + "from src.ai.recommendation_engine import RetentionAgent\nagent = RetentionAgent()\nprofile = {'numTechTickets': 4, 'Contract': 'Month-to-month'}\nprint(agent.get_recommendation(profile))")
    
    print("Pipeline executed successfully!")

if __name__ == '__main__':
    run()
