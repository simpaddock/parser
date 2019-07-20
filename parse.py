from classes.driver import Driver
from classes.lap import Lap
from classes.sessionresult import SessionResult
from classes.event import Event

from classes.parseable import Parseable
from xml.etree import ElementTree as ET
from typing import List
from pathlib import Path
from nameparser import HumanName

def parseXML(xmlPath: str) -> SessionResult:
  from xml.etree import ElementTree as ET
  tree = ET.parse(xmlPath)
  root = tree.getroot()
  result: SessionResult = SessionResult()
  result.Session = "Practise1"
  result.FileName = xmlPath
  sessionKeys = ["Race", "Practise1", "Qualify"]
  for session in sessionKeys:
    if len(root.findall('.//' + session)) == 1:
      result.Session = session
      break
  parseObject(result, root, True)
  for driverNode in root.findall('.//Driver'):
    driver = Driver()
    parseObject(driver, driverNode, False)
    for lapNode in driverNode.findall('.//Lap'):
      lap = Lap() 
      parseObject(lap, lapNode, False)
      lap.Duration = lap.S1 + lap.S2 + lap.S3
      driver.Laps.append(lap)
    humanName = HumanName(driver.Name)
    if len(humanName.last) > 0:
      driver.Name  = humanName.first + " " + humanName.last[0]
    result.Drivers.append(driver)
  for raw in root.findall('.//Stream/Chat') + root.findall('.//Stream/Command') + root.findall('.//Stream/Sector') + root.findall('.//Stream/Incident'):
    e = Event()
    e.Et = raw.attrib.get("et")
    e.Type = raw.tag
    e.Text = raw.text
    result.Stream.append(e)
  result.Name = Path(xmlPath).name.replace(".xml","")
  result.Drivers = sorted(result.Drivers, key= lambda d:d.ClassPosition)
  return result

def parseObject(source: Parseable, rootNode, useFirst: bool):
  for propKey in dir(source):
    if "__" not in propKey and "__TRANSLATION__" != propKey:
      keyToSearch = source.__TRANSLATION__[propKey] if propKey in source.__TRANSLATION__  else propKey
      # try to search for child notes matching
      transferTagText(rootNode,'.//'+keyToSearch,source,propKey, useFirst)
      # try to search for attributes
      for attributeKey, attributeValue in rootNode.attrib.items():
        if propKey in source.__TRANSLATION__ and source.__TRANSLATION__[propKey] == attributeKey:
          setValue(source, propKey, attributeValue)

def setValue(source, propKey, newValue):
  initValue = getattr(source, propKey)
  newParsedValue = newValue.strip()
  if type(initValue) is float:
    newParsedValue = float(newValue.replace(",",".").replace("--.---","0.0"))
  if type(initValue) is str:
    newParsedValue = str(newValue.strip())
  if type(initValue) is int:
    newParsedValue = int(newValue)
  if type(initValue) is type(newParsedValue):
    setattr(source, propKey, newParsedValue)

def transferTagText(rootNode, xPath: str, targetObject: Parseable, targetProperty: str, useFirst: bool):
  results = rootNode.findall(xPath)
  if len(results) == 1:
    setValue(targetObject, targetProperty, rootNode.findall(xPath)[0].text)
  if len(results) > 1:
    if not useFirst:
      raise Exception("Unclear matches: " + targetProperty + " matches: " + str(len(results)))
    else:
      setValue(targetObject, targetProperty, rootNode.findall(xPath)[0].text)
