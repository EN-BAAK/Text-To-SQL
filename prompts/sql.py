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

def review_sql_prompt(question, schema, sql):
    return f"""
        You are an expert SQL reviewer.

        Your task is to verify whether the SQL query correctly answers the question.

        Question:
        {question}

        Schema:
        {schema}

        SQL:
        {sql}

        Instructions:
        - If the SQL is correct, return it unchanged
        - If the SQL is incorrect, fix it
        - Ensure correct columns and tables
        - Ensure proper JOINs if needed
        - Do NOT explain anything
        - Output ONLY the SQL query
        - Output must be in a single line

        SQL:
        """