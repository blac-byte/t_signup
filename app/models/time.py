from .. import db


class time(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    start=db.Column(db.String(20),nullable=False)
    end=db.Column(db.String(20),nullable=False)
    slot_type=db.Column(db.String(10))

    def __init__(self,start,end,slot_type):
        self.start=start
        self.end=end
        self.slot_type=slot_type

