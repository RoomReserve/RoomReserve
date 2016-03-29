from RoomReserve import *
from RoomReserve.admin.guest import *
import re


class form_SearchGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])


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
def guestsearch_page():
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
    form = form_SearchGuest()

    if request.method == 'POST':
        formdata = request.form
        if 'firstname' or 'lastname' or 'email' or 'phone' in formdata:
            firstname = formdata['firstname']
            lastname = formdata['lastname']
            email = formdata['email']

            #strip non-numbers out of phone number
            phone = re.sub(r'[^\w]', '', formdata['phone']) #easier way of taking out symbols

            guests = guestsearch(firstname, lastname, email, phone)

        return render('guestsearch.html', form=form, guests=guests)

    return render('guestsearch.html', form=form)

def guestsearch(firstname, lastname, email, phone):
        '''
        Returns a list containing the matching guests
        '''

        # Add support for search by lowercase name
        firstname = firstname.capitalize()
        lastname = lastname.capitalize()
        lastname = str(lastname)


        guests = []
        if firstname and lastname and email and phone:
            guests = guests + getGuestByName(first=firstname,last=lastname,email=email, phone=phone)

        elif firstname and lastname and email:
            guests = guests + getGuestByNameAndEmail(first=firstname,last=lastname,email=email)

        elif firstname and lastname and phone:
            guests = guests + getGuestByNameAndPhone(first=firstname,last=lastname,phone=phone)

        elif firstname and lastname:
            guests = guests + getGuestByName(first=firstname,last=lastname)

        elif firstname and email:
            guests = guests + getGuestByFirstNameAndEmail(first=firstname,email=email)

        elif firstname and phone:
            guests = guests + getGuestByFirstNameAndPhone(first=firstname,phone=phone)

        elif lastname and email:
            guests = guests + getGuestByLastNameAndEmail(last=lastname,email=email)

        elif lastname and phone:
            guests = guests + getGuestByFirstNameAndPhone(last=lastname,phone=phone)

        elif firstname:
            guests = guests + getGuestByFirstName(firstname)

        elif lastname:
            guests = guests + getGuestByLastName(lastname)

        elif email:
            guests = guests + getGuestByEmail(email)

        elif phone:
            guests = guests + getGuestByPhone(phone)

        return guests


# Guest Profile
@app.route('/admin/gprofile/<gid>')
def gprofile(gid):
    guests = guestQuery(gid)

    return render('gprofile.html', guests=guests)
