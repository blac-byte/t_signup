# app/models/time.py

from .. import db


class time(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_id=db.Column(db.Integer, db.ForeignKey('student.reg_id'))  
    column_id=db.Column(db.Integer)
    start=db.Column(db.String(20), nullable=False)
    end=db.Column(db.String(20), nullable=False)
    course_type=db.Column(db.String(10))

    student = db.relationship('student', backref='time')

    def __init__(self, reg_id, column_id, start, end, course_type):
        self.reg_id=reg_id
        self.column_id=column_id
        self.start=start
        self.end=end
        self.course_type=course_type

