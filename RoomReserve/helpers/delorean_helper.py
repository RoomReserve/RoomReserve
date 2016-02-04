import delorean
from datetime import datetime
from delorean import Delorean, range_daily

def create_delorean(dStart, dEnd, includeLastDay=False):
    '''
    Parameters: DateTime start date, and end date
    Optional parameters: boolean includeLastDay

    Returns a list of datetimes (possibly deloreans in the future)
    that includes every date in the range from the start date
    to end date.
    '''
    #TODO ADD SUPPORT FOR includeLastDay

    delor = list(delorean.range_daily(start=dStart,stop=dEnd))
    datesOnly=[]
    for dt in delor:
        datesOnly.append(dt.date)
    return datesOnly

def delorean_crash(delor1, delor2):
    '''
    Parameters: List of dates, list of dates.
    Retruns True if the deloreans have any conflicting dates, else False.
    '''
    for day1 in delor1:
        if day1 in delor2:
            return True
    return False
