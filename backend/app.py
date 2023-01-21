from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Creating models for database
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    current_activity = db.Column(db.String(200))
    date_login = db.Column(db.DateTime())
    score = db.Column(db.Integer, default = 0)

    def __repr__(self) -> str:
        return f"User(name={self.name})"

class HistoryModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    activity = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    date_complete = db.Column(db.DateTime(timezone = True), default = func.now())

    def __repr__(self) -> str:
        return f'History(activity = {self.activity}, location = {self.location}, date_complete = {self.date_complete})'

class ActivityModel(db.Model):
    name = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = False)

    def __repr__(self) -> str:
        return f'Activity(name = {self.name}, location = {self.location}, description = {self.description})'

# Defining the main request parsers

login_post_args = reqparse.RequestParser()
login_post_args.add_argument("name", type=str, help="Name of the user is required", required=True)
login_post_args.add_argument("password", type=str, help="Password required", required=True)

activity_post_args = reqparse.RequestParser()
activity_post_args.add_argument('name', type= str, help="Name of activity required", required = True)
activity_post_args.add_argument('location', type= str, help="Location of activity required", required = True)
activity_post_args.add_argument('description', type = str, help="Description required", required = True)
if __name__ == '__main__':
    app.run(debug=True)

