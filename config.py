import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    run_tests = os.environ.get("RUN_TESTS", default="False")
    if run_tests == "True":
        MONGO_DB = os.environ.get("MONGO_DB_TEST", default="application_test")
        _MONGO_HOST = os.environ.get("MONGO_HOST_TEST", default="localhost:27018")
        _REDIS_HOST = os.environ.get("REDIS_HOST_TEST", default="localhost:6378")
    elif run_tests == "False":
        MONGO_DB = os.environ.get("MONGO_DB", default="application")
        _MONGO_HOST = os.environ.get("MONGO_HOST", default="localhost:27017")
        _REDIS_HOST = os.environ.get("REDIS_HOST", default="localhost:6377")

    MONGO_URL = f"mongodb://{_MONGO_HOST}/{MONGO_DB}"
    REDIS_URL = f"redis://{_REDIS_HOST}"

    DA_DATA_URL = os.environ.get("DA_DATA_URL")
    DA_DATA_KEY = os.environ.get("DA_DATA_KEY")
    DA_DATA_SECRET = os.environ.get("DA_DATA_SECRET")


config = Config()
