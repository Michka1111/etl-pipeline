from pathlib import Path
from typing import Any

from cffi import FFI
from .binder__abc import BaseBinder
from meta_log.meta_logger import MetaLogger

class CffiBinder(BaseBinder):
    def __init__(self, p_meta_logger: MetaLogger):
        self._ffi = FFI()
        self._ffi.cdef("""
            typedef struct ecs_world_t ecs_world_t;
            typedef uint64_t ecs_id_t;
            typedef ecs_id_t ecs_entity_t;
            ecs_world_t* ecs_init(void);
            ecs_entity_t ecs_new(ecs_world_t *world);
            void ecs_fini(ecs_world_t *world);
        """)
        self._meta_logger = p_meta_logger
        # _LIB INITIALISATION IS ONLY ON-DEMAND
        

    def bind_tool_tuple(self, p_dll_path: Path) -> tuple[Any, Any]:
        self._abs_dll_path = p_dll_path.resolve() # CFFI use only absolute path
        self._lib = self._ffi.dlopen(str(self._abs_dll_path)) # "path/to/flecs.so")
        return self._ffi, self._lib

    def bind_function(self, func_name: str, business_value="default business value"):
        _func = getattr(self._lib, func_name)

        def generated_binding_method(*args, **kwargs):
            result = _func(*args, **kwargs)
            self._meta_logger.meta_log(result, func_name, business_value)
            return result

        method_name = f"binded_{func_name}"
        setattr(self, method_name, generated_binding_method)
        pass

    def get_metalog_type_c_value(self, p_result):
        """Calcule la valeur de la dimension "type_c" de la méta-log selon la bind-techno.
        CFFI:   le type en langage C du retour d'appel de fonction de la DLL liée.
        CTYPES: TODO"""
        return self._ffi.typeof(p_result).cname if isinstance(p_result, self._ffi.CData) else "n/a"
            # entry["type_c"] = type(result).__name__ if hasattr(result, '__class__') else "n/a"

