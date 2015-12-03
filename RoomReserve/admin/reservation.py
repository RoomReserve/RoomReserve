from RoomReserve import *

class form_CreateReservation(Form):

    #guestID and roomID we will need to make some form of searching for them and having a list come up.

    guestID = StringField('Guest ID', validators=[DataRequired()])
    username = IntegerField('Your user id', validators=[DataRequired()])
    roomID = StringField('Room ID', validators=[DataRequired()])



    #the lists below may need to be created into tuples............... Yeah. We'll see.
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



    monthIn = SelectField('Month In', choices=monthList, validators=[DataRequired()])
    dayIn = SelectField('Day', choices=dayList, validators=[DataRequired()])
    yearIn = SelectField('Year', choices=yearList, validators=[DataRequired()])
    hourIn = SelectField('Hour', choices=hourList, validators=[DataRequired()])
    minuteIn = SelectField('Minute', choices=minuteList, validators=[DataRequired()])

    monthOut = SelectField('Month Out', choices=monthList, validators=[DataRequired()])
    dayOut = SelectField('Day', choices=dayList, validators=[DataRequired()])
    yearOut = SelectField('Year', choices=yearList, validators=[DataRequired()])
    hourOut = SelectField('Hour', choices=hourList, validators=[DataRequired()])
    minuteOut = SelectField('Minute', choices=minuteList, validators=[DataRequired()])


    status = RadioField('Status',\
        choices=[('checkedin', 'Checked In'),\
                ('unarrived', 'Unarrived'),\
                ('checkedout', 'Checked Out'),\
                ('waiting', 'Waiting')\
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
        guestID = formdata['guestID']
        username = formdata['username']
        roomID = formdata['roomID']
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
        if createReservation(guestID, username, roomID, checkIn, checkOut, status, notes):
            # Reservation created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render_template('basic.html', content="Could not create reservation.")

    form = form_CreateReservation()
    reservations = getAllReservations()
    return render('reservation.html', form=form, reservations=reservations)

def getAllReservations():
    # returns all reservations in a list
    reservations = []
    for me in db.session.query(Reservation):
    	reservations.append(me)
    return reservations


def getReservation(id):
    # returns single res object with the given id
    # if no res is found with that id, return false.
    reservations = []
    for me in db.session.query(Reservation).filter_by(id=id):
        # Gets reservations from Reservation where id=id
    	reservations.append(me)
    if len(reservations) == 1:
        # if we got a res back, return it.
        return reservations[0]
    return False

def createReservation(guestID, madeby, roomID, checkin, checkout, status, notes):
    # Adds a reservation to the database.
    # Returns True if user added successfully, else False.
    try:
        me = Reservation(guestID, madeby, roomID, checkin, checkout, status, notes)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the reservation could not be added in the terminal.
        print(e)
        return False
