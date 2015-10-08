from RoomReserve import *

class form_CreateUser(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')
    role = RadioField('Role',\
        choices=[('admin', 'Administraitor'),\
                ('standard', 'Standard User'),\
                ('readonly', 'Read Only'),\
                ('inactive', 'Inactive')\
                ])

@app.route('/admin/users', methods=['GET', 'POST'])
def page_users():
    if request.method == 'GET':
        form = form_CreateUser()
        return render_template('users.html', form=form)
    elif request.method == 'POST':
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        password = formdata['password']
        role = formdata['role']
        if createUser(firstname, lastname, email, role):
            content = "hello "
            content += firstname
            return render_template('basic.html', content=content)
        else:
            return render_template('basic.html', content="Could not create user.")
    else:
        return RoomReserve.helpers.errorhandlers.page_error400(400)

def createUser(fn, ln, em, ro):
    try:
        me = User(fn, ln, em, ro)
        db.session.add(me)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
