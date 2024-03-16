import graphene
import logging
import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.mutation import Mutation

from services.query import Query
from utils.responses import success, error

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/entry_point", tags=["GraphQL"], responses={404: {"description": "Not found"}}
)
async def entry_point(request: dict = None) -> JSONResponse:
    try:
        logger.info(f"Executing the query for : {request.get('operation_name')}")
        schema = graphene.Schema(query=Query, mutation=Mutation)
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
