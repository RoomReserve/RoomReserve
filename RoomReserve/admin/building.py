from RoomReserve import *

class form_CreateBuilding(Form):
    name = StringField('Building Name', validators=[DataRequired()])
    numFloors = IntegerField('Number of Floors') #not required
    active = BooleanField('Active')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')




@app.route('/admin/buildings', methods=['GET', 'POST'])
def page_buildings():

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        name = formdata['name']
        numFloors = formdata['numFloors']
        description = formdata['description']
        if formdata['active']:
            status = Static.ready_status
        else:
            status = Static.inactive_status

        # create the building
        if createBuilding(name, numFloors, description, status):
            # building created sucessfully
            pass
        else:
            # createBuilding returned false, the building could not be created.
            return render('basic.html', content="Could not create building.")

    buildings = getAllBuildings()
    if current_user.is_admin():
        form = form_CreateBuilding()
    else:
        form = False
    return render('listbuildings.html', form=form, buildings=buildings)

def getAllBuildings():
    # returns all buildings in a dictionary
    buildings = []
    for me in db.session.query(Building):
    	buildings.append(me)
    return buildings

def getBuilding(myname):
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
