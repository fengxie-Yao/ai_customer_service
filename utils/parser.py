import json
import re


def safe_json_parse(text: str, default: dict):
    """
    永不抛异常的JSON解析
    """
    try:
        return json.loads(text)
    except:
        pass

    # 尝试提取JSON块
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    # 兜底
    return default


def validate_extraction(data: dict):
    return {
        "order_id": str(data.get("order_id", "")),
        "product": str(data.get("product", "")),
        "issue": str(data.get("issue", ""))
    }


def validate_intent(data: dict):
    intent = data.get("intent", "")

    if intent not in ["refund", "complaint", "query"]:
        intent = "query"

    return {"intent": intent}


def call_with_retry(chain, input_data, default, validator, max_retry=2):
    for _ in range(max_retry):
        result = chain.invoke(input_data)
        parsed = safe_json_parse(result.content, default)
        validated = validator(parsed)

        # 判断是否有效
        if any(validated.values()):
            return validated

    return default
