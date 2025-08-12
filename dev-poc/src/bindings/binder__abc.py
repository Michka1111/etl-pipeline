from typing import Any


class BaseBinder:
    def bind_function(self, func_name: str, business_value: Any = None):
        raise NotImplementedError

    # def meta_log(self, result, operation: str, business_value=None):
    #     raise NotImplementedError
