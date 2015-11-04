from RoomReserve import *

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
        return render('login.html')

    email = request.form['email']
    password = request.form['password']

    registered_user = User.query.filter_by(email=email).first()

    if registered_user is not None:
        if not registered_user.check_password(password):
            # wrong password
            print("User password does not match", password)
            return redirect(url_for('login'))
        if registered_user.is_inactive():
            return render('basic.html', content="Your account is inactive.")
    else:
        print("No such user " + email)
        return redirect(url_for('login'))

    login_user(registered_user)
    flash('Logged in successfully')
    try:
        next = request.args.get('next')
    except:
        next = url_for('index')
    return redirect(next or url_for('index'))

@app.route('/login/switch')
def switchUser():
    logout_user()
    return redirect(url_for('login'))

def adminrequired(function):
    @login_required
    def checkIfAdmin(*args, **kwargs):
        if current_user.is_admin():
            return function(*args, **kwargs)
        return render('basic.html', content=\
        "Your permission level is "+current_user.getRole()+\
        ". You must be an Administrator to do this.<br />"+\
        "<a href="+url_for('switchUser')+">Login as another user</a>.")
    return checkIfAdmin

def standardrequired(function):
    @login_required
    def checkIfStandard(*args, **kwargs):
        if current_user.is_standard() or current_user.is_admin():
            return function(*args, **kwargs)
        return render('basic.html', content=\
        "Your permission level is "+current_user.getRole()+\
        ". You must be a Standard User or Administrator to do this.<br />"+\
        "<a href="+url_for('switchUser')+">Login as another user</a>.")
    return checkIfAdmin
