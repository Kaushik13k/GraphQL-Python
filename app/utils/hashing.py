import bcrypt


def hash_password(password, salt_rounds=12):
    salt = bcrypt.gensalt(rounds=salt_rounds)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return salt, hashed_password


def verify_password(password, hash_salt_object):
    return bcrypt.checkpw(password.encode("utf-8"), hash_salt_object.encode("utf-8"))
