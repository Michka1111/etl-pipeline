from pathlib import Path
from typing import Any

from cffi import FFI

from .binder__abc import BaseBinder

class CffiBinder(BaseBinder):
    def __init__(self):
        self._ffi = FFI()       # CFFI CDEF ICI
        self._ffi.cdef("""
            typedef struct ecs_world_t ecs_world_t;
            typedef uint64_t ecs_id_t;
            typedef ecs_id_t ecs_entity_t;
            ecs_world_t * ecs_init(void);
            ecs_entity_t ecs_new(ecs_world_t * world);
            ecs_entity_t ecs_set_name (ecs_world_t * world, ecs_entity_t entity, const char * name);
            void ecs_fini(ecs_world_t *world);
        """)
        self._lib = None
        # Import local pour éviter le'import circulaire
        from flecs_singleton import FlecsWorld as iFW
        _ifw = iFW()
        _ifw.register(name="bind_cmd", system=self._ffi) # Bind techno agnostic
        self._meta_logger = _ifw.get(name="meta_logger")
        self._meta_logger.meta_log(p_result=self, p_operation="__init__", p_business_value="CffiBinder Initialized")
        # _LIB INITIALISATION IS ONLY ON-DEMAND
        

    def bind_tool_tuple(self) -> tuple[Any, Any]:
        # Import local pour éviter le'import circulaire
        from flecs_singleton import FlecsWorld as iFW
        _ifw = iFW()
        _dll_path = _ifw.get(name="dll_path")
        # Si None, il y a lieu de planter !
        assert _dll_path is not None and _dll_path.exists(), "DLL path must be set and exist"
        self._abs_dll_path = _dll_path.resolve() # CFFI use only absolute path
        self._lib = self._ffi.dlopen(str(self._abs_dll_path)) # "path/to/flecs.so")
        assert self._lib is not None, "CFFI: flecs library could not be loaded"
        _ifw.register(name="flecs_lib", system=self._lib)
        self._meta_logger.meta_log(
            p_result=self._lib
            , p_operation="bind_tool_tuple"
            , p_business_value=f"Loaded CFFI library from {_dll_path}"
        )
        return self._ffi, self._lib

    def add_binding_method_to_binder(
            self
            , lib_func_name: str
            , business_value="default business value"
            , p_cdata_type=None
        ):
        _dll_function = getattr(self._lib, lib_func_name)

        def generated_binding_method(*args, **kwargs):
            result = _dll_function(*args, **kwargs)
            if p_cdata_type is not None:
                result = self._ffi.cast(p_cdata_type, result)
            self._meta_logger.meta_log(
                p_result=result
                , p_operation=lib_func_name
                , p_business_value=business_value
            )
            return result

        method_name = f"binded_{lib_func_name}"
        setattr(self, method_name, generated_binding_method)
        pass

    def get_metalog_type_c_value(self, p_result) -> Any:
        """Calcule la valeur de la dimension "type_c" de la méta-log selon la bind-techno.
        CFFI:   le type en langage C du retour d'appel de fonction de la DLL liée.
        CTYPES: TODO"""
        if isinstance(p_result, self._ffi.CData):
            # p_result est bien un type cffi CData
            _r = self._ffi.typeof(p_result).cname
        else:
            # si p_result est un type Python: 
            _r = type(p_result).__name__ if hasattr(p_result, '__class__') else "n/a"
            # _r = "n/a"
        return _r

