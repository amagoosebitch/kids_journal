from pydantic import BaseModel, validator


class CleverBaseModel(BaseModel):
    @validator("*", pre=True)
    def blank_strings(cls, v):
        if v == "None" or v == "":
            return None
        return v
