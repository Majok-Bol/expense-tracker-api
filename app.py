from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#initialize flask app
app=Flask(__name__)
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
if __name__=="__main__":
    app.run(debug=True)