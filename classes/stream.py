from typing import List
from .driver import Driver
from .parseable import Parseable
from .event import Event
class Stream(Parseable):
  def __init__(self):
    self.Events  = List[Event]
