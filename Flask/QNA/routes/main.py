from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=["GET"])
def check_flask():
    return {'Flask is Working'}

