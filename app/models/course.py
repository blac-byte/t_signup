from .. import db



class course(db.Model, ):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_id=db.Column(db.Integer, unique=True, nullable=True)
    course_type=db.Column(db.String(3), unique=False)
    building=db.Column(db.String(10), unique=False, nullable=True)
    room=db.Column(db.String(10), unique=False, nullable=True)
  

    def __init__(self,course_id,course_type,building,room):
        self.course_id=course_id
        self.course_type=course_type
        self.building=building
        self.room=room