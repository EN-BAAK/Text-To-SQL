from services.sql_generator import generate_sql
from llm.models import DeepSeek

def generate_sql_from_agents(question, schema):
    return generate_sql(question, schema, DeepSeek)