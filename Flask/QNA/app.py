from db import db
from flask import Flask
from models import answer,exam,questions,topic,users


app = Flask(__name__)
import routes.main as main
from routes import auth
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'hemangi'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)