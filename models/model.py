from typing import Optional
from pydantic import BaseModel, Extra  # type: ignore


class Model(BaseModel, extra=Extra.allow):
    id: Optional[str] = ""
