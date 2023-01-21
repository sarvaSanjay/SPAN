from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user, UserMixin, LoginManager

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

# Resource fields

activity_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'description': fields.String
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
            user.date_login = func.now()
            login_user(user=user, remember= True)
            resp = {'message': 'login successful'}
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
    def get(self):
        activities = ActivityModel.query.filter_by().all()
        return jsonify({'length': len(activities)})
    def post(self):
        pass

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

if __name__ == '__main__':
    app.run(debug=True)

