from typing import List
from fastapi.exceptions import HTTPException
import pydantic
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Attribute, BooleanAttribute, IntegerAttribute, FloatAttribute, StringAttribute
from ..interfaces import *
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as

select_attribute = with_polymorphic(Attribute, [BooleanAttribute, IntegerAttribute, FloatAttribute, StringAttribute])


async def query_attributes(session: AsyncSession, key: str, remote_reference: str):
    filters = {}
    if remote_reference:
        filters['remote_reference'] = remote_reference
    if key:
        filters['key'] = key
    result = await session.execute(select(select_attribute).filter_by(**filters))
    return result.scalars().all()


async def query_attribute_by_id(session: AsyncSession, id: int):
    
    result = await session.execute(select(select_attribute).where(Attribute.id == id))
    return result.scalars().one()


async def query_attribute_by_remote_and_id(session: AsyncSession, remote_reference: str, id: int) -> Attribute:
    result = await session.execute(
        select(select_attribute)
            .where(
                and_(
                    Attribute.remote_reference == remote_reference,
                    Attribute.id == id
                )
            )
    )
    return result.scalars().one()


async def query_attribute_by_remote_and_key(session: AsyncSession, remote_reference: str, key: str) -> Attribute:
    result = await session.execute(
        select(select_attribute)
            .where(
                and_(
                    Attribute.remote_reference == remote_reference,
                    Attribute.key == key
                )
            )
    )
    return result.scalars().one()


async def query_attributes_by_remote(session: AsyncSession, remote_reference: str) -> List[Attribute]:
    result = await session.execute(
        select(select_attribute)
            .where(
                and_(
                    Attribute.remote_reference == remote_reference,
                )
            )
    )
    return result.scalars().all()



async def insert_attribute(session: AsyncSession, attribute: AttributeIn):

    v = attribute.value

    # The order of this is sensitive
    if isinstance(v, bool):
        new = BooleanAttribute(type=bool.__name__, remote_reference=attribute.remote_reference, key=attribute.key, value=attribute.value)
    elif isinstance(attribute.value, int):
        new = IntegerAttribute(type=int.__name__, remote_reference=attribute.remote_reference, key=attribute.key, value=attribute.value)
    elif isinstance(attribute.value, float):
        new = FloatAttribute(type=float.__name__, remote_reference=attribute.remote_reference, key=attribute.key, value=attribute.value)
    elif isinstance(attribute.value, str):
        new = StringAttribute(type=str.__name__, remote_reference=attribute.remote_reference, key=attribute.key, value=attribute.value)
    else:
        raise HTTPException(501, detail={
            "status": "NOT_IMPLMENTED",
            "message": "Value must be of a type int, float, bool or string"
        })
    try:
        session.add(new)
        await session.commit()
        return parse_obj_as(AttributeOut, new)
    except IntegrityError:
        attribute_query = with_polymorphic(Attribute, [BooleanAttribute, IntegerAttribute, FloatAttribute, StringAttribute])
        found_attr = session.execute(select(attribute_query).where("attribute.key" == attribute.key))
        raise HTTPException(303, detail={
            "status": "ALREADY_EXISTS",
            "message": "Attribute already exisits follow Location"
        })