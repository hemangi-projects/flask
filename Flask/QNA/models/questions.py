from db import db


class QuestionModel(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('TopicModel')
    answer_ids = db.relationship('AnswerModel', lazy='dynamic')



