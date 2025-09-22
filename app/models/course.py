from .. import db


class course(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    slot_id=db.Column(db.String(20),nullable=False)
    course_name=db.Column(db.String(20),nullable=False)
    course_type=db.Column(db.String(10))
    course_room=db.Column(db.String(20),nullable=False)
    batch=db.Column(db.String(10))

    def __init__(self,slot_id,course_name,course_type,course_room,batch):
        self.slot_id=slot_id
        self.course_name=course_name
        self.course_type=course_type
        self.course_room=course_room
        self.batch=batch
