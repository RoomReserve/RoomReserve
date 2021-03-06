from RoomReserve import *
from RoomReserve.admin.guest import processCreateGuestForm, getAllGuests, getGuestByID

class NewGuestForm(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    payment = StringField('Payment', validators=[DataRequired()])
    notes = TextAreaField('Comments/Special Requests')


@app.route('/newguest', methods=['GET', 'POST'])
def newguest():
    form = NewGuestForm()

    if request.method == 'POST' and form.validate():
        # the form has been filled out, import the data
        message = "Your guest account is created successfully. When you make a reservation, simply tell the customer service your name."
        if processCreateGuestForm(request.form):
            # print("Guest created successfully.")
            return render('success.html', message=message)
        else:
            # createGuest returned false, the guest could not be created.
            return render('basic.html', content="Could not create guest.")

    return render('newguest.html', form=form)
