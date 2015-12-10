import delorean
from datetime import datetime
from delorean import Delorean, range_daily

def create_delorean(dStart, dEnd, includeLastDay=False):
    #TODO ADD SUPPORT FOR includeLastDay
    delor = list(delorean.range_daily(start=dStart,stop=dEnd))
    datesOnly=[]
    for dt in delor:
        datesOnly.append(dt.date)
    return datesOnly

def delorean_crash(delor1, delor2):
    for day1 in delor1:
        if day1 in delor2:
            return True
    return False
