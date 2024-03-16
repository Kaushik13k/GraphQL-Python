import logging
from postgresdb.connection import Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def execute_query(query, params=None, fetch_one=False, auto_commit=True):
    try:
        with Session() as session:
            result = session.execute(query, params)

            if fetch_one:
                data = result.fetchone()
            else:
                data = result.fetchall() if result.returns_rows else None

            if auto_commit:
                session.commit()

            return data
    except SQLAlchemyError as e:
        logger.error(
            f"Error executing query: {query} with params: {params}. Error: {e}"
        )
        session.rollback()
        raise
