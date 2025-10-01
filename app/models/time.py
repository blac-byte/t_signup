from .. import db


class time(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    column_id=db.Column(db.Integer)
    start=db.Column(db.String(20),nullable=False)
    end=db.Column(db.String(20),nullable=False)
    course_type=db.Column(db.String(10))

    def __init__(self,column_id,start,end,course_type):
        self.column_id=column_id
        self.start=start
        self.end=end
        self.course_type=course_type

