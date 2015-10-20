from RoomReserve import *

class form_CreateRoom(Form):
    building = SelectField('Building',\
            choices=[], \
            validators=[DataRequired()])
    floor = SelectField('Floor',\
            choices=[], \
            validators=[DataRequired()])
    roomnumber = IntegerField('Room Number', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    active = BooleanField('Active')
    description = TextAreaField('Description')





@app.route('/admin/rooms', methods=['GET', 'POST'])
def page_rooms():

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        building = formdata['building']
        floor = formdata['floor']
        roomnumber = formdata['roomnumber']
        capacity = formdata['capacity']
        active = formdata['active']
        description = formdata['description']

        if active:
            status = "Ready"
        else:
            status = "Inactive"

        # create the room
        if createRoom(roomnumber, floor, building, capacity, description, status):
            # room created sucessfully
            pass
        else:
            # createUser returned false, the room could not be created.
            return render_template('basic.html', content="Could not create room.")

    form = form_CreateRoom()
    rooms = getAllRooms()
    return render_template('listrooms.html', form=form, rooms=rooms)

def getAllRooms():
    # returns all rooms in a dictionary
    rooms = []
    for me in db.session.query(Room):
    	rooms.append(me)
    return rooms

def getUser(myemail):
    # returns single user object with the given email
    # if no user is found with that email, return false.
    users = []
    for me in db.session.query(User).filter_by(email=myemail):
        # Gets users from User where email=myemail
    	users.append(me)
    if len(users) == 1:
        # if we got a user back, return it.
        return users[0]
    return False

def getRoomById(id):
    # returns single room object with the given id
    # if no room is found with that id, return false.
    rooms = []
    for me in db.session.query(Room).filter_by(id=id):
        # Gets users from Room where id=id
    	rooms.append(me)
    if len(rooms) == 1:
        # if we got a room back, return it.
        return rooms[0]
    return False

def createRoom(rn, fl, bldg, cap, desc, st):
    # Adds a room to the database.
    # Returns True if room added successfully, else False.
    try:
        me = Room(rn, fl, bldg, cap, desc, st)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the user could not be added in the terminal.
        print(e)
        return False
