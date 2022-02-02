from db import db


class TopicModel(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True)
    question_ids = db.relationship('QuestionModel', lazy='dynamic')
