from parse import parseXML
from classes.driver import Driver


result = parseXML('C:\\Users\\chm\\Documents\\simpaddock\\parser\\data\\test.xml')


print(result.ServerName, result.TrackEvent, result.MostLapsCompleted, result.Minutes,result.TrackLength)
for driver in result.Drivers:
  print(driver.Name, driver.VehName, driver.Position, driver.ClassPosition, driver.FinishStatus, driver.LapCount, len(driver.Laps))
  for l in driver.Laps:
    print(l)