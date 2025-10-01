from .. import db
from flask_login import UserMixin



class student(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    reg_id=db.Column(db.Integer, unique=True, nullable=True)
    batch=db.Column(db.String(10), unique=False, nullable=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.Text,nullable=True)

    def __init__(self,reg_id,batch,email,password):
        self.reg_id=reg_id
        self.batch=batch
        self.email=email
        self.password=password

