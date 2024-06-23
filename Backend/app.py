from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import json
from utils import perform_OCR, summarize_document_open_ai, find_similar_documents, Embeddings, MongoDB
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'userFiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPEN_AI_KEY = os.getenv("Open_AI_Key")

logging.basicConfig(level=logging.INFO)

# Initialize MongoDB connection
mongo_client = MongoDB(USERNAME, PASSWORD).connect()

if mongo_client:
    logging.info("Successfully connected to MongoDB.")
else:
    logging.error("Failed to connect to MongoDB. Ensure your credentials and network settings are correct.")

def format_json_to_bullets(json_obj):
    bullets = "\n".join([f"• {key}: {value}" for key, value in json_obj.items()])
    return bullets

def stream_text(text):
    for chunk in text.split('\n'):
        yield chunk + '\n'
        logging.info(f"Streaming chunk: {chunk}")
        import time
        time.sleep(0.1)  # Simulate streaming delay

@app.route('/api/messages', methods=['GET'])
def get_messages():
    logging.info("GET /api/messages")
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def add_message():
    text = request.form.get('text')
    file = request.files.get('file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = perform_OCR(file_path)
        summary = summarize_document_open_ai(extracted_text)
        summary = json.loads(summary)

        f_data = {"Input_Doc_summary": summary}
        allegation_nature = summary.get("allegation_nature", "")
        report_summary = summary.get("summary", "")

        if not allegation_nature or not report_summary:
            os.remove(file_path)
            return jsonify(f_data)

        if not mongo_client:
            logging.error("Failed to connect to MongoDB")
            os.remove(file_path)
            return jsonify({"error": "Failed to connect to MongoDB"}), 500

        collection = mongo_client.law_data.old_precedents
        input_embeddings = Embeddings().generate_embeddings(
            text=allegation_nature, use="google_gemini"
        )

        if not input_embeddings:
            os.remove(file_path)
            return jsonify({"error": "Failed to generate embeddings"}), 500

        similar_cases = find_similar_documents(
            collection, input_embeddings, "vector_index", "alle_embeddings", no_of_docs=5
        )

        common_precedents = {}
        for doc_no, doc in enumerate(similar_cases):
            doc_deets = {
                "id": doc.get("id", 0),
                "name": doc.get("name", ""),
                "court_name": doc.get("court_name", ""),
                "jurisdiction": doc.get("jurisdiction", ""),
                "allegation_nature": doc.get("allegation_nature", ""),
                "summary": doc.get("summary", ""),
                "score": doc.get("score", 0.0)
            }
            common_precedents[doc_no] = doc_deets

        f_data["common_precedents"] = common_precedents
        formatted_summary = format_json_to_bullets(f_data)
        
        # Delete the file after processing
        os.remove(file_path)
        
        return Response(stream_text(formatted_summary), content_type='text/plain')
    else:
        return jsonify({"error": "No file provided"}), 400

@app.route('/api/clear', methods=['POST'])
def clear_messages():
    global messages
    messages = []
    logging.info("Messages cleared")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
