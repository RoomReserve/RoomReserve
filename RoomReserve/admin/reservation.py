from RoomReserve import *

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



#this stuff below is supposed to get autocomplete to work.
#Below might also need the following:

#$("#sometextfield").autocomplete({
#            serviceUrl:'/api/product_autocomplete',
#            onSelect: function(val, data) {
#              /* Handle data here */
#            },
#});

# @jsonify
# @app.restrict('GET')

""" def tag_autocomplete(self):
    if 'query' not in request.params:
        abort(400)
    fragment = request.params['query']
    keywords = fragment.split()
    searchstring = "%%".join(keywords)
    searchstring = '%%%s%%' %(searchstring)
    try:
        ac_q = Session.query(Tag)
        res = ac_q.filter(Tag.name.ilike(searchstring)).limit(10)
        return dict(query=fragment, suggestions=[r.name for r in res], data=["%s" %(r.name) for r in res])
    except NoResultFound:
        return dict(query=fragment, suggestions=[], data=[]) """

@app.route('/admin/reservation', methods=['GET', 'POST'])
@login_required

def page_reservation():

    if request.method == 'POST':
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

        checkIn = datetime(int(yearIn), int(monthIn),  int(dayIn), int(hourIn), int(minuteIn))
        checkOut = datetime(int(yearOut), int(monthOut),  int(dayOut), int(hourOut), int(minuteOut))

        # create the reservation
        if createReservation(guestID, userID, roomID, checkIn, checkOut, status, notes):
            # Reservation created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render('basic.html', content="Sorry, could not create reservation. Something's not right!")

    form = form_CreateReservation()
    reservations = getAllReservations()
    return render('reservation.html', form=form, reservations=reservations)




def getAllReservations():
    # returns all reservations in a list
    return db.session.query(Reservation)

def getReservationByID(id):
    # returns single res object with the given id
    return db.session.query(Reservation).filter_by(id=id).first()


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

    # Returns True if user added successfully, else False.
    # try:
    #     me = Reservation(guestID, madeby, roomID, checkin, checkout, status, notes)
    #     db.session.add(me)
    #     db.session.commit()
    #     return True
    #
    # except Exception as e:
    #     # Prints why the reservation could not be added in the terminal.
    #     print(e)
    #     return False

    me = Reservation(guestID, madeby, roomID, checkin, checkout, status, notes)
    db.session.add(me)
    db.session.commit()
    return me
