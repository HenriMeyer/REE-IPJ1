import os

filename: str = "inputlines.txt"

def main():
    PV = 0
    radiation = 0
    windOnshore = 0
    windOffshore = 0
    fullHourLoadOnshore = 0
    fullHourLoadOffshore = 0
    consumption = 0
    electricCar = 0
    vehicleToGrid: str = "yes"
    electricTruck = 0
    semiTrailerTruck = 0
    heatPumps = 0
    heatPumpsConsumption = 0
    pumpCapacity = 0
    pumpLoad = 0
    batteryCapactiy = 0
    batteryLoad = 0
    
    simulationList = ["PV", "OnShore", "Offshore", "Speicher"]
    

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("own\nvalues\n")
        # for name in simulationList:
        #     if name == "PV":
                
        #     if name == "OnShore":
                
        #     if name == "Offshore":
                
        #     if name == "Speicher":
                
        #     else:
        #         print("Error")
        #         break
    
    
    
    
    
if __name__ == "__main__":
    main()