from ctypes import (
    CDLL, Structure
    , c_bool, c_int32, c_void_p, c_uint64, c_size_t, c_char_p
    , byref, POINTER, memmove, sizeof
)
import os

from singleton_registry_path import PathRegistry

# Types de base (correspondance directe avec ctypes.c_*)
ecs_world_t         = c_void_p      # typedef struct ecs_world_t ecs_world_t ; (flecs.h)
ecs_id_t            = c_uint64
ecs_size_t          = c_size_t
bool_t              = c_bool
true_t              = c_bool(True)
int32_t             = c_int32
const_char_p        = c_char_p
# Types dérivés
ecs_entity_t        = ecs_id_t  # Flecs C-API
# Types généricisés
ecs_type_hooks_t    = c_void_p  # typedef struct ecs_type_hooks_t ecs_type_hooks_t
const_ecs_id_t_p    = c_void_p  # const ecs_id_t *
const_ecs_value_t_p = c_void_p  # const ecs_value_t 

# Mécanisme Singleton pour decorator
def singleton(p_cls):
    _instances = {}
    def get_instance(*args, **kwargs):
        if p_cls not in _instances: # une seule instance
            _instances[p_cls] = p_cls(*args, **kwargs)
        return _instances[p_cls]
    return get_instance

#
#
@singleton
class FlecsBinding:
    def __init__(self):
        self._flecs_lib = None
        self._Flecs_world = None
#        _curdir = os.getcwd()
#        print(_curdir)

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self._flecs_lib is None:
            _dll_path = PathRegistry.get_path("flecs_dll_path")
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            self._flecs_lib = CDLL(str(_dll_path))
        return self._flecs_lib

    # Initialisation du monde
    def binded_ecs_init(self) -> None:
        lib = self.binded_load_flecs()
        lib.ecs_init.restype = ecs_world_t
        self._Flecs_world = lib.ecs_init()
        return

    # Fin du monde
    def binded_ecs_fini(self):
        lib = self.binded_load_flecs()
        lib.ecs_fini.argtypes = [ecs_world_t]
        lib.ecs_fini(self._Flecs_world)
        self._Flecs_world = None
        return

    # Création d’une entité
    def binded_ecs_new(self) -> ecs_entity_t:
        lib = self.binded_load_flecs()
        lib.ecs_new.restype = ecs_entity_t
        lib.ecs_new.argtypes = [ecs_world_t]
        return lib.ecs_new(self._Flecs_world)

