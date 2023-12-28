from pydantic import BaseModel


class DinnerSetDB(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_id: int

    class Config:
        from_attributes = True
