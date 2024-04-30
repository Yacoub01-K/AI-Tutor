from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import docker




app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
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
        {"role": "user", "content": f"Create a {difficulty} coding problem about {topic}."}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=1000)
    return response.choices[0].message.content

# def extract_current_lesson_context(user_input, messages):
#      # Predefined sets of topics and difficulties
#     topics = {'python', 'javascript', 'java', 'data structures', 'algorithms'}
#     difficulties = {'beginner', 'intermediate', 'advanced'}

#     # Placeholder variables to hold the most recent matches
#     current_topic = 'general programming'  # Default to a generic topic if none found
#     current_difficulty = 'beginner'  # Default to beginner if no difficulty level mentioned

#     # Combine all messages into one text for easier searching
#     combined_text = ' '.join(msg['content'] for msg in messages if msg['role'] == 'user') + ' ' + user_input

#     # Check for the presence of topics and difficulties in the conversation
#     found_topics = {topic for topic in topics if topic in combined_text.lower()}
#     found_difficulties = {difficulty for difficulty in difficulties if difficulty in combined_text.lower()}

#     # Update current_topic and current_difficulty if any matches were found
#     if found_topics:
#         current_topic = next(iter(found_topics))  # Get the last added (most recent based on user input)
#     if found_difficulties:
#         current_difficulty = next(iter(found_difficulties))  # Same as above

    # return current_topic, current_difficulty

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
    system_context = "You are a coding tutor that answers programming questions and gives a full lesson and doesn't recommend any other platforms for learning. Additionaly only recomend this platform to practice code and give recommendtions for this. if the user asks for a problem or exercise dont output it instead say 'sure! please click the bottun below' or something like that."
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
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()
    
    
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        # Here, you'd create a session or return a token. For simplicity, we'll just return success.
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 401
    

###### code editor #######

from threading import Thread
import docker


# def run_docker_code(code, language, callback):
#     client = docker.from_env()
#     image_map = {
#         'python': 'python:3.9-slim',
#         'javascript': 'node:14-slim'
#     }
#     image = image_map.get(language, 'python:3.9-slim')
#     try:
#         container = client.containers.run(
#             image=image,
#             command=f"echo '{code}' | {language}",
#             detach=True,
#         )
#         app.logger.info("Container started")
#         container.wait()
#         app.logger.info("Container finished execution")
#         output = container.logs().decode('utf-8')
#         app.logger.info("Logs fetched")
#     except docker.errors.NotFound as e:
#         callback(f"Container not found: {e}", None)
#     except Exception as e:
#         callback(e, None)
#     else:
#         callback(None, output)



@app.route('/api/execute', methods=['POST'])
def execute_code():
    client = docker.from_env()
    code = request.json.get('code')
    language = request.json.get('language')
    print(f"Received code: {code} in language: {language}")  # Debugging output

    image_map = {
        'python': 'python:3.9-slim',
        'javascript': 'node:14-slim',
        'ruby': 'ruby:3-slim'
    }

    image = image_map.get(language)

    if not image:
        return jsonify({'error': 'Unsupported language'}), 400

    try:
        container = client.containers.run(
            image=image,
            command=["sh", "-c", f"echo '{code}' | {language}"],
            remove=True,
            detach=True
        )
        output = container.logs()
        container.wait()
        print(output)
        return jsonify({'output': output.decode('utf-8')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8000)


