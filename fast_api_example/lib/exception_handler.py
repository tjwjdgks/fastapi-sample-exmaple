from starlette.requests import Request
from starlette.responses import Response
import json

from fast_api_example.lib.exception_result import default_error_result
from fast_api_example.lib.json import EnhancedJSONEncoder


def default_error_handler(request: Request, exc: Exception):
    # 예시
    return Response(
        content=json.dumps(
            default_error_result(url_path=request.url.path, exc=exc),
            cls=EnhancedJSONEncoder,
        ),
        media_type="application/json",
    )
