from ctypes import (
    CDLL, Structure
    , c_bool, c_char, c_int32, c_void_p, c_uint64, c_size_t, c_char_p
    , byref, POINTER, create_string_buffer, memmove, sizeof
)
import time
from singleton_registry_path import PathRegistry

# Types de base (correspondance directe avec ctypes.c_*)
ecs_world_t         = c_void_p
ecs_id_t            = c_uint64
ecs_size_t          = c_size_t
bool_t              = c_bool
true_t              = c_bool(True)
int32_t             = c_int32
const_char_p        = c_char_p
# Types dérivés
ecs_entity_t        = ecs_id_t  # typedef uint64_t ecs_entity_t;
# Types généricisés
ecs_type_hooks_t    = c_void_p  # typedef struct ecs_type_hooks_t ecs_type_hooks_t
const_ecs_id_t_p    = c_void_p  # const ecs_id_t *
const_ecs_value_t_p = c_void_p  # const ecs_value_t 

#
# Chargement de la DLL
#
_flecs = None

def load_flecs():
    global _flecs
    if _flecs is not None:
        return _flecs
    _flecs_lib_path = PathRegistry.get_path("flecs_dll_path")
    _flecs_lib_name = PathRegistry.get_path("flecs_dll_name")
    _dll_path = _flecs_lib_path / _flecs_lib_name
    if not _dll_path.exists():
        raise FileNotFoundError(f"Flecs DLL not found at {_dll_path}")
    _flecs = CDLL(str(_dll_path))
    return _flecs

# Initialisation du monde
def ecs_init() -> ecs_world_t:
    lib = load_flecs()
    lib.ecs_init.restype = ecs_world_t
    return lib.ecs_init()

# Fin du monde
def ecs_fini(world: ecs_world_t):
    lib = load_flecs()
    lib.ecs_fini.argtypes = [ecs_world_t]
    lib.ecs_fini(world)

# Création d’une entité
def ecs_new(world: ecs_world_t) -> ecs_entity_t:
    lib = load_flecs()
    lib.ecs_new.restype = ecs_entity_t
    lib.ecs_new.argtypes = [ecs_world_t]
    return lib.ecs_new(world)


# Ajout d’un composant à une entité
def ecs_add_component(world, entity, component_id):
    lib = load_flecs()
    lib.ecs_add_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_entity_t]
    lib.ecs_add_id(world, entity, component_id)

# Écriture des données d’un composant
def ecs_set_component_data(world, entity, component_id, data: Structure):
    lib = load_flecs()
    lib.ecs_get_mut_id.restype = c_void_p
    lib.ecs_get_mut_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_entity_t, POINTER(c_bool)]
    is_added = c_bool()
    ptr = lib.ecs_get_mut_id(world, entity, component_id, byref(is_added))
    memmove(ptr, byref(data), sizeof(data))

# Récupération du composant
def get_component_data(world, entity: c_uint64, component_id: c_uint64, struct_cls: type):
    lib = world.lib
    lib.ecs_get_id.restype = c_void_p
    lib.ecs_get_id.argtypes = [c_void_p, c_uint64, c_uint64]
    ptr = lib.ecs_get_id(world.world, entity, component_id)
    if not ptr:
        return None
    data = struct_cls()
    memmove(byref(data), ptr, sizeof(data))
    return data

#
# Application : Structure C pour un composant HTML
#
# Définition d'une classe C pour représenter un composant HTML
class CHTMLComponent(Structure):
    _fields_ = [("html", c_char * 256)]  # taille fixe pour l’exemple

# Définition de l'enregistrement du composant HTML
def register_html_component(world):
    return ecs_register_component_struct(world, "HTMLComponent", CHTMLComponent)

# Entitisation du composant HTML 
# à une entité métier fournie, 
# avec des données HTML fournies (non-contrôlées)
def set_html_component(world, entity, component_id, html_str: str):
    html = CHTMLComponent()
    html.html = html_str.encode("utf-8")[:255]
    ecs_add_component(world, entity, component_id)
    ecs_set_component_data(world, entity, component_id, html)

