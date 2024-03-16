import graphene
import traceback
import logging
from sqlalchemy import update

from utils.hashing import hash_password
from model.user import UserModel
from utils.query_executer import execute_query
from model.reset_password import ResetPasswordModel
from exceptions.exceptions import ResetPasswordDataException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResetPassword(graphene.Mutation):
    class Arguments:
        user_input = ResetPasswordModel(required=True)

    message = graphene.String()

    def mutate(self, info, user_input):
        try:
            if not (user_input.password):
                logger.error("All fields were not filled.")
                raise ResetPasswordDataException("All fields are required.")
            logger.info("Inputs validated successfully")
            logger.info(f"Received request to update user: {user_input.user_name}.")

            password_salted, password_hashed = hash_password(user_input.password)
            logger.info("Salt and hash generated.")
            user_model = UserModel.__table__

            query = (
                update(user_model)
                .where(UserModel.username == user_input.user_name)
                .values(
                    salt=password_salted.decode("utf-8"),
                    hash=password_hashed.decode("utf-8"),
                )
            )
            logger.info(f"The update query is: {query}")

            result = execute_query(query)
            logger.info(f"Data inserted for user: {user_input.user_name} ")
            return ResetPassword(message="successfully updated password")
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(
                f"There wa an error while inserting the data to DB with error: {e}"
            )
            raise ResetPasswordDataException(
                msg="There was error while trying to Signup"
            )
