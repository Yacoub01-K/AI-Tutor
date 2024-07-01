from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json
from models import db, User, get_session, initialize_db, Lesson
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_db(app)

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
        {"role": "system", "content": "You are an AI trained to create and explain coding problems in detail. Generate a problem along with sample inputs and expected outputs."},
        {"role": "user", "content": f"Create a {difficulty} coding problem about {topic} and provide sample test cases with explanations."}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=4096)
    problem_text = response.choices[0].message.content

    # Parse the output to separate the problem description and test cases
    problem_description, *test_cases = problem_text.split('\n\n')
    html_response = f"""
    <div class='problem-sheet'>
        <h1>Problem on {topic.capitalize()}</h1>
        <h2>Difficulty: {difficulty.capitalize()}</h2>
        <p>{problem_description}</p>
    </div>
    """
    return html_response, test_cases

@app.route('/api/get_problem', methods=['POST'])
def get_problem():
    user_input = request.json.get('userInput', '').lower()
    topic = extract_topic(user_input)
    difficulty = assess_difficulty(user_input)
    try:
        html_content, test_cases = generate_problem_sheet(topic, difficulty)
        return jsonify({"problemHTML": html_content, "testCases": test_cases}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    userInput = request.json.get('userInput', '').lower()
    system_context = "You are a coding tutor that answers programming questions and gives a full lesson that places learning objectives, gives a specific learning path, and doesn't recommend any other platforms for learning. Additionally, only recommend this platform to practice code and give recommendations for this. If the user asks for a problem or exercise, don't output it; instead say 'sure! please click the button below' or something like that."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_context}, {"role": "user", "content": userInput}]
    )
    message_content = response.choices[0].message.content
    problem_keywords = ['problem', 'exercise', 'question', 'solve', 'example']
    problemAvailable = any(keyword in userInput.lower() for keyword in problem_keywords)

    problem_description = ""
    if problemAvailable:
        topic = extract_topic(userInput)
        difficulty = assess_difficulty(userInput)
        problem_description, _ = generate_problem_sheet(topic, difficulty)

    html_response = f"<div class='ai-response'><p>{message_content.replace('\n', '<br>')}</p></div>"
    return jsonify({"response": html_response, "problemAvailable": problemAvailable, "problemDescription": problem_description})

@app.route('/api/lessons',methods=['GET'])
def get_lesson():
    lessons = []
    for lesson in Lesson.query.all():  # Needs changing 
        lessons.append({
            'id': lesson.id,
            'name': lesson.name,
            'topic': lesson.topic,
            'difficulty': lesson.difficulty
        })
    print(jsonify(lessons))
    return jsonify(lessons)

######LOGIN SECTION#########    

with app.app_context():
    db.create_all()

def get_email(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return user.email
    else:
        return None 

@app.route('/get_email/<int:user_id>', methods=['GET'])
def fetch_email(user_id):
    email = get_email(user_id)
    if email:
        return jsonify({"email": email}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    new_user = User(username=username, email=email, password=password)

    try:
        session = get_session()
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError as e:
        session.rollback()
        error_message = str(e.orig)
        if "username" in error_message:
            return jsonify({"error": "Username already exists"}), 409
        elif "email" in error_message:
            return jsonify({"error": "Email already exists"}), 409
        else:
            return jsonify({"error": "Username or email already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.remove()

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

import docker

Dockerclient = docker.from_env()
prewarmed_containers = {}

def initialize_prewarmed_containers():
    languages = ['python:3.9-slim', 'node:14-slim']  # Define your language images
    number_each = 2  # Number of containers to pre-warm per language

    for lang in languages:
        prewarmed_containers[lang] = []
        for _ in range(number_each):
            container = Dockerclient.containers.run(
                image=lang,
                command="sleep infinity",  # More clear than 'tail -f /dev/null'
                detach=True
            )
            prewarmed_containers[lang].append(container)
            print(f"Prewarmed container {container.id} for {lang}")

@app.route('/api/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    language = request.json.get('language')
    image_map = {
        'python': 'python:3.9-slim',
        'javascript': 'node:14-slim',
    }
    image = image_map.get(language)

    if not image or not prewarmed_containers.get(image):
        return jsonify({'error': 'Unsupported language or no prewarmed container available'}), 400

    container = prewarmed_containers[image].pop(0)  # Retrieve the first pre-warmed container
    try:
        exec_result = container.exec_run(
            cmd=["sh", "-c", f"echo '{code}' | {language}"],
            detach=False
        )
        output = exec_result.output.decode('utf-8')
        prewarmed_containers[image].append(container)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'output': output})

if __name__ == '__main__':
    initialize_prewarmed_containers()
    app.run(host='0.0.0.0', debug=True, port=8000)
