import graphene
import json


class JSON(graphene.Scalar):
    @staticmethod
    def parse_literal(node):
        return json.loads(node.value)

    @staticmethod
    def parse_value(value):
        return json.loads(value)
