from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Ensure the userFiles directory exists
UPLOAD_FOLDER = 'userFiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = []

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def add_message():
    text = request.form.get('text')
    file = request.files.get('file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        message = {'text': text, 'file': file.filename}
    else:
        message = {'text': text, 'file': None}
    
    messages.append(message)
    return jsonify(message), 201

if __name__ == '__main__':
    app.run(debug=True)
