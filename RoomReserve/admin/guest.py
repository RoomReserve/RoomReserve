from RoomReserve import *

class form_CreateGuest(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=40)])
    lastname = StringField('Last Name', [validators.Length(min=1, max=40)])
    email = StringField('Email Address', [validators.email()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=20)])
    address = StringField('Address', [validators.Length(min=1, max=75)])
    payment = StringField('Payment', [validators.Length(min=1, max=7)])
    notes = TextAreaField('Notes')


@app.route('/admin/guest', methods=['GET', 'POST'])
@login_required
def page_guest():

    if request.method == 'POST' and form.validate():
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

    form = form_CreateGuest()
    guests = getAllGuests()
    return render('guests.html', form=form, guests=guests)

def getAllGuests():
    # returns all guests in a list
    guests = []
    for me in db.session.query(Guest):
    	guests.append(me)
    return guests

def getGuestByFirstName(fn):
    # returns
    guests = []
    for me in db.session.query(Guest).filter_by(first=fn):
    	guests.append(me)
    return guests

def getGuestByLastName(ln):

    for me in db.session.query(Guest).filter_by(last=ln):
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

def getGuestByEmail(myEmail):
    # returns single guest object with the given Email
    # if no guest is found with that phone number, return false.
    guests = []
    for me in db.session.query(Guest).filter_by(email=myEmail):
        # Gets guests from Guest where email=myEmail
    	guests.append(me)
    if len(guests) == 1:
        # if we got a guest back, return it.
        return guests[0]
    return False

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
