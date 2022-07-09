"""
The input format:

    ResearchArea, ConfName, [Deadlines], [Year], Location, ConfDate
"""

import csv

from datetime import datetime


class ConfRecord:
    def __init__(self, researchArea, confName, deadlineList, 
			acceptanceList,
			year, location,
            confDate):
        self.researchArea = researchArea
        self.confName = confName
        self.deadlineList = deadlineList
        self.acceptanceList = acceptanceList
        self.year = year
        self.location = location
        self.confDate = confDate
    def __repr__(self):
        s = " "
        s = s.join([self.confName,
					str(parseDateToStr(self.deadlineList)),
                    self.location])
        s = s + "\n"
        return s

def parseDates(dateStrList):
    dates = []
    for dateStr in dateStrList:
        dates.append(datetime.strptime(dateStr, '%m-%d-%Y'))
    return dates

def collectRecords(file):
    confList = []
    with open(file) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            researchArea = row['ResearchArea']
            confName = row['ConfName']
            deadlineStrList = row['DeadlineList'][1:-1].split(';')
            acceptanceStrList = row['AcceptanceList'][1:-1].split(';')
            deadlines = parseDates(deadlineStrList)
            acceptances = parseDates(acceptanceStrList)
            year = row['Year']
            location = row['Location']
            confDateStr = row['ConfDate']
            try:
                confDate = datetime.strptime(confDateStr, '%m-%d-%Y')
            except:
                confDate = datetime.strptime(confDateStr, '%Y')
            conf = ConfRecord(researchArea,
                    confName,
                    deadlines,
                    acceptances,
                    year,
                    location,
                    confDate)
            confList.append(conf)
    upcoming = []
    past = []
    for c in confList:
        if max(c.deadlineList) >= datetime.now():
            upcoming.append(c)
        else:
            past.append(c)
    return (upcoming, past)
    """
    confMap = {}
    for conf in confList:
        if conf.confName not in confMap:
            confMap[conf.confName] = []
        confMap[conf.confName].append(conf)
    return confMap
    """

def parseDateToStr(dates):
    dateStr = ""
    for date in dates:
        if date < datetime.now():
            dateStr = dateStr + '~'+ date.strftime('%b-%d-%Y')+'~, '
        else:
            dateStr = dateStr + date.strftime('%b-%d-%Y') + ', '
    return dateStr

def generateMarkdown(upcoming, past):
	print('### Nearest:')
	p = sorted(upcoming, key = lambda conf: max(conf.deadlineList))
	print (p)
	print('### Upcoming:')
	print ('| Conference | Deadline | Acceptance Notification | Conference Date | Location |')
	print ('| --- | --- | --- | --- | --- |')
	for conf in upcoming:
		print('| ' + conf.confName + ' | ' + parseDateToStr(conf.deadlineList) + ' | ' + parseDateToStr(conf.acceptanceList) + ' | ' + parseDateToStr([conf.confDate]) + ' | ' + conf.location + ' | ')

	print()
	print('### Previous:')
	print ('| Conference | Deadline | Acceptance Notification | Conference Date | Location |')
	print ('| --- | --- | --- | --- | --- |')
	for conf in past:
		print('| ' + conf.confName + ' | ' + parseDateToStr(conf.deadlineList) + ' | ' + parseDateToStr(conf.acceptanceList) + ' | ' + parseDateToStr([conf.confDate]) + ' | ' + conf.location + '|')

if __name__ == "__main__":
	upcoming, past = collectRecords('conferences.csv')
	generateMarkdown(upcoming, past)
