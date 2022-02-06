from __main__ import app
from db import db
from flask import Flask, request, jsonify, make_response
from models.users import UserModel
from models.topic import TopicModel
from models.questions import QuestionModel
from models.answer import AnswerModel
from routes.auth import token_required
import json
from  werkzeug.security import generate_password_hash

@app.route('/', methods=["GET"])
def check_flask():
    return 'Flask is Working'

@app.route('/user_list',methods=['GET'])
@token_required
def get_user_list(current_user):
    users = UserModel.query.filter_by().all()
    user_list = [{
        'Username':user.username,
        'Type':user.type,
        'AverageMarks':user.avg_marks if user.type=='student' else 'Not Applicable',
        'TotalExams':user.exam_count if user.type=='student' else 'Not Applicable',
    } for user in users]
    return jsonify({'users': user_list})


@app.route('/edit_user',methods=['PUT'])
@token_required
def edit_user(current_user):
    values = json.loads(request.data)
    user = UserModel.query.filter(UserModel.username==values['username']).first()
    if values.get('password',False):
        user.password = generate_password_hash(values.get('password', False))
    db.session.commit()
    return make_response(jsonify({'message': 'User Update successfully'}), 200)

@app.route('/delete_user',methods=['DELETE'])
@token_required
def delete_user(current_user):
    values = json.loads(request.data)
    user = UserModel.query.filter(UserModel.username==values['username']).first()
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({'message':'User deleted Successfully'}), 200)

@app.route('/add_topic', methods=["POST"])
@token_required
def add_topic(current_user):
    values = json.loads(request.data)
    if values.get('name', False):
        topic = TopicModel(
            name=values.get('name', False)
        )
        db.session.add(topic)
        db.session.commit()
        return make_response(jsonify({'message': 'Topic Added Successfully'}), 200)
    else:
        return make_response(jsonify({'message': 'Name can not be blank'}), 404)

@app.route('/topic_list',methods=['GET'])
@token_required
def get_topic_list(current_user):
    topics = TopicModel.query.filter_by().all()
    topic_list = [{
        'name':topic.name,
    } for topic in topics]
    return jsonify({'Topics': topic_list})

@app.route('/edit_topic', methods=["PUT"])
@token_required
def edit_topic(current_user):
    values = json.loads(request.data)
    if values.get('name',False) and values.get('new_name',False):
        topic = TopicModel.query.filter(TopicModel.name==values['name']).first()
        topic.name = values['new_name']
        db.session.commit()
        return make_response(jsonify({'message': 'Topic Updated Successfully'}), 200)
    return make_response(jsonify({'message': 'Name and New Name can not be blank'}), 200)

@app.route('/delete_topic',methods=['DELETE'])
@token_required
def delete_topic(current_user):
    values = json.loads(request.data)
    topic = TopicModel.query.filter(TopicModel.name==values['name']).first()
    db.session.delete(topic)
    db.session.commit()
    return make_response(jsonify({'message': 'Topic deleted Successfully'}), 200)


@app.route('/add_question', methods=["POST"])
@token_required
def add_question(current_user):
    values = json.loads(request.data)
    topic = TopicModel.query.filter_by(name=values['topic']).first()
    if not topic:
        return make_response(jsonify({'message':'Topic not found in database'}), 404)
    if values.get('name', False):
        question = QuestionModel(
            name=values.get('name', False),
            topic_id=topic.id,
        )
        db.session.add(question)
        db.session.commit()
        ans1 = AnswerModel(
            name=values['ans1'],
            is_true=True if values['true_ans'] == 'ans1' else False
        )
        db.session.add(ans1)
        question.answer_ids.append(ans1)
        ans2 = AnswerModel(
            name=values['ans2'],
            is_true=True if values['true_ans'] == 'ans2' else False
        )
        db.session.add(ans2)
        question.answer_ids.append(ans2)
        ans3 = AnswerModel(
            name=values['ans3'],
            is_true=True if values['true_ans'] == 'ans3' else False
        )
        db.session.add(ans3)
        question.answer_ids.append(ans3)
        ans4 = AnswerModel(
            name=values['ans4'],
            is_true=True if values['true_ans'] == 'ans4' else False
        )
        db.session.add(ans4)
        question.answer_ids.append(ans4)
        db.session.commit()

        return make_response(jsonify({'message': 'Question and Answer Added Successfully'}), 200)
    else:
        return make_response(jsonify({'message': 'Name can not be blank'}), 404)


@app.route('/question_list',methods=['GET'])
@token_required
def get_question_list(current_user):
    questions = QuestionModel.query.filter_by().all()
    question_list = []
    for que in questions:
        true_ans = AnswerModel.query.filter(AnswerModel.id.in_([i.id for i in que.answer_ids]),AnswerModel.is_true).first()
        question_list.append({'name':que.name,'ans1':que.answer_ids[0].name,'ans2':que.answer_ids[1].name,'ans3':que.answer_ids[2].name,'ans4':que.answer_ids[3].name,'Correct Answer':true_ans.name})
    return jsonify({'Questions': question_list})


@app.route('/choose_topic',methods=['POST'])
@token_required
def chose_topic(current_user):
    values = json.loads(request.data)
    topic = TopicModel.query.filter_by(name=values['topic']).first()
    if not topic:
        return make_response(jsonify({'message': 'Topic not found in database'}), 404)
    current_user.current_topic_id = topic.id
    question_ids = QuestionModel.query.filter(QuestionModel.topic_id == topic.id).all()
    question_list = []
    for que in question_ids:
        question = {'Question':que.name,
         'Options':[{
             'answer': ans.name,
         } for ans in que.answer_ids]}
        question_list.append(question)
    return make_response(jsonify(question_list),200)

@app.route('/check_answer',methods=['POST'])
@token_required
def check_answer(current_user):
    values = json.loads(request.data)
    count=0
    if values.get('questions',False):
        for que in values['questions']:
            question = QuestionModel.query.filter(QuestionModel.name == que['name']).first()
            ans = AnswerModel.query.filter(AnswerModel.name == que['answer']).first()
            if question and ans and ans.is_true and ans.id in [i.id for i in question.answer_ids]:
                count+=1
            if not question or not ans:
                return make_response(jsonify({'message':'Question or answer not found in database'}),404)
        current_user.exam_count = current_user.exam_count + 1
        current_user.avg_marks = (current_user.avg_marks+count)/current_user.exam_count
        db.session.commit()
        return make_response(jsonify({'Message':'Your score is %s'%count}),200)
    return make_response(jsonify({'message':'please check your input'}),404)
