from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains and routes

# It's crucial to keep your API keys secure and not hard-code them in your files
openai.api_key = os.getenv("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")

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('userInput')
    
    # Ensure there's input to process
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        response = openai.Completion.create(
          engine="text-davinci-003",  # You might need to adjust this based on available engines
          prompt=user_input,
          max_tokens=150
        )
        return jsonify({"response": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": "Error fetching response from OpenAI", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
