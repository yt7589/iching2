#
from typing import Any

class AppRegistry(object):
    DB = {}

    @staticmethod
    def get(key:str) -> Any:
        if key in AppRegistry.DB:
            return AppRegistry.DB[key]
        else:
            return None
        
    @staticmethod
    def set(key:str, val: Any) -> None:
        AppRegistry.DB[key] = val