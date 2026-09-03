from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import timedelta
from flask_jwt_extended import(
create_access_token,
create_refresh_token,
JWTManager,
jwt_required,
unset_jwt_cookies,
set_access_cookies,
set_refresh_cookies,
get_jwt_identity
)
from flask_bcrypt import Bcrypt
#initialize environment variables
load_dotenv()
#initialize flask app
app=Flask(__name__)
#configure database
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
#initialize app with local database SQLAlchemy
db=SQLAlchemy(app)
#handle database schema changes
migrate=Migrate(app,db)
#configure jwt auth
#JWT SECRET KEY for signing JWT tokens
app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
#where to look for the token
#store it in the cookies
app.config['JWT_TOKEN_LOCATION']=['cookies']
#name for cookie
app.config['JWT_ACCESS_COOKIE_NAME']="access_token"
#sent cookies over HTTPS
app.config['JWT_COOKIE_SECURE']=False #true in production
#csrf protection for JWT
app.config['JWT_COOKIE_CSRF_PROTECT']=False #true in production
#prevent JS access
app.config['JWT_COOKIE_HTTPONLY']=False #true in production
#jwt expiration
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=15)
#samesite cookie setting
#allow only same site domains 
app.config['JWT_COOKIE_SAMESITE']='Lax' #Strict in production
#refresh tokens
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(days=1)
#initialize app with JWT
jwt=JWTManager()
#initialize app with Bcrypt
bcrypt=Bcrypt()
bcrypt.init_app(app)
@app.route("/")
def hello():
    return 'Hello world'
#register a user
@app.post("/api/v1/auth/register")
def register():
    #get json data
    data=request.get_json()
    print("Data: ",data)
    if not data:
        return jsonify({
            "error":"JSON body required"
        }),400
    #get username
    username=data.get("username")
    print("Username: ",username)
    #get email
    email=data.get("email")
    print("Email address: ",email)
    #get password
    password=data.get("password")
    print("Password: ",password)
    #confirm password
    # confirm_password=data.get("confirm_password")
    # print("Confirm password: ",confirm_password)
    #bad request status code 400
    if not username or not email:
        return jsonify({
            "error":"Username and Email are required"
        }),400
    existing_user=User.query.filter_by(email=email).first()
    #conflicting request ie status code 409
    if existing_user:
        return jsonify({
            "error":"Email already registered"
        }),409
    # hash password
    hashed_password=bcrypt.generate_password_hash(password)
    #save user to the database
    user=User(username=username,email=email,password=hashed_password)
    #save changes
    db.session.add(user)
    db.session.commit()
    #request created successfully status code 201
    return jsonify({
        "message":"User created successfully",
        "user":{
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "password":user.password
        }
    }),201

#login user
@app.post("/api/v1/auth/login")
def login():
    #get json data
    data=request.get_json()
    #check if username exist
    username=data.get("username")
    print("User username: ",username)
    # #check email
    # email=data.get("email")
    # print("User email: ",email)
    #check password if correct
    password=data.get("password")
    print("User password: ",password)
    if not username or not password:
        return jsonify({
            "error":"Provide a username and password"
        }),400
    #get current user
    user=User.query.filter_by(username=username).first()
    #check if invalid credentials
    #status code 401 for unauthorized access
    if not user:
        return jsonify({
            "error":"Invalid username"
        }),401
    if not check_password_hash(user.password,password):
        return jsonify({
            "error":"Invalid credentials"
        }),401
    #create access token
    access_token=create_access_token(identity=str(user.id))
    return jsonify({
        "username":user.username,
        "password":user.password,
        "access_token":access_token
    }),200

# # users 
# @app.get("/api/v1/users/<id>")
# def users(id):
#     if id:
#         try:
#             id=int(id)
#         except ValueError:
#             return jsonify({
#                 "error":"Id must be an integer"
#             }),400
#         return jsonify({
#             "error":"User not found"
#         }),404


#     #
#     # id=request.args.get("id")
#     return 'Users'

# expenses 
@app.get("/api/v1/expenses")
def expenses():
    return 'Expenses'
#user model
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    #connect expenses to the owner
    expenses=db.relationship("Expenses",back_populates="owner")


#expenses model
class Expenses(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    amount=db.Column(db.Float)
    category=db.Column(db.String(50))
    description=db.Column(db.String(100))
    #foreign key ie points to the primary key of another table
    user_id=db.Column(db.Interval,db.ForeignKey("user.id"))
    #connect owner to the expenses ie know who owns which expenses
    owner=db.relationship("User",back_populates="expenses")
    
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)