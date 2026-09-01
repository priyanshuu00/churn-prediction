import pandas as pd
import numpy as np

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Loads raw Excel data and cleans whitespace issues."""
    df = pd.read_excel(file_path)
    
    # Clean whitespace in TotalCharges caused by tenure=0
    df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # For tenure=0, TotalCharges should technically be 0
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # Convert SeniorCitizen to string category for consistency with other booleans
    df['SeniorCitizen'] = df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})
    
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts analytical features for the ML model."""
    df_engineered = df.copy()
    
    # Encode Target
    df_engineered['Churn_Target'] = df_engineered['Churn'].map({'Yes': 1, 'No': 0})
    
    # Group tenure into cohorts
    df_engineered['Tenure_Cohort'] = pd.cut(
        df_engineered['tenure'], 
        bins=[-1, 12, 36, 60, 100], 
        labels=['New (0-12m)', 'Mid (13-36m)', 'Established (37-60m)', 'Loyal (60m+)']
    )
    
    # Combine ticket activity
    df_engineered['Total_Tickets'] = df_engineered['numAdminTickets'] + df_engineered['numTechTickets']
    
    return df_engineered
