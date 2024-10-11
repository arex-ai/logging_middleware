from enum import Enum
import logging
import uuid
import os

from fastapi import Request
import httpx


# Configs the URL 
LOGGING_API_URL = None

def configure_logging_api(url: str):
    """Function to configure the logging API URL."""
    global LOGGING_API_URL
    LOGGING_API_URL = url


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
    if not LOGGING_API_URL:
        return {
            "Error": "URL must be set for usage."
        }


async def log_context(request: Request):
    user_id = 1  #FIXME
    execution_uuid = request.headers.get('X-Execution-UUID', str(uuid.uuid4()))
    return {
        "execution_uuid": execution_uuid,
        "request": request,
        "user_id": user_id
    }


async def logging_es(level: LogLevelEnum, message: str, context: dict):
    await url_check()
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
                return response
            return response
    except Exception as e:
        logging.error(f"Exception occurred while logging to API: {e}. Log Entry: {log_entry}")
        return e
    

async def logging_es(level: LogLevelEnum, message: str, context: dict):
    await url_check()
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
                print(f"Failed to log to API. Status code: {response.status_code}. Log Entry: {log_entry}")
                return response
            return response
    except Exception as e:
        print(f"Exception occurred while logging to API: {e}. Log Entry: {log_entry}")
        return e
