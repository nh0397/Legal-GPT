from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
from utils import ensure_upload_folder_exists, save_file, extract_text_from_pdf

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'userFiles'
ensure_upload_folder_exists(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = []

def stream_text(text):
    for chunk in text.split():
        yield chunk + ' '
        import time
        time.sleep(0.1)  # Simulate streaming delay

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def add_message():
    text = request.form.get('text')
    file = request.files.get('file')

    if file:
        file_path = save_file(file, app.config['UPLOAD_FOLDER'])
        extracted_text = extract_text_from_pdf(file_path)
        messages.append({'text': text, 'file': file.filename, 'user': True})
        return Response(stream_text(extracted_text), content_type='text/plain')
    else:
        message = {'text': text, 'file': None, 'extracted_text': None}
        messages.append(message)
        return jsonify(message), 201

if __name__ == '__main__':
    app.run(debug=True)
