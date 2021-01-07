from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'dev'
    
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chichi30@localhost/Game Survey'
else:
    app.debug == False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLAlCHEMY_TRACK-MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    age = db.Column(db.Integer)
    genre = db.Column(db.String(200))
    hours_played = db.Column(db.String(200))
    favorite = db.Column(db.String)
    comments = db.Column(db.Text())

    def __init__(self, name, email, age, genre, hours_played, favorite, comments):
        self.name = name
        self.email = email
        self.age = age
        self.genre = genre
        self.hours_played = hours_played
        self.favorite = favorite
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        genre = request.form['genre']
        hours_played = request.form['hours-played']
        favorite = request.form['favorite']
        comments = request.form['comment']
        #print(name, email, age, genre, hours_played, favorite, comments )



        if db.session.query(Feedback).filter(Feedback.name == name).count() == 0 and db.session.query(Feedback).filter(Feedback.email == email).count() == 0:
            data = Feedback(name, email, age, genre, hours_played, favorite, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already taken this survey!')
if __name__=='__main__':
    
    app.run()