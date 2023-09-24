from uuid import uuid4

from fast_api_example.lib.context import app_context
from fast_api_example.persistence.mysql import database


def standalone_session(func):
    async def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        session_context = app_context.set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as e:
            await database.get_connection().rollback()
            raise e
        finally:
            await database.get_connection().remove()
            session_context.reset_session_context(context=session_context)

    return _standalone_session
