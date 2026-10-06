from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Date, Text  
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from datetime import date
import os


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epl.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

class Club(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    stadium: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[date] = mapped_column(Date(), default=date.today())    

    players: Mapped[List['Player']] = relationship(back_populates='club')

    def __repr__(self):
        return f'<Club: {self.name}>'

class Player(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    nationality: Mapped[str] = mapped_column(String(25), nullable=False)
    position: Mapped[str] = mapped_column(String(25), nullable=False)
    shirt_number: Mapped[str] = mapped_column(String(10), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey(Club.id))
    created_at: Mapped[date] = mapped_column(Date(), default=date.today())   

    club: Mapped[Club] = relationship(back_populates='players')

    def __repr__(self):
        return f'<Player: {self.name}>'

@app.route('/')
def home():
    return render_template('index.html', title='Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/clubs')
def clubs():
    all_clubs = db.session.scalars(db.select(Club)).all()
    return render_template('clubs/index.html', title='Clubs Page', clubs=all_clubs)

@app.route('/clubs/<int:id>/details')
def club_detail(id):
    club = db.session.get(Club, id)
    return render_template('clubs/club_detail.html', title='Club Detail Page', club=club)

@app.route('/clubs/new_club', methods=['GET', 'POST'])
def new_club():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        stadium = request.form['stadium']
        image_url = request.form['image_url']

        club = Club(name=name, year=year, stadium=stadium, image_url=image_url)
        db.session.add(club)
        db.session.commit()

        return redirect(url_for('clubs'))

    return render_template('clubs/new_club.html', title='New Club Page')

@app.route('/clubs/<int:id>/edit_club', methods=['GET', 'POST'])
def edit_club(id):
    club = db.session.get(Club, id)
    if request.method == 'POST':
        
        stadium = request.form['stadium']
        

        club.stadium = stadium

        db.session.commit()

        return redirect(url_for('clubs'))

    return render_template('clubs/edit_club.html', title='Edit Club Page', club=club)

@app.route('/players')
def players():
    all_players = db.session.scalars(db.select(Player)).all()

    return render_template('players/index.html', title='Players Page', players=all_players)

@app.route('/players/<int:id>/details')
def player_detail(id):
    player = db.session.get(Player, id)
    return render_template('players/player_detail.html', title='Player Detail Page', player=player)

@app.route('/players/new_player', methods=['GET', 'POST'])
def new_player():
    all_clubs = db.session.scalars(db.select(Club)).all()
    if request.method == 'POST':
        name = request.form['name']
        nationality = request.form['nationality']
        position = request.form['position']
        shirt_number = request.form['shirt_number']
        image_url = request.form['image_url']
        club_id = request.form['club_id']

        player = Player(name=name, nationality=nationality, position=position, shirt_number=shirt_number, image_url=image_url, club_id=club_id)
        db.session.add(player)
        db.session.commit()
        
        return redirect(url_for('players'))

    return render_template('players/new_player.html', title='New Player Page', clubs=all_clubs)