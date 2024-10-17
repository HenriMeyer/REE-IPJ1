import unittest
import pandas as pd
from io import StringIO
from data import row_renewable_sum, row_total_sum, row_residual_sum, total_renewable_sum, total_sum, total_portion_renewable_sum


# Füge hier dein Skript ein, z.B. die read_SMARD-Funktion und andere Funktionen
# (Für den Test verwenden wir einen DataFrame direkt)

# Simulierter CSV-Text, den wir für Tests verwenden
mock_csv = """Datum von;Datum bis;Biomasse [MWh] Originalauflösungen;Wasserkraft [MWh] Originalauflösungen;Wind Offshore [MWh] Originalauflösungen;Wind Onshore [MWh] Originalauflösungen;Photovoltaik [MWh] Originalauflösungen;Sonstige Erneuerbare [MWh] Originalauflösungen;Pumpspeicher [MWh] Originalauflösungen;Sonstige Konventionelle [MWh] Originalauflösungen
05.10.2024 00:00;05.10.2024 00:15;100;150;200;300;50;10;5;20
05.10.2024 00:15;05.10.2024 00:30;110;160;210;310;55;11;6;21
"""

# Testklasse
class TestSMARD(unittest.TestCase):

    def setUp(self):
        # Wir simulieren das Einlesen der Datei mit einem StringIO
        self.df = pd.read_csv(
            StringIO(mock_csv),
            sep=';',
            decimal=',',
            parse_dates=[0, 1],
            dayfirst=True
        )
        
        # Spalten umbenennen, wie in der read_SMARD-Funktion
        self.df = self.df.rename(
            columns={
                'Biomasse [MWh] Originalauflösungen': 'Biomasse',
                'Wasserkraft [MWh] Originalauflösungen': 'Wasserkraft',
                'Wind Offshore [MWh] Originalauflösungen': 'Wind Offshore',
                'Wind Onshore [MWh] Originalauflösungen': 'Wind Onshore',
                'Photovoltaik [MWh] Originalauflösungen': 'Photovoltaik',
                'Sonstige Erneuerbare [MWh] Originalauflösungen': 'Sonstige Erneuerbare',
                'Pumpspeicher [MWh] Originalauflösungen': 'Pumpspeicher',
                'Sonstige Konventionelle [MWh] Originalauflösungen': 'Sonstige Konventionelle'
            }
        )

    # Test für die row_renewable_sum-Funktion
    def test_row_renewable_sum(self):
        result = row_renewable_sum(self.df, 0)
        expected = 100 + 150 + 200 + 300 + 50 + 10 + 5  # Summe der erneuerbaren Energien in Zeile 0
        self.assertEqual(result, expected)

    # Test für die row_total_sum-Funktion
    def test_row_total_sum(self):
        result = row_total_sum(self.df, 0)
        expected = 100 + 150 + 200 + 300 + 50 + 10 + 5 + 20  # Gesamtsumme in Zeile 0
        self.assertEqual(result, expected)

    # Test für die row_residual_sum-Funktion
    def test_row_residual_sum(self):
        result = row_residual_sum(self.df, 0)
        renewable_sum = 100 + 150 + 200 + 300 + 50 + 10 + 5  # Summe der erneuerbaren Energien
        total_sum = 100 + 150 + 200 + 300 + 50 + 10 + 5 + 20  # Gesamtsumme
        expected = total_sum - renewable_sum  # Residuallast = Gesamtsumme - Erneuerbare
        self.assertEqual(result, expected)

    # Test für die total_renewable_sum-Funktion
    def test_total_renewable_sum(self):
        result = total_renewable_sum(self.df)
        expected = (100 + 150 + 200 + 300 + 50 + 10 + 5) + (110 + 160 + 210 + 310 + 55 + 11 + 6)  # Summe aller erneuerbaren Energien
        self.assertEqual(result, expected)

    # Test für die total_sum-Funktion
    def test_total_sum(self):
        result = total_sum(self.df)
        expected = (100 + 150 + 200 + 300 + 50 + 10 + 5 + 20) + (110 + 160 + 210 + 310 + 55 + 11 + 6 + 21)  # Gesamtsumme aller Zeilen
        self.assertEqual(result, expected)

    # Test für die total_portion_renewable_sum-Funktion
    def test_total_portion_renewable_sum(self):
        renewable_sum = total_renewable_sum(self.df)
        total = total_sum(self.df)
        expected = renewable_sum / total  # Anteil erneuerbare an der Gesamtsumme
        result = total_portion_renewable_sum(self.df)
        self.assertAlmostEqual(result, expected, places=5)

if __name__ == "__main__":
    unittest.main()
