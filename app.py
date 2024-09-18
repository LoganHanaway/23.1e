from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, URL, NumberRange, AnyOf, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)

class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField('Photo URL', validators=[URL(require_tld=False), Optional()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30, message='Age must be between 0 and 30'), Optional()])
    notes = StringField('Notes')
    available = BooleanField('Available')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=form.available.data,
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_pet.html', pet=pet, form=form)

if __name__ == '__main__':
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)
    app.run(debug=True)
