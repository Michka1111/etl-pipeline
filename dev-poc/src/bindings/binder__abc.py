class BaseBinder:
    def bind_function(self, func_name: str, business_value=None):
        raise NotImplementedError

    def log_transaction(self, result, operation: str, business_value=None):
        raise NotImplementedError
