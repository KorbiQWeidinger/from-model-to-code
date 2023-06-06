# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-06-06T15:13:36+00:00

from __future__ import annotations

from typing import List, Union

from fastapi import FastAPI

from models import Pedelec, PedelecFullData

app = FastAPI(
    title='Pedelec API',
    description='CRUD operations for Pedelec',
    version='0.0.1',
    servers=[{'url': 'http://localhost:8000'}],
)


@app.get('/pedelecs', response_model=List[PedelecFullData])
def get_pedelecs() -> List[PedelecFullData]:
    """
    Retrieve all Pedelecs
    """
    pass


@app.post(
    '/pedelecs', response_model=None, responses={'201': {'model': PedelecFullData}}
)
def post_pedelecs(body: Pedelec) -> Union[None, PedelecFullData]:
    """
    Create a new Pedelec
    """
    pass


@app.get('/pedelecs/{id}', response_model=PedelecFullData)
def get_pedelecs_id(id: str) -> PedelecFullData:
    """
    Get a specific Pedelec by ID
    """
    pass