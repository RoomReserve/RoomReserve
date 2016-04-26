from RoomReserve import *
import RoomReserve.helpers.login as Login
from RoomReserve.dbtables.building import Building
from RoomReserve.dbtables.room import Room

class form_CreateBuilding(Form):
    name = StringField('Building Name', validators=[DataRequired()])
    numFloors = IntegerField('Number of Floors') #not required
    status = SelectField('Status',\
        choices=[(CONST.ready_status, 'Ready'),\
                (CONST.inactive_status, 'Inactive')])
    description = TextAreaField('Description')

    def populate(self, thisBuilding):
        '''
        Populates the fields of the form with the data currently
        in the building given.

        Parameters: a building object
        '''

        self.name.default = thisBuilding.name
        self.numFloors.default = thisBuilding.numfloors
        self.status.default = thisBuilding.status
        self.description.default = thisBuilding.description
        self.process()



@app.route('/admin/buildings', methods=['GET', 'POST'])
@login_required
def page_buildings():

    # Editor
    def edit_form(id):
        '''
        Returns the form back populated with the building information
        from the ID given.

        Parameters: id for a building.
        '''
        form = form_CreateBuilding()
        id=int(id)
        form.populate(getBuildingById(id))
        return form

    def allowEdit(id=0):
        '''
        Figures out if the current user should be allowed
        to edit the building. Currently, the buildingID is ignored.

        Parameters: buildingID (optional)
        '''
        if current_user.is_admin():
            # Only admins can edit buildings
            return True
        else:
            return False
    # /Editor

    # form = form_CreateBuilding()

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        name = formdata['name']
        numFloors = formdata['numFloors']
        status = formdata['status']
        description = ''

        # create the building
        if createBuilding(name, numFloors, description, status):
            # building created sucessfully
            pass
        else:
            # createBuilding returned false, the building could not be created.
            return render('basic.html', content="Could not create building.")

    # Get all the buildings currently in the database
    # so that they can be displayed on the page.
    buildings = getAllBuildings()
    if current_user.is_admin():
        # Only admins should see the form to create buildings
        form = form_CreateBuilding()
    else:
        # Not an admin, don't get the form.
        form = False
    return render('listbuildings.html', form=form, buildings=buildings, \
      edit_form=edit_form, allowEdit=allowEdit)

@app.route('/admin/buildings/<id>', methods=['POST'])
@login_required
def page_updateBuilding(id):
    '''
    Processing page for the building update form.

    When update is complete, redirect to the list of buildings page
    '''

    id=int(id)
    myBuilding = getBuildingById(id)

    formdata = request.form
    name = formdata['name']
    numfloors = int(formdata['numFloors'])
    description = formdata['description']
    status = formdata['status']

    # Check to see if any of the fields have changed
    # update any that have changed.
    if name != myBuilding.get_name():
        myBuilding.set_name(name)
    if numfloors != myBuilding.get_floors():
        myBuilding.set_floors(numfloors)
    if status != myBuilding.get_status():
        myBuilding.set_status(status)
    if description != myBuilding.get_description():
        myBuilding.set_description(description)

    return redirect(url_for('page_buildings'))


def getAllBuildings():
    # returns all buildings in a list
    buildings = []
    for me in db.session.query(Building):
    	buildings.append(me)
    return buildings

def getBuildingByName(myname):
    # returns single building object with the given name
    # if no building is found with that name, return false.
    building = []
    for me in db.session.query(Building).filter_by(name=myname):
        # Gets building from Building where email=myemail
    	building.append(me)
    if len(building) == 1:
        # if we got a building back, return it.
        return building[0]
    return False # returns false if the building wasn't returned.
    # This can be for two reasons:
    # No building was found or two building were found with the same name (should never happen)

def getBuilding(myname):
    # See documentation for getBuildingByName
    return getBuildingByName(myname)

def getBuildingById(id):
    # returns single building object with the given id
    # if no building is found with that id, return false.
    buildings = []
    for me in db.session.query(Building).filter_by(id=id):
        # Gets building from building where id=id
    	buildings.append(me)
    if len(buildings) == 1:
        # if we got a building back, return it.
        return buildings[0]
    return False # returns false if the building wasn't returned.
    # This can be for two reasons:
    # No building was found or two building were found with the same id (should never happen)

def createBuilding(name, numfl, desc, st):
    # Adds a building to the database.
    # Returns True if building added successfully, else False.
    try:
        me = Building(name, numfl, st, desc)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the building could not be added in the terminal.
        print(e)
        return False
        



@app.route('/admin/buildings/<id>/delete')
@Login.admin_required
def confirmDeleteBuilding(id):
    id = int(id)
    me = getBuildingById(id)
    if db.session.query(Room).filter_by(buildingID = id).first() != None:
        return render('basic.html', content = "Building still contains rooms")
    return render('deleteconfirmation.html', type="building", obj=me)

@app.route('/admin/buildings/deleteme', methods=['POST'])
@Login.admin_required
def processDeleteBuilding():
    formdata = request.form
    id = int(formdata['id'])
    me = getBuildingById(id)
    if deleteBuilding(me):
        return redirect(url_for('page_buildings'))
    return abort(501)

def deleteBuilding(me):
    # Removes a building from the database.
    # Returns True if building deleted successfully, else false
    try:
        db.session.delete(me)
        db.session.commit()
    except Exception as e:
        # Prints why the building could not be deleted in the terminal.
        print(e)
        return False
    return True
