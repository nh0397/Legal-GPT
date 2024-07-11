from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import json
from utils import perform_OCR, summarize_document, find_similar_documents, Embeddings, MongoDB
from dotenv import load_dotenv
import logging
import google.generativeai as genai

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

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

logging.basicConfig(level=logging.INFO)

# Initialize MongoDB connection
mongo_client = MongoDB(USERNAME, PASSWORD).connect()

if mongo_client:
    logging.info("Successfully connected to MongoDB.")
else:
    logging.error("Failed to connect to MongoDB. Ensure your credentials and network settings are correct.")

messages = []  # In-memory store for messages

def format_json_to_bullets(json_obj):
    bullets = "\n".join([f"• {key}: {value}" for key, value in json_obj.items()])
    return bullets

def print_message_list():
    for i, msg in enumerate(messages):
        logging.info(f"Message {i+1}: {'User' if msg['user'] else 'Assistant'}: {msg['text']}")

@app.route('/api/messages', methods=['GET'])
def get_messages():
    logging.info("GET /api/messages")
    return jsonify(messages)  # Returning stored messages

@app.route('/api/messages', methods=['POST'])
def add_message():
    global messages
    common_precedents = {}  # Initialize common_precedents

    text = request.form.get('text')
    file = request.files.get('file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = perform_OCR(file_path)
        
        # Set a breakpoint here to inspect the OCR result
        summary = summarize_document(extracted_text)
        
        if not summary:
            logging.error("Summarize document returned an empty response.")
            return jsonify({"error": "Failed to summarize document"}), 500

        logging.info(f"Raw summary: {summary}")

        # Clean the response by removing backticks
        summary = summary.strip('```json').strip('```')

        try:
            summary = json.loads(summary)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return jsonify({"error": "Invalid JSON from summarization"}), 500

        f_data = {"Input_Doc_summary": summary}
        category = summary.get("category", None)
        report_summary = summary.get("summary", "")

        if not category or not report_summary:
            os.remove(file_path)
            messages.append({"user": False, "text": f_data})
            print_message_list()
            return jsonify(f_data)

        if not mongo_client:
            logging.error("Failed to connect to MongoDB")
            os.remove(file_path)
            messages.append({"user": False, "text": {"error": "Failed to connect to MongoDB"}})
            print_message_list()
            return jsonify({"error": "Failed to connect to MongoDB"}), 500

        collection = mongo_client.law_data.old_precedents
        input_embeddings = Embeddings().generate_embeddings(
            text=category, use="google_gemini"
        )

        if not input_embeddings:
            os.remove(file_path)
            messages.append({"user": False, "text": {"error": "Failed to generate embeddings"}})
            print_message_list()
            return jsonify({"error": "Failed to generate embeddings"}), 500

        similar_cases = find_similar_documents(
            collection, input_embeddings, "vector_index", "alle_embeddings", no_of_docs=5
        )

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

        messages.append({"user": True, "text": f"File uploaded: {file.filename}"})
        messages.append({"user": False, "text": formatted_summary})
        
        print_message_list()  # Print the message list
        
        return jsonify({"Input_Doc_summary": {"summary": formatted_summary}})
    elif text:
        messages.append({"user": True, "text": text})
        conversation_context = "\n".join([f"{'User' if msg['user'] else 'Assistant'}: {msg['text']}" for msg in messages])
        
        try:
            # Check if the text is asking for a plan of action
            if "plan of action" in text.lower() or "next steps" in text.lower():
                last_summary = next((msg['text'] for msg in messages[::-1] if not msg['user']), None)
                if last_summary:
                    combined_context = f"{conversation_context}\n{last_summary}\nPlease suggest a plan of action based on the above information."
                    response = model.generate_content(combined_context)
                    response_text = response.text
                    messages.append({"user": False, "text": response_text})
                    print_message_list()  # Print the message list
                    return jsonify({"response": response_text})
            
            # Regular conversation handling
            response = model.generate_content(f"{conversation_context}\nUser: {text}")
            response_text = response.text
            
            messages.append({"user": False, "text": response_text})
            print_message_list()  # Print the message list
            return jsonify({"response": response_text})
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            messages.append({"user": False, "text": "Error processing your request. Please try again."})
            print_message_list()  # Print the message list in case of error
            return jsonify({"error": "Error processing your request. Please try again."}), 500
    else:
        return jsonify({"error": "No input provided"}), 400

@app.route('/api/clear', methods=['POST'])
def clear_messages():
    global messages
    messages = []
    logging.info("Messages cleared")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
