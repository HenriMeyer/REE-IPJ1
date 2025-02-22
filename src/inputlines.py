import random
import os

FILENAME = "inputlines.txt"
HOWOFTEN = 50

def main():
    # Start values [min, max]
    PV_min, PV_max = 180000, 240000
    radiation_min, radiation_max = 1036, 1266.6
    windOnshore_min, windOnshore_max = 60000, 100000
    windOffshore_min, windOffshore_max = 8500, 30000
    fullHourLoadOnshore_min, fullHourLoadOnshore_max = 2700, 3300
    fullHourLoadOffshore_min, fullHourLoadOffshore_max = 4000, 5000
    consumption_min, consumption_max = 557328000, 646198000
    electricCar_min, electricCar_max = 4590000, 10590000
    electricTruck_min, electricTruck_max = 105339, 1431907
    semiTrailerTruck_min, semiTrailerTruck_max = 3936, 30504
    heatPumps_min, heatPumps_max = 1600000, 6000000
    heatPumpsConsumption_min, heatPumpsConsumption_max = 1917, 7933
    pumpCapacity_min, pumpCapacity_max = 45000, 120000
    pumpLoad_min, pumpLoad_max = 9700, 30000
    batteryCapacity_min, batteryCapacity_max = 1924, 145000
    batteryLoad_min, batteryLoad_max = 1500, 25000
    vehicleToGrid = str("yes")


    with open(FILENAME, 'w', encoding='utf-8') as f:
        for i in range(HOWOFTEN):
            szenarioName = f"Random{i}"
            
            # Factor for the random values
            FACTOR = 1

            f.write(
                "owndelete\nvalues\n"
                f"{round(random.uniform(PV_min, PV_max * FACTOR), 2)}\n"
                f"{round(random.uniform(radiation_min, radiation_max), 2)}\n"
                f"{round(random.uniform(windOnshore_min, windOnshore_max * FACTOR), 2)}\n"
                f"{round(random.uniform(windOffshore_min, windOffshore_max * FACTOR), 2)}\n"
                f"{round(random.uniform(fullHourLoadOnshore_min, fullHourLoadOnshore_max), 2)}\n"
                f"{round(random.uniform(fullHourLoadOffshore_min, fullHourLoadOffshore_max), 2)}\n"
                f"{round(random.uniform(consumption_min, consumption_max), 2)}\n"
                f"{round(random.uniform(electricCar_min, electricCar_max * FACTOR), 2)}\n"
                f"{round(random.uniform(electricTruck_min, electricTruck_max * FACTOR), 2)}\n"
                f"{round(random.uniform(semiTrailerTruck_min, semiTrailerTruck_max * FACTOR), 2)}\n"
                f"{round(random.uniform(heatPumps_min, heatPumps_max * FACTOR), 2)}\n"
                f"{round(random.uniform(heatPumpsConsumption_min, heatPumpsConsumption_max), 2)}\n"
                f"{round(random.uniform(pumpCapacity_min, pumpCapacity_max * FACTOR), 2)}\n"
                f"{round(random.uniform(pumpLoad_min, pumpLoad_max * FACTOR), 2)}\n"
                f"{round(random.uniform(batteryCapacity_min, batteryCapacity_max * FACTOR), 2)}\n"
                f"{round(random.uniform(batteryLoad_min, batteryLoad_max * FACTOR), 2)}\n"
                f"{vehicleToGrid}\n{szenarioName}\ny\n"
            )


        f.write("takebest\nvisualize\nall\nquit\n")
        folder = "../output/"
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Directory ({folder}) created")

if __name__ == "__main__":
    main()