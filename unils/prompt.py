def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_history(memory):
    return "\n".join([
        f"{m['role']}：{m['content']}"
        for m in memory[-5:]  # 只保留最近5轮
    ])
