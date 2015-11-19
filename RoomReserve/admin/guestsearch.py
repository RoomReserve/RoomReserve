from RoomReserve import *

class form_FindGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])


@app.route('/admin/guestsearch', methods=['GET', 'POST'])
def page_guestsearch():

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        phone = formdata['phone']


        # create the guest
        if getGuestSearch(firstname, lastname, email, phone):
            # guest found sucessfully
            pass
        else:
            # createGuest returned false, the guest could not be created.
            return render('basic.html', content="Could not find guest.")

    form = form_FindGuest()
    guests = getAllGuests()
    return render('guestsearch.html', form=form, guests=guests)
    
    


def getAllGuests():
    # returns all guests in a dictionary
    guests = []
    for me in db.session.query(Guest):
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
    
def getGuestSearch(first, last, email, phone):
    guests = []
    filterstring = ""
    
    # make a query from which fields are filled
    if first != "":
      filterstring += "first=first"
      
    if last != "":
      if filterstring != "":
        filterstring += ",last=last"
        
      else:
        filterstring += "last=last"
        
    if email != "":
      if filterstring != "":
        filterstring += ",email=email"
        
      else:
        filterstring += "email=email"
        
    if phone != "":
      if filterstring != "":
        filterstring += ",phone=phone"
        
      else:
        filterstring += "phone=phone"
        
    for me in db.session.query(Guest).filter_by(filterstring):
        # Gets guests from Guest where phone=myphone
    	guests.append(me)
    if len(guests) >= 1:
        # if we got a guest back, return it.
        return guests
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
