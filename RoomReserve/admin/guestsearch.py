from RoomReserve import * 
from RoomReserve.admin.guest import *


class form_SearchGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    

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

def guestsearch():
    form = form_SearchGuest()

    if request.method == 'POST':
        if 'firstname' in request.form: 
            firstname = request.form['firstname']

            gid = getGuestByFirstName(firstname)[0].id
            gid = str(gid)
            full_url = url_for('gprofile', gid=gid)
            return redirect(full_url)

        if 'lastname' in request.form: 
            lastname = request.form['lastname']

            gid = getGuestByFirstName(lastname)[0].id
            gid = str(gid)
            full_url = url_for('gprofile', gid=gid)
            return redirect(full_url) 
            
    return render('guestsearch.html', form=form)


# Guest Profile
@app.route('/admin/gprofile/<gid>')
def gprofile(gid):
    guests = guestQuery(gid)

    return render('gprofile.html', guests=guests)

