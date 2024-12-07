# Flask API with JWT Authentication and RBAC

This is a Flask-based API implementing user authentication with JWT and Role-Based Access Control (RBAC). Users can register, log in, and access resources based on their roles (e.g., `admin` or `user`).

---

## **Features**

1. **User Registration and Login**
   - Register users with hashed passwords.
   - Log in to receive a JWT for authentication.

2. **Role-Based Access Control (RBAC)**
   - `admin` users can create, update, delete, and view resources.
   - `user` role can only view resources.

3. **CRUD Operations for Projects**
   - Perform operations like adding and viewing projects.

4. **MongoDB Support**
   - Store users and projects in MongoDB.

5. **JWT Authentication**
   - Authenticate and authorize API requests using JWT.

---

## **Endpoints**

0. **Health Check**
   - **GET** `/health`

1. **User Registration**
   - **POST** `/register`
   - Body: `{ "username": "example", "password": "password123", "role": "user" }`

2. **User Login**
   - **POST** `/login`
   - Body: `{ "username": "example", "password": "password123" }`
   - Response: `{ "access_token": "JWT_TOKEN" }`

3. **Get Projects**
   - **GET** `/projects`
   - Requires: JWT

4. **Create Project**
   - **POST** `/projects`
   - Body: `{ "name": "Project A", "description": "Description of project" }`
   - Requires: JWT with `admin` role.

5. **Update Project**
   - **PUT** `/projects/<project_id>`
   - Body: `{  "name": "Updated Project Name", "description": "Updated Project Description"}`
   - Requires: JWT with `admin` role.

6. **Delete Project**
   - **DELETE** `/projects/<project_id>`
   - Requires: JWT with `admin` role.

## **Setup Instructions**

### Prerequisites
1. Python 3.9+
2. MongoDB running locally or in the cloud.

### Steps
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run using python cmd: 
   ```bash
   python app.py
4. Run using Flask-run (If not 3.)
   ```bash
   flask run --port 5000
Note: Kindly Update `JWT_SECRET_KEY` and `MongoDB_Connection_String` in **app.py** at line 10 and 11
