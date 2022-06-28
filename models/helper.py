import json
from typing import List
from pydantic import BaseModel


def store_models(path: str, models: List[BaseModel]):
    with open(path, "w") as f:
        models = [model.dict() for model in models]
        f.write(json.dumps(models, default=str))
