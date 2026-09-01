import pandas as pd
import numpy as np

def create_customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Creates meaningful customer segments based on available features."""
    df_seg = df.copy()
    
    # Value Segments based on MonthlyCharges
    median_charges = df_seg['MonthlyCharges'].median()
    df_seg['Value_Segment'] = np.where(df_seg['MonthlyCharges'] > median_charges, 'High Value', 'Low Value')
    
    # Friction Segment: M2M + High Tech Tickets
    df_seg['High_Friction'] = (df_seg['Contract'] == 'Month-to-month') & (df_seg['numTechTickets'] >= 3)
    
    # Tenure Cohorts
    df_seg['Tenure_Cohort'] = pd.cut(
        df_seg['tenure'], 
        bins=[-1, 12, 36, 60, 100], 
        labels=['New (0-12m)', 'Mid (13-36m)', 'Established (37-60m)', 'Loyal (60m+)']
    )
    return df_seg

def analyze_segment_risk(df_seg: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    grouped = df_seg.groupby(segment_col).agg(
        total_customers=('customerID', 'count'),
        churned_customers=('Churn', lambda x: (x == 'Yes').sum()),
        avg_monthly_charges=('MonthlyCharges', 'mean')
    )
    grouped['churn_rate'] = grouped['churned_customers'] / grouped['total_customers']
    return grouped.reset_index()
