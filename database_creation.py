from script import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(64), unique=False, nullable=False)
    sender = db.Column(db.String(64), unique=False, nullable=False)
    date = db.Column(db.String(64), unique=False, nullable=False)
    time = db.Column(db.String(64), unique=False, nullable=False)
    title = db.Column(db.String(256), unique=False)
    message = db.Column(db.String(10240), unique=False, nullable=False)


db.create_all()
