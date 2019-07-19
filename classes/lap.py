from json import dumps
from .parseable import Parseable
class Lap(Parseable):
  def __init__(self):
    self.Num: int = -1
    self.Position: int = -1
    self.Et: float = 0.0
    self.S1: float = 0.0
    self.S2: float = 0.0
    self.S3: float = 0.0
    self.Fuel: float = 0.0
    self.TwFl: float = 0.0
    self.TwFr: float = 0.0
    self.TwRl: float = 0.0
    self.TwRr: float = 0.0
    self.FCompound: str = ""
    self.RCompound: str = ""
    self.Duration: float = 0.0
    self.__TRANSLATION__ = {
      "Num": "num",
      "Position": "p",
      "S1": "s1",
      "S2": "s2",
      "S3": "s3",
      "Fuel": "fuel",
      "Et": "et",
      "TwFl": "twfl",
      "TwFr": "twfr",
      "TwRl": "twrl",
      "TwRr": "twrr",
      "FCompound": "fcompound",
      "RCompound": "rcompound"
    }
  def __str__(self):
    return "Lap {0}: P{1} ({2})".format(self.Num, self.Position, self.Duration)