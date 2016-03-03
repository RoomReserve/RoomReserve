from RoomReserve import *
from RoomReserve.admin.guest import processCreateGuestForm, getAllGuests 

class form_CreateGuest(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    payment = StringField('Payment', validators=[DataRequired()])
    notes = TextAreaField('Notes')


@app.route('/newguest', methods=['GET', 'POST'])
def newguest():
    form = form_CreateGuest()

    if request.method == 'POST':
        # the form has been filled out, import the data
        if processCreateGuestForm(request.form):
            # guest created sucessfully
            pass
        else:
            # createGuest returned false, the guest could not be created.
            return render('basic.html', content="Could not create guest.")

    return render('newguest.html', form=form)


