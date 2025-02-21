import random

FILENAME = "inputlines.txt"
HOWOFTEN = 30

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

    with open(FILENAME, 'w', encoding='utf-8') as f:
        for i in range(0, HOWOFTEN):
            szenarioName = "Random" + str(i)
            
            factorPump = random.uniform(1, 1.5)
            pumpCapacityNew = round(factorPump * pumpCapacity, 2)
            pumpLoadNew = round(factorPump * pumpLoad, 2)
            
            factorBattery = random.uniform(1, 1.5)
            batteryCapactiyNew = round(factorBattery * batteryCapactiy, 2)
            batteryLoadNew = round(factorBattery * batteryLoad, 2)

            f.write(f"owndelete\nvalues\n"
                    f"{round(random.uniform(PV, PV*1.5), 2)}\n"
                    f"{round(random.uniform(radiation, radiation*1.5), 2)}\n"
                    f"{round(random.uniform(windOnshore, windOnshore*1.5), 2)}\n"
                    f"{round(random.uniform(windOffshore, windOffshore*1.5), 2)}\n"
                    f"{round(random.uniform(fullHourLoadOnshore, fullHourLoadOnshore*1.5), 2)}\n"
                    f"{round(random.uniform(fullHourLoadOffshore, fullHourLoadOffshore*1.5), 2)}\n"
                    f"{round(random.uniform(consumption, consumption*1.5), 2)}\n"
                    f"{round(random.uniform(electricCar, electricCar*1.5), 2)}\n"
                    f"{round(random.uniform(electricTruck, electricTruck*1.5), 2)}\n"
                    f"{round(random.uniform(semiTrailerTruck, semiTrailerTruck*1.5), 2)}\n"
                    f"{round(random.uniform(heatPumps, heatPumps*1.5), 2)}\n"
                    f"{round(random.uniform(heatPumpsConsumption, heatPumpsConsumption*1.5), 2)}\n"
                    f"{pumpCapacityNew}\n{pumpLoadNew}\n{batteryCapactiyNew}\n{batteryLoadNew}\n"
                    f"{vehicleToGrid}\n{szenarioName}\ny\n")
    
        f.write("takebest\nvisualize\nall\nquit\n")

if __name__ == "__main__":
    main()