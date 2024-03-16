import graphene
import logging
import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.mutation import MuscleMutation

from services.query import MuscleQuery
from utils.responses import success, error

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/muscle", tags=["GraphQL"], responses={404: {"description": "Not found"}}
)
async def muscle(request: dict = None) -> JSONResponse:
    try:
        logger.info(f"Executing the query for : {request.get('operation_name')}")
        schema = graphene.Schema(query=MuscleQuery, mutation=MuscleMutation)
        result = schema.execute(
            request.get("query"), variable_values=request.get("variables")
        )
        if result.errors:
            logger.info(f"There was error while executing the schema")
            raise Exception(result.errors)
        return success(result.data)
    except Exception as e:
        logger.error(f"There was an error while processing the query with error: {e}")
        return error(f"Couldn't {request.get('operation_name')}, Because: {e}")
