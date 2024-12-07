from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import User, Project
from utils import role_required
import mongoengine as me

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"
app.config["CONNECTION_STRING"] = "MongoDB_Connection_String"
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Connect to MongoDB using connection string
try:
    me.connect(host=app.config["CONNECTION_STRING"])
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# User Registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if User.objects(username=username):
            return jsonify({"message": "User already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, role=role)
        user.save()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

# User Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.objects(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            token = create_access_token(identity={"username": username, "role": user.role})
            return jsonify({"access_token": token}), 200

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

# # Get Projects (Accessible by all users)
@app.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        projects = Project.objects()
        serialized_projects = [{'id': str(p.id), 'name': p.name, 'description': p.description} for p in projects]
        return jsonify(serialized_projects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create Project (Admin only)
@app.route('/projects', methods=['POST'])
@jwt_required()
@role_required("admin")
def create_project():
    try:
        data = request.json
        project = Project(name=data["name"], description=data["description"])
        project.save()
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

# Update Project by ID (Admin only)
@app.route('/projects/<project_id>', methods=['PUT'])
@jwt_required()
@role_required("admin")
def update_project(project_id):
    try:
        data = request.json
        project = Project.objects(id=ObjectId(project_id)).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project.update(
            name=data.get("name", project.name),
            description=data.get("description", project.description)
        )
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete Project by ID (Admin only)
@app.route('/projects/<project_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin")
def delete_project(project_id):
    try:
        project = Project.objects(id=ObjectId(project_id)).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project.delete()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health-check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
