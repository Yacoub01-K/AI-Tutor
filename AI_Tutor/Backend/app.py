from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
# print("Using OpenAI API Key:", os.getenv('OPENAI_API_KEY'))

########AI API SECTION###########
# print("Using OpenAI API Key:", os.getenv('OPENAI_API_KEY'))

########AI API SECTION###########

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No OpenAI API key set. Please configure the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    return jsonify({"message": "Test route is working!"})

def extract_topic(user_input):
    topics = {'python', 'javascript', 'java', 'data structures', 'algorithms'}
    words = set(user_input.lower().split())
    found_topics = topics.intersection(words)
    return next(iter(found_topics), 'general programming')

def assess_difficulty(user_input):
    if 'beginner' in user_input:
        return 'beginner'
    elif 'intermediate' in user_input:
        return 'intermediate'
    elif 'advanced' in user_input:
        return 'advanced'
    return 'beginner'

def generate_problem_sheet(topic, difficulty):
    messages = [
        {"role": "system", "content": "You are an AI trained to create and explain coding problems while giving examples of inputs and outputs of the problem."},
        {"role": "user", "content": f"Create a {difficulty} coding problem about {topic} and provide a brief solution outline."}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=1000)
    return response.choices[0].message.content


@app.route('/api/get_problem', methods=['POST'])
def get_problem():
    user_input = request.json.get('userInput', '')
    topic = extract_topic(user_input)
    difficulty = assess_difficulty(user_input)
    try:
        problem_content = generate_problem_sheet(topic, difficulty)
        return jsonify({"problem": problem_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    userInput = request.json.get('userInput', '').lower()
    system_context = "You are a coding tutor that answers programming questions and gives a full lesson and doesn't recommend any other platforms for learning. Additionaly only recomend this platform to practice code and give recommendtions for this. if the user asks for a problem or exercise dont output it only give them a suitable lesson, this means dont say things like 'instead of problem...'."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_context}, {"role": "user", "content": userInput}]
    )
    message_content = response.choices[0].message.content
    problem_keywords = ['problem', 'exercise', 'question', 'solve', 'example']
    problemAvailable = any(keyword in userInput.lower() for keyword in problem_keywords)

    problem_description = ""
    if problemAvailable:
        topic = extract_topic(userInput)  # You would define this function to extract topics from user input
        difficulty = assess_difficulty(userInput)  # Similarly, this function determines difficulty
        problem_description = generate_problem_sheet(topic, difficulty)

    html_response = f"<div class='ai-response'><p>{message_content.replace('\n', '<br>')}</p></div>"
    return jsonify({"response": html_response, "problemAvailable": problemAvailable, "problemDescription": problem_description})

######LOGIN SECTION#########    

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Ensure email is unique
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



with app.app_context():
    db.create_all()

#this is not secure will probably need to be changed. 
@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not password or not email:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        # Here, you'd typically want to create a session or return a token.
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False, "message": "Invalid credentials"}), 401
    

###### code editor #######
@app.route('/api/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    language = request.json.get('language', 'python')  # Default to Python if not specified
    
    # Mapping of languages to Docker images
    language_images = {
        'python': 'python:3.9-slim',
        'javascript': 'node:14-slim',
        'ruby': 'ruby:3-slim',
        # Add other languages and their respective Docker images here
    }

    image = language_images.get(language, 'python:3.9-slim')  # Fallback to Python image

    try:
        container = client.containers.run(
            image,
            command=["sh", "-c", f"echo '{code}' | {language}"],
            remove=True,
            detach=True
        )
        output = container.logs()
        container.wait()  # Ensure the container finishes execution
        return jsonify({'output': output.decode('utf-8')})
    except docker.errors.ContainerError as e:
        return jsonify({'error': 'Error executing code', 'details': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8000)


