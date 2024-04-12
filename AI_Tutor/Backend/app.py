from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


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
    

    
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)


