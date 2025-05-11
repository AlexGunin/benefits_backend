from pydantic import BaseModel

class ORMBaseModel(BaseModel):
    """
    Базовая модель для всех Pydantic-схем, которые используют from_attributes.
    """
    class Config:
        from_attributes = True