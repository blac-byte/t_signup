# app/models/course.py

from .. import db


class course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(20), unique=False, nullable=False)  # Changed to String and unique=False
    course_type = db.Column(db.String(3), unique=False)
    batch = db.Column(db.String(10), unique=False)
    building = db.Column(db.String(10), unique=False, nullable=True)
    room = db.Column(db.String(10), unique=False, nullable=True)

    def __init__(self, course_id, course_type, batch, building, room):
        self.course_id = course_id
        self.course_type = course_type
        self.batch = batch
        self.building = building
        self.room = room

    @staticmethod
    def insert_sample_courses():
        if course.query.first():
            return
        courses = [
            course(course_id="BAEEE101", course_type="ETH", batch='ALL03', building="PRP", room="105"),
            course(course_id="BACSE103", course_type="ETH", batch='ALL03', building="PRP", room="105"),
            course(course_id="BAMAT101", course_type="ETH", batch='ALL03', building="PRP", room="105"),
            course(course_id="BACHY105", course_type="ETH", batch='ALL03', building="PRP", room="105"),
            course(course_id="BAMAT101", course_type="ELA", batch='ALL03', building="PRP", room="445"),
            course(course_id="BACSE101", course_type="LO", batch='ALL03', building="PRP", room="117A"),
            course(course_id="BACHY105", course_type="ELA", batch='ALL03', building="PRP", room="G07"),
            course(course_id="BACSE103", course_type="ELA", batch='ALL03', building="PRP", room="356"),
            course(course_id="BAEEE101", course_type="ELA", batch='ALL03', building="PRP", room="355"),
        ]

        for i in courses:
            db.session.add(i)
        db.session.commit()
