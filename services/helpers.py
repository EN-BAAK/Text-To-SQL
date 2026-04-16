import re
import json

SQL_KEYWORDS = {
    "select", "from", "where", "join", "inner", "left", "right",
    "group", "order", "by", "having", "insert", "update", "delete",
    "count", "max", "min", "avg", "sum"
}
FORBIDDEN_SQL_ACTIONS = ["drop", "delete", "update", "insert", "alter", "create"]

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

def clean_sql_output(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    match = re.search(r"select .*", text, re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(0)
    else:
        return ""

    text = text.split(";")[0]

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    if not text.lower().startswith("select"):
        return ""

    return text

def extract_sql_keywords(sql):
    sql = sql.lower()
    words = re.findall(r"\b\w+\b", sql)
    return set([w for w in words if w in SQL_KEYWORDS])

def is_safe_sql(sql: str):
    if not sql:
        return False, "Empty SQL"

    sql_lower = sql.lower()

    if not sql_lower.strip().startswith("select"):
        return False, "Only SELECT statements are allowed"

    for word in FORBIDDEN_SQL_ACTIONS:
        if word in sql_lower:
            return False, f"Forbidden keyword detected: {word}"

    return True, None