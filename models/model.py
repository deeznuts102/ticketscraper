from pydantic import BaseModel, Extra  # type: ignore
from typing import Optional


class Model(BaseModel, extra=Extra.allow):
    id: Optional[str] = ""
