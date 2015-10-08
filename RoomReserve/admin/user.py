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

    if request.method == 'POST':
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        password = formdata['password']
        role = formdata['role']

        if createUser(firstname, lastname, email, role):
            #user created sucessfully
            pass
        else:
            #could not create user
            return render_template('basic.html', content="Could not create user.")

    form = form_CreateUser()
    users = getAllUsers()
    return render_template('users.html', form=form, users=users)

def getAllUsers():
    #returns all users in a dictionary
    users = []
    for me in db.session.query(User):
    	users.append(me)
    return users

def getUser(myemail):
    #returns single user object with the given email
    users = []
    for me in db.session.query(User).filter_by(email=myemail):
    	users.append(me)
    if len(users) == 1:
        return users[0]
    return False


def createUser(fn, ln, em, ro):
    try:
        me = User(fn, ln, em, ro)
        db.session.add(me)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
