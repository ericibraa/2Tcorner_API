from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Configs(BaseSettings):
    app_name:str= "2Tcornet API"
    app_version:str= "0.0.1"
    mongo_host: str
    mongo_db : str
    do_spaces_key: str
    do_spaces_secret: str
    do_spaces_region: str
    do_spaces_bucket: str
    model_config = SettingsConfigDict(env_file=".env")
    jwt_secrete_key : str
    jwt_algorithm:str

@lru_cache
def get_configs():
    return Configs()