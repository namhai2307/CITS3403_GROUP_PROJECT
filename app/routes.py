from flask import redirect, render_template, url_for, session, flash, request
from app import app
from app.forms import LoginForm, SignUpForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')

#Sample username list to simulate the "database" for login
users = [
    {'username': 'admin@gmail.com', 'password': 'adminadminadmin'},
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_password = form.password.data

        #Check if user supplied correct username and password
        if any(user['username'] == input_email and user['password'] == input_password for user in users):
            session['logged_in'] = True
            session['username'] = input_email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  #If user login successful, then redirect to dashboard
        else:
            flash('Invalid email or password', 'error')  #Otherwise, show an error message

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        #if account created properly, then success
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    #Make sure if user is logged before entering the dashboard
    if not session.get('logged_in'):
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
