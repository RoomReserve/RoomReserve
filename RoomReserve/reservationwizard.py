from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms, createReservation, getReservationByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.building import getBuildingById


@app.route('/res/new', methods=['GET', 'POST'])
@Login.standard_required
def page_reservation_wizard():
    '''
    The first page in the reservation wizard
    '''
    if True: # User has permission to make reservations
        form = True
    return render('reswizard/wizard1.html', form=form)

@app.route('/res/new/room', methods=['POST'])
#@Login.standard_required
def page_reservation_wizard_2():
    '''
    Processes the data from the first page
    which includes the desired check in, out dates
    and minimum capacity

    Displays a list of rooms that are available
    during the time and fit the criteria
    '''
    formdata = request.form
    indate = formdata['dates'].split()[0]
    outdate = formdata['dates'].split()[2]
    if formdata['capacity'] == "":
        capacity = 1
    else: capacity = int(formdata['capacity'])

    indate = delorean.parse(indate).naive()
    outdate = delorean.parse(outdate).naive()

    availableRooms = find_available_rooms(indate, outdate, capacity=capacity)

    myRes = createReservation(guestID=-1, madeby=current_user.getID(), roomID=-1, \
                        checkin=indate, checkout=outdate, status=CONST.draft_status)
    return render('reswizard/wizard2.html', rooms=availableRooms, resID=myRes.getID())



@app.route('/res/new/guest', methods=['POST'])
def page_reservation_wizard_3():
    '''
    Updates the reservation with the selected room.

    Asks for the guest information
    '''
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))
    room = getRoomByID(int(formdata['roomID']))

    res.setRoom(room=room)
    buildingName = getBuildingById(room.get_building_id()).get_name()

    from RoomReserve.admin.guestsearch import form_SearchGuest
    guestSearchForm = form_SearchGuest()

    from RoomReserve.admin.guest import form_CreateGuest
    createGuestForm = form_CreateGuest()

    return render('reswizard/wizard3.html', guestSearchForm=guestSearchForm,\
        room=getRoomByID(res.getRoomID()), buildingName=buildingName, resID=res.getID())

@app.route('/res/new/guest/new', methods=['POST'])
def page_reservation_wizard_3_new_guest():
    '''
    The user has selected to create a new guest.
    Display the form to create a new guest
    and use that new guest as the guest on the reservation.
    '''
    from RoomReserve.admin.guest import form_CreateGuest #, processCreateGuestForm
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))

    form = form_CreateGuest()

    return render('reswizard/wizard3_newguest.html', form=form, res=res)


@app.route('/res/new/guest/new/process', methods=['POST'])
def page_reservation_wizard_3_new_guest_process():
    # the form has been filled out, import the data
    formdata = request.form
    from RoomReserve.admin.guest import form_CreateGuest, processCreateGuestForm
    myGuest = processCreateGuestForm(formdata)
    if myGuest == False:
        # the guest could not be created.
        return render('basic.html', content="Could not create guest.")
    myGuestID = myGuest.get_id()
    myRes = getReservationByID(int(formdata['resID']))
    myRes.setGuest(guestID=myGuestID)


    return render('reswizard/confirm.html', res=myRes)


@app.route('/res/new/guest/search', methods=['POST'])
def page_reservation_wizard_3_search_existing_guest():
    '''
    The user has selected to search for an existing guest.
    Display the results of the search and allow the selection of one.

    TODO: Also have an option for making a new guest in case the user
    doesn't find the guest they were looking for.
    '''
    from RoomReserve.admin.guestsearch import guestsearch, form_SearchGuest
    form = form_SearchGuest()

    formdata = request.form
    myResID = int(formdata['resID'])
    # myRes = getReservationByID(int(formdata['resID']))
    print("___+++___previous information processed")
    #if search form submitted
    if 'searching' in formdata:
        print("___+++___Processing search information")
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']

        #strip non-numbers out of phone number
        phone = ""
        for char in formdata['phone']:
            if char in "0123456789":
                phone += char

        guests = guestsearch(firstname, lastname, email, phone)

        return render('guestsearch.html', resID=myResID, form=form, target="/res/new/guest/search", guests=guests)

    return render('guestsearch.html', resID=myResID, form=form, target="/res/new/guest/search")


@app.route('/res/new/guest/search/process', methods=['POST'])
def page_reservation_wizard_3_search_existing_guest_process():
    formdata = request.form
    myRes = getReservationByID(int(formdata['resID']))
    myRes.setGuest(guestID=int(formdata['guestID']))

    return render('reswizard/confirm.html', res=myRes)


@app.route('/res/confirm', methods=['POST'])
def page_draft_reservation_confirm():
    '''
    The reservation wizard is done.
    Make the reservation non-draft and give the user a confirmation number.
    '''
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))
    res.set_status(CONST.unarrived_status)

    return render('basic.html', content = "Confirmation Number: " + str(res.getID()))
