from RoomReserve import *

class form_CreateReservation(Form):

    #guestID and roomID we will need to make some form of searching for them and having a list come up.
    
    guestID = StringField('Guest ID', validators=[DataRequired()])
    username = StringField('Your Name', validators=[DataRequired()])
    roomID = StringField('Room ID', validators=[DataRequired()])
    

    
    #the lists below may need to be created into tuples............... Yeah. We'll see.
    minuteList = [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    hourList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    monthList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dayList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    yearList = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113]
    
    monthIn = SelectField('Month In', choices=hourList, validators=[DataRequired()])
    dayIn = SelectField('Day', choices=dayList, validators=[DataRequired()])
    yearIn = SelectField('Year', choices=yearList, validators=[DataRequired()])
    hourIn = SelectField('Hour', choices=hourList, validators=[DataRequired()])
    minuteIn = SelectField('Minute', choices=minuteList, validators=[DataRequired()])
    
    monthOut = SelectField('Month Out', choices=hourList, validators=[DataRequired()])
    dayOut = SelectField('Day', choices=dayList, validators=[DataRequired()])
    yearOut = SelectField('Year', choices=yearList, validators=[DataRequired()])
    hourOut = SelectField('Hour', choices=hourList, validators=[DataRequired()])
    minuteOut = SelectField('Minute', choices=minuteList, validators=[DataRequired()])
    
    checkIn = monthIn + dayIn + yearIn + hourIn + minuteIn
    checkOut = monthOut + dayOut + yearOut + hourOut + minuteOut

    status = RadioField('Status',\
        choices=[('checkedin', 'Checked In'),\
                ('unarrived', 'Unarrived'),\
                ('checkedout', 'Checked Out'),\
                ('waiting', 'Waiting')\
                ])
    notes = StringField('Check Out Time', validators=[DataRequired()])
    

@app.route('/admin/reservation', methods=['GET', 'POST'])
def page_reservation():

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        guestID = formdata['guestID']
        username = formdata['username']
        roomID = formdata['roomID']
        checkIn = formdata['checkIn']
        checkOut = formdata['checkOut']
        status = formdata['status']
        notes = formdata['notes']

        # create the reservation
        if createReservation(guestID, username, roomID, checkIn, checkOut, status, notes):
            # Reservation created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render_template('basic.html', content="Could not create reservation.")

    form = form_CreateReservation()
    reservations = getAllReservations()
    return render_template('reservation.html', form=form, reservation=reservation)

def getAllReservations():
    # returns all reservations in a dictionary
    reservations = []
    for me in db.session.query(Reservation):
    	reservations.append(me)
    return reservations

def getReservation(guestID):
    # returns single user object with the given email
    # if no user is found with that email, return false.
    reservations = []
    for me in db.session.query(Reservation).filter_by(guest=guestID):
        # Gets users from User where email=myemail
    	reservations.append(me)
    if len(reservations) == 1:
        # if we got a reservation back, return it.
        return reservations[0]
    return False

def getReservationById(id):
    # returns single user object with the given id
    # if no user is found with that id, return false.
    reservations = []
    for me in db.session.query(Reservation).filter_by(id=id):
        # Gets reservations from User where id=id
    	reservations.append(me)
    if len(reservations) == 1:
        # if we got a user back, return it.
        return reservations[0]
    return False

def createReservation(guest, madeby, place, checkin, checkout, status, notes):
    # Adds a reservation to the database.
    # Returns True if user added successfully, else False.
    try:
        me = Reservation(guest, madeby, place, checkin, checkout, status, notes)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the reservation could not be added in the terminal.
        print(e)
        return False
