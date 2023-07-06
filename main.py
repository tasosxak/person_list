from app.routes import app
from loguru import logger
logger.add("app.log", rotation="500 MB", compression="zip", format="{time} - {level} - {message}")