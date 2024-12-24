import os
import time
from urllib.request import Request, urlopen
from lxml import etree
from prometheus_client import start_http_server, Gauge

# Prometheus metrics
total_consumed_metric = Gauge('total_energy_consumed', 'Total energy consumed')
public_grid_metric = Gauge('energy_from_grid', 'Total energy from grid')
solar_panel_metric = Gauge('solar_panel_energy', 'Solar panel energy')
total_excess_metric = Gauge('total_energy_to_grid', 'Total energy exported to grid')

def clear_screen():
    # Clears the terminal screen (works in most environments)
    os.system('clear')  # For Linux/Mac; use 'cls' for Windows if needed

def energy():
    publicGridName = "Total energy from grid"
    upstairsName = "Home"
    downstairsName = "Garage"
    solarPanelName = "Solar panels"
    wallBoxName = "Wallbox"

    totalConsumedName = "Total energy consumed"
    totalExcessName = "Total energy to grid"

    # Sources from the BTicino Energy Data Logger
    sources = {
        publicGridName: 0,
        upstairsName: 1,
        downstairsName: 2,
        solarPanelName: 5,
        wallBoxName: 6,
    }

    try:
        values = {}

        # Clear the screen before printing new data
        clear_screen()

        for (name, index) in sources.items():
            page = urlopen(Request(f"http://192.168.0.6/istval_0{index}00.xml", headers={}))
            page = page.read().decode("utf-8")
            page = etree.XML(page)
            values[name] = int(page[1].text)  # Read and convert to integer

        total_consumed = values[downstairsName] + values[upstairsName] + values[wallBoxName]
        total_excess = values[solarPanelName] - total_consumed

        if total_excess < 0:
            total_excess = 0

        # Print the latest data
        print(f"{totalConsumedName} {total_consumed}")
        print(f"{publicGridName} {values[publicGridName]}")
        print(f"{solarPanelName} {values[solarPanelName]}")
        print(f"{totalExcessName} {total_excess}")

        # Update Prometheus metrics
        total_consumed_metric.set(total_consumed)
        public_grid_metric.set(values[publicGridName])
        solar_panel_metric.set(values[solarPanelName])
        total_excess_metric.set(total_excess)

    except Exception as e:
        print(f"Error in retrieving energy data: {e}")

if __name__ == "__main__":
    # Start the Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Starting energy monitoring script...")
    while True:
        energy()
        time.sleep(60)  # Wait 60 seconds between each run
