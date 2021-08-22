from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.attributes import query_attribute_by_remote_and_id, query_attribute_by_remote_and_key, query_attributes, insert_attribute, query_attributes_by_remote
from ..dependencies import get_session
from ..interfaces import AttributeOut, AttributeIn, ErrorOut


router = APIRouter(
    prefix="/attributes",
    tags=['Attributes']
)


@router.get(
    "/{remote_reference}/{id}",
    response_model=AttributeOut,
    operation_id="get_attribute_by_remote_and_id"
)
async def get_attribute_by_remote_and_id(
        remote_reference: str,
        id: int, 
        session: AsyncSession = Depends(get_session)
    ):
    result = await query_attribute_by_remote_and_id(session=session, remote_reference=remote_reference, id=id)
    return result



@router.get(
    "/{remote_reference}/key/{key}",
    response_model=AttributeOut,
    operation_id="get_attribute_by_remote_and_key"
)
async def get_attribute_by_remote_and_key(
        remote_reference: str,
        key: str, 
        session: AsyncSession = Depends(get_session)
    ):
    result = await query_attribute_by_remote_and_key(session=session, remote_reference=remote_reference, key=key)
    return result


@router.get(
    "/{remote_reference}/",
    response_model=List[AttributeOut],
    operation_id="list_attributes_by_remote"
)
async def list_attributes_by_remote(
        remote_reference: str,
        session: AsyncSession = Depends(get_session)
    ):
    results = await query_attributes_by_remote(session=session, remote_reference=remote_reference)
    return results


@router.get(
    "/",
    response_model=List[AttributeOut],
    operation_id="list_attributes"
)
async def list_attributes(
        key: Optional[str] = None, 
        remote_reference: Optional[str] = None, 
        session: AsyncSession = Depends(get_session)
    ):
    results = await query_attributes(session=session, key=key, remote_reference=remote_reference)
    return results


@router.post(
    '/', 
    response_model=AttributeOut,
    operation_id="create_attribute",
    responses={
        501: {
            "description": "Not Implmented",
            "model": ErrorOut
        }
    }
)
async def create_attribute(
        attribute: AttributeIn, 
        session: AsyncSession = Depends(get_session)
    ):
    """
    Attributes are stored and retrieved against the remote_reference value
    - **remote_reference**: 256 character length string value, perfect for keccack256 hashes. How you decide to use this is up to you.
    - **key**: 256 character length string for the name of your attribute that you want to store. You can only have one key per remote_reference
    - **value**: values are for the value you want to store with the key. 

    Extra Info: Values are infered by type and stored in their own database table
    """
    result = await insert_attribute(session=session, attribute=attribute)
    return result

