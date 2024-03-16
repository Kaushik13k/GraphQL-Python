import graphene

from services.signup import SignUp
from services.muscle_group import CreateMuscleGroup
from services.reset_password import ResetPassword


class Mutation(graphene.ObjectType):
    signup = SignUp.Field()
    reset_password = ResetPassword.Field()


class MuscleMutation(graphene.ObjectType):
    create_muscle = CreateMuscleGroup.Field()
    # reset_password = ResetPassword.Field()
