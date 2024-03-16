import graphene


class Signup(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    user_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    phone_number = graphene.Int(required=True)
    age = graphene.Int(required=True)
