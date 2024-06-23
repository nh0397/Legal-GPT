import openai
from retrying import retry
import fitz  # PyMuPDF
import pymongo
from pymongo.server_api import ServerApi
from typing import List, Dict, Union
import numpy as np
import google.generativeai as genai
import torch
from transformers import AutoTokenizer, AutoModel
import json
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

# Environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
OPEN_AI_KEY = os.getenv("Open_AI_Key")

openai.api_key = OPEN_AI_KEY

# Retry condition: Retry on any exception
def retry_if_exception(exception):
    return isinstance(exception, Exception)

# Function to summarize document with retry mechanism
@retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=5, wait_fixed=2000)
def summarize_document_open_ai(document: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a legal expert who provides concise summaries of legal documents.\nSummarize the following legal document, focusing on key aspects relevant for legal analysis and precedent search:\n1. Clearly identify the name of the case, including parties involved, formatted as 'Plaintiff vs Defendant.\n2. Mention the court where the case was heard and the citation details.\n3. Specify the jurisdiction under which the case was tried.\n4 Provide a comprehensive summary that includes the main issues, arguments presented, rulings made, and the final verdict. Aim for a concise summary but ensure all critical legal points and outcomes are covered. Limit the summary to approximately 500 tokens for optimal relevance and clarity.\n5. Nature of the allegation. Also, can you give the output as single json with key value pairs.",
            },
            {"role": "user", "content": document},
        ],
        max_tokens=2000,  # Adjust based on your needs
        functions=[function_schema],
        function_call={"name": "extract_relevant_data"},
    )
    # Extract the function call arguments
    function_args = response["choices"][0]["message"]["function_call"]["arguments"]
    return function_args

def perform_OCR(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def find_similar_documents(
    collection: pymongo.collection.Collection,
    inp_document_embedding: List,
    index_name: str,
    col_name: str,
    no_of_docs: int = 3,
    query: Dict = {},
) -> List:
    documents = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "path": col_name,
                    "queryVector": inp_document_embedding,
                    "numCandidates": 49,
                    "limit": no_of_docs,
                }
            },
            {"$match": query},
            {
                "$project": {
                    "name": 1,
                    "id": 1,
                    "court_name": 1,
                    "jurisdiction": 1,
                    "allegation_nature": 1,
                    "summary": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]
    )
    result_documents = list(documents)[:no_of_docs]
    return result_documents

class GoogleEmbeddings:
    def __init__(self, model_name: str = "models/embedding-001") -> None:
        self.model_name = model_name

    def generate_embeddings(self, inp: str) -> np.ndarray:
        if not GOOGLE_API_KEY:
            print("Please set correct Google API key")
            return []

        genai.configure(api_key=GOOGLE_API_KEY)
        result = genai.embed_content(
            model=self.model_name, content=inp, task_type="SEMANTIC_SIMILARITY"
        )
        embds = np.array(result["embedding"])
        return list(embds.reshape(1, -1)[0])

class BERTEmbeddings:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

    def generate_embeddings(self, inp: str):
        inputs = self.tokenizer(inp, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state
        embeddings = embeddings.mean(dim=1)
        return embeddings.tolist()[0]

class Embeddings:
    def __init__(self) -> None:
        pass

    def generate_embeddings(self, text: str, use: str = "bert") -> List:
        """
        use: "bert" or "google_gemini"
        """
        if use == "bert":
            embedding_model = BERTEmbeddings()
            return embedding_model.generate_embeddings(text)
        embedding_model = GoogleEmbeddings()
        return embedding_model.generate_embeddings(text)

class MongoDB:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def connect(self) -> Union[pymongo.MongoClient, None]:
        if not self.password:
            print("Please set env variable for password!")
            return

        escaped_username = quote_plus(self.username)
        escaped_password = quote_plus(self.password)

        uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.5hufumz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = pymongo.MongoClient(uri, server_api=ServerApi("1"))

        try:
            client.admin.command("ping")
            print("Successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(e)
        return None
