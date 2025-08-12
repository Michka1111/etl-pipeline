from cffi import FFI
from singleton_registry_path import PathRegistry
from bindings.binder_cffi import CffiBinder
from meta_log.meta_logger import MetaLogger

class FlecsWorld(CffiBinder):
    def __init__(self):
        # TODO : refactorer cette init dans CffiBinder
        self.ffi = FFI()
        self.ffi.cdef("""
            typedef struct ecs_world_t ecs_world_t;
            typedef uint64_t ecs_id_t;
            typedef ecs_id_t ecs_entity_t;
            ecs_world_t* ecs_init(void);
            ecs_entity_t ecs_new(ecs_world_t *world);
            void ecs_fini(ecs_world_t *world);
        """)

        self.flecs_lib = None
        self.flecs_world = None
        self._meta_logger = MetaLogger(self.ffi)
        super().__init__(self.ffi, self.flecs_lib, self._meta_logger)

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self.flecs_lib is None:
            _dll_path = PathRegistry.get_path("flecs_dll_path")
            _abs_path = _dll_path.resolve()
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            self.flecs_lib = self.ffi.dlopen(str(_abs_path)) # "path/to/flecs.so")
            self._meta_logger.meta_log(self.flecs_lib, "binded_load_flecs", business_value=f"Loaded {_dll_path}")
        return self.flecs_lib # type: ignore

    # def is_binded_type(self, p_obj, p_type_name: str) -> bool:

    def binded_ecs_init(self):
        self.binded_load_flecs()
        self.flecs_world = self.flecs_lib.ecs_init() # type: ignore
        self._meta_logger.meta_log(self.flecs_world, "ecs_init", business_value="default business value")

    def binded_shutdown(self):
        self._meta_logger.meta_log(self.flecs_world, "ecs_fini", business_value="default business value")
        self.flecs_lib.ecs_fini(self.flecs_world) # type: ignore
        self.flecs_world = None
        FlecsWorld._instance = None

    def binded_ecs_new(self, name=None):
# SI ON ARRIVE JUSQU'ICI, C'EST QUE FLECS ESI INITIALISÉ ==> PAS DE TEST-BOULET
#        if self.flecs_world is None:
#            raise RuntimeError("World non initialisé")
        _result = self.flecs_lib.ecs_new(self.flecs_world) # type: ignore
        self._meta_logger.meta_log(
            _result # pour "type_c", devrait meta_logger "ecs_entity_t" ?
            , "ecs_new"
            , business_value=_result
        ) # business_value=result if name is None else name)
        return _result
