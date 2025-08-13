import time
from typing import Any

from meta_log.config_flags import MetaConfigFlags
from bindings.binder__abc import BaseBinder

class MetaLogger:
    def __init__(self):
        self._meta_log = []
        self._user_view = []
        self._binder = self.set_binder_instance(None)
        self._config_flags = MetaConfigFlags()
        # { "timestamp": True, "type_c": True, "business": True, "operation": True, }

    def set_binder_instance(self, p_binder):
        # _binder doit être initialisé avant de méta-loguer "type_c"
        self._binder = p_binder if p_binder is not None else None # ici, pas de ':' ;-)

    def meta_log(self, p_result, p_operation, p_business_value=None):
        entry = {}
        if self._config_flags.is_enabled("timestamp"):
            entry["timestamp"] = time.time() # lequel est déprécié ? /?\
        if self._config_flags.is_enabled("type_c"):
            # Ce champ dépend du binder
            if self._binder:
                entry["type_c"] = self._binder.get_metalog_type_c_value(p_result) # type: ignore
            else:
                entry["type_c"] = "Meta-Log: Binder Not Set ?!"
        if self._config_flags.is_enabled("business"):
            entry["business"] = p_business_value or "n/a"
        if self._config_flags.is_enabled("operation"):
            entry["operation"] = p_operation
        entry["value"] = p_result
        self._meta_log.append(entry)

    def filter_view(self, **criteria):
        self._user_view = [
            entry for entry in self._meta_log
            if all(entry.get(k) == v for k, v in criteria.items())
        ]
        return self._user_view
