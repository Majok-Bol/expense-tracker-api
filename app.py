from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
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
@app.route("/")
def hello():
    return 'Hello world'
# users 
@app.get("/api/v1/users")
def users():
    # id=request.args.get("id")
    return 'Users'

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


#expenses model
class Expenses(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    amount=db.Column(db.Float)
    category=db.Column(db.String(50))
    description=db.Column(db.String(100))
    
if __name__=="__main__":
    app.run(debug=True)