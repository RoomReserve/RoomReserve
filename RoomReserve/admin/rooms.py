from RoomReserve import *

class form_CreateRoom(Form):


    building = SelectField('Building',\
            choices=[], \
            validators=[DataRequired()])
    floor = SelectField('Floor',\
            choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8)], \
            validators=[DataRequired()])
    roomnumber = IntegerField('Room Number', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    active = BooleanField('Active')


    def __init__(self):
        super(form_CreateRoom, self).__init__()
        from RoomReserve.admin.building import getAllBuildings

        for b in getAllBuildings():
            self.building.choices.append((b.id, b.name))



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
            return render('basic.html', content="Could not create room.")

    if current_user.is_admin():
        # Only admins should see the form to create rooms
        form = form_CreateRoom()
    else:
        # Not an admin, don't show the form
        form = False
    rooms = getAllRooms()
    return render('listrooms.html', form=form, rooms=rooms)

def getAllRooms():
    # returns all rooms
    rooms = []
    for me in db.session.query(Room):
    	rooms.append(me)
    return rooms

def getRoomInBuilding(bldgID, rn):
    # returns single room object with the given building and room number
    # if room number is not found in building, return false.
    #TODO: Test this to see if it works.
    room = db.session.query(Room).filter_by(buildingID=bldgID, roomnumber=rn).first()
    if room is not None:
        return room
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
        # Prints why the room could not be added in the terminal.
        print(e)
        return False
