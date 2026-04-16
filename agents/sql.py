from services.sql_generator import generate_sql
from llm.models import DeepSeek

def generate_sql_from_agents(question, schema, model=DeepSeek):
    return generate_sql(question, schema, model)