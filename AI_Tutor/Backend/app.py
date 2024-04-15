from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import logging


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

@app.route('/api/chat', methods=['POST'])
def chat():
    userInput = request.json.get('userInput')

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": userInput}],
        )
        message_content = response.choices[0].message.content
        print(response)
        return jsonify({"response": message_content})
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return jsonify({"error": "Failed to get response from OpenAI"}), 500
    
    
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
    
    
    
    #### CODE EDITOR #####

# Function to execute code using Judge0
logging.basicConfig(level=logging.DEBUG)

JUDGE0_ENDPOINT = "https://api.judge0.com/submissions?base64_encoded=false&wait=true"

def execute_code_with_judge0(code, language_id=63):
    data = {
        "source_code": code,
        "language_id": language_id,
        "stdin": "",
        "expected_output": "",
        "memory_limit": 256000,
        "cpu_time_limit": 5
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(JUDGE0_ENDPOINT, json=data, headers=headers, timeout=10)  # Timeout set to 10 seconds
        return response.json()
    except requests.Timeout:
        logging.error("Timeout occurred while trying to execute code.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

@app.route('/api/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    logging.info("Received code for execution.")
    result = execute_code_with_judge0(code)
    if not result:
        return jsonify({'error': 'Failed to execute code due to timeout or server error'}), 500

    output = result.get('stdout', '')
    stderr = result.get('stderr', '')
    compile_error = result.get('compile_output', '')

    full_output = output + (f"\nErrors: {stderr}" if stderr else "") + (f"\nCompilation Errors: {compile_error}" if compile_error else "")
    
    logging.info("Code executed successfully.")
    return jsonify({'output': full_output})


    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8000)


