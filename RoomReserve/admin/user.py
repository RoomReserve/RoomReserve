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


        if createUser(firstname, lastname, email, role, password):
            # user created sucessfully
            pass
        else:
            # createUser returned false, the user could not be created.
            return render('basic.html', content="Could not create user.")

    users = getAllUsers()
    if current_user.is_admin():
        # Only admins can see the form to create users.
        form = form_CreateUser()
    else:
        # Not an admin, no form.
        form = False
    return render('users.html', form=form, users=users)

@app.route('/admin/users/<id>', methods=['GET', 'POST'])
def page_updateUser(id):
    if current_user.is_admin():
        # Only admins can edit users
        allowEdit = True
    else:
        allowEdit = False

    form = form_createUser
    return render('users_edit.html', form=form, allowEdit=allowEdit)

def getAllUsers():
    # returns all users in a list
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

def createUser(fn, ln, em, ro, pw="helloworld"):
    # Adds a user to the database.
    # TODO: add support for passwords.
    # Returns True if user added successfully, else False.
    try:
        me = User(fn, ln, em, ro, pw)
        db.session.add(me)
        db.session.commit()
        return True

    except Exception as e:
        # Prints why the user could not be added in the terminal.
        print(e)
        return False
