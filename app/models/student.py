from .. import db
from flask_login import UserMixin



class student(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.Text,nullable=True)

    def __init__(self,email,password):
        self.email=email
        self.password=password

