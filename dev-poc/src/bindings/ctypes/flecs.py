from collections.abc import Callable
from ctypes import (
    CDLL
    , c_bool, c_int32, c_void_p, c_uint64, c_size_t, c_char_p
#    , byref, POINTER, memmove, sizeof
)
#import os # "not accessed" depuis le commentaire de get_cwd()
from typing import Any

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
def singleton(p_cls) -> Any:
    _instances = {}
    def get_instance(*args, **kwargs):
        if p_cls not in _instances: # une seule instance
            _instances[p_cls] = p_cls(*args, **kwargs)
        return _instances[p_cls]
    return get_instance
#
@singleton
class FlecsBinding:
    def __init__(self):
        self.flecs_lib = None
        self.flecs_world = None
#        _curdir = os.getcwd()
#        print(_curdir)

    # Chargement de la DLL
    def binded_load_flecs(self) -> None:
        if self.flecs_lib is None:
            _dll_path = PathRegistry.get_path("flecs_dll_path")
            if not _dll_path.exists():
                raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
            self.flecs_lib = CDLL(str(_dll_path))
        return self.flecs_lib # type: ignore

    # Initialisation du monde
    def binded_ecs_init(self) -> None:
        _lib = self.binded_load_flecs()
        if self.flecs_world is None:
            _lib.ecs_init.restype = ecs_world_t # type: ignore
            self.flecs_world = _lib.ecs_init() # type: ignore
        return

    # Fin du monde
    def binded_ecs_fini(self):
        _lib = self.binded_load_flecs()
        _lib.ecs_fini.argtypes = [ecs_world_t] # type: ignore
        _lib.ecs_fini(self.flecs_world) # type: ignore
        self.flecs_world = None
        return

    # Création d’une entité
    def binded_ecs_new(self) -> ecs_entity_t:
        _lib = self.binded_load_flecs()
        _lib.ecs_new.restype = ecs_entity_t # type: ignore
        _lib.ecs_new.argtypes = [ecs_world_t] # type: ignore
        return _lib.ecs_new(self.flecs_world) # type: ignore
    
    # Test si une entité a un composant
    def binded_ecs_has_id(
            self
            , _e: ecs_entity_t
            , _c: ecs_id_t
        ):
        _lib = self.binded_load_flecs()
        _lib.ecs_has_id.restype = c_bool # type: ignore
        _lib.ecs_has_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_id_t] # type: ignore
        _r = _lib.ecs_has_id(self.flecs_world, _e, _c) # type: ignore
        return _r
    
    # Test si une entité a un composant
    def binded_ecs_owns_id(
            self
            , _e: ecs_entity_t
            , _c: ecs_id_t
        ):
        _lib = self.binded_load_flecs()
        _lib.ecs_owns_id.restype = c_bool # type: ignore
        _lib.ecs_owns_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_id_t] # type: ignore
        _r = _lib.ecs_owns_id(self.flecs_world, _e, _c) # type: ignore
        return _r

    # CREATE OR GET AN ENTITY WITH NAME
    # https://www.flecs.dev/flecs/group__paths.html
    # ecs_entity_t 	ecs_set_name (ecs_world_t *world, ecs_entity_t entity, const char *name)
    #     _bob = _bdr_ecs.binded_ecs_set_name(0, "Bob")
    def binded_ecs_set_name(
            self
            , p_e: ecs_entity_t
            , p_name: str # _name.encode("utf-8")
    ):
        _lib = self.binded_load_flecs()
        _lib.ecs_set_name.restype = ecs_entity_t # type: ignore
        _lib.ecs_set_name.argtypes = [ecs_world_t, ecs_entity_t, const_char_p] # type: ignore
        _r = _lib.ecs_set_name(self.flecs_world, p_e, p_name.encode("utf-8")) #.encode("utf-8"))   # type: ignore
        return _r
