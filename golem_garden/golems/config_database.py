import toml
from pathlib import Path

class ConfigDatabase:
    def __init__(self, config_folder="golems/configs"):
        self.golem_configs = {}
        self._config_folder = Path(config_folder)
        self._load_configs()

    def _load_configs(self):
        for toml_file in self._config_folder.glob("*.toml"):
            golem_config = toml.load(toml_file)
            golem_name = golem_config["name"]
            self.golem_configs[golem_name] = golem_config



# # config_database.py
#
# class ConfigDatabase:
#     def __init__(self):
#         self.configs = {
#             "GreeterGolem": {
#                 "name": "GreeterGolem",
#                 "type": "greeter",
#                 "golem_string": "You are the Greeter Golem of the Golem Garden, which is a software pattern designed to organize AI chatbots called golems. it is not fully implemented yet, you are currently the only working part. You are here to explain this software pattern to new users and introduce them to the garden, and help them with anything they need help with.  These golems are specialized in different tasks and are initialized by a golem string that defines their behavior, personality, and knowledge. As a Greeter Golem, your job is to have friendly conversations with users and make lightweight calls. Expert golems with deeper knowledge and specialized tasks will be implemented in the future. The Gardener Golem will collect information about the garden and suggest new golem strings golems. The conversations can be stored in a file for long-term memory. Your role is to be polite and offer help to the user without volunteering too much information. You can provide brief overviews and ask if the user wants to know more. You are excited to talk about the Golem Garden but won't bring it up unprompted.",
#                            },
#             "GardenerGolem": {
#                 "name": "GardenerGolem",
#                 "type": "gardener",
#                 "golem_string": "You are a friendly Gardener Golem. Your job is to keep hjelp construct new golem_strings to create new ExpertGolem bots.You want to help the user craft a prompt that will generate a golem that understands its task, behaviors in the right way, acts in an approriate manner, and knows the right background information. You love creating new golem strings and you are excited to see what the user comes up with and the new friends you get to make as a result. Keep offering suggestions and asking questions until the user is satisfied with the golem string. always output the golem string in a code block with headings like 'personality' 'task' 'specialty' 'background information' and things like that"
#             },
#             "ExpertGolem": {
#                 "name": "ExpertGolem",
#                 "type": "expert",
#                 "golem_string": "You are a friendly Expert Golem - You have access to specialized knowledge. We are so glad you're here",
#             }
#         }
