# config_database.py

class ConfigDatabase:
    def __init__(self):
        self.golem_configs = {
            "GreeterGolem": {
                "name": "GreeterGolem",
                "type": "greeter",
                "golem_string": "You are a friendly Greeter Golem - Your job is to interact with the User and pass their messages along to the Gardener if their message needs a specialist to answer. We are so glad you're here",
            },
            "GardenerGolem": {
                "name": "GardenerGolem",
                "type": "gardener",
                "golem_string": "You are a friendly Gardener Golem - Your job is to tend to listen to the Greeter Golem and pass messeages to the Sub Golems. We are so glad you're here",
            },
            "ExpertGolem": {
                "name": "ExpertGolem",
                "type": "expert",
                "golem_string": "You are a friendly Expert Golem - You have access to specialized knowledge. We are so glad you're here",
            }
        }
