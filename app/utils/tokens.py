import os
import jwt
import logging
from datetime import datetime, timedelta
from exceptions.exceptions import TokenDataException
from enums.envs import Env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# openssl rand -hex 32
# secret_key = "ecbcf08955a279fac25d44f808f88f672287e34f72f5610905f0006d9de1a318"


def generate_token(payload, expiration_hours=360):
    logger.error(f"Generating the token")
    payload["exp"] = datetime.today() + timedelta(hours=expiration_hours)
    return jwt.encode(payload, Env.JWT_SECRET.value, algorithm="HS256")


def decode_token(token: str):
    try:
        logger.error(f"Trying to decode the token")
        return jwt.decode(
            token, Env.JWT_SECRET.value, verify=True, algorithms=["HS256"]
        )
    except Exception as e:
        logger.error(f"Failed to decode the token with error: {e}")
        return None


def validate_token(token: str):
    decoded_token = decode_token(token)
    if (
        not decoded_token
        or decoded_token.get("exp") <= datetime.today().timestamp() + 10 * 60
    ):
        logger.info("Token is expired or failed to decode. Refresh it.")
        return None
    return decoded_token.get("username")
