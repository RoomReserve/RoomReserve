from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms, createReservation, getReservationByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.building import getBuildingById

class Form_Wizard_Form(Form):
    '''
    The first form for the reservation wizard.
    Asks for dates and capacity.
    '''
    check_in_date = DateField('Check In')
    check_out_date = DateField('Check Out')
    capacity = IntegerField()

@app.route('/res/new', methods=['GET', 'POST'])
@Login.standard_required
def page_reservation_wizard():
    '''
    The first page in the reservation wizard
    '''
    form = Form_Wizard_Form()
    return render('reswizard/wizard1.html', form=form)

@app.route('/res/step-2', methods=['POST'])
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
    indate = formdata['check_in_date']
    outdate = formdata['check_out_date']
    capacity = int(formdata['capacity'])

    indate = delorean.parse(indate).naive()
    outdate = delorean.parse(outdate).naive()

    availableRooms = find_available_rooms(indate, outdate, capacity=capacity)

    myRes = createReservation(guestID=-1, madeby=current_user.getID(), roomID=-1, \
                        checkin=indate, checkout=outdate, status=CONST.draft_status)
    return render('reswizard/wizard2.html', rooms=availableRooms, resID=myRes.getID())

@app.route('/res/step-3', methods=['POST'])
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
        room=getRoomByID(res.getRoomID()), buildingName=buildingName)

@app.route('/res/step-3/new', methods=['POST'])
def page_reservation_wizard_3_new_guest():
    pass

@app.route('/res/step-3/search', methods=['POST'])
def page_reservation_wizard_3_existing_guest():
    '''
    The user has selected to search for an existing guest.
    Display the results of the search and allow the selection of one.
    Also have an option for making a new guest in case the user
    doesn't find the guest they were looking for.
    '''
    from RoomReserve.admin.guestsearch import guestsearch
