import os


class Config:
    MONGO_DB = os.environ.get("MONGO_DB", default="application")
    _MONGO_HOST = os.environ.get("MONGO_HOST", default="localhost:27017")
    MONGO_URL = f"mongodb://{_MONGO_HOST}/{MONGO_DB}"

    _REDIS_HOST = os.environ.get("REDIS_HOST", default="localhost")
    REDIS_URL = f"redis://{_REDIS_HOST}"

    DA_DATA_URL = os.environ.get("DA_DATA_URL")
    DA_DATA_KEY = os.environ.get("DA_DATA_KEY")
    DA_DATA_SECRET = os.environ.get("DA_DATA_SECRET")


config = Config()
