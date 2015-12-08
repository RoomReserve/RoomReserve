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
    active = BooleanField('Active', default=True)


    def __init__(self):
        super(form_CreateRoom, self).__init__()
        from RoomReserve.admin.building import getAllBuildings
        self.building.choices = []

        for b in getAllBuildings():
            self.building.choices.append((b.id, b.name))

    def populate(self, thisRoom):
        '''
        Populates the fields of the form with the data currently
        in the room given.

        Parameters: a room object
        '''
        self.building.default = thisRoom.get_building_id()
        self.floor.default = thisRoom.get_floor()
        self.roomnumber.default = thisRoom.get_room_number()
        self.capacity.default = thisRoom.get_capacity()
        #TODO: implement status
        self.process()

@app.route('/admin/rooms', methods=['GET', 'POST'])
@login_required
def page_rooms():

    # Editor
    def edit_form(id):
        '''
        Returns the form back populated with the room information
        from the ID given.

        Parameters: id for a room.
        '''
        form = form_CreateRoom()
        id=int(id)
        form.populate(getRoomByID(id))
        return form

    def allowEdit(id=0):
        '''
        Figures out if the current user should be allowed
        to edit the room. Currently, the roomID is ignored.

        Parameters: roomID (optional)
        '''
        if current_user.is_admin():
            # Only admins can edit rooms
            return True
        else:
            return False
    # /Editor



    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        building = formdata['building']
        floor = formdata['floor']
        roomnumber = formdata['roomnumber']
        capacity = formdata['capacity']
        if 'active' in formdata:
            status = Static.ready_status
        else:
            status = Static.inactive_status
        #description = formdata['description']
        description = ""


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
    return render('listrooms.html', form=form, rooms=rooms, \
      edit_form=edit_form, allowEdit=allowEdit)

@app.route('/admin/rooms/<id>', methods=['POST'])
def page_updateRoom(id):
    '''
    Processing page for the room update form.

    When update is complete, redirect to the list of rooms page
    '''

    id=int(id)
    myRoom = getRoomById(id)

    formdata = request.form
    building = formdata['building']
    floor = formdata['floor']
    roomnumber = formdata['roomnumber']
    capacity = formdata['capacity']

    # Check to see if any of the fields have changed
    # update any that have changed.
    if building != myRoom.get_building_id():
        myRoom.set_building_id(building)
    if floor != myRoom.get_floor():
        myRoom.set_floor(floor)
    if roomnumber != myRoom.get_room_number():
        myRoom.set_room_number(roomnumber)
    if capacity != myRoom.get_capacity():
        myRoom.set_capacity(capacity)

    return redirect(url_for('page_rooms'))



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

def getRoomByID(id):
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
