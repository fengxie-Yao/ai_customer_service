import redis
import json
from typing import Dict, Optional
from redis.exceptions import RedisError
from langchain_core.messages import message_to_dict, messages_from_dict


class RedisSessionStore:
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            decode_responses: bool = True
    ):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses
        )
        self.available = True
        try:
            self.redis.ping()
        except RedisError:
            self.available = False

    # 获取会话
    def get(self, session_id: str) -> Dict:
        if not self.available:
            return self._default_session()
        try:
            data = self.redis.get(f"session:{session_id}")
        except RedisError:
            return self._default_session()
        if data:
            data = json.loads(data)
            data["memory"] = messages_from_dict(data["memory"])
            return data
        return self._default_session()

    # 保存会话（可加过期时间，工程必备）
    def save(
            self,
            session_id: str,
            session: Dict,
            ex: Optional[int] = 86400  # 默认 1 天过期
    ):
        if not self.available:
            return

        key = f"session:{session_id}"
        msg_dicts = [message_to_dict(m) for m in session["memory"]]
        data = {
            "memory": msg_dicts,
            "state": {
                "order_id": session["state"]["order_id"],
                "product": session["state"]["product"],
                "issue": session["state"]["issue"],
                "intent": session["state"]["intent"]
            }
        }
        try:
            self.redis.set(
                key,
                json.dumps(data, ensure_ascii=False),
                ex=ex
            )
        except RedisError:
            return

    def _default_session(self) -> Dict:
        return {
            "memory": [],
            "state": {"order_id": "", "product": "", "issue": "", "intent": ""}
        }
