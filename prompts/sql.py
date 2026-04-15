def build_sql_prompt(question, schema):
    return f"""
        You are a SQL expert.

        Database schema:
        {schema}

        Convert the following question to SQL:
        {question}

        NOTES:
        - Use JOIN only if necessary for answering the question

        IMPORTANT:
        - Only output the SQL query
        - Do NOT explain
        - Do NOT include reasoning
        - Do NOT format the SQL query, just output it as a single line without any line breaks or indentation.
        """

def build_schema_linking_prompt(question, schema):
    return f"""
        You are a database expert.

        Your task is to select ONLY the necessary tables and columns needed to answer the question.

        Database schema:
        {schema}

        Question:
        {question}

        Return format (STRICT JSON):
        {{
        "tables": ["table1", "table2"],
        "columns": {{
            "table1": ["col1", "col2"],
            "table2": ["col3"]
            }}
        }}

        Rules:
        - Only include necessary tables
        - Only include necessary columns
        - Do NOT include explanations
        - Output ONLY valid JSON
        """