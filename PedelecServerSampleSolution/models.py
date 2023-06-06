# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-05-19T12:33:48+00:00

from __future__ import annotations

from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, conint


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Location(BaseModel):
    latitude: float
    longitude: float
    altitude: float


class Pedelec(BaseModel):
    charge: Optional[conint(ge=0, le=100)] = Field(
        None,
        description='Current charge level of the pedelec, expressed as percentage in (0,100)',
        title='Charge',
    )
    isAvailable: bool
    location: Optional[Location] = None
    name: str


class PedelecFullData(Pedelec):
    id: PyObjectId = Field(..., description='The ID of the pedelec', alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}