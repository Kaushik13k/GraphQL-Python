import logging
import graphene
import traceback
from sqlalchemy import insert

from model.signup import Signup
from model.user import UserModel
from exceptions.exceptions import SignupDataException
from utils.query_executer import execute_query
from utils.hashing import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignUp(graphene.Mutation):
    class Arguments:
        user_input = Signup(required=True)

    username = graphene.String()
    email = graphene.String()

    def mutate(self, info, user_input):
        try:
            if not (
                user_input.first_name
                and user_input.last_name
                and user_input.user_name
                and user_input.email
                and user_input.password
                and user_input.phone_number
                and user_input.age
            ):
                logger.error("All fields were not filled.")
                raise SignupDataException("All fields are required.")
            logger.info("Inputs validated successfully")
            logger.info(f"Received request to create user: {user_input.user_name}.")

            password_salted, password_hashed = hash_password(user_input.password)
            logger.info("Salt and hash generated.")
            user_model = UserModel.__table__

            query = insert(user_model).values(
                first_name=user_input.first_name,
                lastname=user_input.last_name,
                username=user_input.user_name,
                email=user_input.email,
                salt=password_salted.decode("utf-8"),
                hash=password_hashed.decode("utf-8"),
                phone_number=user_input.phone_number,
                age=user_input.age,
            )
            logger.info(f"The insert query is: {query}")

            result = execute_query(query, fetch_one=True)
            logger.info(f"Data inserted for user: {user_input.user_name} ")
            return SignUp(username=user_input.user_name, email=user_input.email)
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(
                f"There wa an error while inserting the data to DB with error: {e}"
            )
            raise SignupDataException(msg="There was error while trying to Signup")
