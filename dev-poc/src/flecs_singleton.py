from cffi import FFI
from singleton_registry_path import PathRegistry
from bindings.binder_cffi import CffiBinder
from meta_log.transaction_logger import TransactionLogger

class FlecsWorld(CffiBinder):
    def __init__(self):
        self.ffi = FFI()
        self.flecs_lib = self.ffi.dlopen("libflecs.so")
        self.transaction_logger = TransactionLogger()
        self.flecs_world = None
        super().__init__(self.ffi, self.flecs_lib, self.transaction_logger)

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self.flecs_lib is None:
            _dll_path = PathRegistry.get_path("flecs_dll_path")
            _abs_path = _dll_path.resolve()
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            self.flecs_lib = self.ffi.dlopen(str(_abs_path)) # "path/to/flecs.so")
        return self.flecs_lib # type: ignore

    # def is_binded_type(self, p_obj, p_type_name: str) -> bool:

    def binded_ecs_init(self):
        self.binded_load_flecs()
        self.flecs_world = self.flecs_lib.ecs_init() # type: ignore
        self.log_transaction(self.flecs_world, "ecs_init", business_value="default business value")

    def binded_shutdown(self):
        self.log_transaction(self.flecs_world, "ecs_fini", business_value="default business value")
        self.flecs_lib.ecs_fini(self.flecs_world) # type: ignore
        self.flecs_world = None
        FlecsWorld._instance = None

    def binded_ecs_new(self, name=None):
# SI ON ARRIVE JUSQU'ICI, C'EST QUE FLECS ESI INITIALISÉ
#        if self.flecs_world is None:
#            raise RuntimeError("World non initialisé")
        result = self.flecs_lib.ecs_new(self.flecs_world)
        self.log_transaction(result, "ecs_new", business_value=name)
        return result
