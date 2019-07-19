from collections import OrderedDict
from classes.sessionresult import SessionResult
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from hashlib import sha256
import random

def getHotLaps(results: List[SessionResult]):
  tracks = OrderedDict()
  for result in results:
    if result.TrackEvent not in tracks:
      tracks[result.TrackEvent] = OrderedDict()
    for driver in result.Drivers:
      hotlapTime = driver.BestLapTime
      if driver.getHash() in tracks[result.TrackEvent]:
        existingHotLap =  tracks[result.TrackEvent][driver.getHash()]["BestLapTime"]
        if existingHotLap > hotlapTime:
           tracks[result.TrackEvent][driver.getHash()]["BestLapTime"] = hotlapTime
        tracks[result.TrackEvent][driver.getHash()]["LapsDone"] = tracks[result.TrackEvent][driver.getHash()]["LapsDone"] + driver.getTimedLaps()
      else:
        tracks[result.TrackEvent][driver.getHash()] = {
          "Name": driver.Name,
          "Vehicle": driver.VehName,
          "BestLapTime": driver.BestLapTime,
          "LapsDone": driver.getTimedLaps()
        }
  return tracks

def calculateGaps(result: SessionResult):
  gaps= OrderedDict()
  for lapCount in range(0, result.MostLapsCompleted ):
    leadingTime = 0.0
    for driver in result.Drivers:
      if  driver.Name not in gaps:
        gaps[driver.Name] = []
      # get the currently leading car
      if lapCount < len(driver.Laps):
        if  driver.Laps[lapCount].Position == 1:
          leadingTime = driver.Laps[lapCount].Et


    for driver in result.Drivers:   
      if lapCount < len(driver.Laps):
        ownTime =  driver.Laps[lapCount].Et
        delta = ownTime - leadingTime
        # negative delta?
        gaps[driver.Name].append(delta)
  
  return gaps

def plotGaps(result: SessionResult):
  gaps = calculateGaps(result)
  for driver in gaps:
    y = gaps[driver]
    x = []
    for i in range(0, len(y) ):
      x.append(i)
    plt.plot(x,y,label=driver,color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)))
  
  plt.xlim(left=0,right=result.MostLapsCompleted -1)
  plt.xticks(np.arange(0, result.MostLapsCompleted , 1.0))
  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  plt.savefig("data/{0}_gaps.png".format(getHash(result.Mod)), bbox_inches='tight')



  



def getPositions(result: SessionResult):
  results = OrderedDict()
  for driver in result.Drivers:
    results[driver.Name] = [driver.ClassGridPos]
    for lap in driver.Laps:
      results[driver.Name].append(lap.Position)
  return results

def plotPositionGraph(result: SessionResult):
  results = getPositions(result)
  yticks = []
  sortedDrivers = sorted(result.Drivers, key=lambda x: x.ClassGridPos, reverse=False)
  for driver in sortedDrivers:
    yticks.append(driver.Name)
  for name in results:
    x = []
    y = results[name]
    for i in range(0, len(y) ):
      x.append(i)
   
    plt.plot(x,y,label=name)
  plt.xlim(left=1,right=result.MostLapsCompleted)
  plt.ylim(bottom=len(result.Drivers), top=0)
  plt.yticks(np.arange(1,len(result.Drivers)  +1),yticks)
  plt.xticks(np.arange(0, result.MostLapsCompleted +1, 1.0))
  plt.savefig("data/{0}_positions.png".format(getHash(result.Mod)), bbox_inches='tight')

def getHash(toHash: str):
  m =  sha256()
  m.update(toHash.encode())
  return m.hexdigest()

