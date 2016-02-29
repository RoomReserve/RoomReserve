from RoomReserve import *
from RoomReserve.admin.guest import *
from RoomReserve.admin.reservation import *
from RoomReserve.admin.rooms import *
from RoomReserve.admin.building import *

import re

@app.route('/admin/guestsearch', methods=['GET','POST'])
def search_page():
    guests = guestsearch(firstname, lastname, email, phone)


    return render('guestsearch.html', form=form, guests=guests)

def overallsearch(searchStr):
        '''
        Returns a list containing the matching strings
        '''
    re.sub(r'[^\w]', '', searchStr) #removes all symbols
    results = dict{"rooms":[], "reservations":[], "guests":[], "buildings":[]}
    
    if searchStr.isdigit(): #Either Reserve ID, Guest ID, Guest phone, room ID, room number
        searchInt = int(searchStr)
        resID = getReservationByID(searchInt)
        guestID = getGuest(searchInt)
        guestPhone = getGuestByPhone(searchInt)
        roomID = getRoomByID(searchInt)
        roomNum = getRoomByNum(searchInt)
        
        if len(resID) > 0:
            for i in resID:
                results["reservations"].append(i)
        if len(guestID) > 0:
            for i in guestID:
                results["guests"].append(i)
        if len(guestPhone) > 0:
            for i in guestPhone:
                results["guests"].append(i)
        if len(roomID) > 0:
            for i in roomID:
                results["rooms"].append(i)
        if len(resID) > 0:
            for i in resID:
                results["reservations"].append(i)
        
        
    else: # either guest notes, first name, lastname, email, address, building, room status
        guestfirst = getGuestByFirstName(searchStr)
        guestlast = getGuestByLastName(searchStr)
        guestemail = getGuestByEmail(searchStr)
        roomID = getRoomByID(searchInt)
        roomNum = getRoomByNum(searchInt)
        
        if len(guestfirst) > 0:
            for i in guestfirst:
                results["guests"].append(i)
        if len(guestlast) > 0:
            for i in guestlast:
                results["guests"].append(i)
        if len(guestemail) > 0:
            for i in guestemail:
                results["guests"].append(i)
        if len(roomID) > 0:
            for i in roomID:
                results["rooms"].append(i)
        if len(resID) > 0:
            for i in resID:
                results["reservations"].append(i)

# Guest Profile
@app.route('/admin/gprofile/<gid>')
def gprofile(gid):
    guests = guestQuery(gid)

    return render('gprofile.html', guests=guests)
