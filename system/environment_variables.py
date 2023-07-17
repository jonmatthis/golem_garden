import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_admin_users() -> List[str]:
    admin_users = os.getenv('ADMIN_USER_IDS')
    admin_users = admin_users.split(',')
    admin_users = [int(user) for user in admin_users]
    return admin_users


def get_mongo_uri() -> str:
    is_docker = os.getenv('IS_DOCKER', False)
    if is_docker:
        return os.getenv('MONGO_URI_DOCKER')
    else:
        return os.getenv('MONGO_URI_LOCAL')


def get_mongo_database_name():
    return os.getenv('MONGODB_DATABASE_NAME')


def get_mongo_chat_history_collection_name():
    return os.getenv('MONGODB_HISTORY_COLLECTION_NAME')


def is_course_server(server_id: int) -> bool:
    if server_id == int(os.getenv("COURSE_SERVER_ID")):
        return True
    return False
