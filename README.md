# Expense Tracker API

A RESTful **Expense Tracker API** built with **Python and Flask**.

The API provides user registration and authentication, JWT-based authorization using cookies, expense CRUD operations, filtering, searching, pagination, category-based expense analytics, password hashing, login rate limiting, database relationships, and timezone-aware expense timestamps.

This project is primarily a **backend/API development and learning project** focused on building practical REST APIs with Flask, SQLAlchemy, authentication, authorization, database queries, and foundational API security.

---

##  Features

### User Authentication

* User registration
* User login
* Password hashing with Bcrypt
* JWT-based authentication
* Access tokens
* Refresh tokens
* JWT tokens stored in HTTP cookies
* Logout
* Access-token refresh
* JWT expiration
* Invalid-token handling
* Missing-authentication handling
* Duplicate email detection

### Basic API Security

* Bcrypt password hashing
* JWT-protected expense endpoints
* User-owned expenses
* User-specific database queries
* Login rate limiting
* Input validation
* Authentication error handling
* JWT error handlers
* HTTP status codes
* Environment variables for secrets
* Cookie-based authentication

### Expense Management

Authenticated users can:

* Create expenses
* View expenses
* Update expenses
* Delete expenses
* Search expenses
* Filter expenses
* Paginate expenses
* View category totals
* View gross expense totals

### Filtering & Searching

The expense listing endpoint supports:

* Expense ID filtering
* Category filtering
* Description searching
* General description search
* Amount filtering
* Pagination
* Sorting by creation date

### Expense Analytics

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

# Technologies Used

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

#  Project Structure

The current learning version keeps most application logic inside `app.py`.

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

As the project grows, the application can be refactored into a modular structure:

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

#  Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/expense-tracker-api.git
```

```bash
cd expense-tracker-api
```

---

## 2. Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example:

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

# Environment Variables

Create a `.env` file in the project root:

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

You can safely commit an `.env.example` file:

```env
DATABASE_URL=
SECRET_KEY=
```

---

# Database

The application uses **SQLAlchemy** as its ORM.

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

---

## Database Relationship

One user can have many expenses.

```text
User
  │
  ├── Expense
  ├── Expense
  ├── Expense
  └── Expense
```

The relationship is implemented using SQLAlchemy:

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

Each expense contains a foreign key:

```python
user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=False
)
```

---

# Database Migrations

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

After modifying the models:

```bash
flask db migrate -m "describe your change"
```

Then:

```bash
flask db upgrade
```

---

# Running the API

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

# Authentication API

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

The API creates:

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

# Logout

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

# Refresh Access Token

```http
POST /api/v1/auth/refresh
```

Requires a valid refresh token.

A new access token is generated and stored in the access-token cookie.

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

# Expense API

All expense endpoints require JWT authentication.

The API retrieves the authenticated user's ID using:

```python
user_id = get_jwt_identity()
```

The JWT is stored in authentication cookies.

---

# Create Expense

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
        "created_at": "2026-09-17T15:30:00+03:00"
    }
}
```

### Status

```text
201 Created
```

---

# Timezone Handling

Expenses are created using a UTC timestamp:

```python
datetime.now(timezone.utc)
```

When the expense is returned after creation, the timestamp is converted to:

```text
Africa/Tanzania
```

using:

```python
ZoneInfo("Africa/Tanzania")
```

Example:

```text
2026-09-17T15:30:00+03:00
```

The database column is timezone-aware:

```python
created_at = db.Column(
    db.DateTime(timezone=True),
    nullable=False
)
```

> Note: The current implementation explicitly converts the response timestamp to `Africa/Nairobi`. It does not automatically detect an arbitrary timezone from each API client.

---

# Get Expenses

```http
GET /api/v1/expenses
```

Returns expenses belonging to the authenticated user.

Expenses are sorted by:

```text
created_at DESC
```

Example:

```http
GET /api/v1/expenses
```

---

# Pagination

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

The current API limits `per_page` to:

```text
1 - 100
```

The default is:

```text
page = 1
per_page = 5
```

---

# Filter by ID

```http
GET /api/v1/expenses?id=5
```

The ID must be an integer.

---

# Filter by Category

```http
GET /api/v1/expenses?category=Food
```

Category filtering uses SQLAlchemy's:

```python
ilike()
```

which provides case-insensitive matching.

---

# Search by Description

```http
GET /api/v1/expenses?search=lunch
```

The search is performed against the expense description.

The search uses:

```python
Expenses.description.ilike(f"%{search}%")
```

---

# Filter by Description

```http
GET /api/v1/expenses?description=lunch
```

---

# Filter by Amount

```http
GET /api/v1/expenses?amount=500
```

The amount is converted to a floating-point number before filtering.

---

# Combine Filters

Multiple query parameters can be combined.

Example:

```http
GET /api/v1/expenses?category=Food&search=lunch&page=1&per_page=5
```

---

# Category Totals

```http
GET /api/v1/expenses/category-totals
```

Returns total spending grouped by category for the authenticated user.

It also returns the user's gross total spending.

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

The query is restricted to the authenticated user's expenses.

---

# Update Expense

```http
PATCH /api/v1/expenses/<id>
```

Example:

```http
PATCH /api/v1/expenses/5
```

### Request

Only the fields that need to change have to be supplied.

```json
{
    "category": "Shopping",
    "amount": 2500
}
```

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

### Status

```text
200 OK
```

---

#  Delete Expense

```http
DELETE /api/v1/expenses/<id>
```

Example:

```http
DELETE /api/v1/expenses/5
```

The API first searches for the expense using both:

```text
user_id
```

and:

```text
expense_id
```

This ensures that a user can only delete their own expense.

### Response

```text
204 No Content
```

---

# User Data Isolation

Expenses are associated with the authenticated user through the JWT identity:

```python
user_id = get_jwt_identity()
```

Queries are restricted to that user's records.

For example:

```python
Expenses.query.filter_by(
    user_id=user_id,
    id=id
).first()
```

This authorization pattern prevents users from directly accessing, updating, or deleting another user's expenses through the expense ID alone.

---

# Rate Limiting

Login requests are currently limited to:

```python
@limiter.limit("3 per minute")
```

This provides basic protection against repeated login attempts.

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

The current limiter uses the remote client address as its key:

```python
get_remote_address
```

---

# JWT Error Handling

The API provides custom responses for common JWT authentication failures.

## Expired Token

```json
{
    "error": "Token expired",
    "message": "Your access token has expired.Please refresh your token or login again"
}
```

Status:

```text
401 Unauthorized
```

## Invalid Token

```json
{
    "error": "Invalid token",
    "message": "The provided JWT Is invalid"
}
```

Status:

```text
401 Unauthorized
```

## Missing Authentication

```json
{
    "error": "Authenticatation required",
    "message": "Please login to access this resource"
}
```

Status:

```text
401 Unauthorized
```

---

#  Testing With Postman

A recommended testing flow is:

```text
1. Register
       ↓
2. Login
       ↓
3. Authentication cookies are received
       ↓
4. Create expenses
       ↓
5. Get expenses
       ↓
6. Filter/search expenses
       ↓
7. Test pagination
       ↓
8. View category totals
       ↓
9. Update an expense
       ↓
10. Delete an expense
       ↓
11. Test logout
       ↓
12. Test protected endpoints after logout
```

---

## Example Test Data

### Food

```json
{
    "category": "Food",
    "description": "Lunch at restaurant",
    "amount": 750
}
```

### Transport

```json
{
    "category": "Transport",
    "description": "Taxi to town",
    "amount": 450
}
```

### Shopping

```json
{
    "category": "Shopping",
    "description": "Bought new clothes",
    "amount": 2500
}
```

### Bills

```json
{
    "category": "Bills",
    "description": "Internet subscription",
    "amount": 3000
}
```

---

#  API Testing Checklist

Use Postman to test both successful and unsuccessful requests.

### Authentication

* [ ] Register with valid data
* [ ] Register without JSON
* [ ] Register with missing fields
* [ ] Register using an existing email
* [ ] Login with valid credentials
* [ ] Login with an incorrect username
* [ ] Login with an incorrect password
* [ ] Login without JSON
* [ ] Login with missing credentials
* [ ] Exceed the login rate limit
* [ ] Logout
* [ ] Refresh access token
* [ ] Access a protected endpoint without authentication

### Expenses

* [ ] Create a valid expense
* [ ] Create expense without JSON
* [ ] Create expense without category
* [ ] Create expense without description
* [ ] Create expense with invalid amount
* [ ] Get expenses
* [ ] Filter by ID
* [ ] Filter by category
* [ ] Search description
* [ ] Filter by description
* [ ] Filter by amount
* [ ] Combine filters
* [ ] Test pagination
* [ ] Test invalid page
* [ ] Test invalid `per_page`
* [ ] View category totals
* [ ] Update an expense
* [ ] Update only one field
* [ ] Update a nonexistent expense
* [ ] Delete an expense
* [ ] Attempt to access another user's expense

---

#  HTTP Status Codes

| Status | Meaning                                        |
| ------ | ---------------------------------------------- |
| `200`  | Request successful                             |
| `201`  | Resource created                               |
| `204`  | Resource deleted successfully                  |
| `400`  | Invalid request                                |
| `401`  | Authentication required or invalid credentials |
| `404`  | Resource not found                             |
| `409`  | Conflict, such as an existing email            |
| `429`  | Rate limit exceeded                            |

---

# Security Configuration

The current development configuration contains intentionally relaxed JWT cookie settings:

```python
JWT_COOKIE_SECURE = False
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_HTTPONLY = False
JWT_COOKIE_SAMESITE = "Lax"
```

These settings are suitable only for local development/testing and should be reviewed before production deployment.

For a production HTTPS deployment, the configuration should be hardened:

```python
JWT_COOKIE_SECURE = True
JWT_COOKIE_CSFR_PROTECT = True
JWT_COOKIE_HTTPONLY = True
JWT_COOKIE_SAMESITE = "Strict"
```

The API should also be deployed behind HTTPS.

---
# What This Project Demonstrates

This project demonstrates practical backend and API development concepts including:

### Python & Flask

* Python application structure
* Flask routing
* HTTP methods
* Request handling
* JSON request/response handling

### REST API Development

* REST endpoint design
* CRUD operations
* Query parameters
* HTTP status codes
* API error responses
* Pagination

### Database Development

* SQLAlchemy ORM
* Database models
* Foreign keys
* One-to-many relationships
* SQL filtering
* `filter_by()`
* `filter()`
* `ilike()`
* SQL aggregation
* `func.sum()`
* `group_by()`
* Database migrations

### Authentication & Authorization

* User registration
* Password hashing
* JWT authentication
* Access tokens
* Refresh tokens
* Cookie-based authentication
* JWT expiration
* JWT error handling
* User-specific authorization
* Data isolation

### Basic API Security

* Password hashing
* Login rate limiting
* Authentication enforcement
* Input validation
* Secure database ownership checks
* Environment variables
* Cookie security considerations

### Time Handling

* UTC timestamps
* Timezone-aware database fields
* `datetime`
* `timezone.utc`
* `ZoneInfo`
* Africa/Tanzania timezone conversion

---

# Project Goal

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
Database Relationships
   ↓
Authentication
   ↓
Authorization
   ↓
API Security
   ↓
Production Deployment
```

The project provides a foundation for building more advanced **secure backend APIs and security-focused applications**.



# License

This project is intended for learning and development purposes.
