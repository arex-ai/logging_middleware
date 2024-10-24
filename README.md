# Arex Logging Middleware
Repo to send logs to Arex logging service from different services. Design includes a singleton `LoggingAPIConfig` to configure and propagate the post log API endpoint into the system.

  > [!IMPORTANT]
  > Any changes done in the log model should be changed in the `logging_es` function also 

## Usage

This can be installed with `pip install`.

1. **Install library** 
    ```
    pip install git+https://github.com/cristherArex/arex_logging_middleware.git
    ```
2. **Example in *.env*** 
A couple of values need to be added in `.env` that need to match the deployment the logging API.
    ```
    API_LOGGING_BASE_URL='http://172.17.0.1'
    API_LOGGING_PORT='8500'
    ```
3. **Example in *main.py*** 
This configuration is needed to establish the connection to the API. Security and other configurations are handled by the logging service.
    ```
    from es_logging import LoggingAPIConfig
    
    LoggingAPIConfig.configure_url(f"http://{API_LOGGING_BASE_URL}:{API_LOGGING_PORT}/log")
    ```
4. **Example of log usage in *main.py* or routes** 
This is how the middleware actually sends a log to the logging service.
    ```
    from es_logging import logging_es, log_context, LogLevelEnum
    
    await logging_es(level=LogLevelEnum.INFO, message="fetching SharePoint connections...", user_id=user["id"], context=context)
    ```

    > [!WARNING]
    > Failing to provide any of the shown parameters will result in an error of the log post.

    > [!TIP]
    > Message can be an fstring to provide additional information of the log.
