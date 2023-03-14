import os
from dotenv import load_dotenv
from ast import literal_eval
load_dotenv()


class Config:
    # FASTAPI
    TITLE = os.environ.get("TITLE")
    VERSION = os.environ.get("VERSION")
    DESCRIPTION = os.environ.get("DESCRIPTION")

    # SQLITE
    SQLITE_PATH = os.environ.get("SQLITE_PATH")
    SQLITE_DB = f"sqlite:///{SQLITE_PATH}"

    # Log settings
    LOG_FOLDER = os.environ.get("LOG_FOLDER")

    # Mecha Melters Token and Staking Contract ABI
    MMABI = literal_eval(os.environ.get("MMABI"))
    MMSABI = literal_eval(os.environ.get("MMSABI"))
    MM_STAKING_ADD = os.environ.get("MM_STAKING_ADD")
