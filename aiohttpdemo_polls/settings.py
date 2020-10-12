import pathlib
import yaml
import os

BASE_DIR = pathlib.Path(__file__).parent
# print(BASE_DIR)
config_path = os.path.join(BASE_DIR, 'config/polls.yaml')

def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config(config_path)
