from pydantic import BaseModel


class RestaurantDB(BaseModel):
    id: int
    name: str
    contact_info: str
    location: str
    image_id: int

    class Config:
        from_attributes = True
