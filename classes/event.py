from typing import List
from .driver import Driver
from .parseable import Parseable
class Event(Parseable):
  def __init__(self):
    self.Text : str = ""
    self.Et: float = 0.0
    self.Type: str = ""
    self.__TRANSLATION__ = {
      "Et": "et"
    }
