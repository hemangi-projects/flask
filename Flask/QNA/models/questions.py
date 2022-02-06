from db import db

answers = db.Table('answers',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), primary_key=True)
)


class QuestionModel(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('TopicModel',foreign_keys=[topic_id])
    answer_ids = db.relationship('AnswerModel', secondary=answers, lazy='subquery',
                           backref=db.backref('question', lazy=True))



