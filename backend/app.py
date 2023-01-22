from random import randint
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user, UserMixin, LoginManager
from map_func import isclose, string_to_tup
import datetime
import requests
import base64

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'asdfghjkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

# Creating models for database
class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    current_activity = db.Column(db.String(200))
    date_login = db.Column(db.DateTime(), default = None)
    score = db.Column(db.Integer, default = 0)

    def __repr__(self) -> str:
        return f"User(name={self.name})"

class HistoryModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    activity = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    date_complete = db.Column(db.DateTime(timezone = True), default = func.now())
    image_url = db.Column(db.String(300), nullable = False)

    def __repr__(self) -> str:
        return f'History(activity = {self.activity}, location = {self.location}, date_complete = {self.date_complete})'

class ActivityModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = False)

    def __repr__(self) -> str:
        return f'Activity(name = {self.name}, location = {self.location}, description = {self.description})'

with app.app_context():
    db.create_all()

# Defining the main request parsers

login_post_args = reqparse.RequestParser()
login_post_args.add_argument("name", type=str, help="Name of the user is required", required=True)
login_post_args.add_argument("password", type=str, help="Password required", required=True)

register_post_args = reqparse.RequestParser()
register_post_args.add_argument("name", type=str, help="Name of the user is required", required=True)
register_post_args.add_argument("password", type=str, help="Password required", required=True)
register_post_args.add_argument("confirm-password", type=str, help="Password confirmation required", required=True)

activity_post_args = reqparse.RequestParser()
activity_post_args.add_argument('name', type= str, help="Name of activity required", required = True)
activity_post_args.add_argument('location', type= str, help="Location of activity required", required = True)
activity_post_args.add_argument('description', type = str, help="Description required", required = True)

image_post_args = reqparse.RequestParser()
image_post_args.add_argument("image", type=str, help="Base64 encoded image string", required=True, location='json')

# Resource fields

activity_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'description': fields.String
}

history_resource_fields = {
    'id': fields.Integer,
    'user-id': fields.Integer,
    'activity': fields.String,
    'location': fields.String,
    'description': fields.String,
    'image-url': fields.String
}

# Resources
class Login(Resource):
    def post(self):
        args = login_post_args.parse_args()
        user = UserModel.query.filter_by(name = args['name']).first()
        if not user:
            abort(404, message="could not find user")
        elif not check_password_hash(user.password, args['password']):
            abort(404, message="incorrect password")
        else:
            login_user(user=user, remember= True)
            print(current_user.date_login)
            return jsonify(success=True)

class Register(Resource):
    def post(self):
        args = register_post_args.parse_args()
        user = UserModel.query.filter_by(name = args['name']).first()
        if user:
            abort(404, message="username already exists")
        if args['password'] != args['confirm-password']:
            abort(404, message="passwords do not match")
        new_user = UserModel(name = args['name'], password = generate_password_hash(args['password']), )
        db.session.add(new_user)
        db.session.commit()
        login_user(user = new_user, remember= True)
        return jsonify(success=True)

class Activity(Resource):
    @login_required
    @marshal_with(activity_resource_fields)
    def get(self):
        print(current_user.date_login)
        if not current_user.date_login or datetime.datetime.now().strftime('%d/%m/%Y') != current_user.date_login.strftime('%d/%m/%Y'):
            print(current_user.date_login)
            activities = ActivityModel.query.filter_by().all()
            rand_id = randint(0, len(activities))
            rand_activity = ActivityModel.query.filter_by(id = rand_id).first()
            current_user.current_activity = rand_activity.name
            current_user.date_login = func.now()
            db.session.commit()
        return ActivityModel.query.filter_by(name = current_user.current_activity).first()

class History(Resource):
    @login_required
    @marshal_with(history_resource_fields)
    def get(self):
        history = HistoryModel.query.filter_by(user_id = current_user.id).all()
        return history
    @login_required
    def post(self, location):
        activity = ActivityModel.query.filter_by(name = current_user.current_activity)
        image = image_post_args.parse_args(strict=True).get("image", None)
        if isclose(location, string_to_tup(activity.location)):
            with open("new_image.jpg","wb") as new_file:
                new_file.write(base64.decodebytes(image))
            url = "//api.estuary.tech/content/add"
            payload={}
            files = [('data',('file', open('new_image.jpg','rb'),'application/octet-stream'))]
            headers = {'Accept': 'application/json','Authorization': 'Bearer EST44af082e-cf73-4b71-bc2d-fe8f00cb7671ARY'}
            response = requests.request("POST", url, headers=headers, data=payload,files = files)
            url = "https://gateway.estuary.tech/gw/ipfs/" + response['cid']
            new_history = HistoryModel(user_id = current_user.id, activity = activity.name, location = activity.location, description = activity.description, image_url = url)
            current_user.score += 50
            db.session.add(new_history)
            db.session.commit()
            return jsonify(success = True)
        else:
            return abort(404, message = "Not close to location")


class ActivityAdder(Resource):
    def post(self):
        args = activity_post_args.parse_args()
        new_activity = ActivityModel(name= args['name'], location= args['location'], description= args['description'])
        db.session.add(new_activity)
        db.session.commit()
        return jsonify(success = True)
    
    @marshal_with(activity_resource_fields)
    def get(self):
        activities = ActivityModel.query.filter_by().all()
        return activities  

api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(ActivityAdder, "/addactivity")
api.add_resource(Activity, "/activity")
api.add_resource(History, '/history')

if __name__ == '__main__':
    app.run(debug=True)

