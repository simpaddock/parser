from classes.driver import Driver
from classes.lap import Lap
from classes.sessionresult import SessionResult
from classes.event import Event

from classes.parseable import Parseable
from xml.etree import ElementTree as ET
from typing import List

def parseXML(xmlPath: str) -> SessionResult:
  from xml.etree import ElementTree as ET
  tree = ET.parse(xmlPath)
  root = tree.getroot()
  result: SessionResult = SessionResult()
  parseObject(result, root)
  for driverNode in root.findall('.//Driver'):
    driver = Driver()
    parseObject(driver, driverNode)
    for lapNode in driverNode.findall('.//Lap'):
      lap = Lap() 
      parseObject(lap, lapNode)
      lap.Duration = lap.S1 + lap.S2 + lap.S3
      driver.Laps.append(lap)
    result.Drivers.append(driver)
  
  for raw in root.findall('.//Stream/Chat') + root.findall('.//Stream/Command') + root.findall('.//Stream/Sector'):
    e = Event()
    e.Type = raw.tag
    e.Text = raw.text
    result.Stream.append(e)
  return result

def parseObject(source: Parseable, rootNode):
  for propKey in dir(source):
    if "__" not in propKey and "__TRANSLATION__" != propKey:
      keyToSearch = source.__TRANSLATION__[propKey] if propKey in source.__TRANSLATION__  else propKey
      # try to search for child notes matching
      transferTagText(rootNode,'.//'+keyToSearch,source,propKey)
      # try to search for attributes
      for attributeKey, attributeValue in rootNode.attrib.items():
        if propKey in source.__TRANSLATION__ and source.__TRANSLATION__[propKey] == attributeKey:
          setValue(source, propKey, attributeValue)

def setValue(source, propKey, newValue):
  initValue = getattr(source, propKey)
  newParsedValue = newValue
  if type(initValue) is float:
    newParsedValue = float(newValue.replace(",",".").replace("--.---","0.0"))
  if type(initValue) is str:
    newParsedValue = str(newValue)
  if type(initValue) is int:
    newParsedValue = int(newValue)
  if type(initValue) is type(newParsedValue):
    setattr(source, propKey, newParsedValue)



def transferTagText(rootNode, xPath: str, targetObject: Parseable, targetProperty: str):
  results = rootNode.findall(xPath)
  if len(results) == 1:
    setValue(targetObject, targetProperty, rootNode.findall(xPath)[0].text)
  if len(results) > 1:
    raise Exception("Unclear matches: " + targetProperty + " matches: " + str(len(results)))