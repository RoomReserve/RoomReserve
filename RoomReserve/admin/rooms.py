from RoomReserve import *
from RoomReserve.helpers.login import admin_required

class form_CreateRoom(Form):


    building = SelectField('Building',\
            choices=[], \
            validators=[DataRequired()])
    roomnumber = IntegerField('Room Number', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    status = SelectField('Status',\
        choices=[(CONST.ready_status, 'Ready - Unoccupied'),\
                (CONST.occupied_status, 'Ready - Occupied'),\
                (CONST.inactive_status, 'Inactive')])

    description = TextAreaField('Description')


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
        self.roomnumber.default = thisRoom.get_room_number()
        self.capacity.default = thisRoom.get_capacity()
        self.status.default = thisRoom.get_status()
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


    # form = form_CreateRoom()

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        building = formdata['building']
        roomnumber = formdata['roomnumber']
        capacity = formdata['capacity']
        status = formdata['status']
        description = ''


        # create the room
        if createRoom(roomnumber, building, capacity, description, status):
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
      edit_form=edit_form, allowEdit=allowEdit, CONST=CONST)

@app.route('/admin/rooms/<id>', methods=['POST'])
def page_updateRoom(id):
    '''
    Processing page for the room update form.

    When update is complete, redirect to the list of rooms page
    '''

    id=int(id)
    myRoom = getRoomByID(id)

    formdata = request.form
    building = formdata['building']
    roomnumber = formdata['roomnumber']
    capacity = formdata['capacity']
    status = formdata['status']

    # Check to see if any of the fields have changed
    # update any that have changed.
    if building != myRoom.get_building_id():
        myRoom.set_building_id(building)
    if roomnumber != myRoom.get_room_number():
        myRoom.set_room_number(roomnumber)
    if status != myRoom.get_status():
        myRoom.set_status(status)
    if capacity != myRoom.get_capacity():
        myRoom.set_capacity(capacity)

    return redirect(url_for('page_rooms'))



def getAllRooms():
    # returns all rooms
    rooms = []
    for me in db.session.query(Room):
    	rooms.append(me)
    return rooms

def getActiveRooms(buildingID=None):
    '''
    returns a list of rooms that are not inactive.
    if a buildingID is passed, then it only displays rooms in the selected bldg.
    '''
    # if buildingID:
    #     return db.session.query(Room).filter_by(status=CONST.ready_status, buildingID=buildingID)
    # return db.session.query(Room).filter_by(status=CONST.ready_status)

    if buildingID:
        return db.session.query(Room).filter( \
        Room.status != CONST.inactive_status, \
        Room.buildingID == buildingID \
        )
    else:
        return db.session.query(Room).filter( \
        Room.status != CONST.inactive_status, \
        )

def getInactiveRooms(buildingID=None):
    '''
    returns a list of rooms that are marked inactive.
    if a buildingID is passed, then it only displays rooms in the selected bldg.
    '''

    if buildingID:
        return db.session.query(Room).filter( \
        Room.status == CONST.inactive_status, \
        Room.buildingID == buildingID \
        )
    else:
        return db.session.query(Room).filter( \
        Room.status == CONST.inactive_status, \
        )

def getRoomsByStatus(statusSelect):
    rooms = []
    for me in db.session.query(Room).filter_by(status=statusSelect):
        rooms.append(me)
    return rooms

def getRoomsByPartialStatus(statusSelect):
    rooms = []
    for me in db.session.query(Room):
        if statusSelect in me.get_status().lower():
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

def getRoomInBuildingWithName(bldgName, rn):
    # returns single room object with the given building and room number
    # if room number is not found in building, return false.
    #TODO: Test this to see if it works.
    # Miller 401
    rooms = []
    for builds in db.session.query(Building).filter_by(name=bldgName):
        roomReturned = getRoomInBuilding(builds.id, rn)
        if roomReturned != False:
            rooms.append(roomReturned)
    return rooms

def getRoomInBuildingWithPartialName(bldgName, rn):
    # returns single room object with the given building and room number
    # if room number is not found in building, return false.
    #TODO: Test this to see if it works.
    # Miller 401
    rooms = []
    for builds in db.session.query(Building):
        if bldgName in builds.getBuildingName().lower():
            if rn == -1:
                for aroom in db.session.query(Room).filter_by(buildingID=builds.id):
                    rooms.append(aroom)
            else:
                roomReturned = getRoomInBuilding(builds.id, rn)
                if roomReturned != False:
                    rooms.append(roomReturned)
    return rooms


def getRoomByNum(rn):
    # returns single room object with the given building and room number
    # if room number is not found in building, return false.
    #TODO: Test this to see if it works.
    rooms = []
    for room in db.session.query(Room).filter_by(roomnumber=rn):
        rooms.append(room)
    return rooms


def getRoomByIDList(id):
    # returns single room object with the given id
    # if no room is found with that id, return false.
    rooms = []
    for me in db.session.query(Room).filter_by(id=id):
        # Gets users from Room where id=id
    	rooms.append(me)
    return rooms


def getRoomByID(id):
    # returns single room object with the given id
    # if no room is found with that id, return false.
    return db.session.query(Room).filter_by(id=id).first()

def createRoom(bldg, rn, cap, desc, st):
    # Adds a room to the database.
    # Returns True if room added successfully, else False.
    try:
        me = Room(bldg, rn, cap, desc, st)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the room could not be added in the terminal.
        print(e)
        return False

@app.route('/admin/rooms/<id>/delete')
#@admin_required
def confirmDeleteRoom(id):
    id = int(id)
    me = getRoomByID(id)
    return render('deleteconfirmation.html', type="room", obj=me)

@app.route('/admin/rooms/deleteme', methods=['POST'])
def processDeleteRoom():
    formdata = request.form
    id = int(formdata['id'])
    me = getRoomByID(id)
    if deleteRoom(me):
        return redirect(url_for('page_rooms'))
    return abort(501)

def deleteRoom(me):
    # Removes a room from the database.
    # Returns True if room deleted successfully, else false
    try:
        db.session.delete(me)
        db.session.commit()
    except Exception as e:
        # Prints why the room could not be deleted in the terminal.
        print(e)
        return False
    return True
