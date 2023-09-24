from uuid import uuid4

from starlette.types import ASGIApp, Scope, Receive, Send

from fast_api_example.lib.context import app_context
from fast_api_example.persistence.mysql import database


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        session_context = app_context.set_session_context(session_id=session_id)
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await database.get_connection().remove()
            app_context.reset_session_context(context=session_context)


class LogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        app_context.set_log_context(trace_id=session_id)
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
