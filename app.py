from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anything_will_be_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
nav = Nav()
nav.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(25))
    password = db.Column(db.String(80))


@nav.navigation()
def mynavbar():
    return Navbar(
        'Used Car Price Prediction',
        View('Home', 'index'),
        View('Predict', 'predict'),
        View('Log In', 'login'),
        View('Log Out', 'logout')
    )


if __name__ == '__main__':
    app.run()
    db.create_all()


import routes
