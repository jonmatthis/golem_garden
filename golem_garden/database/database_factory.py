from enum import Enum

from typing import Optional

from golem_garden.database._strategies.json_database import JSONDatabase
from golem_garden.database._strategies.mongo_database import MongoDatabase


class DatabaseType(Enum):
    JSON = "json"
    MONGODB = "mongodatabase"
    SQL = "sql"


def get_database(database_type: DatabaseType = DatabaseType.JSON,
                 database_path: Optional[str] = None):
    if database_type == DatabaseType.JSON:
        return JSONDatabase()

    elif database_type == DatabaseType.MONGODB:
        # Set up appropriate parameters and return an instance of the MongoDB class
        pass

    elif database_type == DatabaseType.SQL:
        return MongoDatabase(database_path)
    else:
        raise ValueError(f"Unsupported database type: {database_type}")


if __name__ == "__main__":
    database_type = DatabaseType.JSON
    database_path = "chat_history.json"
    subject_id = "subject1"
    golem_id = "golem1"

    database = get_database(database_type, database_path)

    database.add_message(subject_id, golem_id, "Hello Golem!")
    database.add_response(subject_id, golem_id, "Hello, how can I help you?")

    query_dict = {
        "subject_id": subject_id,
        "golem_id": golem_id
    }

    print(database.get_history(query_dict))
