from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('art_id', db.Integer, db.ForeignKey('art.id'))
)

dislikes = db.Table('dislikes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('art_id', db.Integer, db.ForeignKey('art.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    type_of_account = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    arts = db.relationship('Art', backref='author', lazy=True)

    liked_arts = db.relationship('Art', secondary=likes, backref=db.backref('likes'), lazy='dynamic')
    disliked_arts = db.relationship('Art', secondary=dislikes, backref=db.backref('dislikes'), lazy='dynamic')

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "type_of_account": self.type_of_account,
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.type_of_account}')"

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)
    img_id = db.Column(db.String(20), nullable=False)
    img_extension = db.Column(db.String(5), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "img_id": self.img_id,
            "author": self.author.toJSON(),
            "date_posted": str(self.date_posted),
            "likes": [user.toJSON() for user in self.likes],
            "dislikes": [user.toJSON() for user in self.dislikes]
        }

    def __repr__(self):
        return f"{self.title}\n{self.description}\n{self.img_extenstion}\n{self.user_id}\n{str(self.date_posted)}"
        #return f"Art('{self.title}', {self.description}, {self.img_extension}, {self.user_id} ,'{self.date_posted}')"
