
import traceback
from functools import wraps
def log_trace(log_key: str, args, kwargs):
    exc: Exception | None = None
    url_path: str = ""
    for arg in args:
        if isinstance(arg, Exception):
            exc = arg
    if "exc" in kwargs:
        exc = kwargs["exc"]
    if "url_path" in kwargs:
        url_path = kwargs["url_path"]
    if exc:
        trace_info = "".join(traceback.format_tb(exc.__traceback__))
        print("log_key:", log_key)
        print({"url_path": url_path, "trace_info": trace_info, "error_message": str(exc)})


def log_traceback_handler(log_key: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            log_trace(log_key, args, kwargs)
            return function(*args, **kwargs)

        return wrapper

    return decorator


def async_log_traceback_handler(log_key: str):
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            log_trace(log_key, args, kwargs)
            return await function(*args, **kwargs)

        return wrapper

    return decorator


@log_traceback_handler(log_key="ERROR")
def default_error_result(*, url_path: str, exc: Exception):
    return {
        "result": "fail",
        "code": "ERROR",
        "message": str(exc),
        "url_path": url_path,
    }
