from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catelogs.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False, index=True)
    avatar = db.Column(db.String(300))
    username = db.Column(db.String(80))


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
        }


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(1000))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'create_date': self.create_date,
        }
