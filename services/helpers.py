import re
import json

def clean_selection_tables(text: str):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "tables": [],
            "columns": {}
        }