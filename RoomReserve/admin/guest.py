from RoomReserve import *

class form_CreateGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    payment = StringField('Payment', validators=[DataRequired()])
    notes = TextAreaField('Notes')


@app.route('/admin/guest', methods=['GET', 'POST'])
@login_required
def page_guest():

    form = form_CreateGuest()

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        phone = ""
        for char in formdata['phone']:
            if char in "0123456789":
                phone += char
        phone = int(phone)
        address = formdata['address']
        payment = ""
        for char in formdata['payment']:
            if char in "0123456789":
                payment += char
        payment = int(payment)
        notes = formdata['notes']

        # create the guest
        if createGuest(firstname, lastname, email, phone, address, payment, notes):
            # guest created sucessfully
            pass
        else:
            # createGuest returned false, the guest could not be created.
            return render('basic.html', content="Could not create guest.")

    guests = getAllGuests()
    return render('guests.html', form=form, guests=guests)

def getAllGuests():
    # returns all guests in a list
    guests = []
    for me in db.session.query(Guest):
    	guests.append(me)
    return guests

def getGuestByFirstName(fn):
    # returns a list of all guests with that first name
    guests = []
    for me in db.session.query(Guest).filter_by(first=fn):
    	guests.append(me)
    return guests

def getGuestByLastName(ln):
    # returns a list of all guests with that last name
    guests = []
    for me in db.session.query(Guest).filter_by(last=ln):
    	guests.append(me)
    return guests

def getGuestByName(first, last):
    # returns a list of all guests with that first and last name
    # parameters: (first, last)
    # remember that it is possible to have a guest that has the
    # same first and last name as another.
    guests = []
    for me in db.session.query(Guest).filter_by(first=first, last=last):
        guests.append(me)
    return guests

def getGuestByNameAndEmail(first, last, email):
    # returns a list of all guests with that first, last name and email
    # parameters: (first, last, email)
    # remember that it is possible to have a guest that has the
    # same first and last name as another.
    guests = []
    for me in db.session.query(Guest).filter_by(first=first, last=last, email=email):
        guests.append(me)
    return guests

def getGuestByFirstNameAndEmail(first, email):
    # returns a list of all guests with that first name and email
    # parameters: (first, email)

    guests = []
    for me in db.session.query(Guest).filter_by(first=first, email=email):
        guests.append(me)
    return guests

def getGuestByLastNameAndEmail(last, email):
    # returns a list of all guests with that last name and email
    # parameters: (last, email)

    guests = []
    for me in db.session.query(Guest).filter_by(last=first, email=email):
        guests.append(me)
    return guests


def getGuestByPhone(myphone):
    # returns single guest object with the given phone number
    # if no guest is found with that phone number, return false.
    guests = []
    for me in db.session.query(Guest).filter_by(phone=myphone):
        # Gets guests from Guest where phone=myphone
    	guests.append(me)
    if len(guests) == 1:
        # if we got a guest back, return it.
        return guests[0]
    return False

# def getGuestByEmail(myEmail):
#     # returns single guest object with the given Email
#     # if no guest is found with that phone number, return false.
#     guests = []
#     for me in db.session.query(Guest).filter_by(email=myEmail):
#         # Gets guests from Guest where email=myEmail
#     	guests.append(me)
#     if len(guests) == 1:
#         # if we got a guest back, return it.
#         return guests[0]
#     return False

def getGuestByEmail(myEmail):
    # returns a list of all guests with that email
    guests = []
    for me in db.session.query(Guest).filter_by(email=myEmail):
        guests.append(me)
    return guests


def getGuest(myid):
    # returns single guest object with the given id
    # if no guest is found with that id, return false.
    guests = []
    for me in db.session.query(Guest).filter_by(id=myid):
        # Gets guest from Guest where id=myid
    	guests.append(me)
    if len(guests) == 1:
        # if we got a guest back, return it.
        return guests[0]
    return False

def getGuestByID(myID):
    # see docs for getGuest
    return getGuest(myID)

def createGuest(fn, ln, em, ph, addr, paym, notes):
    # Adds a guest to the database.
    # Returns True if guest added successfully, else False.
    try:
        me = Guest(fn, ln, em, ph, addr, paym, notes)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the guest could not be added in the terminal.
        print(e)
        return False
