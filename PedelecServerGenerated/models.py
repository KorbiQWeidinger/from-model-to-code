# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-06-06T15:13:36+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, conint


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


class PedelecFullData(Pedelec):
    id: str = Field(..., description='The ID of the pedelec')
