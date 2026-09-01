import pytest
import pandas as pd
import numpy as np
import os

def test_risk_tier_logic():
    # Test the risk tier boundaries directly
    probs = np.array([0.1, 0.39, 0.4, 0.69, 0.7, 0.9])
    threshold = 0.4
    
    tiers = np.where(probs >= 0.7, 'Critical',
            np.where(probs >= threshold, 'High', 'Low'))
            
    assert tiers[0] == 'Low'
    assert tiers[1] == 'Low'
    assert tiers[2] == 'High'
    assert tiers[3] == 'High'
    assert tiers[4] == 'Critical'
    assert tiers[5] == 'Critical'

def test_pipeline_integration_output():
    # Verify that the actual generated dashboard feed meets product requirements
    feed_path = 'data/processed/tableau_dashboard_feed.csv'
    
    # Only run this test if the pipeline has been executed
    if not os.path.exists(feed_path):
        pytest.skip(f"Dashboard feed not found at {feed_path}. Run build_project.py first.")
        
    df = pd.read_csv(feed_path)
    
    # 1. High/Critical Risk must have NBA and TopRiskDriver
    high_risk_mask = df['RiskTier'].isin(['High', 'Critical'])
    high_risk = df[high_risk_mask]
    
    assert (high_risk['TopRiskDriver1'] != 'N/A').all()
    assert (high_risk['NextBestAction'] != 'N/A').all()
    
    # 2. Low Risk must have NaN (read as N/A in string form) for NBA and TopRiskDriver
    low_risk = df[~high_risk_mask]
    assert low_risk['TopRiskDriver1'].isna().all()
    assert low_risk['NextBestAction'].isna().all()
    
    # 3. Recommendations must be from approved list
    approved_interventions = [
        "Proactive Tech Support Outreach",
        "Contract Upgrade Incentive",
        "Payment Method Assistance",
        "Free 1-month Security Upgrade",
        "VIP Loyalty Check-in",
        "N/A"
    ]
    
    invalid_actions = df[df['NextBestAction'].notna() & ~df['NextBestAction'].isin(approved_interventions)]
    assert len(invalid_actions) == 0, f"Found invalid recommended actions: {invalid_actions['NextBestAction'].unique()}"
