from pydantic import BaseModel
import json

def base_model_to_json(model: BaseModel):
    return json.dumps(model.dict())