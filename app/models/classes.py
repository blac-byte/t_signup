from .. import db


class classes(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    reg_id=db.Column(db.String(20),nullable=False)
    course_id=db.Column(db.String(20),nullable=False)
    course_type=db.Column(db.String(10))

    def __init__(self,reg_id,course_id,course_type):
        self.reg_id=reg_id
        self.course_id=course_id
        self.course_type=course_type

