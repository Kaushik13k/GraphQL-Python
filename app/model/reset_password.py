import graphene


class ResetPasswordModel(graphene.InputObjectType):
    user_name = graphene.String(required=True)
    password = graphene.String(required=True)
