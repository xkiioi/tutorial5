from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm

# Create a Blueprint named "auth"
auth = Blueprint("auth", __name__)

# Route for user login
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if a user with the provided email exists
        user = User.query.filter_by(email=email).first()
        if user:
            # If the user exists, check if the provided password is correct
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True) # Log the user in
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Route for user registration
@auth.route("/sign-up", methods=('GET', 'POST'))
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    # Create a registration form instance
    form = RegistrationForm()
    # Validate form submission and create a new user if successful
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            (form.password.data), method='sha256')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form, user=current_user)

# Route for user logout (requires authentication)
@auth.route("/logout")
@login_required
def logout():
    logout_user() # Log the user out
    return redirect(url_for("views.home"))