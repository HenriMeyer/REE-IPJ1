
FILENAME = "inputlines.txt"
HOWOFTEN = 5

def main():
    # start values
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

    with open(FILENAME, 'w', encoding='utf-8') as f:
        for i in range(HOWOFTEN):
            szenarioName = "Test" + str(i)
            f.write("own\nvalues\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\nyes\n" + szenarioName + "\ny\n")
        f.write("visualize\nall\nquit\n")
        # f.write("own\nvalues\n")
        # for name in simulationList:
        #     if name == "PV":
        #         for i in range(HOWOFTEN):
                    
        #     if name == "OnShore":
        #         for i in range(HOWOFTEN):
        #     if name == "Offshore":
        #         for i in range(HOWOFTEN):
        #     if name == "Speicher":
        #         for i in range(HOWOFTEN):
        #     else:
        #         print("Error")
        #         break
    
def writeToFile(list: list()) -> str:
    if list:
        stringToWrite = None
        # with open(FILENAME, 'w', encoding='utf-8') as f:
        #     for line in list:
        #         f.write(line)
        return stringToWrite
    else:
        return "quit"

if __name__ == "__main__":
    main()