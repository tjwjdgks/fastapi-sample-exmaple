import datetime
from dataclasses import is_dataclass, asdict
from enum import Enum
from json import JSONEncoder

from pydantic import BaseModel


class EnhancedJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.model_dump()
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, Enum):
            return o.value
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)
