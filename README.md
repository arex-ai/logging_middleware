# Arex Logging MiddleWare
Repo to send logs to Arex logging service from different services.

## Usage

This can be installed as pip install in requirements or copy the es_logging.py file inside the required repository to use.

To install as pip add the following line to requirements.txt
  ```
  git+https://github.com/cristherArex/arex_logging_middleware.git
  ```
1. **Example in *main.py*** This establish the connection url for sending logs to the service, security and other configurations are handled by the middleware.
   ```
   from es_logging import configure_logging_api
   
   configure_logging_api("http://logging_service_url:logging_service_port/log")
   ```
 2. **Example of log insertion in *main.py* or routes** This is how we actually send logs to the logging service.
   ```
   from es_logging import logging_es, log_context, LogLevelEnum
   
   await logging_es(level=LogLevelEnum.INFO, message="Some log message...", context=context)
   ```
