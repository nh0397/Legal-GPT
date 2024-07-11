function_schema = {
    "name": "extract_relevant_data",
    "description": "You are a legal expert who provides concise summaries of legal documents.",
    "parameters": {
        "type": "object",
        "properties": {
            "case_name": {
                "type": "string",
                "description": ""
            },
            "court_name": {
                "type": "string",
                "description": "Mention the court where the case was heard and the citation details"
            },
            "jurisdiction": {
                "type": "string",
                "description": "Specify the jurisdiction under which the case was tried"
            },
            "summary": {
                "type": "string",
                "description": "Provide a comprehensive summary that includes the main issues, arguments presented, rulings made, and the final verdict. Aim for a concise summary but ensure all critical legal points and outcomes are covered. Limit the summary to approximately 500 tokens for optimal relevance and clarity"
            },
            "allegation_nature": {
                "type": "string",
                "description": "Provide the nature of the allegation"
            },
        },
        "required": ["case_name", "court_name", "jurisdiction", "summary", "allegation_nature"]
    }
}