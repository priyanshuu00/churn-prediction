import pandas as pd

def calculate_historical_revenue_lost(df: pd.DataFrame) -> float:
    """Calculates actual Monthly Charges lost from already churned customers."""
    return df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()

def calculate_predicted_revenue_at_risk(df_scored: pd.DataFrame, risk_threshold: float = 0.5) -> float:
    """
    Calculates total MRR for ACTIVE customers whose churn probability exceeds the threshold.
    Requires model probabilities to be present in df_scored.
    """
    active_at_risk = df_scored[(df_scored['Churn'] == 'No') & (df_scored['ChurnProbability'] >= risk_threshold)]
    return active_at_risk['MonthlyCharges'].sum()

def calculate_estimated_revenue_protected(df_scored: pd.DataFrame, risk_threshold: float = 0.5, success_rate: float = 0.2) -> float:
    """
    Scenario Estimate: How much revenue would we save if we retain X% of the high-risk active customers?
    """
    at_risk_revenue = calculate_predicted_revenue_at_risk(df_scored, risk_threshold)
    return at_risk_revenue * success_rate
