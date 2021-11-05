import time
import numpy as np
import argparse
import os

import json

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
args = parser.parse_args()

try:
    from ledPixels import *
    ledPix = ledPixels(args.nPix, board.D18)
except:
    print("ledPix not active")

currentDir = os.path.dirname(os.path.realpath(__file__))
templateFileName = currentDir + '/outputTemplate.html'
outFileName = currentDir + '/output.html'
print(f"template: {templateFileName}")
print(f'output.html: {outFileName}')

with open(templateFileName, "r") as f:
    htmlTemplate = f.read()

weeklySchedule = """
[
    {
        "day": "Monday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Tuesday",
        "periods": [
            ["8:00", "8:14"],
            ["8:15", "8:29"],
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Wednesday",
        "periods": [
            ["8:15", "9:10"],
            ["9:15", "10:10"],
            ["10:15", "11:10"],
            ["11:15", "11:30"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:25"],
            ["13:30", "15:30"],
            ["16:15", "17:45"]
        ]
    },
    {
        "day": "Thursday",
        "periods": [
            ["8:00", "9:10"],
            ["9:15", "9:55"],
            ["10:00", "10:40"],
            ["10:45", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Friday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },

    {
        "day": "Saturday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"],
            ["18:30", "19:55"],
            ["20:00", "21:00"]
        ]
    },
    {
        "day": "Sunday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"],
            ["18:30", "19:55"],
            ["20:00", "21:00"]
        ]
    }
]
"""

#
# {
#     "day": "Friday",
#     "periods": [
#         ["8:00", "8:12"],
#         ["9:00", "9:12"],
#         ["9:45", "9:57"],
#         ["10:00", "10:12"],
#         ["10:15", "10:27"],
#         ["11:00", "11:12"],
#         ["11:30", "11:42"],
#         ["13:00", "13:12"],
#         ["14:30", "14:47"],
#         ["15:15", "15:27"]
#     ]
# },
#



class uTime:
    def __init__(self, t_str):
        # t_str is a string that has the time as "9:30"
        t = t_str.split(":")
        self.hr = int(t[0])
        self.min = int(t[1])
        self.totMins = self.hr * 60 + self.min
    def printTime(self):
        return f'{self.hr}:{str(self.min).zfill(2)}'

def uTimeNow():
    now = time.localtime()
    return uTime(str(now.tm_hour)+":"+str(now.tm_min))

class period:
    def __init__(self, startTime, endTime):
        self.startTxt = startTime
        self.endTxt = endTime
        self.start = uTime(startTime)
        self.end = uTime(endTime)

    def printTxt(self):
        t = f'{self.start.hr}:{self.start.min}-{self.end.hr}:{self.end.min}'
        return t


class schedule:
    def __init__(self):
        self.days = json.loads(weeklySchedule)
        for i in range(len(self.days)):
            #print(i, self.days[i]["day"])
            for t in range(len(self.days[i]["periods"])):
                #print(t, self.days[i]["periods"][t])
                strt = self.days[i]["periods"][t][0]
                end = self.days[i]["periods"][t][1]
                self.days[i]["periods"][t] = period(strt, end)
                #print("p:", self.days[i]["periods"][t].start.totMins, self.days[i]["periods"][t].end.totMins)


    def findPeriod2(self, tm = uTimeNow(), d=time.localtime().tm_wday):
        # t is an instance of uTime
        #tm = uTime(str(h)+":"+str(m))
        period = -1
        #print("d:", d, len(self.days))
        p = self.days[d]["periods"]
        #print("day", d, h, m, self.days[d]["day"], len(p))
        for i in range(len(p)):
            #print(h, p[i].start.hr, m, p[i].start.min, p[i].start.totMins)

            if (tm.totMins >= p[i].start.totMins and tm.totMins <= p[i].end.totMins):
                #print("findPeriod2 (start, tm, end):",  p[i].start.totMins, tm.totMins, p[i].end.totMins)
                period = i
        return (d, period)

    def getPeriod2(self, tm = uTimeNow(), d=time.localtime().tm_wday):
        (d, p) = self.findPeriod2(tm, d)
        if p == -1:
            return None
        else:
            return self.days[d]["periods"][p]

    def findPeriod3(self, tm = uTimeNow(), d=None):
        # t is an instance of uTime
        #tm = uTime(str(h)+":"+str(m))
        activePeriod = None
        passingTime = True
        beforeTime = False
        afterTime = False
        #print("d:", d)

        if d == None:
            d = time.localtime().tm_wday

        p = self.days[d]["periods"]
        #print("day", d, h, m, self.days[d]["day"], len(p))

        # if before any periods
        if (tm.totMins < p[0].start.totMins):
            beforeTime = True
            i = -1

        elif (tm.totMins > p[-1].end.totMins):
            i = -2

        else:

            for i in range(len(p)):
                #print(h, p[i].start.hr, m, p[i].start.min, p[i].start.totMins)

                if (tm.totMins >= p[i].start.totMins and tm.totMins <= p[i].end.totMins):
                    #print("findPeriod2 (start, tm, end):",  p[i].start.totMins, tm.totMins, p[i].end.totMins)
                    activePeriod = p[i]
                    passingTime = False
                    break

                if i > 0:
                    if (tm.totMins > p[i-1].end.totMins and tm.totMins < p[i].start.totMins):
                        activePeriod = period(p[i-1].endTxt, p[i].startTxt)
                        break
        return (activePeriod, i, passingTime, d)


def startupSequence():
    for i in range(args.nPix):
        ledPix.light(i, (0, 200,200))
        time.sleep(0.1)

doneColor = (150, 0, 0)
togoColor = (0, 150, 0)
passColor = (0, 0, 150)
passDoneColor = (0, 75, 75)

s = schedule()
print(s.days[0]["periods"][0].start.hr, s.days[0]["periods"][0].start.min)

print("--------------------------------------------")

#startupSequence()

l_start = True

while True:
    now = time.localtime()
    uNow = uTimeNow()
    (cp, pIndex, l_passing, d) = s.findPeriod3(uNow)
    if cp != None:
        if (pIndex == -1): # Before first period
            print(f'Before First Period: {uNow.printTime()} - {cp.printTime}')
        elif (pIndex == -2): # After last period.
            print(f'After Last Period: {uNow.printTime()} - {cp.printTime}')
        else:
            #print(cp.start.hr, cp.start.min)
            frac = (uNow.totMins - cp.start.totMins) / (cp.end.totMins-cp.start.totMins)
            #print("frac:", frac)

            nLights = min(int(frac*args.nPix), args.nPix)
            # try:
            #     ledPix.twoColors(nLights, (150,0,0), (0,150,0))
            # except:
            #     print("pixels not lit")
            if l_passing:
                leftColor = passColor
                elapsedColor = passDoneColor
            else:
                leftColor = togoColor
                elapsedColor = doneColor
            if l_start:
                ledPix.twoColorsTimestep(nLights, elapsedColor, leftColor, 0.1)
                l_start = False
            else:
                ledPix.twoColors(nLights, elapsedColor, leftColor)
            outputTxt = f'day:{s[d].day} ({d})|P{pIndex}|{l_passing}: {uNow.printTime()} - {cp.printTxt()}, n={nLights}/{args.nPix}, frac: {round(frac*100)}%'
            print(outputTxt, end="\r", flush=True)

    else:
        ledPix.setColor((0,0,100))
        outputTxt = 'Period not found: {uNow.printTime()}'
        print(outputTxt)
    htmlTemplate.replace('<<status>>', outputTxt)
    with open(outFileName, "w") as f:
        f.write(outputTxt)
    time.sleep(10)
