import time


class TransactionLogger:
    def __init__(self, config_flags=None):
        self._meta_log = []
        self._user_view = []
        self._config_flags = config_flags or {
            "timestamp": True,
            "type_c": True,
            "business": True,
            "operation": True,
        }

    def log_transaction(self, result, operation, business_value=None):
        entry = {}
        if self._config_flags["timestamp"]:
            entry["timestamp"] = time.time() # lequel est déprécié ? /?\
        if self._config_flags["type_c"]:
            entry["type_c"] = type(result).__name__ if hasattr(result, '__class__') else "n/a"
        if self._config_flags["business"]:
            entry["business"] = business_value or "n/a"
        if self._config_flags["operation"]:
            entry["operation"] = operation
        entry["value"] = result
        self._meta_log.append(entry)

    def filter_view(self, **criteria):
        self._user_view = [
            entry for entry in self._meta_log
            if all(entry.get(k) == v for k, v in criteria.items())
        ]
        return self._user_view
