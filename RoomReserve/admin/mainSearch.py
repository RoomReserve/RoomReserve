from RoomReserve import *
from RoomReserve.admin.guest import *
from RoomReserve.admin.reservation import *
from RoomReserve.admin.rooms import *
from RoomReserve.admin.building import *
import re

class form_MainSearch(Form):
    search = StringField('searchString', validators=[DataRequired()])


@app.route('/admin/mainSearch', methods=['GET','POST'])
def mainsearch_page():
    form = form_MainSearch()

    if request.method == 'POST':
        formdata = request.form
        if 'search' in formdata:
            searchStr = formdata['search']

            results = overallsearch(searchStr)

        return render('mainSearch.html', results=results)

    return render('mainSearch.html', results=[])
def overallsearch(searchStr):
    '''
    Returns a list containing the matching string
    '''

    rawSearchStr = searchStr
    searchStr = re.sub(r'[^\w]', '', searchStr) #removes all symbols
    searchStr = searchStr.lower()
    results = {}
    results["rooms"] = set()
    results["reservations"] = set()
    results["guests"] = set()
    results["buildings"] = set()
    if len(searchStr) == 0:
        return results
    
    if searchStr.isdigit(): #Either Reserve ID, Guest ID, Guest phone, room ID, room number
        searchInt = int(searchStr)
        resID = list(getReservationByID(searchInt))
        guestID = list(getGuest(searchInt))
        guestPhone = getGuestByPhone(searchInt)
        roomID = getRoomByID(searchInt)
        roomNum = getRoomByNum(searchInt)
        
        if len(resID) > 0:
            for i in resID:
                results["reservations"].add(i)
        if len(guestID) > 0:
            for i in guestID:
                results["guests"].add(i)
        if len(guestPhone) > 0:
            for i in guestPhone:
                results["guests"].add(i)
        if len(roomID) > 0:
            for i in roomID:
                results["rooms"].add(i)
        if len(roomNum) > 0:
            for i in roomNum:
                results["rooms"].add(i)
        
        
    else: # either guest notes, first name, lastname, email, address, building with room, room status
        guestnotes = getGuestByMatchingNotes(searchStr)
        searchStrAsList = searchStr.split()
        guestfirst = []
        guestlast = []
        anotherGuestFirst = []
        if len(searchStrAsList) > 0:
            guestfirst = getGuestByPartialFirstName(searchStrAsList[0])
            if len(searchStrAsList) > 1:
                guestlast = getGuestByPartialLastName(searchStrAsList[1])
                anotherGuestFirst = getGuestByPartialFirstName(searchStrAsList[1])
            else:
                guestlast = getGuestByPartialLastName(searchStrAsList[0])
        guestemail = getGuestByPartialEmail(rawSearchStr)
        roomStatus = getRoomByPartialStatus(searchStr)
        guestAddress = getGuestByAddress(rawSearchStr)
        roomBuildingMix = []
        
        intIndex = -1
        searchStrMinusInts = ""
        
        for i in searchStrAsList: #looking for a mix of strings and ints
            if i.isdigit():
                #found a mix of strings and ints
                intIndex = i
            else:
                if searchStrMinusInts != "":
                    searchStrMinusInts += " " + i
                else:
                    searchStrMinusInts += i
                
        if intIndex != -1 and searchStrMinusInts != "":
            roomBuildingMix = getRoomInBuildingWithPartialName(searchStrMinusInts, int(searchStrAsList[intIndex]))

        
        
        if len(guestnotes) > 0:
            for i in guestnotes:
                results["guests"].add(i)
        if len(guestfirst) > 0:
            for i in guestfirst:
                results["guests"].add(i)
        if len(guestlast) > 0:
            for i in guestlast:
                results["guests"].add(i)
        if len(anotherGuestFirst) > 0:
            for i in guestlast:
                results["guests"].add(i)
        if len(guestemail) > 0:
            for i in guestemail:
                results["guests"].add(i)
        if len(roomStatus) > 0:
            for i in roomStatus:
                results["rooms"].add(i)
        if len(guestAddress) > 0:
            for i in guestAddress:
                results["guests"].add(i)
        if len(roomBuildingMix) > 0:
            for i in roomBuildingMix:
                results["rooms"].add(i)

    return results
