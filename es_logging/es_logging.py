from enum import Enum
import logging
import uuid
import os

from fastapi import Request
import httpx


class LoggingAPIConfig:
    _url = None

    @classmethod
    def configure_url(cls, url: str):
        cls._url = url
        print(f"Logging API URL set to: {cls._url}")

    @classmethod
    def get_url(cls):
        if cls._url is None:
            raise ValueError("Logging API URL has not been set. Call 'configure_logging_api' first.")
        return cls._url
    

# Create the 'es_logs' directory and set up the logging fallback file
LOG_DIR = os.path.join(os.getcwd(), "es_logs")
LOG_FILE = os.path.join(LOG_DIR, "logging_fallback.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)


class LogLevelEnum(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


async def url_check():
    logging_api_url = LoggingAPIConfig.get_url()
    if not logging_api_url:
        return {
            "Error": "URL must be set for usage."
        }


async def log_context(request: Request):
    execution_uuid = request.headers.get('X-Execution-UUID', str(uuid.uuid4()))

    token = request.headers.get('authorization')
    if not token:
        raise ValueError("Authorization token is missing from the headers.")
    
    return {
        "token": token,
        "execution_uuid": execution_uuid,
        "request": request,
    }


async def logging_es(level: LogLevelEnum, message: str, user_id: int, context: dict):
    await url_check()
    execution_uuid = context['execution_uuid']
    request = context['request']
    token = context['token']

    headers = {
        "Authorization": token
    }

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
            logging_api_url = LoggingAPIConfig.get_url()
            response = await client.post(logging_api_url, headers=headers, json=log_entry)
            if response.status_code != 200:
                print(f"Failed to log to API. Status code: {response.status_code}. Headers: {headers}. Log Entry: {log_entry}")
                return response
            return response
    except Exception as e:
        print(f"Exception occurred while logging to API: {e}. Log Entry: {log_entry}")
        return e
