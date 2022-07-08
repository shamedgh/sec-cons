"""
The input format:

    ResearchArea, ConfName, [Deadlines], [Year], Location, ConfDate
"""

import csv

from datetime import datetime

class ConfRecord:
    def __init__(self, researchArea, confName, deadlineList, year, location,
            confDate):
        self.researchArea = researchArea
        self.confName = confName
        self.deadlineList = deadlineList
        self.year = year
        self.location = location
        self.confDate = confDate
    def __repr__(self):
        s = " "
        s = s.join([self.researchArea, self.confName,
                    ' '.join(self.deadlineList), self.year,
                    self.location])
        s = s + "\n"
        return s

def collectRecords(file):
    confList = []
    with open(file) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            researchArea = row['ResearchArea']
            confName = row['ConfName']
            deadlines = row['DeadlineList'][1:-1].split(';')
            year = row['Year']
            location = row['Location']
            confDate = row['ConfDate']
            conf = ConfRecord(researchArea,
                    confName,
                    deadlines,
                    year,
                    location,
                    confDate)
            confList.append(conf)
    upcoming = [conf in confList if 
    confMap = {}
    for conf in confList:
        if conf.confName not in confMap:
            confMap[conf.confName] = []
        confMap[conf.confName].append(conf)
    return confMap


if __name__ == "__main__":
    confMap = collectRecords('conferences.csv')
    print(confMap)

