import pytest
import pandas as pd
import numpy as np
from src.model.churn_classifier import ChurnModel

@pytest.fixture
def sample_data():
    df = pd.DataFrame({
        'gender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female'],
        'SeniorCitizen': ['No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'Partner': ['Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes'],
        'Dependents': ['No', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'No'],
        'InternetService': ['DSL', 'Fiber optic', 'No', 'DSL', 'Fiber optic', 'Fiber optic', 'DSL', 'No', 'Fiber optic', 'DSL'],
        'Contract': ['Month-to-month', 'One year', 'Two year', 'Month-to-month', 'Two year', 'Month-to-month', 'One year', 'Two year', 'Month-to-month', 'Two year'],
        'PaymentMethod': ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)'],
        'TechSupport': ['No', 'No', 'No internet service', 'Yes', 'Yes', 'No', 'Yes', 'No internet service', 'No', 'Yes'],
        'tenure': [1, 34, 2, 45, 8, 12, 50, 72, 3, 24],
        'MonthlyCharges': [29.85, 56.95, 53.85, 42.30, 70.70, 85.00, 45.00, 20.00, 95.00, 60.00],
        'TotalCharges': [29.85, 1889.50, 108.15, 1840.75, 151.65, 1020.00, 2250.00, 1440.00, 285.00, 1440.00],
        'numTechTickets': [0, 1, 0, 2, 0, 3, 0, 0, 4, 1],
        'Churn_Target': [1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    })
    return df

def test_churn_model_training(sample_data):
    model = ChurnModel()
    X_train, X_test, y_train, y_test = model.prepare_data(sample_data)
    
    assert len(X_train) == 8
    assert len(X_test) == 2
    
    model.train(X_train, y_train)
    assert model.feature_names is not None
    assert len(model.feature_names) > len(model.numerical_cols)

def test_churn_model_prediction_and_range(sample_data):
    model = ChurnModel()
    X_train, X_test, y_train, y_test = model.prepare_data(sample_data)
    model.train(X_train, y_train)
    
    report, auc = model.evaluate(X_test, y_test, threshold=0.4)
    assert isinstance(report, str)
    
    probs = model.model.predict_proba(X_test)[:, 1]
    assert np.all((probs >= 0.0) & (probs <= 1.0))

def test_model_coefficients(sample_data):
    model = ChurnModel()
    X_train, _, y_train, _ = model.prepare_data(sample_data)
    model.train(X_train, y_train)
    
    coeffs = model.get_model_coefficients()
    assert 'Feature' in coeffs.columns
    assert 'Coefficient' in coeffs.columns
    assert len(coeffs) == len(model.feature_names)

def test_unknown_categorical_handling(sample_data):
    model = ChurnModel()
    X_train, _, y_train, _ = model.prepare_data(sample_data)
    model.train(X_train, y_train)
    
    # Create unseen category data
    unseen_df = sample_data.iloc[[0]].copy()
    unseen_df['Contract'] = 'Three year'
    unseen_df['PaymentMethod'] = 'Bitcoin'
    
    # Predict should not crash thanks to handle_unknown='ignore'
    X_unseen = unseen_df[model.categorical_cols + model.numerical_cols]
    probs = model.model.predict_proba(X_unseen)[:, 1]
    assert len(probs) == 1
