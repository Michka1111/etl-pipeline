from cffi import FFI

from singleton_registry_path import PathRegistry

class FlecsBindings:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlecsBindings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.ffi = FFI()
            self.ffi.cdef("""
                typedef struct ecs_world_t ecs_world_t;
                ecs_world_t* ecs_init(void);
                void ecs_fini(ecs_world_t *world);
            """)
            self.flecs_lib = None
            self.flecs_world = None
            self.__class__._initialized = True

    def is_binded_type(self, p_obj, p_type_name: str) -> bool:
        try:
            return (
                isinstance(p_obj, self.ffi.CData)
                and self.ffi.typeof(p_obj).cname == p_type_name
            )
        except Exception:
            return False

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self.flecs_lib is None:
            _dll_path = PathRegistry.get_path("flecs_dll_path")
            _abs_path = _dll_path.resolve()
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            self.flecs_lib = self.ffi.dlopen(str(_abs_path)) # "path/to/flecs.so")
        return self.flecs_lib # type: ignore

    def binded_ecs_init(self):
        self.binded_load_flecs()
        self.flecs_world = self.flecs_lib.ecs_init() # type: ignore

    def binded_shutdown(self):
        self.flecs_lib.ecs_fini(self.flecs_world) # type: ignore
        self.flecs_world = None
        FlecsBindings._instance = None
