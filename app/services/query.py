import logging
import graphene
import traceback

from sqlalchemy import select
from model.user import UserModel
from utils.query_executer import execute_query

from utils.tokens import generate_token
from utils.hashing import verify_password
from utils.json_creator import JSON
from exceptions.exceptions import LoginDataException, TokenDataException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    get_user = JSON(
        description="Login Response",
        username=graphene.String(),
        password=graphene.String(),
    )

    get_token = JSON(
        description="Token Response",
        username=graphene.String(),
    )

    get_availablity = JSON(
        description="User Response",
        username=graphene.String(),
    )

    def resolve_get_user(self, info, username, password):
        logger.info(f"Login Process started... for the username : {username}")
        try:
            query = select(
                UserModel.id,
                UserModel.first_name,
                UserModel.lastname,
                UserModel.username,
                UserModel.email,
                UserModel.salt,
                UserModel.hash,
                UserModel.phone_number,
                UserModel.age,
            ).where(UserModel.username == username)
            logger.info(f"the query is: {query}")
            result = execute_query(query, fetch_one=True)

            if result:
                logger.info(f"The query resulted with some data.")
                column_names = [col.name for col in UserModel.__table__.columns]
                user_data = {
                    column_names[i]: result[i] for i in range(len(column_names))
                }

                is_valid_password = verify_password(password, user_data.get("hash"))

                if is_valid_password:
                    del user_data["hash"], user_data["salt"]
                    token = generate_token(user_data)
                    logger.info(
                        f"The password is verified for username: {username}, and the token: {token} -  is generated."
                    )
                    return {
                        "username": user_data.get("username"),
                        "email": user_data.get("email"),
                        "token": token,
                    }
                else:
                    logger.info(
                        f"The password could not be verified for username: {username}."
                    )
                    raise LoginDataException(
                        msg="Seems like there was an invalid password entered."
                    )
            else:
                raise LoginDataException(
                    msg="Seems like there was an invalid username entered."
                )
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(f"There was an error while fetching Login data: {e}.")
            raise LoginDataException(msg=e)

    def resolve_get_token(self, info, username):
        logger.info(f"Getting token for the username : {username}")
        try:
            query = select(UserModel.username, UserModel.email).where(
                UserModel.username == username
            )
            logger.info(f"the query is: {query}")
            result = execute_query(query, fetch_one=True)

            if result:
                logger.info(f"The query resulted with some data.")
                column_names = ["username", "email"]
                user_data = {
                    column_names[i]: result[i] for i in range(len(column_names))
                }
                token = generate_token(user_data)
                logger.info(
                    f"The password is verified for username: {username}, and the token: {token} -  is generated."
                )
                return {
                    "username": user_data.get("username"),
                    "token": token,
                }
            else:
                raise TokenDataException(
                    msg="Seems like there was an invalid username entered."
                )
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(f"There was error while getting token: {e}.")
            raise TokenDataException(msg="There was error while getting token")

    def resolve_get_availablity(self, info, username):
        logger.info(f"Checking if the username exists: {username}")
        try:
            query = select(
                UserModel.username,
            ).where(UserModel.username == username)
            logger.info(f"the query is: {query}")
            result = execute_query(query, fetch_one=True)

            if result:
                return {"is_available": True}
            else:
                logger.info(msg="Seems like there was an invalid username entered.")
                return {"is_available": False}
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(f"There was error while getting token: {e}.")
            raise TokenDataException(msg="There was error while getting token")
