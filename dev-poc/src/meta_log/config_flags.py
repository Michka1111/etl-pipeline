class MetaConfigFlags:
    def __init__(self, **flags):
        self.flags = {
            "timestamp": True,
            "type_c": True,
            "business": True,
            "operation": True,
            **flags
        }

    def is_enabled(self, key: str) -> bool:
        return self.flags.get(key, False)
