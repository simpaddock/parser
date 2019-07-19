
from .parseable import Parseable
from .lap import Lap
from typing import List
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
    self.Pittops: int = 0
    self.FinishStatus: str = ""
    self.__TRANSLATION__ = {
      "LapCount": "Laps",
      "ClassPosition": "ClassPosition"
    }