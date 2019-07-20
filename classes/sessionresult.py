from typing import List
from .driver import Driver
from .parseable import Parseable
from .event import Event
from hashlib import sha256
class SessionResult(Parseable):
  def __init__(self):
    self.TrackEvent: str = ""
    self.RaceLaps: int = -1
    self.RaceTime: float = 0.0
    self.Drivers: List[Driver] = []
    self.Stream: List[Event] = []
    self.MostLapsCompleted: int = -1
    self.Minutes: float = 0.0
    self.LapCount: int = -1
    self.ServerName: str = ""
    self.DamageMult: float = 0.0
    self.FuelMult: float = 0.0
    self.TireMult: float = 0.0
    self.GameVersion: str = ""
    self.TrackLength: float = 0.0
    self.Session: str = ""
    self.VehiclesAllowed: List[str] = []
    self.Mod: str = ""
    self.HadFormationLap: bool = False
    self.DateTime: str = ""
    self.__TRANSLATION__ = {
      "Laps": "LapCount"
    }
  def getHash(self):
    m =  sha256()
    m.update(str(self.Mod+ self.DateTime).encode())
    return m.hexdigest()
