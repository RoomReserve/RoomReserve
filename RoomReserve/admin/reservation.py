from RoomReserve import *
from datetime import datetime

class form_CreateReservation(Form):

    #guestID and roomID we will need to make some form of searching for them and having a list come up.
    
    guestID = StringField('Guest ID', validators=[DataRequired()])
    username = StringField('Your Name', validators=[DataRequired()])
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
    
    checkIn = datetime(yearIn, monthIn,  dayIn, hourIn, minuteIn, 00)
    checkOut = datetime(yearOut, monthOut,  dayOut, hourOut, minuteOut, 00)

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
