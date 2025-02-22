import unittest
import csv
import data
import os
import pandas as pd

FILENAME_GEN = "test_gen_tmp.csv"
FILENAME_USE = "test_use_tmp.csv"
FILENAME_LOAD_LEAP = "test_load_leap_tmp.csv"
FILENAME_LOAD_NORMAL = "test_load_normal_tmp.csv"

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Dummy generation csv file
        header = [
            "Datum von", "Datum bis", "Biomasse [MWh] Originalauflösungen", 
            "Wasserkraft [MWh] Originalauflösungen", "Wind Offshore [MWh] Originalauflösungen", 
            "Wind Onshore [MWh] Originalauflösungen", "Photovoltaik [MWh] Originalauflösungen", 
            "Sonstige Erneuerbare [MWh] Originalauflösungen", "Kernenergie [MWh] Originalauflösungen", 
            "Braunkohle [MWh] Originalauflösungen", "Steinkohle [MWh] Originalauflösungen", 
            "Erdgas [MWh] Originalauflösungen", "Pumpspeicher [MWh] Originalauflösungen", 
            "Sonstige Konventionelle [MWh] Originalauflösungen"
        ]
        dataCSV = [
            ["01.01.2025 00:00", "01.01.2025 00:15", 400.1, 300, 500, 600, 450, 200, 700, 800, 600, 500, 300, 250],
            ["01.01.2025 00:15", "01.01.2025 00:30", 420.3, 310, 520, 620, 460, 210, 710, 820, 620, 510, 320, 260],
            ["01.01.2025 00:30", "01.01.2025 00:45", 430.6, 320, 530, 630, 470, 220, 720, 830, 630, 520, 330, 270]
        ]
        with open("../data/" + FILENAME_GEN, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerows(dataCSV)
        
        # Dummy consumption csv file
        header = [
            "Datum von", "Datum bis", "Gesamt (Netzlast) [MWh] Originalauflösungen", 
            "Residuallast [MWh] Originalauflösungen", "Pumpspeicher [MWh] Originalauflösungen"
        ]
        dataCSV = [
            ["01.01.2025 00:00", "01.01.2025 00:15", 1000, 100, 50],
            ["01.01.2025 00:15", "01.01.2025 00:30", 1020, 110, 60],
            ["01.01.2025 00:30", "01.01.2025 00:45", 1030, 120, 70]
        ]
        with open("../data/" + FILENAME_USE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerows(dataCSV)
            
        # Dummy loadprofiles csv file
        header = ["Jahr_von","Zeit_von", "Waermepumpe[in kWh]", "Elektroauto[Tagesnormiert]", "ELKW[Tagesnormiert]"]
        dataCSV = [
            ["01.01.2025", "00:00:00", "0,2", "0,01", "0,1"],
            ["01.01.2025", "00:15:00", "0,1", "0,5", "0,05"],
            ["01.01.2025", "00:30:00", "0,3", "0,3", "0,2"]
        ]
        with open(FILENAME_LOAD_LEAP, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerows(dataCSV)
        
        
        header = ["Jahr_von","Zeit_von", "Waermepumpe[in kWh]", "Elektroauto[Tagesnormiert]", "ELKW[Tagesnormiert]"]
        dataCSV = [
            ["01.01.2025", "00:00:00", "0,3", "0,05", "0,2"],
            ["01.01.2025", "00:15:00", "0,2", "0,1", "0,1"],
            ["01.01.2025", "00:30:00", "0,4", "0,9", "0,4"]
        ]
        with open(FILENAME_LOAD_NORMAL, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerows(dataCSV)
            
        cls.dfList: list[pd.DataFrame] = cls.dfList.append(data.readSMARD(FILENAME_GEN, FILENAME_USE))
        cls.load: dict[str, pd.DataFrame] = data.readLoadProfile(FILENAME_LOAD_LEAP, FILENAME_LOAD_NORMAL)
    
    @classmethod
    def tearDownClass(cls):
        # Delete Dummy csv files
        for filename in ["../data/" + FILENAME_GEN, "../data/" + FILENAME_USE, FILENAME_LOAD_LEAP, FILENAME_LOAD_NORMAL]:
            if os.path.exists(filename):
                os.remove(filename)
        if os.path.exists("../output/test/CSV/2025.csv"):
            os.remove("../output/test/CSV/2025.csv")
        if os.path.exists("../output/test/Excel/Simulation.xlsx"):
            os.remove("../output/test/Excel/Simulation.xlsx")
    
    # data.py
    def test_dataRead(self):
        # Check if the dataframes are not empty
        self.assertFalse(self.dfList.empty)
        self.assertFalse(self.load["leap"].empty)
        self.assertFalse(self.load["normal"].empty)
        
    # def test_writeCSV(self):
    #     # Check if the csv files are written correctly
    #     data.writeCSV(self.dfDict)
    #     self.assertTrue(os.path.exists("../output/test/CSV/2025.csv"))
        
        
    # def test_writeExcel(self):
    #     # Check if the excel files are written correctly
    #     data.writeExcel(self.dfDict)
    #     self.assertTrue(os.path.exists("../output/test/Excel/Simulation.xlsx"))
    # ---------------------------------------------------------------------------
    
    # simulation.py
    
    # ---------------------------------------------------------------------------
    # graphics.py
    
    # ---------------------------------------------------------------------------
        
# Run the tests
if __name__ == "__main__":
    unittest.main()