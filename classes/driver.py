
from .parseable import Parseable
from .lap import Lap
from typing import List
from hashlib import sha256
import math
import numpy as np
class Driver(Parseable):
  def __init__(self):
    self.Name = ""
    self.VehName = ""
    self.Category = ""
    self.CarType = ""
    self.CarClass = ""
    self.CarNumber: str = ""
    self.TeamName = ""
    self.Position: int = -1
    self.ClassPosition: int = -1
    self.LapRankIncludingDiscos: int = -1
    self.BestLapTime: float = 0.0
    self.Laps: List[Lap] = []
    self.LapCount: int = -1
    self.Pitstops: int = 0
    self.ClassGridPos: int = 0
    self.FinishStatus: str = ""
    self.__TRANSLATION__ = {
      "LapCount": "Laps",
      "ClassPosition": "ClassPosition"
    }
  def getHash(self):
    m =  sha256()
    m.update(self.Name.encode())
    m.update(self.VehName.encode())
    return m.hexdigest()
  def getTimedLaps(self):
    return len(list(filter(lambda l: l.isTimed(),self.Laps)))
  def getStandardDeviation(self):
    times = []
    firstLap = True
    for lap in self.Laps:
      if firstLap:
        firstLap = False
      else:
        times.append(lap.Duration)
    
    average = np.median(times)

    variance = 0

    for lap in self.Laps:
      variance = variance + pow(lap.Duration - average,2)
    
    variance = variance / (self.LapCount -1) # first lap is ignored

    return math.sqrt(variance)

