from RoomReserve import *
import re

class form_CreateGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    payment = StringField('Payment')
    notes = TextAreaField('Notes')

    def populate(self, thisGuest):
        '''
        Populates the fields of the form with the data currently
        in the guest given.

        Parameters: a guest object
        '''
        self.firstname.default = thisGuest.first
        self.lastname.default = thisGuest.last
        self.email.default = thisGuest.email
        self.phone.default = thisGuest.phone
        self.address.default = thisGuest.address
        self.payment.default = thisGuest.payment
        self.notes.default = thisGuest.notes
        self.process()


@app.route('/admin/guest/new', methods=['GET', 'POST'])
@app.route('/admin/guest', methods=['GET', 'POST'])
@login_required
def page_guest():

    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1

    if request.args.get('per'):
        perPage = int(request.args.get('per'))
    else:
        perPage = 10

    # Editor

    def edit_form(id):
        '''
        Returns the form back populated with the guest information
        from the ID given.

        Parameters: id for a guest.
        '''
        form = form_CreateGuest()
        id=int(id)
        myGuest = getGuestByID(id)
        form.populate(myGuest)
        return form

    def allowEdit(id):
        '''
        Figures out if the current user should be allowed
        to edit the guest object.

        Parameters: GuestID for the guest we want to edit
        '''
        if current_user.is_standard():
            # Only admins and standard users can edit guests
            return True
        else:
            return False

    #/Editor


    form = form_CreateGuest()

    if request.method == 'POST' and form.validate():
        # the form has been filled out, import the data
        if processCreateGuestForm(request.form):
            # guest created sucessfully
            pass
        else:
            # createGuest returned false, the guest could not be created.
            return render('basic.html', content="Could not create guest.")


    #guests = getAllGuests()
    guests = Guest.query.order_by(Guest.id)
    guests = guests.paginate(page, perPage, False)

    return render('guests.html', perPage=perPage, form=form, guests=guests,
    edit_form=edit_form, allowEdit=allowEdit)

def processCreateGuestForm(formdata):
    '''
    Parameters: formdata (request.form) from a CreateGuest form.
    Returns true if guest created successfully
     else false.
    '''
    firstname = formdata['firstname']
    lastname = formdata['lastname']
    email = formdata['email']

    phone = re.sub(r'[^\w]', '', formdata['phone'])
    phone = int(phone)

    address = formdata['address']

    payment = re.sub(r'[^\w]', '', formdata['payment'])
    try:
        payment = int(payment)
    except ValueError:
        payment = 0

    notes = formdata['notes']

    # create the guest
    return createGuest(firstname, lastname, email, phone, address, payment, notes)

@app.route('/admin/guest/<id>', methods=['POST'])
def page_updateGuest(id):
    id = int(id)
    myGuest = getGuestByID(id)

    if request.method == 'POST':
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        phone = int(re.sub(r'[^\w]', '', formdata['phone']))
        address = formdata['address']
        payment = re.sub(r'[^\w]', '', formdata['payment'])
        try:
            payment = int(payment)
        except ValueError:
            payment = 0
        notes = formdata['notes']

        if firstname != myGuest.first:
            myGuest.set_first_name(firstname)
        if lastname != myGuest.last:
            myGuest.set_last_name(lastname)
        if email != myGuest.email:
            myGuest.set_email(email)
        if phone != myGuest.phone:
            myGuest.set_phone(phone)
        if address != myGuest.address:
            myGuest.set_address(address)
        if payment != myGuest.payment:
            myGuest.set_payment(payment)
        if notes != myGuest.notes:
            myGuest.set_notes(notes)

    return redirect(url_for('page_guest'))




def getAllGuests():
    # returns all guests in a list
    guests = []
    for me in db.session.query(Guest):
    	guests.append(me)
    return guests

def getGuest(myid):
    # returns single guest object with the given id
    return db.session.query(Guest).filter_by(id=myid).first()

def getGuests(myid):
    # returns multiple guest objects with the given id
    return db.session.query(Guest).filter_by(id=myid)


def getGuestsByIDList(myid):
    # returns multiple guest objects with the given id
    guests = []
    for me in db.session.query(Guest).filter_by(id=myid):
        guests.append(me)
    return guests

def getGuestByID(myID):
    # see docs for getGuest
    return getGuest(myID)

def getGuestByFirstName(fn):
    # returns a list of all guests with that first name
    guests = []
    for me in db.session.query(Guest).filter_by(first=fn):
    	guests.append(me)
    return guests

def getGuestByPartialFirstName(fn):
    # returns a list of all guests with that last name
    guests = []
    for me in db.session.query(Guest):
    	if fn in me.get_first_name().lower():
    	    guests.append(me)
    return guests

def getGuestByPartialLastName(ln):
    # returns a list of all guests with that last name
    guests = []
    for me in db.session.query(Guest):
    	if ln in me.get_last_name().lower():
    	    guests.append(me)
    return guests

def getGuestByPartialEmail(emailstr):
    # returns a list of all guests with that last name
    guests = []
    for me in db.session.query(Guest):
    	if emailstr in me.get_email().lower():
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

def getGuestByEmail(myEmail):
    # returns a list of all guests with that email
    guests = []
    for me in db.session.query(Guest).filter_by(email=myEmail):
        guests.append(me)
    return guests


def getGuestByPhone(myPhone):
    # returns a list of all guests with that phone
    guests = []
    for me in db.session.query(Guest):
        if me.phone != None:
            phoneInt = int(re.sub(r'[^\w]', '', me.phone))
            if myPhone == phoneInt:
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

def getGuestByFirstNameAndPhone(first, phone):
    # returns a list of all guests with that first name and email
    # parameters: (first, phone)

    guests = []
    for me in db.session.query(Guest).filter_by(first=first, phone=phone):
        guests.append(me)
    return guests

def getGuestByLastNameAndPhone(last, phone):
    # returns a list of all guests with that last name and phone
    # parameters: (last, phone)

    guests = []
    for me in db.session.query(Guest).filter_by(last=first, phone=phone):
        guests.append(me)
    return guests

def getGuestByMatchingNotes(notes):
    # returns a list of all guests with that containing the notes string
    # parameters: (notes)

    guests = []
    if notes == None:
        return guests
    if len(notes) == 0:
        return guests
    for me in db.session.query(Guest):
        if notes in me.get_notes().lower():
            guests.append(me)
    return guests

def getGuestByAddress(address):
    # returns a list of all guests with that cantaining the address string
    # parameters: (address)

    guests = []
    if address == None:
        return guests
    if len(address) == 0:
        return guests
    for me in db.session.query(Guest):
        if address in me.get_address().lower():
            guests.append(me)
    return guests

def createGuest(fn, ln, em, ph, addr, paym, notes):
    # Adds a guest to the database.
    # Returns the Guest if guest added successfully, else False.
    try:
        me = Guest(fn, ln, em, ph, addr, paym, notes)
        db.session.add(me)
        db.session.commit()
        return me

    except Exception as e:
        # Prints why the guest could not be added in the terminal.
        print(e)
        return False
