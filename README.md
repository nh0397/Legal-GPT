# Legal Document Analysis Platform

## Overview
This platform leverages Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to analyze and summarize archaic legal documents related to crime. It aims to provide valuable insights and recommendations to various stakeholders, including legal professionals, laymen, law students, researchers, and policymakers.

## Features
- **Document Summarization**: Generate concise summaries of lengthy legal documents for quick reference.
- **Information Retrieval**: Advanced search capabilities to find relevant cases or documents based on specific queries.
- **Legal Analysis and Recommendations**: Analyze historic case documents to generate insights and actionable plans.
- **Context-Specific Question Answering**: Ask questions about legal documents and receive detailed, context-specific answers.

## Use Cases
### Legal Research
- Quick access to relevant case precedents and summaries.
- Aids in case preparation and study of legal trends.

### Case Preparation
- Obtain actionable plans based on past judgments and current evidence.
- Suggest legal strategies based on historical case outcomes.

### Public Access to Legal Information
- Simplified summaries of complex legal documents for laymen.
- Recommendations for suitable legal teams based on success ratios.

### Judicial Analytics
- Analysis of historical data for decision-making.
- Insights into legal outcomes for policy formulation and judicial review.

## Benefits
### For Legal Professionals
- **Efficiency**: Reduced time spent on manual document review and research.
- **Accuracy**: Improved accuracy in finding relevant cases and legal precedents.
- **Insights**: Enhanced ability to develop legal strategies based on historical data.

### For Laymen/Plaintiffs
- **Accessibility**: Easier access to legal information and understanding of legal processes.
- **Informed Decisions**: Ability to make informed decisions about legal representation and strategies.

### For Law Students and Researchers
- **Educational Tool**: A valuable resource for studying legal history and understanding case law.
- **Research Aid**: Facilitates in-depth legal research with quick access to summarized and relevant information.

### For Judges and Policymakers
- **Data-Driven Decisions**: Ability to make informed, data-driven decisions and policies.
- **Trend Analysis**: Insights into legal trends and patterns over time.

## Getting Started

### Prerequisites
- Python 3.8+
- MongoDB
- Node.js
- Required Python libraries (listed in `requirements.txt`)
- Required Node.js packages (listed in `client/package.json`)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/legal-document-analysis-platform.git
    cd legal-document-analysis-platform
    ```

2. **Install the required libraries for the backend:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up MongoDB and ensure it's running.**

4. **Install the required packages for the frontend:**
    ```sh
    cd client
    npm install
    cd ..
    ```

5. **Set up the environment variables:**
    Create a `.env` file in the root directory and add the following lines:
    ```plaintext
    GEMINI_API_KEY=your_gemini_api_key
    USER_NAME=your_username
    PASSWORD=your_password
    Open_AI_Key=your_openai_key
    ```

### Usage

1. **Data Ingestion:**
    - Convert the archaic legal documents into word embeddings.
    - Store the embeddings and summaries in MongoDB.

2. **Running the Platform:**
    - Start the backend server:
        ```sh
        python app.py
        ```
    - Start the frontend server:
        ```sh
        cd client
        npm start
        ```

3. **Access the web interface at `http://localhost:3000`.**

4. **Using the Features:**
    - **Summarization**: Upload documents and generate summaries.
    - **Search**: Use the search bar to find relevant cases.
    - **Q&A**: Ask questions about legal documents and get detailed answers.
    - **Analysis**: Generate insights and recommendations based on historical data.

## Demo

![LegalGpt](./Gif/LegalGPT.gif)

## Contributing

We welcome contributions to improve this platform. Please follow these steps to contribute:

1. **Fork the repository.**
2. **Create a new branch:**
    ```sh
    git checkout -b feature-branch
    ```
3. **Commit your changes:**
    ```sh
    git commit -am 'Add new feature'
    ```
4. **Push to the branch:**
    ```sh
    git push origin feature-branch
    ```
5. **Create a new Pull Request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact Naisarg Halvadiya.
