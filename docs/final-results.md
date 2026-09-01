# Final Pipeline Results

## Business Analysis
- Total Customers: 7043
- Churn Rate: 26.54%
- Historical Revenue Lost: $139,130.85
- High-Risk Customer Count (Active): 1330
- Monthly Revenue Exposure from High-Risk Customers: $83,429.70

## Model Evaluation
- Model: Logistic Regression (balanced class weight)
- Chosen Threshold: 0.4 (Prioritizing recall over precision)
- ROC-AUC: 0.925

### Classification Report (Threshold=0.4):
```
              precision    recall  f1-score   support

           0       0.97      0.75      0.84      1035
           1       0.57      0.93      0.71       374

    accuracy                           0.80      1409
   macro avg       0.77      0.84      0.78      1409
weighted avg       0.86      0.80      0.81      1409

```
