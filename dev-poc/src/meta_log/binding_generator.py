# binding_generator.py
def add_binding(singleton, func_name: str, business_value="default business value"):
    flecs_c_api = getattr(singleton.flecs_lib, func_name)

    def generated_binded_method(*args, **kwargs):
        result = flecs_c_api(*args, **kwargs)
        singleton._meta_logger.meta_log(
            result,
            operation=func_name,
            business_value=business_value
        )
        return result

    method_name = f"binded_{func_name}"
    setattr(singleton, method_name, generated_binded_method)
    pass
