from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import timedelta,datetime
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
from sqlalchemy import func
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
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
#where to look for the token
#store JWT it in the cookie
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
jwt.init_app(app)
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
    if not data:
        return jsonify({
            "error":"JSON body required"
        }),400
    #get username
    username=data.get("username")
    # print("Username: ",username)
    #get email
    email=data.get("email")
    # print("Email address: ",email)
    #get password
    password=data.get("password")
    # print("Password: ",password)
    #confirm password
    # confirm_password=data.get("confirm_password")
    # print("Confirm password: ",confirm_password)
    #bad request status code 400
    if not username or not email or not password:
        return jsonify({
            "error":"username,email and password are required"
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
        }
    }),201

#login user
@app.post("/api/v1/auth/login")
def login():
    #get json data
    data=request.get_json()
    if not data:
        return jsonify({
            "error":"JSON body required"
        }),400
    #check if username exist
    username=data.get("username")
    #check password if correct
    password=data.get("password")
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
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({
            "error":"Invalid credentials"
        }),401
    #create access token
    access_token=create_access_token(identity=str(user.id))
    refresh_token=create_refresh_token(identity=str(user.id))
    #create response
    response=jsonify({
        "message":"login successful",
        "username":user.username
    })
    #put JWT inside cookie
    set_access_cookies(response,access_token)
    #set refresh tokens
    set_refresh_cookies(response,refresh_token)
    return response,200
#refresh token
@app.post("/api/v1/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id=get_jwt_identity()
    new_access_token=create_access_token(identity=str(user_id))
    response=jsonify({
        "message":"Access token refreshed"
    })
    set_access_cookies(response,new_access_token)
    return response,200
    #handle JWT errors
#expired JWT token
@jwt.expired_token_loader
def expired_token_loader(jwt_header,jwt_payload):
    return jsonify({
        "error":"Token expired",
        "message":"Your access token has expired.Please refresh your token or login again"

    }),401
#invalid JWT tokens provided
@jwt.invalid_token_loader
def invalid_token_loader(error):
    return jsonify({
        "error":"Invalid token",
        "message":"The provided JWT Is invalid"
    }),401
#no JWT token provided
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error":"Authenticatation required",
        "message":"Please login to access this resource"
    }),401

# expenses 
@app.post("/api/v1/expenses")
@jwt_required()
def create_expense():
    user_id=get_jwt_identity()
    data=request.get_json()
    if not data:
        return jsonify({
            "error":"JSON body required"
        }),400

    category=data.get("category")
    if not category:
        return jsonify({
            "error":"Provide category"
        }),400
    description=data.get("description")
    if not description:
        return jsonify({
            "error":"Provide description"
        }),400
    amount=data.get("amount")
    if not isinstance(amount,(int,float)) or amount<=0:
        return jsonify({
            "error":"Amount must be a positive number"
        }),400
    #create expense
    expense=Expenses(category=category,description=description,amount=amount,user_id=user_id)
    db.session.add(expense)
    db.session.commit()
    return jsonify({
        "message":"Expense created successfully",
        "expense":{
            "category":expense.category,
            "description":expense.description,
            "amount":expense.amount,
            "user_id":expense.user_id
        }
    }),201


#filter expenses
#search for expense
@app.get("/api/v1/expenses")
@jwt_required()
def get_expenses():
    user_id=get_jwt_identity()
    id=request.args.get("id")
    category=request.args.get("category")
    search=request.args.get("search")
    description=request.args.get("description")
    amount=request.args.get("amount")
    page=request.args.get("page",default=1,type=int)
    if page<1:
        return jsonify({
            "error":"Page must be greater than  or equal to 1"
        }),400
    per_page=request.args.get("per_page",default=5,type=int)
    if per_page<1 or per_page>100:
        return jsonify({
            "error":"per page must be between 1 and 100"
        }),400
    #fetch user id
    query=Expenses.query.filter_by(user_id=user_id).order_by(Expenses.created_at.desc())
    if id:
        try:
            id=int(id)
            query=query.filter(Expenses.id==id)
        except ValueError:
            return jsonify({
                "error":"Id must be an integer"
            }),400
    if category:
        query=query.filter(Expenses.category.ilike(category))
    if search:
        query=query.filter(Expenses.description.ilike(f"%{search}%"))
    if description:
        query=query.filter(Expenses.description.ilike(f"%{description}%"))
    if amount:
        try:
            amount=float(amount)
            query=query.filter(Expenses.amount==float(amount))
        except ValueError:
            return jsonify({
                "error":"Amount must be a number"
            }),400
    # expenses=query.all()
  
    #pagination
    pagination=query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    expenses=pagination.items
    if not expenses:
        return jsonify({
            "error":"Page not found",
            "message":"The requested page does not exist"
        }),404
    filtered_expenses=[]
    for expense in expenses:
        expense_data={
            "id":expense.id,
            "category":expense.category,
            "description":expense.description,
            "amount":expense.amount
        }
        filtered_expenses.append(expense_data)
        print("Filtered expeneses: ",filtered_expenses)
    return jsonify({
        "Filtered expenses":filtered_expenses,
        "pagination":{
            "page":pagination.page,
            "per_page":pagination.per_page,
            "total":pagination.total,
            "pages":pagination.pages,
            "has_next":pagination.has_next,
            "has_prev":pagination.has_prev
        }
    }),200
#calculate category totals
@app.get("/api/v1/expenses/category-totals")
@jwt_required()
def category_totals():
    user_id=get_jwt_identity()
    results=db.session.query(Expenses.category,
    func.sum(Expenses.amount)).filter(Expenses.user_id==user_id).group_by(Expenses.category).all()
    totals=[]
    gross_totals=0
    
    for category,total in results:
        totals.append({
            "category":category,
            "total":total
        })
        gross_totals+=total
    
    return jsonify({
        "category_totals":totals,
        "gross_total":gross_totals
    }),200
#delete task
@app.delete("/api/v1/expenses/<id>")
@jwt_required()
def delete_expense(id):
    user_id=get_jwt_identity()
    print('Expense to delete id: ',user_id)
    if id:
        try:
            id=int(id)
        except ValueError:
            return jsonify({
                "error":"Id must be an integer"
            }),400
    expense=Expenses.query.filter_by(user_id=user_id,id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return "",204


#update expenses
@app.patch("/api/v1/expenses/<id>")
@jwt_required()
def update_expense(id):
    user_id=get_jwt_identity()
    print("Expense id to update: ",user_id)
    if id:
        try:
            id=int(id)
        except ValueError:
            return jsonify({
                "error":"Id must be an integer"
            }),400
    
    #get expense
    expense=Expenses.query.filter_by(user_id=user_id,id=id).first()
    # print('Expense: ',expense)
    if not expense:
        return jsonify({
            "error":"Expense not found"
        }),404
    #data
    data=request.get_json()
    if not data:
        return jsonify({
            "error":"JSON body required"
        }),400
    #update only provided fields
    if "category" in data:
        expense.category=data["category"]
    if "description" in data:
        expense.description=data["description"]
    if "amount" in data:
        expense.amount=data["amount"]

    print(data["category"])
    print(data["description"])
    print(data["amount"])
    #save changes
    db.session.commit()
    return jsonify({
        "message":"Expense updated successfully",
        "Updated expense":{
            "id":expense.id,
            "category":expense.category,
            "description":expense.description,
            "amount":expense.amount
        }
    }),200
    





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
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    #foreign key ie points to the primary key of another table
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    #connect owner to the expenses ie know who owns which expenses
    owner=db.relationship("User",back_populates="expenses")
    
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)