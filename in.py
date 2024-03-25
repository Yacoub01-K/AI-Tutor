from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    question = data['question']
    # Here you would preprocess the question and pass it to your model
    # For demonstration, we'll just return a dummy response
    response = {"category": "syntax_error", "confidence": 0.9}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)