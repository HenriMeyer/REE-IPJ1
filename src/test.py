import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from data import read_SMARD, formatTime, addDataInformation, addPercantageRenewable, countPercentageRenewable, countPercentageRenewableExclude, sumTotal

class TestSMARDFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a sample DataFrame for testing."""
        data = {
            'Datum von': pd.to_datetime(['2021-01-01 00:00', '2021-01-01 00:15']),
            'Datum bis': pd.to_datetime(['2021-01-01 00:15', '2021-01-01 00:30']),
            'Biomasse': [50, 55],
            'Wasserkraft': [30, 35],
            'Wind Offshore': [100, 105],
            'Wind Onshore': [80, 85],
            'Photovoltaik': [40, 45],
            'Sonstige Erneuerbare': [20, 25],
            'Kernenergie': [200, 210],
            'Braunkohle': [150, 160],
            'Steinkohle': [100, 110],
            'Erdgas': [80, 85],
            'Pumpspeicher': [60, 65],
            'Sonstige Konventionelle': [30, 35]
        }
        self.df = pd.DataFrame(data)

    def test_formatTime(self):
        """Test if time formatting works correctly."""
        df_formatted = formatTime(self.df.copy())
        self.assertIn('Jahr', df_formatted.columns)
        self.assertIn('Monat', df_formatted.columns)
        self.assertIn('Tag', df_formatted.columns)
        self.assertIn('Uhrzeit', df_formatted.columns)
        self.assertIn('Monat Tag', df_formatted.columns)
        self.assertNotIn('Datum von', df_formatted.columns)
        self.assertNotIn('Datum bis', df_formatted.columns)

    def test_addDataInformation(self):
        """Test if renewable, total, and residual columns are calculated correctly."""
        df_with_info = addDataInformation(self.df.copy())
        expected_renewable = [380, 415]  # Sum of all renewables
        expected_total = [940, 1015]  # Sum of all columns except Datum columns
        expected_residual = [560, 600]  # Total - Renewable

        self.assertListEqual(df_with_info['Erneuerbar'].tolist(), expected_renewable)
        self.assertListEqual(df_with_info['Total'].tolist(), expected_total)
        self.assertListEqual(df_with_info['Residual'].tolist(), expected_residual)

    def test_addPercantageRenewable(self):
        """Test if renewable percentage is calculated correctly."""
        df_with_info = addDataInformation(self.df.copy())
        df_with_percentage = addPercantageRenewable(df_with_info)
        
        expected_percentage = [(380 / 940) * 100, (415 / 1015) * 100]
        self.assertAlmostEqual(df_with_percentage['Anteil Erneuerbar [%]'].iloc[0], round(expected_percentage[0], 2))
        self.assertAlmostEqual(df_with_percentage['Anteil Erneuerbar [%]'].iloc[1], round(expected_percentage[1], 2))

        def test_countPercentageRenewable(self):
            """Test if renewable percentage counts are calculated correctly."""
            df_with_info = addDataInformation(self.df.copy())
            df_with_percentage = addPercantageRenewable(df_with_info)
            percentage_count = countPercentageRenewable(df_with_percentage)
            
            # Hier die erwartete Erneuerbare Energien Anteil festlegen
            # (ca. 40% in den Beispieldaten)
            self.assertGreaterEqual(percentage_count[4], 2)  # Beide Zeilen haben ca. 40 %
            self.assertEqual(percentage_count[10], 0)  # Keine Zeile über 90%

    def test_countPercentageRenewableExclude(self):
        """Test if renewable percentage counts are calculated correctly excluding already counted ranges."""
        df_with_info = addDataInformation(self.df.copy())
        df_with_percentage = addPercantageRenewable(df_with_info)
        percentage_count = countPercentageRenewableExclude(df_with_percentage)
        
        # For the given test data, both rows have a renewable percentage around 40%
        self.assertEqual(percentage_count[4], 2)  # Both rows between 40-50%
        self.assertEqual(percentage_count[10], 0)  # No rows in the 90-100% range

    def test_sumTotal_generation(self):
        """Test if total sum calculation works for generation data."""
        df_with_info = addDataInformation(self.df.copy())
        total_sum = sumTotal(df_with_info)
        self.assertEqual(total_sum, df_with_info['Total'].sum())

    def test_sumTotal_consumption(self):
        """Test if total sum calculation works for consumption data."""
        # Add a sample consumption column for testing
        self.df['Gesamt'] = [500, 600]
        total_sum = sumTotal(self.df, generation=False)
        self.assertEqual(total_sum, sum([500, 600]))

if __name__ == '__main__':
    unittest.main()
