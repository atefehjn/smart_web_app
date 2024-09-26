# routes.py
from flask import render_template, redirect, url_for, flash, Blueprint, abort, session
from .forms import RegistrationForm, SignInForm
from flask import request
from .models import db, User, bcrypt
from flask_login import login_user, logout_user, login_required, current_user


bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("main.signin"))
    else:
        flash("Username already exists. Please choose a different one.", "danger")
    return render_template("register.html", form=form)


@bp.route("/signin", methods=["GET", "POST"])
def signin():
    form = SignInForm()  # Initialize the form object
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if form.validate_on_submit():  # This checks if the form is submitted and valid
        username = form.username.data  # Accessing data from the form
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Login failed. Please check your username and password", "danger")

    return render_template("signin.html", form=form)  # Pass form to template


@bp.route("/input_page")
@login_required
def input_page():
    return render_template("input_page.html")


@bp.route("/prediction_results")
@login_required
def prediction_results():
    return render_template("prediction_results.html")


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
