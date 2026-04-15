from llm.client import client
from prompts.sql import build_schema_linking_prompt, build_sql_prompt
from services.helpers import clean_selection_tables

def llm_model_response(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

def generate_sql(question, schema, model):
    prompt = build_sql_prompt(question, schema)
    return llm_model_response(prompt, model)

def llm_selection_schema(question, schema, model):
    prompt = build_schema_linking_prompt(question, schema)
    response = llm_model_response(prompt, model)

    return clean_selection_tables(response)