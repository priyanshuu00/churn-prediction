import pandas as pd

def get_overall_churn_rate(df: pd.DataFrame) -> dict:
    total = len(df)
    churned = len(df[df['Churn'] == 'Yes'])
    return {
        'total_customers': total,
        'churned_customers': churned,
        'churn_rate': churned / total if total > 0 else 0
    }

def analyze_churn_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Returns churn rate grouped by a specific categorical dimension."""
    grouped = df.groupby(dimension).agg(
        total_customers=('customerID', 'count'),
        churned_customers=('Churn', lambda x: (x == 'Yes').sum())
    )
    grouped['churn_rate'] = grouped['churned_customers'] / grouped['total_customers']
    return grouped.reset_index().sort_values('churn_rate', ascending=False)
