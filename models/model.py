from pydantic import BaseModel, Extra
from typing import Optional


class Model(BaseModel, extra=Extra.allow):
    # title: str
    id: Optional[str] = ""


#     @validator("id", pre=True)
#     def set_id(cls, v, values):
#         return create_unique_id(values["title"])


# def create_unique_id(title: str):
#     return hashlib.md5(title.encode("utf-8")).hexdigest()
