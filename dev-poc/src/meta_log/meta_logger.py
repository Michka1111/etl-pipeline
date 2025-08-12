import time
from typing import Any

from meta_log.config_flags import MetaConfigFlags

class MetaLogger:
    def __init__(self, p_ffi: Any =None):
        self._meta_log = []
        self._user_view = []
        self._ffi = p_ffi 
        self._config_flags = MetaConfigFlags()
        # { "timestamp": True, "type_c": True, "business": True, "operation": True, }

    def meta_log(self, result, operation, business_value=None):
        entry = {}
        if self._config_flags.is_enabled("timestamp"):
            entry["timestamp"] = time.time() # lequel est déprécié ? /?\
        if self._config_flags.is_enabled("type_c"):
            entry["type_c"] = self._ffi.typeof(result).cname if isinstance(result, self._ffi.CData) else "n/a"
            # entry["type_c"] = type(result).__name__ if hasattr(result, '__class__') else "n/a"
        if self._config_flags.is_enabled("business"):
            entry["business"] = business_value or "n/a"
        if self._config_flags.is_enabled("operation"):
            entry["operation"] = operation
        entry["value"] = result
        self._meta_log.append(entry)

    def filter_view(self, **criteria):
        self._user_view = [
            entry for entry in self._meta_log
            if all(entry.get(k) == v for k, v in criteria.items())
        ]
        return self._user_view
