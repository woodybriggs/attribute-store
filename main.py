from pydantic.tools import parse_obj_as
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.interfaces import *
import uvicorn
import asyncio
import typer

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional

from src.db import init_models
from src.db import get_session
from src.service import insert_attribute, query_attribute_by_id, query_attribute_by_remote_type_id_id, query_attribute_by_remote_type_id_key, query_attributes, query_attributes_by_remote_type_id
from src.interfaces import AttributeOut, AttributeIn, ErrorOut

app = FastAPI()
cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/attributes/{id}", response_model=AttributeOut)
async def get_attribute_by_id(
        id: int, 
        session: AsyncSession = Depends(get_session)
    ):
    attr = await query_attribute_by_id(session=session, id=id)
    return attr


@app.get("/attributes/{remote_reference}/{id}", response_model=AttributeOut)
async def get_attribute_by_remote_and_id(
        remote_reference: str,
        id: int, 
        session: AsyncSession = Depends(get_session)
    ):
    result = await query_attribute_by_remote_type_id_id(session=session, remote_reference=remote_reference, id=id)
    return result



@app.get("/attributes/{remote_reference}/key/{key}", response_model=AttributeOut)
async def get_attribute_by_remote_and_key(
        remote_reference: str,
        key: str, 
        session: AsyncSession = Depends(get_session)
    ):
    result = await query_attribute_by_remote_type_id_key(session=session, remote_reference=remote_reference, key=key)
    return result


@app.get("/attributes/{remote_reference}/", response_model=List[AttributeOut])
async def list_attributes_by_remote(
        remote_reference: str,
        session: AsyncSession = Depends(get_session)
    ):
    results = await query_attributes_by_remote_type_id(session=session, remote_reference=remote_reference)
    return results


@app.get("/attributes/", response_model=List[AttributeOut])
async def list_attributes(
        key: Optional[str] = None, 
        remote_reference: Optional[str] = None, 
        session: AsyncSession = Depends(get_session)
    ):
    results = await query_attributes(session=session, key=key, remote_reference=remote_reference)
    return results


@app.post('/attributes/', response_model=AttributeOut)
async def create_attribute(
        attribute: AttributeIn, 
        session: AsyncSession = Depends(get_session)
    ):
    result = await insert_attribute(session=session, attribute=attribute)
    return result


if __name__ == '__main__':
    cli()