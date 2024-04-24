import json
import os
from pydantic import BaseModel

from src.api.controller import Controller


controller = Controller()

config_dir = os.path.join(os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), 'com.github.mwickham.gwarden')
config_file = os.path.join(config_dir, 'config.json')
class Configs(BaseModel):

    username: str = ""

    @classmethod
    def load(cls):
        try:
            with open(config_file) as file:
                contents = file.read()
                contents = json.loads(contents)
                return cls(**contents)
        except:
            value = cls()
            value.save()
            return value


    def save(self):

        with open(config_file, 'w') as file:
            file.write(json.dumps(self.dict()))

configs = Configs.load()
