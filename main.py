from agents.schema import select_schema
from agents.sql import generate_sql_from_agents
from agents.validator import main_validator
from services.tables import get_training_data, get_schema

def run_pipeline(example):
    question = example["question"]
    db_id = example["db_id"]
    gold_sql = example["query"]

    print("\n" + "="*80)
    print("🧠 QUESTION:", question)
    print("="*80)

    try:
        schema = select_schema(question, db_id)
        if not schema.strip():
            raise ValueError("Empty schema from LLM")
    except Exception as e:
        print("\n⚠️ Schema selection failed, using full schema")
        print("Error:", e)

        full_schema = get_schema(db_id)
        schema = str(full_schema)

    print("\n📦 SCHEMA:\n", schema)

    try:
        sql = generate_sql_from_agents(question, schema)

        if not sql:
            raise ValueError("Empty SQL generated")

    except Exception as e:
        print("\n⚠️ SQL generation failed")
        print("Error:", e)
        sql = ""

    print("\n🧾 GENERATED SQL:\n", sql)
    print("\n🧾 GOLD SQL:\n", gold_sql)

    try:
        result = main_validator(sql, gold_sql, db_id)
    except Exception as e:
        print("\n💥 Validator crashed!")
        print("Error:", e)

        result = {
            "syntax_valid": False,
            "execution_success": False,
            "execution_match": False,
            "keyword_score": 0,
            "error": str(e)
        }

    return result


if __name__ == "__main__":
    spider_data = get_training_data()
    example = spider_data[1]
    run_pipeline(example)