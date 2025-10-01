# app/models/time.py

from .. import db


class classes(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_id=db.Column(db.Integer, db.ForeignKey('student.reg_id'))                 
    course_id=db.Column(db.String(20), nullable=False) #             for now, change in future
    course_type=db.Column(db.String(10))
    day=db.Column(db.String(3))
    column_id=db.Column(db.Integer)

    student = db.relationship('student', backref='classes')


    def __init__(self, reg_id, course_id, course_type, day, column_id):
        self.reg_id=reg_id
        self.course_id=course_id
        self.course_type=course_type
        self.day=day
        self.column_id=column_id
