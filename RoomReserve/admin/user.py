from RoomReserve import *

class form_CreateUser(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')
    role = SelectField('Role',\
        choices=[('admin', 'Administrator'),\
                ('standard', 'Standard User'),\
                ('readonly', 'Read Only'),\
                ('inactive', 'Inactive')\
                ])


@app.route('/admin/users', methods=['GET', 'POST'])
def page_users():

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        password = formdata['password']
        role = formdata['role']

        # create the user
        # TODO: add support for passwords. Currently they are ignored.
        if createUser(firstname, lastname, email, role):
            # user created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render('basic.html', content="Could not create user.")

    form = form_CreateUser()
    users = getAllUsers()
    return render('users.html', form=form, users=users)

def getAllUsers():
    # returns all users in a dictionary
    users = []
    for me in db.session.query(User):
    	users.append(me)
    return users

def getUser(myemail):
    # returns single user object with the given email
    # if no user is found with that email, return false.
    users = []
    for me in db.session.query(User).filter_by(email=myemail):
        # Gets users from User where email=myemail
    	users.append(me)
    if len(users) == 1:
        # if we got a user back, return it.
        return users[0]
    return False

def getUserById(id):
    # returns single user object with the given id
    # if no user is found with that id, return false.
    users = []
    for me in db.session.query(User).filter_by(id=id):
        # Gets users from User where id=id
    	users.append(me)
    if len(users) == 1:
        # if we got a user back, return it.
        return users[0]
    return False

def createUser(fn, ln, em, ro):
    # Adds a user to the database.
    # TODO: add support for passwords.
    # Returns True if user added successfully, else False.
    try:
        me = User(fn, ln, em, ro)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the user could not be added in the terminal.
        print(e)
        return False
