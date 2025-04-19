from flask import redirect, render_template, url_for, session, flash, request
from app import app
from app.forms import LoginForm, SignUpForm

#Sample test login for testing purposes
users = [
    {'email': 'admin@gmail.com', 'password': 'adminadminadmin'},
]

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_password = form.password.data

        #Check if the email and password match a user in the "database"
        if any(user['email'] == input_email and user['password'] == input_password for user in users):
            session['logged_in'] = True
            session['email'] = input_email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  #If user successful, then redirect to dashboard
        else:
            flash('Invalid email or password', 'error')  #Otherwise, show an error

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_password = form.password.data

        #If user account already created, then show error message
        if any(user['email'] == input_email for user in users):
            flash('Email is already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        #Add new user data to register if successful
        users.append({'email': input_email, 'password': input_password})
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('sign_up.html', form=form)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    #Make sure user is logged in before accessing the dashboard
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
