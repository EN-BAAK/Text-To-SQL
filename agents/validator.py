import sqlite3
import re

from services.tables import print_execution_results

database_files_path = "./spider_data/spider_data/database"

SQL_KEYWORDS = {
    "select", "from", "where", "join", "inner", "left", "right",
    "group", "order", "by", "having", "insert", "update", "delete",
    "count", "max", "min", "avg", "sum"
}

def execute_query(sql, db):
    db_path = f"{database_files_path}/{db}/{db}.sqlite"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return set(result)
    except:
        conn.close()
        return None

def extract_sql_keywords(sql):
    sql = sql.lower()
    words = re.findall(r"\b\w+\b", sql)
    return set([w for w in words if w in SQL_KEYWORDS])


def keyword_similarity(pred_sql, gold_sql):
    pred_keys = extract_sql_keywords(pred_sql)
    gold_keys = extract_sql_keywords(gold_sql)

    if not pred_keys and not gold_keys:
        return 1.0

    intersection = pred_keys.intersection(gold_keys)
    union = pred_keys.union(gold_keys)

    return len(intersection) / len(union)

def validate_syntax(sql, db):
    db_path = f"{database_files_path}/{db}/{db}.sqlite"

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(sql)
        conn.close()
        return True
    except:
        conn.close()
        return False

def validate_execution(pred_sql, gold_sql, db):
    pred_result = execute_query(pred_sql, db)
    gold_result = execute_query(gold_sql, db)

    if pred_result is None or gold_result is None:
        return False

    is_match = pred_result == gold_result

    return {
        "is_match": is_match,
        "pred_result": pred_result,
        "gold_result": gold_result
    }

def main_validator(pred_sql, gold_sql, db):
    syntax_valid = validate_syntax(pred_sql, db)
    execution_match = validate_execution(pred_sql, gold_sql, db)
    keyword_score = keyword_similarity(pred_sql, gold_sql)

    print_execution_results(execution_match["pred_result"], execution_match["gold_result"])

    return {
        "syntax_valid": syntax_valid,
        "execution_match": execution_match["is_match"],
        "keyword_score": keyword_score
    }