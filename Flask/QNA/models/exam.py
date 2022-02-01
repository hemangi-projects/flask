from db import db


class examModel(db.Model):
    __tablename__ = 'exam'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('TopicModel')
    total_marks = db.Column(db.Integer)


