from agents.schema import select_schema
from agents.sql import generate_sql_from_agents
from agents.validator import main_validator
from services.tables import get_training_data

spider_data = get_training_data()

example = spider_data[1]
question = example["question"]
db_id = example["db_id"]
query = example["query"]

schema = select_schema(question, db_id, )
sql = generate_sql_from_agents(question, schema)
valid = main_validator(sql, query, f"{db_id}")

print("Question:", question)
print("Schema:\n", schema)
print("SQL:", sql)
print("Ground Truth SQL:", query)
print("Valid SQL:", valid)