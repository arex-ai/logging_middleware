from enum import Enum
import logging
from fastapi import Request
import httpx
import uuid


LOGGING_API_URL = "http://localhost:8500/log"


logging.basicConfig(
    filename='logging_fallback.log', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.ERROR
)


class LogLevelEnum(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


async def log_context(request: Request):
    user_id = 1  # You might change this based on actual context
    execution_uuid = request.headers.get('X-Execution-UUID', str(uuid.uuid4()))
    return {
        "execution_uuid": execution_uuid,
        "request": request,
        "user_id": user_id
    }


async def logging_es(level: LogLevelEnum, message: str, context: dict):
    execution_uuid = context['execution_uuid']
    user_id = context['user_id']
    request = context['request']

    log_entry = {
        "execution_UUID": execution_uuid,
        "user_id": user_id,
        "headers": dict(request.headers),
        "ip": request.client.host,
        "port": request.client.port,
        "method": request.method,
        "path": request.url.path,
        "level": level,
        "message": message,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(LOGGING_API_URL, json=log_entry)
            if response.status_code != 200:
                logging.error(f"Failed to log to API. Status code: {response.status_code}. Log Entry: {log_entry}")
    except Exception as e:
        logging.error(f"Exception occurred while logging to API: {e}. Log Entry: {log_entry}")
