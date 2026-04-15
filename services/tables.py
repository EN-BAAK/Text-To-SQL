import json

tables_file = "./spider_data/spider_data/tables.json"
training_data="./spider_data/spider_data/train_spider.json"

def map_type(col_type):
    if col_type.lower() in ["text", "varchar", "char"]:
        return "TEXT"
    elif col_type.lower() in ["number", "integer", "int", "real", "float"]:
        return "INTEGER"
    elif col_type.lower() in ["boolean", "bool"]:
        return "BOOLEAN"
    else:
        return "TEXT"

def get_schema(db_id, tables_file=tables_file):
    with open(tables_file, "r") as f:
        tables_data = json.load(f)

    return next(db for db in tables_data if db["db_id"] == db_id)

def build_schema_from_llm(selected, full_schema_dict):
    table_names = full_schema_dict["table_names_original"]
    column_names = full_schema_dict["column_names_original"]
    column_types = full_schema_dict["column_types"]
    primary_keys = full_schema_dict["primary_keys"]

    schema_str = ""

    pk_set = set(primary_keys)

    for table in selected["tables"]:
        schema_str += f"TABLE {table} (\n"

        cols = []

        for idx, (t, col) in enumerate(column_names):
            if table_names[t] == table:
                col_name = col
                col_type = column_types[idx]

                if col_name in selected["columns"].get(table, []):
                    col_def = f"{col_name} {col_type}"

                    if idx in pk_set:
                        col_def += " PRIMARY KEY"

                    cols.append(col_def)

        schema_str += ", ".join(cols)
        schema_str += "\n)\n\n"

    return schema_str.strip()

def get_training_data(spider_file=training_data):
    with open(spider_file, "r") as f:
        spider_data = json.load(f) 
    return spider_data

def print_execution_results(pred_result, gold_result):
    print("\n" + "="*80)
    print("📊 EXECUTION RESULT COMPARISON")
    print("="*80)

    print(f"\n🔵 Predicted Rows ({len(pred_result)} rows):")
    for i, row in enumerate(sorted(pred_result), 1):
        print(f"{i:02d}. {row}")

    print("\n" + "-"*80)

    print(f"\n🟢 Gold Rows ({len(gold_result)} rows):")
    for i, row in enumerate(sorted(gold_result), 1):
        print(f"{i:02d}. {row}")

    print("\n" + "="*80)

    pred_set = set(pred_result)
    gold_set = set(gold_result)

    correct = pred_set & gold_set
    missing = gold_set - pred_set
    extra = pred_set - gold_set

    print("📌 SUMMARY:")
    print(f"✔ Correct matches: {len(correct)}")
    print(f"❌ Missing rows: {len(missing)}")
    print(f"➕ Extra rows: {len(extra)}")

    print("="*80 + "\n")