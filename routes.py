import json

from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from brain import input_process, make_predict, get_makes, data, get_cars
from charts import info
from form import inputForm, set_years, RegisterForm, LoginForm
from app import app, User, db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', info=info)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = inputForm()
    if request.method == 'POST':
        year = form.year.data
        odometer = form.odometer.data
        make = form.make.data
        model = form.model.data
        transmission = form.transmission.data

        car = {'year': year, 'odometer': '{:,}'.format(odometer), 'make': make, 'model': model, 'transmission': transmission}
        info = input_process(year, odometer, make, model, transmission)
        predicted_list = make_predict(info)
        return render_template('result.html', car=car, predictions=predicted_list)

    form.year.choices = set_years()
    form.make.choices = get_makes(data)
    return render_template('predict.html', form=form, name=current_user.username)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')

        existing_member = User.query.filter_by(email=form.email.data).first()
        if existing_member:
            flash("You have an account with this email. Please log in.")
            return redirect(url_for('login'))

        else:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('predict'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('predict'))
        flash("Invalid username or password !")
    return render_template('login.html', form=form)


@app.route('/predict/<string:make>')
def find_models(make):
    cars = get_cars(data)
    models = []

    for model in cars[make]:
        models.append(model)
    return jsonify({'models': models})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/forget')
def forget():
    return render_template('forget.html')
