from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from send_email import send_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5435/test'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Float, nullable=False)

    def __init__(self, email, height):
        self.email = email
        self.height = height

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def average_height(cls):
        return db.session.query(func.avg(cls.height)).scalar()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def success():
    email = request.form.get('email_name')
    height = request.form.get('height')
    data = Data(email=email, height=height)
    data.add_to_db()
    average_height = Data.average_height()
    send_email(email, average_height)
    #db.session.add(email, height)
    #db.session.commit()
    print(Data.average_height())
    #return f"Email: {email}, Height: {height}"
    return render_template('success.html', email=email, height=height)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

