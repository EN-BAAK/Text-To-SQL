import re
from services.helpers import extract_sql_keywords, is_safe_sql
from services.tables import execute_query, print_execution_results

def keyword_similarity(pred_sql, gold_sql):
    pred_keys = extract_sql_keywords(pred_sql)
    gold_keys = extract_sql_keywords(gold_sql)

    if not pred_keys and not gold_keys:
        return 1.0

    intersection = pred_keys.intersection(gold_keys)
    union = pred_keys.union(gold_keys)

    return len(intersection) / len(union)

def validate_execution(pred_sql, gold_sql, db):
    pred = execute_query(pred_sql, db)
    gold = execute_query(gold_sql, db)

    return {
        "is_match": False if not pred["success"] or not gold["success"] else pred["result"] == gold["result"],
        "pred_result": pred["result"],
        "gold_result": gold["result"],
        "error": pred["error"] or gold["error"]
    }

def main_validator(pred_sql, gold_sql, db):
    is_safe, reason = is_safe_sql(pred_sql)
    if not is_safe:
        print("\n🚫 Unsafe SQL detected!")
        print("Reason:", reason)

        return {
            "syntax_valid": False,
            "execution_success": False,
            "execution_match": False,
            "keyword_score": 0.0,
            "error": reason,
            "pred_result": None,
            "gold_result": None
        }

    execution = validate_execution(pred_sql, gold_sql, db)
    keyword_score = keyword_similarity(pred_sql, gold_sql)

    result = {
        "syntax_valid": execution.get("error") is None,
        "execution_success": False,
        "execution_match": False,
        "keyword_score": keyword_score,
        "error": execution.get("error"),
        "pred_result": execution.get("pred_result"),
        "gold_result": execution.get("gold_result")
    }

    if result["pred_result"] is not None and result["gold_result"] is not None:
        result["execution_success"] = True
        result["execution_match"] = execution.get("is_match", False)

    if result["execution_success"]:
        print_execution_results(
            result["pred_result"],
            result["gold_result"]
        )
    else:
        print("\n⚠️ Execution failed")
        print("Error:", result["error"])

    return result