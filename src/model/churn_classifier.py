import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

class ChurnModel:
    def __init__(self):
        self.categorical_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 
                                 'InternetService', 'Contract', 'PaymentMethod', 'TechSupport']
        self.numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'numTechTickets']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numerical_cols),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), self.categorical_cols)
            ])
            
        self.model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000))
        ])
        self.feature_names = None
    
    def prepare_data(self, df: pd.DataFrame):
        """Splits the raw dataframe into train and test sets."""
        X = df[self.categorical_cols + self.numerical_cols]
        y = df['Churn_Target']
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        
        # Extract feature names after fitting OneHotEncoder
        cat_encoder = self.model.named_steps['preprocessor'].named_transformers_['cat']
        cat_features = cat_encoder.get_feature_names_out(self.categorical_cols)
        self.feature_names = self.numerical_cols + list(cat_features)
        
    def evaluate(self, X_test, y_test, threshold=0.5):
        probs = self.model.predict_proba(X_test)[:, 1]
        preds = (probs >= threshold).astype(int)
        
        report = classification_report(y_test, preds)
        auc = roc_auc_score(y_test, probs)
        
        return report, auc
        
    def get_model_coefficients(self):
        """Returns logistic regression coefficients mapped to feature names."""
        classifier = self.model.named_steps['classifier']
        importance = pd.DataFrame({
            'Feature': self.feature_names,
            'Coefficient': classifier.coef_[0]
        })
        return importance.sort_values(by='Coefficient', ascending=False)
