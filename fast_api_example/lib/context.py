from contextvars import ContextVar, Token

from fast_api_example.meta_singleton import MetaSingleton


class Context(metaclass=MetaSingleton):
    def __init__(self) -> None:
        self.session_context: ContextVar[str] = ContextVar("session_context")
        self.log_context: ContextVar[str] = ContextVar(
            "log_context", default="default_only_for_tests"
        )

    def get_session_context(self) -> str:
        return self.session_context.get()

    def set_session_context(self, session_id: str) -> Token:
        return self.session_context.set(session_id)

    def reset_session_context(self, context: Token) -> None:
        self.session_context.reset(context)

    def get_log_context(self) -> str:
        return self.log_context.get()

    def set_log_context(self, trace_id: str) -> Token:
        return self.log_context.set(trace_id)

    def reset_log_context(self, context: Token) -> None:
        self.log_context.reset(context)


app_context = Context()
