from cffi import FFI

from bindings.binder_cffi import CffiBinder
from meta_log.meta_logger import MetaLogger
from singleton_registry_path import PathRegistry

    # REFACTOR SINGLETON SYSTÉMIQUE "GLOBAL PROVIDER"
    # évite les paramètres des "systèmes" dans les fonctions et méthodes.
    # comme "ffi", "méta-logger", "Flecs_world", etc.
    # Remplacé dans toutes les classes par la demande d'un racouci à 
    # une instance d'outil interne.
    # ex. 
    # Dans CffiBinder.__init__() :
    #     _my_tool_to_register = FFI()
    #     FlecsWorld().register(name="bind_cmd", system=_my_tool_to_register)
    # À un autre moment, dans une autre classe :  
    #    self._lib = FlecsWorld().get(name="flecs_lib")  
class FlecsWorld:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._systems = {} # type: ignore
        return cls._instance

    def register(self, name, system):
        self._systems[name] = system

    def get(self, name):
        return self._systems.get(name)

    def __getattr__(self, name):
        return self._systems.get(name)

    def __init__(self): 
        if self._is_initialized:
            # NE DEVRAIT PAS ARRIVER
            # See Also src.meta_log.MetaLogger
            return 
        self._is_initialized = True
        # REFACTOR SINGLETON SYSTÉMIQUE
        # remplacement des attributs des systèmes internes par 
        # l'enregistrement des systèmes correspondants pour accès "public"
        # au sein du singleton FlecsWorld.  
        # REFACTOR Initialisation du Binder sauce techno-agnostic
        # par défaut, CFFI. Pour changer, changer la classe ici et l'import ci-dessus.
        # See also: classe bindings.binder__abc.BaseBinder.
        self.register(name="binder_cls", system=CffiBinder) # Prêt-à-initialiser
        self.register(name="flecs_lib", system=None)
        self.register(name="flecs_world", system=None)
        self.register(name="meta_logger", system=MetaLogger()) # init sans Binder qui devra être initialisé plus tard.
        # plus de return dans __init__ # return None
        pass
        # _ml = self.get(name="meta_logger")
        # _ml.initialize()
        pass

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        _sys_key_flecs_lib = "flecs_lib"
        _sys_key_dll_path = "dll_path"
        _sys_key_binder_cls = "binder_cls"
        _sys_key_binder = "binder"
        _sys_key_bind_cmd = "bind_cmd"
        _sys_key_meta_logger = "meta_logger"
        if self.get(name=_sys_key_flecs_lib) is None:
            self.register(name=_sys_key_dll_path, system=PathRegistry.get_path("flecs_dll_path"))
            _dll_path = self.get(name=_sys_key_dll_path)
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            _binder_cls = self.get(name=_sys_key_binder_cls)
            assert _binder_cls is not None
            _binder = _binder_cls()
            assert _binder is not None
            self.register(name=_sys_key_binder, system=_binder) # type: ignore # self._meta_logger) plus besoin avec register/get
            # SELF.FLECS_LIB = self._binder._lib
            # self.bind_cmd, self.flecs_lib = self._binder.bind_tool_tuple(self._dll_path)
            _bind_cmd, _flecs_lib = _binder.bind_tool_tuple() # self._dll_path) plus besoin avec register/get
            assert _flecs_lib is not None, "Flecs_lib is None"
            assert _bind_cmd is not None, "Bind_cmd (ffi) is None"
            # _bind_cmd est None avec CTYPES, mais pas avec CFFI
            # self.register(name=_sys_key_bind_cmd, system=_bind_cmd)
            self.register(name=_sys_key_flecs_lib, system=_flecs_lib)
            #
            # MetaLogger est "None-proof" pour Binder.
            # Au cas où
            _meta_logger = self.get(name=_sys_key_meta_logger)
            _meta_logger.initialize()
            _meta_logger.meta_log(
                p_result=_flecs_lib
                , p_operation="binded_load_flecs"
                , p_business_value=f"Loaded {_dll_path}"
            )
        return None

    # def is_binded_type(self, p_obj, p_type_name: str) -> bool:

    def binded_ecs_init(self) -> None:
        self.binded_load_flecs()
        _flecs_w = self.get(name="flecs_lib").ecs_init() # type: ignore
        self.register(name="flecs_world", system=_flecs_w)
        self.get(name="meta_logger").meta_log(
            p_result=self.get(name="flecs_world")
            , p_operation="ecs_init"
            , p_business_value="default business value")
        return None

    def binded_shutdown(self) -> None:
        self.get(name="meta_logger").meta_log(
            p_result=self.get(name="flecs_world")
            , p_operation="ecs_fini"
            , p_business_value="default business value"
        )
        self.get(name="flecs_lib").ecs_fini(self.get(name="flecs_world")) # type: ignore
        self.register(name="flecs_world", system=None)
        self.register(name="flecs_lib", system=None)
        FlecsWorld._instance = None
        return None

    def binded_ecs_new(self, name=None):
# SI ON ARRIVE JUSQU'ICI, C'EST QUE FLECS ESI INITIALISÉ ==> PAS DE TEST-BOULET
#        if self.flecs_world is None:
#            raise RuntimeError("World non initialisé")
        _result = self.get(name="flecs_lib").ecs_new(self.get(name="flecs_world")) # type: ignore
        self.get(name="meta_logger").meta_log(
            p_result=_result # pour "type_c", devrait meta_logger "ecs_entity_t" ?
            , p_operation="ecs_new"
            , p_business_value=_result
        ) # business_value=result if name is None else name)
        return _result
