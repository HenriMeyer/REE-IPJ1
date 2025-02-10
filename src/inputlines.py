FILENAME = "inputlines.txt"
HOWOFTEN = 5

def main():
    # start values
    PV = 215000
    radiation = 1151.5
    windOnshore = 115000
    windOffshore = 40000
    fullHourLoadOnshore = 3000
    fullHourLoadOffshore = 5000
    consumption = 557328000
    electricCar = 7590000
    electricTruck = 761243
    semiTrailerTruck = 9840
    heatPumps = 5500000
    heatPumpsConsumption = 3514
    pumpCapacity = 120000
    pumpLoad = 30000
    batteryCapactiy = 200000
    batteryLoad = 34483
    vehicleToGrid: str = "yes"
    # "PV", "OnShore", "Offshore",
    simulationList = ["Speicher"]

    with open(FILENAME, 'w', encoding='utf-8') as f:
        # for i in range(HOWOFTEN):
        #     szenarioName = "Test" + str(i)
        #     f.write("own\nvalues\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\n100000\nyes\n" + szenarioName + "\ny\n")
        for name in simulationList:
            # if name == "PV":
            #     for i in range(1, HOWOFTEN):
            #         f.write(writeToFile(...))
            # if name == "OnShore":
            #    for i in range(1, HOWOFTEN):
            # if name == "Offshore":
            #    for i in range(1, HOWOFTEN):
            if name == "Speicher":
                for i in range(5, HOWOFTEN + 4):
                    szenarioName = name + str(i)
                    f.write(f"owndelete\nvalues\n{PV}\n{radiation}\n{windOnshore}\n{windOffshore}\n{fullHourLoadOnshore}\n{fullHourLoadOffshore}\n{consumption}\n{electricCar}\n{electricTruck}\n{semiTrailerTruck}\n{heatPumps}\n{heatPumpsConsumption}\n{round((1 + i / 10) * pumpCapacity, 2)}\n{round((1 + i / 10) * pumpLoad, 2)}\n{round((1 + i / 10) * batteryCapactiy, 2)}\n{round((1 + i / 10) * batteryLoad, 2)}\n{vehicleToGrid}\n" + szenarioName + "\ny\n")
                    # f.write(String + writeToFile([pumpCapacity, pumpLoad, batteryCapactiy, batteryLoad]))
                f.write("visualize\nall\nquit\n")
            else:
                print("Error!")
                break
    
# def writeToFile(list: list(), int factor) -> str:
#     if list:
#         stringToWrite = "own\nvalues\n"
#             for line in list:
#                 f.write(line)
#         return stringToWrite
#     else:
#         return "quit"

if __name__ == "__main__":
    main()