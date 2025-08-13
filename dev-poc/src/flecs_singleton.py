from cffi import FFI

from bindings.binder_cffi import CffiBinder
from meta_log.meta_logger import MetaLogger
from singleton_registry_path import PathRegistry

class FlecsWorld: # (CffiBinder):
    def __init__(self): 
        # REFACTOR Initialisation du Binder sauce techno-agnostic
        # par défaut, CFFI. Pour changer, changer la classe ici et l'import ci-dessus.
        # See also: classe bindings.binder__abc.BaseBinder.
        self._binder_cls = CffiBinder # Prêt-à-initialiser
        self.flecs_lib = None
        self.flecs_world = None
        self._meta_logger = MetaLogger() # init sans Binder qui devra être initialisé plus tard.
        # super().__init__(self.ffi, self.flecs_lib, self._meta_logger) ?!

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self.flecs_lib is None:
            self._dll_path = PathRegistry.get_path("flecs_dll_path")
            if not self._dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {self._dll_path}")
            self._binder = self._binder_cls(self._meta_logger)
            self.bind_cmd, self.flecs_lib = self._binder.bind_tool_tuple(self._dll_path)
            self._meta_logger.set_binder_instance(self._binder) # MetaLogger est "None-proof" pour Binder.
            self._meta_logger.meta_log(
                self.flecs_lib
                , "binded_load_flecs", p_business_value=f"Loaded {self._dll_path}"
            )
        return self.flecs_lib # type: ignore

    # def is_binded_type(self, p_obj, p_type_name: str) -> bool:

    def binded_ecs_init(self):
        self.binded_load_flecs()
        self.flecs_world = self.flecs_lib.ecs_init() # type: ignore
        self._meta_logger.meta_log(self.flecs_world, "ecs_init", p_business_value="default business value")

    def binded_shutdown(self):
        self._meta_logger.meta_log(self.flecs_world, "ecs_fini", p_business_value="default business value")
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
            , p_business_value=_result
        ) # business_value=result if name is None else name)
        return _result
