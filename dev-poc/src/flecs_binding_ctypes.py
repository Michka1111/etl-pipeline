from ctypes import CDLL, c_void_p, c_uint64, c_size_t, c_char_p, POINTER, create_string_buffer
from pathlib import Path
from singleton_registry_path import PathRegistry

# Chargement de la DLL
_flecs = None

def load_flecs():
    global _flecs
    if _flecs is not None:
        return _flecs
    _flecs_lib_path = PathRegistry.get_path("flecs_dll_path")
    _flecs_lib_name = PathRegistry.get_path("flecs_dll_name")
    dll_path = _flecs_lib_path / _flecs_lib_name
    if not dll_path.exists():
        raise FileNotFoundError(f"Flecs DLL not found at {dll_path}")
    _flecs = CDLL(str(dll_path))
    return _flecs

# Types de base
ecs_world_t = c_void_p
ecs_entity_t = c_uint64

# Initialisation du monde
def ecs_init() -> ecs_world_t:
    lib = load_flecs()
    lib.ecs_init.restype = ecs_world_t
    return lib.ecs_init()

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

# Ajout d’un composant (simplifié)
def ecs_set(world: ecs_world_t, entity: ecs_entity_t, component_id: int, value: str):
    lib = load_flecs()
    buf = create_string_buffer(value.encode("utf-8"))
    lib.ecs_set.argtypes = [ecs_world_t, ecs_entity_t, c_uint64, c_size_t, c_void_p]
    lib.ecs_set(world, entity, component_id, len(value), buf)

# Exemple de composant Python → C
class HTMLComponent:
    def __init__(self, html: str):
        self.html = html

    def to_c(self):
        return self.html  # pour l’instant, juste une string

# Utilisation
if __name__ == "__main__":
    world = ecs_init()
    entity = ecs_new(world)
    html = HTMLComponent("<html>Test</html>")
    ecs_set(world, entity, 1, html.to_c())  # 1 = ID fictif du composant
    ecs_fini(world)
