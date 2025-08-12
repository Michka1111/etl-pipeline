from .binder__abc import BaseBinder

class CffiBinder(BaseBinder):
    def __init__(self, p_ffi, p_flecs_lib, p_meta_logger):
        self.ffi = p_ffi
        self.flecs_lib = p_flecs_lib
        self._meta_logger = p_meta_logger

    def bind_function(self, func_name: str, business_value="default business value"):
        flecs_func = getattr(self.flecs_lib, func_name)

        def generated_binding_method(*args, **kwargs):
            result = flecs_func(*args, **kwargs)
            self._meta_logger.meta_log(result, func_name, business_value)
            return result

        method_name = f"binded_{func_name}"
        setattr(self, method_name, generated_binding_method)
        pass
