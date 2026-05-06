import logging

logger = logging.getLogger("ai_service")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("app.log")
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)