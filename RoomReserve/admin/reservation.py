from RoomReserve import *
from RoomReserve.admin.guest import getGuestByID, getAllGuests
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.user import getUserById
import datetime

class form_CreateReservation(Form):

    #guestID and roomID we will need to make some form of searching for them and having a list come up.

    guestID = IntegerField('Guest ID', validators=[DataRequired()])
    userID = IntegerField('User ID', validators=[DataRequired()])
    roomID = IntegerField('Room ID', validators=[DataRequired()])

    minuteList = []
    hourList = []
    monthList = [(1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"), (7, "July"), (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December")]
    dayList = []
    yearList = []

    for min in range(10):
        myMin = "0" + str(min)
        minuteList.append((min, myMin))

    for min in range(10, 60):
        minuteList.append((min, str(min)))

    hourList.append((0, "0"))

    for i in range(1, 24):
        hourList.append((i, str(i)))
        dayList.append((i, str(i)))

    for i in range(24, 32):
        dayList.append((i, str(i)))

    for year in range(2015, 2115):
        yearList.append((year, str(year)))

    monthIn = SelectField('Month In', default=12, choices=monthList, validators=[DataRequired()])
    dayIn = SelectField('Day', default=8, choices=dayList, validators=[DataRequired()])
    yearIn = SelectField('Year', choices=yearList, validators=[DataRequired()])
    hourIn = SelectField('Hour', default=14, choices=hourList, validators=[DataRequired()])
    minuteIn = SelectField('Minute', choices=minuteList, validators=[DataRequired()])

    monthOut = SelectField('Month Out', choices=monthList, validators=[DataRequired()])
    dayOut = SelectField('Day', choices=dayList, validators=[DataRequired()])
    yearOut = SelectField('Year', default=2016, choices=yearList, validators=[DataRequired()])
    hourOut = SelectField('Hour',  default=8, choices=hourList, validators=[DataRequired()])
    minuteOut = SelectField('Minute', choices=minuteList, validators=[DataRequired()])


    status = SelectField('Status', default='unarrived',\
        choices=[(CONST.checkedin_status, 'Checked In'),\
                (CONST.unarrived_status, 'Unarrived'),\
                (CONST.checkedout_status, 'Checked Out'),\
                (CONST.waiting_status, 'Waiting')\
                ])

    notes = TextAreaField('Notes', validators=[DataRequired()])

@app.route('/admin/reservationlist', methods=['GET', 'POST'])
@login_required
def page_reservation():
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1

    if request.args.get('per'):
        perPage = int(request.args.get('per'))
    else:
        perPage = 10

    if request.method == 'POST' and form.validate():
        # the form has been filled out, import the data
        formdata = request.form
        guestID = int(formdata['guestID'])
        userID = int(formdata['userID'])
        roomID = int(formdata['roomID'])
        status = formdata['status']
        notes = formdata['notes']

        yearIn = formdata['yearIn']
        monthIn = formdata['monthIn']
        dayIn = formdata['dayIn']
        hourIn = formdata['hourIn']
        minuteIn = formdata['minuteIn']

        yearOut = formdata['yearOut']
        monthOut = formdata['monthOut']
        dayOut = formdata['dayOut']
        hourOut = formdata['hourOut']
        minuteOut = formdata['minuteOut']

        checkIn = datetime.datetime(int(yearIn), int(monthIn),  int(dayIn), int(hourIn), int(minuteIn))
        checkOut = datetime.datetime(int(yearOut), int(monthOut),  int(dayOut), int(hourOut), int(minuteOut))

        # create the reservation
        if createReservation(guestID, userID, roomID, checkIn, checkOut, status, notes):
            # Reservation created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render('basic.html', content="Sorry, could not create reservation. Something's not right!")

    form = form_CreateReservation()

    #reservations = getAllReservations()
    reservations = Reservation.query.order_by(Reservation.id)
    reservations = reservations.paginate(page, perPage, False)
    return render('listreservations.html', perPage=perPage, form=form, reservations=reservations,
    getGuestByID=getGuestByID, getRoomByID=getRoomByID)

def getAllReservations():
    # returns all reservations in a list
    return db.session.query(Reservation)

def getReservationByID(id):
    # returns single res object with the given id
    return getReservationsByID(id)

def getReservationsByIDList(id):
    # returns single res object with the given id
    res = []
    for myres in db.session.query(Reservation).filter_by(id=id):
        res.append(myres)
    return res

def getReservationsByID(id):
    # returns single res object with the given id
    return db.session.query(Reservation).filter_by(id=id).first()

def getReservationsStartingBetweenDates(dStart, dEnd):
    dEnd = dEnd + datetime.timedelta(days=1)
    reslist = db.session.query(Reservation).filter( \
        Reservation.checkintime >= dStart, \
        Reservation.checkintime < dEnd, \
        Reservation.status != CONST.draft_status )
    if reslist:
        return reslist
    return []

def getReservationsEndingBetweenDates(dStart, dEnd):
    dEnd = dEnd + datetime.timedelta(days=1)
    reslist = db.session.query(Reservation).filter( \
        Reservation.checkouttime >= dStart, \
        Reservation.checkouttime < dEnd, \
        Reservation.status != CONST.draft_status )
    if reslist:
        return reslist
    return []
    
def getMissedReservations(mydate):
    reslist = []
    results = db.session.query(Reservation).filter( \
        Reservation.checkintime > mydate , \
        Reservation.status == CONST.unarrived_status )
        
    for item in results:
        reslist.append(item)
        
        
    results = db.session.query(Reservation).filter( \
        Reservation.checkouttime < mydate, \
        Reservation.status == CONST.checkedin_status )
        
    for item in results:
        reslist.append(item)

    return reslist

def find_available_rooms(startDate, endDate, buildingID=None, capacity=0):
    '''
    Returns a list of room objects that do not have reservations during
    the requested date ranges.
    Parameters: datetime startDate, datetime endDate.
    Optional parameters: buildingID, capacity
    When buildingID is passed, it only returns rooms in that buildingID.
    When a capacity is passed, it only returns rooms that can hold
    that many or more people.
    '''
    # TODO: Implement buildingID filtering

    from RoomReserve.admin.rooms import getActiveRooms
    def is_room_available(roomID, delor):
        for res in get_active_reservations_for_roomID(roomID):
            if delorean_helper.delorean_crash(res.get_delorean(), delor):
                return False
        return True

    delor = delorean_helper.create_delorean(startDate, endDate)
    availableRooms = []
    for rm in getActiveRooms():
        if capacity and rm.get_capacity() >= capacity:
            if is_room_available(rm.getID(),delor):
                availableRooms.append(rm)
    return availableRooms
    
def find_first_available_room(startDate, endDate, buildingID=None, capacity=0):
    '''
    Returns a list of room objects that do not have reservations during
    the requested date ranges.
    Parameters: datetime startDate, datetime endDate.
    Optional parameters: buildingID, capacity
    When buildingID is passed, it only returns rooms in that buildingID.
    When a capacity is passed, it only returns rooms that can hold
    that many or more people.
    '''
    # TODO: Implement buildingID filtering

    from RoomReserve.admin.rooms import getActiveRooms
    def is_room_available(roomID, delor):
        for res in get_active_reservations_for_roomID(roomID):
            if delorean_helper.delorean_crash(res.get_delorean(), delor):
                return False
        return True

    delor = delorean_helper.create_delorean(startDate, endDate)
    for rm in getActiveRooms():
        if capacity and rm.get_capacity() >= capacity:
            if is_room_available(rm.getID(),delor):
                return rm
    return None

def get_active_reservations_for_roomID(roomID):
    '''
    Parameters: roomID
    Returns a list of upcomming and current reservations for that roomID.
    '''

    return db.session.query(Reservation).filter( \
        Reservation.roomID==roomID, \
        Reservation.status != CONST.checkedout_status, \
        Reservation.status != CONST.cancelled_status, \
        Reservation.status != CONST.draft_status \
        )

def createReservation(guestID, madeby, roomID, checkin, checkout, status, notes=""):
    '''
    Adds a reservation to the database
    '''
    # TODO: catch errors.

    me = Reservation(guestID, madeby, roomID, checkin, checkout, status, notes)
    db.session.add(me)
    db.session.commit()
    return me


@app.route('/res/<int:resID>')
@login_required
def page_viewReservation(resID):
    res = getReservationByID(resID)
    if res is None:
        # Reservation not found
        return render('basic.html', content="No such reservation with ID "+str(resID))

    return render('reservation.html', res=res, guest=res.get_guest(), room=res.get_room(), CONST=CONST, getUserById=getUserById, editingAllowed = True)

@app.route('/res/<int:resID>/edit/guest')
@Login.standard_required
def page_assignGuest(resID):
    res = getReservationByID(resID)
    if res is None:
        # Reservation not found
        return render('basic.html', content="No such reservation with ID "+str(resID))
    return render('reswizard/wizard3.html', editsession=True, resID=res.getID())

@app.route('/res/edit/guest/new', methods=['POST'])
@Login.standard_required
def page_assignGuest_newGuest():
    '''
    The user has selected to create a new guest.
    Display the form to create a new guest
    and use that new guest as the guest on the reservation.
    '''
    from RoomReserve.admin.guest import form_CreateGuest
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))
    if res is None:
        # Reservation not found
        return render('basic.html', content="No such reservation with ID "+str(resID))

    form = form_CreateGuest()

    return render('reswizard/wizard3_newguest.html', editsession=True, form=form, res=res)

@app.route('/res/edit/guest/new/process', methods=['POST'])
@Login.standard_required
def page_assignGuest_newGuestProcess():
    # the form has been filled out, import the data
    formdata = request.form
    from RoomReserve.admin.guest import form_CreateGuest, processCreateGuestForm
    myGuest = processCreateGuestForm(formdata)
    if myGuest == False:
        # the guest could not be created.
        return render('basic.html', content="Could not create guest.")
    myGuestID = myGuest.get_id()
    res = getReservationByID(int(formdata['resID']))
    res.setGuest(guestID=myGuestID)

    return redirect('/res/'+str(res.getID()))

@app.route('/res/edit/guest/search', methods=['POST'])
@Login.standard_required
def page_assignGuest_searchForGuest():
    from RoomReserve.admin.guestsearch import guestsearch, form_SearchGuest
    form = form_SearchGuest()

    formdata = request.form
    myResID = int(formdata['resID'])
    # myRes = getReservationByID(int(formdata['resID']))
    print("___+++___previous information processed")
    #if search form submitted
    guests = getAllGuests()

    return render('guestsearch.html', editsession=True, resID=myResID, form=form, target="/res/edit/guest/search", guests=guests)

@app.route('/res/edit/guest/search/process', methods=['POST'])
@Login.standard_required
def page_assignGuest_existingGuestProcess():
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))
    res.setGuest(guestID=int(formdata['guestID']))
    return redirect('/res/'+str(res.getID()))

@app.route('/res/<int:resID>/edit/room')
@Login.standard_required
def page_assignRoom(resID):
    res = getReservationByID(resID)
    if res is None:
        # Reservation not found
        return render('basic.html', content="No such reservation with ID "+str(resID))
    availableRooms = find_available_rooms(res.get_check_in_datetime(), res.get_check_out_datetime(), capacity=1)
    return render('reswizard/wizard2.html', editsession=True, rooms=availableRooms, resID=res.getID())

@app.route('/res/edit/room/confirm', methods=['POST'])
@Login.standard_required
def page_processAssignRoom():
    formdata = request.form
    res = getReservationByID(int(formdata['resID']))
    room = getRoomByID(int(formdata['roomID']))

    try:
        res.setRoom(room=room)
    except RoomDoesNotExistException:
        return render('basic.html', content="Room with ID " + formdata['roomID'] + " does not exist")
    return redirect('/res/'+str(res.getID()))


@app.route('/res/<int:resID>/confirm')
@Login.standard_required
def page_processMakeReservationConfirmed(resID):
    res = getReservationByID(resID)
    if res is None:
        # Reservation not found
        return render('basic.html', content="No such reservation with ID "+str(resID))

    if res.confirm():
        return redirect('/res/'+str(resID))

    return render('basic.html', content="Could not confirm reservation with ID "+str(resID))

@app.route('/res/<id>/delete')
@Login.admin_required
def confirmDeleteReservation(id):
    id = int(id)
    me = getReservationByID(id)
    return render('deleteconfirmation.html', type="reservation", obj=me)

@app.route('/res/deleteme', methods=['POST'])
@Login.admin_required
def processDeleteReservation():
    formdata = request.form
    id = int(formdata['id'])
    me = getReservationByID(id)
    if deleteReservation(me):
        return redirect(url_for('page_reservation'))
    return abort(501)

@app.route('/res/deletedraft', methods=['POST'])
@Login.standard_required
def processDeleteDraft():
    formdata = request.form
    id = int(formdata['id'])
    me = getReservationByID(id)
    if deleteReservation(me):
        return redirect(url_for('page_reservationDrafts'))
    return abort(501)

def deleteReservation(me):
    # Removes a res from the database.
    # Returns True if res deleted successfully, else false
    try:
        db.session.delete(me)
        db.session.commit()
    except Exception as e:
        # Prints why the res could not be deleted in the terminal.
        print(e)
        return False
    return True

def getReservationsByStatus(status):
    # returns single res object with the given id
    myres = []
    for ares in db.session.query(Reservation).filter_by(status=status):
        myres.append(ares)
    return myres

@app.route('/admin/reservation/resdrafts', methods=['GET', 'POST'])
@login_required
def page_reservationDrafts():
    reservations = getReservationsByStatus(CONST.draft_status)
    return render('listdraftreservations.html',  reservations=reservations,
    getGuestByID=getGuestByID, getRoomByID=getRoomByID)
