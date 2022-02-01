from db import db


class AnswerModel(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True)
    is_true = db.Column(db.Boolean())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('QuestionModel')

