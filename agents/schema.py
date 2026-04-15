from services.sql_generator import llm_selection_schema
from services.tables import build_schema_from_llm, get_schema
from llm.models import DeepSeek

def select_schema(question, db_id):
    db_schema = get_schema(db_id)

    table_names = db_schema["table_names_original"]
    column_names = db_schema["column_names_original"]
    column_types = db_schema["column_types"]
    primary_keys = db_schema["primary_keys"]

    table_columns = {i: [] for i in range(len(table_names))}

    for idx, (table_id, col_name) in enumerate(column_names):
        if table_id == -1:
            continue

        col_type = column_types[idx]
        is_pk = idx in primary_keys
        table_columns[table_id].append((col_name, col_type, is_pk))

    selected = llm_selection_schema(question, db_schema, DeepSeek)
    return build_schema_from_llm(selected, db_schema)