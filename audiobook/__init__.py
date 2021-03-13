from flask import Flask, url_for
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
import os, shutil
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta

app = Flask(__name__)
cors = CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["12 per second",]
)
api = Api(app)
# app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
app.config['MONGO_URI'] = os.getenv('MONGO')
app.config["JWT_COOKIE_SECURE"] = True
app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_JWT')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)
mongo = PyMongo(app)
db = mongo.db

# print(db.Users.find_one({'first_name':'abhyam'}))
# db.Users.insert_one({'some':'thing'})

# try:
#     db = connector.connect(
#             host=os.getenv('HOST'),
#             user=os.getenv('USER'),
#             port=int(os.getenv('PORT')),
#             passwd=os.getenv('PASS'),
#             database=os.getenv('BATABASE')
#             )
#     # cursor = mydb.cursor(buffered=True)
#     # q = "CREATE TABLE Users(UID TEXT, UserName INTEGER)"
#     #
#     # cursor.execute(q)
#     print('********Successfully connected to database********')
#
# except mysql.connector.Error as err:
#     # if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     #     print("Something is wrong with your user name or password")
#     # elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     #     print("Database does not exist")
#     # else:
#     print(err)

@app.route('/')
def hdfd():
    return f"Running... {get_remote_address()}"

from audiobook.Resources import users
api.add_resource(users.UserRegistration, '/registerUser')
api.add_resource(users.UserLogin, '/loginUser')
# api.add_resource(user.UserLogin, '/login')
# api.add_resource(user.UserProfile, '/profile/<string:username>')
# api.add_resource(user.UserProfileUpdate, '/edit/profile')
# api.add_resource(user.TokenRefresh, '/refreshToken')
# api.add_resource(user.User, '/profile')
# api.add_resource(user.UserReset, '/reset/<string:username>')
# api.add_resource(user.UserVerify, '/verify/<string:username>')
# api.add_resource(user.ChangeProfilePic, '/edit/profile/pic')
# api.add_resource(saman.addSaman, '/add')
# api.add_resource(saman.SingleSaman, '/saman/<string:id>')
# api.add_resource(saman.listallsaman, '/saman')
# api.add_resource(saman.userSaman, '/myposts')
# api.add_resource(saman.flagsaman, '/flag/<string:id>')
# entertainment
# api.add_resource(entertainment.addEntertainmentrResource, '/entertainment/add')
