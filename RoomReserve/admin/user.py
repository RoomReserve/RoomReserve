from RoomReserve import *

class form_CreateUser(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password')
    role = SelectField('Role',\
        choices=[(CONST.role_admin, 'Administrator'),\
                (CONST.role_standard, 'Standard User'),\
                (CONST.role_readonly, 'Read Only'),\
                (CONST.role_inactive, 'Inactive')\
                ])

    def populate(self, thisUser):
        '''
        Populates the fields of the form with the data currently
        in the user given.

        Parameters: a user object
        '''
        self.firstname.default = thisUser.first
        self.lastname.default = thisUser.last
        self.email.default = thisUser.email
        self.password.default = ""
        self.role.default = thisUser.role
        self.process()


@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def page_users():


    # Editor

    def edit_form(id):
        '''
        Returns the form back populated with the user information
        from the ID given.

        Parameters: id for a user.
        '''
        form = form_CreateUser()
        id=int(id)
        myUser = getUserById(id)
        form.populate(myUser)
        return form

    def allowEdit(id):
        '''
        Figures out if the current user should be allowed
        to edit the user object.

        Parameters: User ID for the user we want to edit
        '''
        if current_user.is_admin() or current_user.getID() == id:
            # Only admins can edit users
            # Users can edit themselves
            return True
        else:
            return False

    def isCurrentUser(id):
        '''
        Returns true if the userID given is that
        of the current logged in user.

        Parameters: userID
        '''
        return current_user.getID() == id
    # /Editor
    form = form_CreateUser()

    if request.method == 'POST' and form.validate():
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
    return render('listusers.html', form=form, users=users,
    edit_form=edit_form, allowEdit=allowEdit, isCurrentUser=isCurrentUser)

@app.route('/admin/users/<id>', methods=['POST'])
@login_required
def page_updateUser(id):
    id=int(id)
    myUser = getUserById(id)

    if request.method == 'POST':
        # the form has been filled out, import the data
        formdata = request.form
        firstname = formdata['firstname']
        lastname = formdata['lastname']
        email = formdata['email']
        role = formdata['role']
        password = formdata['password']

        if firstname != myUser.first:
            myUser.setFirstName(firstname)
        if lastname != myUser.last:
            myUser.setLastName(lastname)
        if email != myUser.email:
            myUser.setEmail(email)
        if role != myUser.role:
            myUser.setRole(role)
        if password != "":
            myUser.setPassword(password)

    return redirect(url_for('page_users'))

def getAllUsers():
    # returns all users in a list
    # users = []
    # for me in db.session.query(User):
    # 	users.append(me)
    return db.session.query(User)

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

def createUser(fn, ln, em, ro, pw):
    # Adds a user to the database.
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
