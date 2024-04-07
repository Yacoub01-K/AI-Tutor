from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
print("Using OpenAI API Key:", os.getenv('OPENAI_API_KEY'))

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No OpenAI API key set. Please configure the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
        # Assuming the response object has a 'choices' attribute
        # and accessing the first choice's 'message' attribute for content
        message_content = response.choices[0].message.content
        print(response)
        return jsonify({"response": message_content})
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return jsonify({"error": "Failed to get response from OpenAI"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)


