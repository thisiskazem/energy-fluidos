#!/usr/bin/python3

from urllib.request import Request, urlopen
from lxml import etree

def energy():
  publicGridName = "Total energy from grid"
  upstairsName = "Home"
  downstairsName = "Garage"
  heatPumpCoolingName =  "Heat pump cooling"
  heatPumpWaterName = "Heat pump water"
  solarPanelName = "Solar panels"
  wallBoxName = "Wallbox"
  burnersName = "Burners"
  owenName = "Owen"

  totalConsumedName = "Total energy consumed"
  totalConsumed = 0
  totalExcessName = "Total energy to grid"
  totalExcess = 0

  # Sources from the BTicino Energy Data Logger
  sources = {
    publicGridName: 0,
    upstairsName: 1,
    downstairsName: 2,
    #heatPumpCoolingName: 3,
    #heatPumpWaterName: 4,
    solarPanelName: 5,
    wallBoxName: 6,
    #burnersName: 7,
    #owenName: 8,
  }

  try:
    values = {}

    for (name, index) in sources.items():
      page = urlopen(Request(f"http://192.168.0.6/istval_0{index}00.xml", headers={}))
      page = page.read().decode("utf-8")
      page = etree.XML(page)
      values[name] = int(page[1].text) #/ 1000
      #print(f"{name} {values[name]}")

    totalConsumed = values[downstairsName] + values[upstairsName] + values[wallBoxName]
    totalExcess = values[solarPanelName] - totalConsumed

    if  (totalExcess < 0) :
      totalExcess = 0

    print(f"{totalConsumedName} {totalConsumed}")
    print(f"{publicGridName} {values[publicGridName]}")
    print(f"{solarPanelName} {values[solarPanelName]}")
    print(f"{totalExcessName} {totalExcess}")

    return

  except Exception as e:
    print(f"Error in retrieving energy data: {e}")
    return

if __name__ == "__main__":
  energy()
