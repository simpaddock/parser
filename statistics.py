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
    if result.getHash() not in tracks:
      tracks[result.getHash()] = OrderedDict()
    for driver in result.Drivers:
      hotlapTime = driver.BestLapTime
      if driver.getHash() in tracks[result.getHash()]:
        existingHotLap =  tracks[result.getHash()][driver.getHash()]["BestLapTime"]
        if existingHotLap > hotlapTime:
           tracks[result.getHash()][driver.getHash()]["BestLapTime"] = hotlapTime
        tracks[result.getHash()][driver.getHash()]["LapsDone"] = tracks[result.getHash()][driver.getHash()]["LapsDone"] + driver.getTimedLaps()
      else:
        tracks[result.getHash()][driver.getHash()] = {
          "Name": driver.Name,
          "Vehicle": driver.VehName,
          "CarType": driver.CarType,
          "BestLapTime": driver.BestLapTime,
          "LapsDone": driver.getTimedLaps(),
          "Track": result.TrackEvent
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
  
  plt.clf()
  plt.cla()
  plt.close()
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
  plt.savefig("data/{0}{1}_gaps.png".format(result.getHash(),result.DateTime), bbox_inches='tight')



  



def getPositions(result: SessionResult):
  results = OrderedDict()
  for driver in result.Drivers:
    results[driver.Name] = [driver.ClassGridPos]
    for lap in driver.Laps:
      results[driver.Name].append(lap.Position)
  return results

def plotPositionGraph(result: SessionResult):
  
  plt.clf()
  plt.cla()
  plt.close()
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
  plt.savefig("data/{0}{1}_positions.png".format(result.getHash(),result.DateTime), bbox_inches='tight')

def plotStandardDeviation(result:SessionResult):
  x = []
  y = []
  for driver in result.Drivers:
    x.append(driver.Name)
    y.append(driver.getStandardDeviation())

  
  plt.clf()
  plt.cla()
  plt.close()
    
  objects = x
  y_pos = np.arange(len(x))
  performance = [10,8,6,4,2,1]

  plt.bar(y_pos, y, align='center', alpha=0.5)
  plt.xticks(y_pos, x)
  plt.ylabel('Deviation in seconds')
  plt.xticks(rotation=90)
  plt.savefig("data/{0}_deviations.png".format(result.getHash()), bbox_inches='tight')



