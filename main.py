from parse import parseXML
from classes.driver import Driver
from classes.sessionresult import SessionResult
from typing import List
from jsonpickle import dumps
from statistics import getHotLaps, getPositions, plotPositionGraph,calculateGaps, plotGaps, plotStandardDeviation
from collections import OrderedDict
import datetime
from os import listdir
import argparse

parser = argparse.ArgumentParser(description='Poor man\'s rf2 logfile parser')
parser.add_argument('source', metavar='src', type=str, help='Source path to find rf2 logfiles')
parser.add_argument('target', metavar='target', type=str, help='Target path for generated files')
args = parser.parse_args()

def renderTemplate(data: object, templateName: str, targetPath: str):
  template = templateEnv.get_template(templateName)
  output = template.render(data)
  with open(targetPath, 'w') as f:
    f.write(output)


from jinja2 import Environment, FileSystemLoader
from os.path import join
fileLoader = FileSystemLoader("templates")
templateEnv = Environment(loader=fileLoader)

def toTime(input):
  deltaValue = str(datetime.timedelta(seconds=input))
  if deltaValue != "0.0":
    return deltaValue.lstrip("0:0")
  else:
    return deltaValue

templateEnv.filters['toTime'] = toTime
# single session reuslt:

def createResultPageForSingleResult(result: SessionResult, targetDirectory: str):
  if "Race" in result.Session:
    plotPositionGraph(result,targetDirectory)
    plotGaps(result,targetDirectory)
  result.Drivers = list(filter(lambda d: d.getTimedLaps() > 0,  result.Drivers))
  renderTemplate({"trackName": result.TrackEvent, "trackHash": result.getHash(), "result": result}, "session-result.html", join(targetDirectory, result.getPageFilename()))

def createHotlapsPage(results: List[SessionResult], targetDirectory: str):
  hotlaps = getHotLaps(results)
  for trackHash, drivers in hotlaps.items():
    trackName =results[0].TrackEvent
    sortedByBestLap = OrderedDict(sorted(drivers.items(), key=lambda d:d[1]["BestLapTime"]))
    renderTemplate({"drivers": sortedByBestLap, "trackName": trackName, "trackHash": trackHash, "results": results}, "hotlap-result.html", join(targetDirectory, trackHash + "_hotlaps.html"))
  

raw = []
output = {}
sourceDir = args.source
logFiles = listdir(sourceDir)
for logFile in logFiles:
  try:
    if ".xml" in logFile:
      fullPath = join(sourceDir, logFile)
      result = parseXML(fullPath)
      raw.append(result)
      
      createResultPageForSingleResult(result, args.target)
      
  except Exception as e:
    print(e)
    pass


indexLinks = OrderedDict()
for result in raw:
  if result.getHash() not in output:
    output[result.getHash()] = [result]
    indexLinks[result.getHash()] = {
      "TrackName": result.TrackEvent,
      "Sessions": 1
    }
  else:
    output[result.getHash()].append(result)
    indexLinks[result.getHash()]["Sessions"] = indexLinks[result.getHash()]["Sessions"] + 1

for trackHash, results in output.items():
  createHotlapsPage(results, args.target)


renderTemplate({"indexLinks": indexLinks}, "index.html", join(args.target, "index.html"))
