from RoomReserve import *
from functools import wraps

class Form_Login(Form):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        # Loading this page, send back the form
        return render('login.html')


    # The form has been filled out, process input.
    email = request.form['email']
    password = request.form['password']

    # Find the user with the given email address
    registered_user = User.query.filter_by(email=email).first()

    if registered_user is not None:
        # A user with the given email was found.
        if not registered_user.check_password(password):
            # wrong password
            print("User password does not match", password)
            return redirect(url_for('login'))
        if registered_user.is_inactive():
            # This user has a role of inactive
            return render('basic.html', content="Your account is inactive.")
    else:
        # No user with the given email was found.
        print("No such user " + email)
        return redirect(url_for('login'))

    login_user(registered_user)
    try:
        # Allows a redirect to the requested page (if applicable) after login
        next = request.args.get('next')
    except:
        next = url_for('index')
    return redirect(next or url_for('index'))

@app.route('/login/switch')
def switchUser():
    # Logs out the current user and lets a new user log in
    logout_user()
    return redirect(url_for('login'))

def admin_required(function):
    # Admin role is required to access this page
    # Use: as a decorator
    #     @Login.admin_required
    @login_required
    @wraps(function)
    def checkIfAdmin(*args, **kwargs):
        if current_user.is_admin():
            # If the user is an admin, then return the requested page
            return function(*args, **kwargs)
        # User does not have sufficient privleges to access this page
        print("Insufficent privleges.")
        return render('basic.html', content=\
        "Your permission level is "+current_user.getRole()+\
        ". You must be an Administrator to do this.<br />"+\
        "<a href="+url_for('switchUser')+">Login as another user</a>.")
    return checkIfAdmin

def standard_required(function):
    # Standard role is or above required to access this page
    # Use: as a decorator
    #     @Login.standard_required
    @login_required
    @wraps(function)
    def checkIfStandard(*args, **kwargs):
        if current_user.is_standard():
            # If the user is a standard user or above, then return the requested page
            return function(*args, **kwargs)
        # User does not have sufficient privleges to access this page
        flash("Insufficent privleges.")
        return render('basic.html', content=\
        "Your permission level is "+current_user.getRole()+\
        ". You must be a Standard User or Administrator to do this.<br />"+\
        "<a href="+url_for('switchUser')+">Login as another user</a>.")
    return checkIfStandard
