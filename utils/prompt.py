from pathlib import Path
from langchain_core.messages import BaseMessage

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_prompt(path: str):
    p = PROJECT_ROOT / path
    with p.open("r", encoding="utf-8") as f:
        return f.read()


def _msg_to_role_content(m):
    # BaseMessage 和旧 dict
    if isinstance(m, BaseMessage):
        return m.type, m.content
    if isinstance(m, dict):
        return m.get("role", "unknown"), m.get("content", "")
    return "unknown", str(m)


def format_history(memory):
    lines = []
    for m in memory[-5:]:
        role, content = _msg_to_role_content(m)
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
