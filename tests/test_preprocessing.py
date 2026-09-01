import unittest
import pandas as pd
import numpy as np
from src.data.preprocessing import load_and_clean_data

class TestPreprocessing(unittest.TestCase):
    def test_total_charges_whitespace(self):
        # Create a mock dataframe with whitespace in TotalCharges
        df = pd.DataFrame({
            'customerID': ['1', '2'],
            'tenure': [0, 10],
            'TotalCharges': [' ', '50.5'],
            'SeniorCitizen': [1, 0],
            'Churn': ['No', 'Yes'],
            'numAdminTickets': [0, 0],
            'numTechTickets': [0, 0]
        })
        
        # Save mock to excel
        mock_path = 'mock_data.xlsx'
        df.to_excel(mock_path, index=False)
        
        cleaned = load_and_clean_data(mock_path)
        
        # Check that the whitespace was converted to 0
        self.assertEqual(cleaned.loc[cleaned['customerID'].astype(str) == '1', 'TotalCharges'].values[0], 0.0)
        self.assertEqual(cleaned.loc[cleaned['customerID'].astype(str) == '2', 'TotalCharges'].values[0], 50.5)
        
        import os
        os.remove(mock_path)

if __name__ == '__main__':
    unittest.main()
