from services.sql_generator import generate_sql, llm_review_sql
from llm.models import DeepSeek

def generate_sql_from_agents(question, schema):
    sql = generate_sql(question, schema, DeepSeek)

    for _ in range(2):
        new_sql = llm_review_sql(question, schema, sql, DeepSeek)
        if not new_sql or new_sql == sql:
            break
        sql = new_sql

    return sql