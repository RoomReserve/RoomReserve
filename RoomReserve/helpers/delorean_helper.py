import delorean
from datetime import datetime
from delorean import Delorean, range_daily

def create_delorean(dStart, dEnd, includeLastDay=False):
    #TODO ADD SUPPORT FOR includeLastDay
    return list(delorean.range_daily(start=dStart,stop=dEnd))

def delorean_crash(delor1, delor2):
    for day1 in delor1:
        if day1 in delor2:
            return True
    return False
