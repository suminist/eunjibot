import motor.motor_asyncio

from secret_keys import MONGODB_CONNECTION
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION)


def get_guilds_collection():
    return get_database()["guilds"]


def get_users_collection():
    return get_database()["users"]


def get_feeds_twitter_collection():
    return get_database()["feeds_twitter"]


def get_database():
    return client.overall
