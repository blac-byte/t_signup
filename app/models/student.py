# app/models/student.py

from .. import db
from flask_login import UserMixin



class student(db.Model, UserMixin):
    reg_id=db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    batch=db.Column(db.String(10), unique=False, nullable=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.Text, nullable=True)

    def get_id(self):
        return str(self.reg_id)
    


