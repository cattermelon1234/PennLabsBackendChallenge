from app import db
#from flask_login import UserMixin
#from flask_wtf import wtforms
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import InputRequired, Length, ValidationError
meta = db.metadata

Club_Categories=db.Table(
    'Club_Categories', meta,
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('club_code', db.String, db.ForeignKey('clubs.code')),
    db.Column('tag_name', db.String, db.ForeignKey('tags.name'))
)

#pass in UserMixin
class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(80), nullable=False)

class Club(db.Model):
    __tablename__ = "clubs"
    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    likes = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=Club_Categories, back_populates='clubs')

    def __repr__(self):
        return '<Club %r>' % self.name


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    clubs = db.relationship('Club', secondary=Club_Categories, back_populates='tags')

    def __repr__(self):
        return '<Tag %r>' % self.name

#UNFINISHED USER AUTHENTICATION CODE    
"""
db.create_all()
print('hi2')
PreProfessional = Tag(name="Pre-Professional")
Athletics = Tag(name="Athletics")

PennMemes = Club("penn-memes", "Penn Memes Club", "this is my description", 0, tags=[PreProfessional, Athletics])
db.session.add(PreProfessional, Athletics, PennMemes)
db.session.commit()
"""