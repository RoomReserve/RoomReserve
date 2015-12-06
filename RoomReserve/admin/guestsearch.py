from RoomReserve import * 
from RoomReserve.admin.guest import *


class form_SearchGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    

# Get all the guest info from the database
def guestQuery(gid):

    result = []
    q = getGuest(gid)
    result.append(q)

    return result

def findGuestid(name):

    q = session.query(Guest).filter(Guest.first == first).one() 
    return q.id


@app.route('/admin/guestsearch', methods=['GET','POST'])

# Need a more detailed guest search
def guestsearch():
    form = form_SearchGuest()

    if request.method == 'POST':
        if 'firstname' or 'lastname' or 'email' in request.form: 
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']

            firstname = firstname.capitalize()
            lastname = lastname.capitalize()


            guests = []

            if firstname and lastname and email:
                guests = guests + getGuestByName(first=firstname,last=lastname,email=email)


            if firstname and lastname:
                guests = guests + getGuestByName(first=firstname,last=lastname)

            if firstname and email:
                guests = guests + getGuestByFirstNameAndEmail(first=firstname,email=email)

            if lastname and email:
                guests = guests + getGuestByLastName(last=lastname,email=email)

            elif firstname:
                guests = guests + getGuestByFirstName(firstname)

            elif lastname:
                guests = guests + getGuestByLastName(lastname)

            elif email:
                guests = guests + getGuestByEmail(email)

            return render('guestsearch.html', form=form, guests=guests)

    return render('guestsearch.html', form=form)


# Guest Profile
@app.route('/admin/gprofile/<gid>')
def gprofile(gid):
    guests = guestQuery(gid)

    return render('gprofile.html', guests=guests)

