import logging
import graphene
import traceback
from sqlalchemy import insert
from sqlalchemy import select


from model.muscle_group import MuscleGroup, MuscleGroupModel
from exceptions.exceptions import MuscleGroupCreationException
from utils.query_executer import execute_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateMuscleGroup(graphene.Mutation):
    class Arguments:
        user_input = MuscleGroup(required=True)

    muscle_group_name = graphene.String()
    muscle_group_image = graphene.String()
    muscle_group_message = graphene.String()


    def mutate(self, info, user_input):
        try:
            if not (
                user_input.muscle_group_name
                and user_input.muscle_group_image
            ):
                logger.error("All fields were not filled.")
                raise MuscleGroupCreationException("All fields are required.")
            logger.info("Inputs validated successfully")
            logger.info(f"Received request to create muscle group: {user_input.muscle_group_name}.")

            user_model = MuscleGroupModel.__table__
            check_query = select([user_model.c.id]).where(user_model.c.muscle_group_name == user_input.muscle_group_name)
            result = execute_query(check_query, fetch_one=True)

            if result:
                logger.error("Muscle group name already exists.")
                return CreateMuscleGroup(muscle_group_name=None, muscle_group_image=None, muscle_group_message="Muscle group name already exists.")

            query = insert(user_model).values(
                muscle_group_name=user_input.muscle_group_name,
                muscle_group_image=user_input.muscle_group_image,
            )
            logger.info(f"The insert query is: {query}")

            result = execute_query(query, fetch_one=True)
            logger.info(f"Data inserted for muscle_group_name: {user_input.muscle_group_name} ")
            return CreateMuscleGroup(muscle_group_name=user_input.muscle_group_name, muscle_group_image=user_input.muscle_group_image, muscle_group_message="Inserted Successfully.")

        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(
                f"There wa an error while inserting the data to DB with error: {e}"
            )
            raise MuscleGroupCreationException(msg="There was error while trying to CreateMuscleGroup")
