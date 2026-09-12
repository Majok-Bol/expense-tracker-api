Below is a production-style README tailored to the features actually present in your Flask Expense Tracker API, while also making it clear that some security settings are currently development-oriented.

# 💰 Expense Tracker API

A RESTful **Expense Tracker API** built with **Python and Flask**. The API provides user authentication, JWT-based authorization, expense CRUD operations, filtering, searching, pagination, category-based expense totals, and rate limiting for login attempts.

This project is designed as a backend/API development project for learning and practicing **REST API design, authentication, database relationships, SQLAlchemy queries, pagination, and basic API security**.

---

## 🚀 Features

### 👤 User Authentication

* User registration
* User login
* Password hashing with Bcrypt
* JWT authentication
* Access tokens
* Refresh tokens
* JWT stored in HTTP cookies
* Logout
* Access-token refresh
* JWT expiration handling
* Invalid-token handling
* Authentication-required handling

### 🔐 Basic API Security

* Password hashing with Bcrypt
* JWT-protected expense endpoints
* User-owned expenses
* Login rate limiting
* Input validation
* HTTP status codes
* JWT error handlers
* User-specific database queries

### 💰 Expense Management

Authenticated users can:

* Create expenses
* View expenses
* Update expenses
* Delete expenses
* Search expenses
* Filter expenses
* Paginate expenses
* View category totals
* View their gross expense total

### 🔎 Filtering & Searching

The expense listing endpoint supports:

* Expense ID filtering
* Category filtering
* Description searching
* General text searching
* Amount filtering
* Pagination
* Sorting by creation date

### 📊 Expense Analytics

The API provides:

* Total spending per category
* Gross total spending for the authenticated user

Example:

```json
{
    "category_totals": [
        {
            "category": "Food",
            "total": 1500.0
        },
        {
            "category": "Transport",
            "total": 800.0
        }
    ],
    "gross_total": 2300.0
}
```

---

# 🛠️ Technologies Used

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-Migrate**
* **SQLAlchemy**
* **Flask-JWT-Extended**
* **Flask-Bcrypt**
* **Flask-Limiter**
* **python-dotenv**
* **PostgreSQL / SQL database**
* **Postman** for API testing

---

# 📁 Project Structure

A recommended project structure for this application:

```text
expense-tracker-api/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── migrations/
│   └── ...
│
└── instance/
    └── ...
```

For the current learning version, most of the application logic is contained in `app.py`.

As the project grows, the application can be refactored into:

```text
expense-tracker-api/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── expenses.py
│   └── extensions.py
│
├── migrations/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/expense-tracker-api.git
```

```bash
cd expense-tracker-api
```

---

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
Flask-Bcrypt
Flask-Limiter
python-dotenv
psycopg2-binary
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Example:

```env
DATABASE_URL=postgresql://username:password@localhost/expense_tracker
SECRET_KEY=change_this_to_a_long_random_secret
```

Do **not** commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

You can provide a `.env.example` file:

```env
DATABASE_URL=
SECRET_KEY=
```

---

# 🗄️ Database

The application uses SQLAlchemy for database interaction.

There are two primary models:

## User

```text
User
├── id
├── username
├── email
├── password
└── expenses
```

## Expenses

```text
Expenses
├── id
├── amount
├── category
├── description
├── created_at
└── user_id
```

### Relationship

One user can have many expenses:

```text
User
  │
  ├── Expense
  ├── Expense
  ├── Expense
  └── Expense
```

The relationship is implemented using:

```python
expenses = db.relationship(
    "Expenses",
    back_populates="owner"
)
```

and:

```python
owner = db.relationship(
    "User",
    back_populates="expenses"
)
```

---

# 🔄 Database Migrations

Initialize migrations if required:

```bash
flask db init
```

Create a migration:

```bash
flask db migrate -m "create users and expenses tables"
```

Apply the migration:

```bash
flask db upgrade
```

After changing your models:

```bash
flask db migrate -m "describe your change"
```

Then:

```bash
flask db upgrade
```

---

# ▶️ Running the API

Start the Flask development server:

```bash
python app.py
```

The API will normally be available at:

```text
http://127.0.0.1:5000
```

Test the root endpoint:

```http
GET /
```

Response:

```text
Hello world
```

---

# 🔐 Authentication API

## Register

```http
POST /api/v1/auth/register
```

### Request

```json
{
    "username": "bashbytes",
    "email": "bashbytes@example.com",
    "password": "StrongPassword123"
}
```

### Response

```json
{
    "message": "User created successfully",
    "user": {
        "id": 1,
        "username": "bashbytes",
        "email": "bashbytes@example.com"
    }
}
```

### Status

```text
201 Created
```

---

# Login

```http
POST /api/v1/auth/login
```

### Request

```json
{
    "username": "bashbytes",
    "password": "StrongPassword123"
}
```

The API generates:

* Access token
* Refresh token

The tokens are stored in cookies.

### Response

```json
{
    "message": "login successful",
    "username": "bashbytes"
}
```

### Status

```text
200 OK
```

---

# 🚪 Logout

```http
POST /api/v1/auth/logout
```

Requires authentication.

The JWT cookies are removed.

### Response

```json
{
    "message": "You have been logged out"
}
```

### Status

```text
200 OK
```

---

# 🔄 Refresh Access Token

```http
POST /api/v1/auth/refresh
```

Requires a valid refresh token.

### Response

```json
{
    "message": "Access token refreshed"
}
```

### Status

```text
200 OK
```

---

# 💰 Expense API

All expense endpoints require authentication.

```text
Authorization:
JWT stored in authentication cookies
```

---

# ➕ Create Expense

```http
POST /api/v1/expenses
```

### Request

```json
{
    "category": "Food",
    "description": "Lunch",
    "amount": 500
}
```

### Response

```json
{
    "message": "Expense created successfully",
    "expense": {
        "category": "Food",
        "description": "Lunch",
        "amount": 500,
        "user_id": 1,
        "created_at": "2026-09-12T13:30:00+03:00"
    }
}
```

### Status

```text
201 Created
```

The expense timestamp is stored using UTC and converted to the `Africa/Nairobi` timezone when returned by the API.

---

# 📋 Get Expenses

```http
GET /api/v1/expenses
```

Returns expenses belonging to the authenticated user.

Example:

```http
GET /api/v1/expenses
```

---

# 📄 Pagination

Pagination is supported using:

```text
?page=1&per_page=5
```

Example:

```http
GET /api/v1/expenses?page=1&per_page=5
```

Example response:

```json
{
    "Filtered expenses": [
        {
            "id": 5,
            "category": "Food",
            "description": "Lunch",
            "amount": 500
        },
        {
            "id": 4,
            "category": "Transport",
            "description": "Taxi",
            "amount": 300
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 5,
        "total": 2,
        "pages": 1,
        "has_next": false,
        "has_prev": false
    }
}
```

`per_page` must be between:

```text
1 - 100
```

---

# 🔎 Filter by ID

```http
GET /api/v1/expenses?id=5
```

---

# 🏷️ Filter by Category

```http
GET /api/v1/expenses?category=Food
```

Category matching uses SQLAlchemy's `ilike()` for case-insensitive matching.

---

# 🔍 Search by Description

```http
GET /api/v1/expenses?search=lunch
```

The search is performed against the expense description.

---

# 📝 Filter by Description

```http
GET /api/v1/expenses?description=lunch
```

---

# 💵 Filter by Amount

```http
GET /api/v1/expenses?amount=500
```

---

# 🔗 Combine Filters

Multiple query parameters can be combined.

Example:

```http
GET /api/v1/expenses?category=Food&search=lunch&page=1&per_page=5
```

---

# 📊 Category Totals

```http
GET /api/v1/expenses/category-totals
```

Returns the total amount spent in each category by the authenticated user.

Example:

```json
{
    "category_totals": [
        {
            "category": "Food",
            "total": 2500.0
        },
        {
            "category": "Transport",
            "total": 1200.0
        }
    ],
    "gross_total": 3700.0
}
```

The calculation uses SQL aggregation:

```python
func.sum(Expenses.amount)
```

and:

```python
group_by(Expenses.category)
```

---

# ✏️ Update Expense

```http
PATCH /api/v1/expenses/<id>
```

Example:

```http
PATCH /api/v1/expenses/5
```

### Request

```json
{
    "category": "Shopping",
    "amount": 2500
}
```

Only the fields provided in the request are updated.

### Response

```json
{
    "message": "Expense updated successfully",
    "Updated expense": {
        "id": 5,
        "category": "Shopping",
        "description": "Lunch",
        "amount": 2500
    }
}
```

---

# 🗑️ Delete Expense

```http
DELETE /api/v1/expenses/<id>
```

Example:

```http
DELETE /api/v1/expenses/5
```

The API ensures that the expense belongs to the authenticated user before deleting it.

### Response

```text
204 No Content
```

---

# 🔒 User Data Isolation

Expenses are associated with the authenticated user through:

```python
user_id = get_jwt_identity()
```

Queries are restricted using the authenticated user's ID.

For example:

```python
Expenses.query.filter_by(
    user_id=user_id,
    id=id
).first()
```

This prevents one authenticated user from modifying another user's expenses.

---

# 🛡️ Rate Limiting

Login requests are limited to:

```python
@limiter.limit("3 per minute")
```

This helps reduce basic brute-force login attempts.

If the limit is exceeded:

```json
{
    "error": "Too many login attempts.Please try again later"
}
```

Status:

```text
429 Too Many Requests
```

---

# ⚠️ JWT Error Handling

The API provides custom responses for common JWT problems.

### Expired Token

```json
{
    "error": "Token expired",
    "message": "Your access token has expired.Please refresh your token or login again"
}
```

### Invalid Token

```json
{
    "error": "Invalid token",
    "message": "The provided JWT Is invalid"
}
```

### Missing Authentication

```json
{
    "error": "Authenticatation required",
    "message": "Please login to access this resource"
}
```

---

# 🧪 Testing With Postman

Recommended testing flow:

```text
1. Register
      ↓
2. Login
      ↓
3. Cookie is received
      ↓
4. Create expense
      ↓
5. Get expenses
      ↓
6. Filter/search expenses
      ↓
7. View category totals
      ↓
8. Update expense
      ↓
9. Delete expense
      ↓
10. Logout
```

Example test data:

```json
{
    "category": "Food",
    "description": "Lunch at restaurant",
    "amount": 750
}
```

```json
{
    "category": "Transport",
    "description": "Taxi to town",
    "amount": 450
}
```

```json
{
    "category": "Shopping",
    "description": "Bought new clothes",
    "amount": 2500
}
```

```json
{
    "category": "Bills",
    "description": "Internet subscription",
    "amount": 3000
}
```

---

# 📌 HTTP Status Codes

| Status | Meaning                                     |
| ------ | ------------------------------------------- |
| `200`  | Request successful                          |
| `201`  | Resource created                            |
| `204`  | Resource deleted successfully               |
| `400`  | Invalid request                             |
| `401`  | Authentication required/invalid credentials |
| `404`  | Resource not found                          |
| `409`  | Conflict, such as existing email            |
| `429`  | Rate limit exceeded                         |

---

# 🔐 Security Considerations

This project currently contains development-oriented JWT cookie settings:

```python
JWT_COOKIE_SECURE = False
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_HTTPONLY = False
JWT_COOKIE_SAMESITE = "Lax"
```

For production deployment, these settings should be hardened.

Recommended production configuration includes:

```python
JWT_COOKIE_SECURE = True
JWT_COOKIE_CSRF_PROTECT = True
JWT_COOKIE_HTTPONLY = True
JWT_COOKIE_SAMESITE = "Strict"
```

The API should also be deployed behind HTTPS.

Additional production improvements include:

* Strong randomly generated secret keys
* Password-strength requirements
* Account lockout or progressive delays
* Refresh-token revocation
* JWT blocklist/revocation
* Audit logging
* Security headers
* CORS configuration
* Centralized error handling
* Persistent rate-limit storage such as Redis
* Automated tests
* Input/schema validation
* Production WSGI server such as Gunicorn
* PostgreSQL in production
* Environment-specific configuration

---

# 🧠 What This Project Demonstrates

This project demonstrates practical backend/API concepts including:

* REST API design
* Flask routing
* HTTP methods
* JSON request/response handling
* HTTP status codes
* CRUD operations
* SQLAlchemy ORM
* Database relationships
* Foreign keys
* SQL filtering
* `filter_by()`
* `filter()`
* `ilike()`
* SQL aggregation
* `func.sum()`
* `group_by()`
* Pagination
* JWT authentication
* Access and refresh tokens
* Cookie-based authentication
* Password hashing
* Rate limiting
* Environment variables
* Timezone-aware timestamps
* User-based authorization



# 🎯 Project Goal

The goal of this project is to build a practical REST API while developing strong foundations in:

```text
Python
   ↓
Flask
   ↓
REST APIs
   ↓
SQLAlchemy
   ↓
Authentication
   ↓
Authorization
   ↓
API Security
   ↓
Production Deployment
```

The project serves as a foundation for building more advanced **secure backend APIs and security-focused applications**.

---

## 📄 License

This project is intended for learning and development purposes.

This README is intentionally aligned with your **current implementation**, rather than claiming features you haven't implemented yet. The **Future Improvements** section gives you a clean progression toward the more security-focused version of the API.
