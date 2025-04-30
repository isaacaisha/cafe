from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import random
import json
import time
from datetime import datetime
from pprint import pprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import (
    RegistrationForm, LoginForm, SearchCafeForm,
    UpdateCafePriceForm, AddCafeForm, DeleteCafeForm, DeleteUserForm
)
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'cafes.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
time_sec = time.localtime()
current_year = time_sec.tm_year
dt_now = datetime.now()
current_time = dt_now.strftime("%a %d %B")

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role     = db.Column(db.String(20), default='user', nullable=False)
    cafes_   = relationship("Cafe", back_populates="author")

class Cafe(db.Model):
    __tablename__ = 'cafes'
    id              = db.Column(db.Integer, primary_key=True)
    author_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    author          = relationship("User", back_populates="cafes_")
    name            = db.Column(db.String(250), unique=True, nullable=False)
    map_url         = db.Column(db.String(500), nullable=False)
    img_url         = db.Column(db.String(500), nullable=False)
    location        = db.Column(db.String(250), nullable=False)
    seats           = db.Column(db.String(250), nullable=False)
    has_toilet      = db.Column(db.Boolean, nullable=False)
    has_wifi        = db.Column(db.Boolean, nullable=False)
    has_sockets     = db.Column(db.Boolean, nullable=False)
    can_take_calls  = db.Column(db.Boolean, nullable=False)
    coffee_price    = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('assets/images/favicon.ico')

@app.route('/')
def home():
    cafes = Cafe.query.all()
    if cafes:
        return render_template('index.html', cafes=cafes, date=current_time, year=current_year)
    else:
        error_message = 'Sorry No Cafes found 😭 ¡!¡'
        return render_template('index.html', error_message=error_message, date=current_time, year=current_year)

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    return render_template('cafe_detail.html', cafe=cafe, date=current_time, year=current_year)

@app.route('/random')
def get_random_cafe():
    cafes = Cafe.query.all()
    if not cafes:
        flash('No cafés available.', 'info')
        return redirect(url_for('home'))
    random_cafe = random.choice(cafes)
    return render_template('random_cafe.html', random_cafe=random_cafe, date=current_time, year=current_year)

@app.route('/search', methods=['GET', 'POST'])
def search_cafes_by_location():
    form = SearchCafeForm()
    error_message = None
    cafes = []

    # Only on a POST (and valid form) do we actually search
    if request.method == 'POST' and form.validate_on_submit():
        # Grab the raw string from the form
        query_location = form.loc.data

        # Fresh DB lookup
        cafes = Cafe.query.filter_by(location=query_location).all()

        if cafes:
            # success—‘cafes’ will be non-empty for the template
            print(json.dumps({"Cafe by location 👍🏿":[c.to_dict() for c in cafes]}, indent=4))
        else:
            # no results—set an error message
            error_message = f"Sorry, we don't have cafes in '{query_location}'."
            print(error_message)

    # On GET (or invalid POST) we simply show the form, plus whatever 'cafes' and 'error_message' we built
    return render_template(
        'search.html',
        form=form,
        cafes_by_location=cafes,
        error_message=error_message,
        date=current_time,
        year=current_year
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", "warning")
            return redirect(url_for('login'))
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Welcome, {new_user.username}!", "success")
        return redirect(url_for('home'))
    return render_template('register.html', form=form, date=current_time, year=current_year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password. Please try again.", "danger")
            return render_template('login.html', form=form, date=current_time, year=current_year)
        if form.secret_code.data == 'siisi321' and user.role != 'admin':
            user.role = 'admin'
            db.session.commit()
            flash("Admin access granted!", "info")
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form, date=current_time, year=current_year)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Only admins allowed.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/add', methods=['GET', 'POST'])
@admin_required
def add_new_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        if Cafe.query.filter_by(name=form.name.data).first():
            flash('Cafe name exists.', 'warning')
            return render_template('add_cafe.html', form=form, date=current_time, year=current_year)
        new_cafe = Cafe(
            author_id=current_user.id,
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.loc.data,
            seats=form.seats.data,
            has_toilet=form.toilet.data,
            has_wifi=form.wifi.data,
            has_sockets=form.sockets.data,
            can_take_calls=form.calls.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafe_detail', cafe_id=new_cafe.id))
    return render_template('add_cafe.html', form=form, date=current_time, year=current_year)

@app.route('/choose-cafe', methods=['GET'])
def choose_cafe():
    cafes = Cafe.query.all()
    return render_template('choose_cafe.html', cafes=cafes, date=current_time, year=current_year)

@app.route('/update-price/<int:cafe_id>', methods=['GET', 'POST', 'PATCH'])
@admin_required
def update_cafe_price(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    form = UpdateCafePriceForm()
    if form.validate_on_submit():
        cafe.coffee_price = form.new_price.data
        db.session.commit()
        flash(f"Price updated to {cafe.coffee_price}.", "success")
        return redirect(url_for('cafe_detail', cafe_id=cafe_id))
    return render_template('update_price.html', cafe=cafe, form=form, date=current_time, year=current_year)

@app.route('/delete-cafe', methods=['GET', 'POST'])
@admin_required
def delete_cafe():
    form = DeleteCafeForm()
    if form.validate_on_submit():
        cafe = Cafe.query.get(form.id.data)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            flash('Cafe deleted.', 'success')
        else:
            flash('Cafe not found.', 'warning')
    return render_template('delete.html', form=form, date=current_time, year=current_year)

@app.route('/delete-user', methods=['GET', 'POST'])
@admin_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = User.query.get(form.id.data)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted.', 'success')
        else:
            flash('User not found.', 'warning')
    return render_template('delete_user.html', form=form, date=current_time, year=current_year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
