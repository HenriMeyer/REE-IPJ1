import random
import os

FILENAME = "inputlines.txt"
HOWOFTEN = 100
# Factor for the random values
FACTOR = 1

def main():
    # Start values [min, max]
    PV_min, PV_max = 180000, 240000
    radiation_mid = 1151.5
    windOnshore_min, windOnshore_max = 60000, 115000
    windOffshore_min, windOffshore_max = 8500, 40000
    fullHourLoadOnShore_mid = 3000
    fullHourLoadOffShore_mid = 5000
    consumption_mid = 557328000
    electricCar_mid = 7590000
    electricTruck_mid = 761243
    semiTrailerTruck_mid = 9840
    heatPumps_mid = 5500000
    heatPumpsConsumption_mid = 3514
    pumpCapacity_min, pumpCapacity_max = 45000, 120000
    pumpLoad_min, pumpLoad_max = 9700, 30000
    batteryCapacity_min, batteryCapacity_max = 1924, 232000
    batteryLoad_min, batteryLoad_max = 1500, 40000
    vehicleToGrid = str("yes")


    with open(FILENAME, 'w', encoding='utf-8') as f:
        for i in range(HOWOFTEN):
            szenarioName = f"Random{i}"
            
            # pumpLoad ~ pumpCapacity -> linearise between pumpLoad_min and pumpLoad_max -> same for battery
            pumpCapacity = round(random.uniform(pumpCapacity_min, pumpCapacity_max * FACTOR), 2)
            pumpLoad = round(((pumpCapacity - pumpCapacity_min) / (pumpCapacity_max - pumpCapacity_min)) * (pumpLoad_max - pumpLoad_min) + pumpLoad_min, 2)
            batteryCapacity = round(random.uniform(batteryCapacity_min, batteryCapacity_max * FACTOR), 2)
            batterLoad = round(((batteryCapacity - batteryCapacity_min) / (batteryCapacity_max - batteryCapacity_min)) * (batteryLoad_max - batteryLoad_min) + batteryLoad_min, 2)

            f.write(
                "owndelete\nvalues\n"
                f"{round(random.uniform(PV_min, PV_max * FACTOR), 2)}\n"
                f"{radiation_mid}\n"
                f"{round(random.uniform(windOnshore_min, windOnshore_max * FACTOR), 2)}\n"
                f"{round(random.uniform(windOffshore_min, windOffshore_max * FACTOR), 2)}\n"
                f"{fullHourLoadOnShore_mid}\n"
                f"{fullHourLoadOffShore_mid}\n"
                f"{consumption_mid}\n"
                f"{electricCar_mid}\n"
                f"{electricTruck_mid}\n"
                f"{semiTrailerTruck_mid}\n"
                f"{heatPumps_mid}\n"
                f"{heatPumpsConsumption_mid}\n"
                f"{pumpCapacity}\n"
                f"{pumpLoad}\n"
                f"{batteryCapacity}\n"
                f"{batterLoad}\n"
                f"{vehicleToGrid}\n{szenarioName}\ny\n"
            )


        f.write("takebest\nvisualize\nall\nquit\n")
        folder = "../output/"
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Directory ({folder}) created")

if __name__ == "__main__":
    main()