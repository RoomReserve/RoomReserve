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
    print()
    registered_user = User.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    print("Logged in as")
    print(registered_user)
    try:
        next = request.args.get('next')
    except:
        next = url_for('index')
    return redirect(next or url_for('index'))
