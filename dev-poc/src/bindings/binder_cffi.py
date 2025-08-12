from .binder__abc import BaseBinder

class CffiBinder(BaseBinder):
    def __init__(self, ffi, flecs_lib, transaction_logger):
        self.ffi = ffi
        self.flecs_lib = flecs_lib
        self.transaction_logger = transaction_logger

    def bind_function(self, func_name: str, business_value=None):
        flecs_func = getattr(self.flecs_lib, func_name)

        def generated_method(*args, **kwargs):
            result = flecs_func(*args, **kwargs)
            self.transaction_logger.log_transaction(result, func_name, business_value)
            return result

        method_name = f"binded_{func_name}"
        setattr(self, method_name, generated_method)
