from ctypes import (
    Structure
    , c_double
)

from bindings.ctypes.component import register_dataclass_component
from bindings.ctypes.flecs import *

class Position(Structure):
    _fields_ = [
        (  "x", c_double)
        , ("y", c_double)
    ]

def test_register_position_component():
    _world = binded_ecs_init()
    _component_id = register_dataclass_component(
        p_world_ptr =_world
        , p_struct_cls = Position
        , p_flecs_lib = binded_load_flecs()
    )

    assert isinstance(_component_id, int)
    assert _component_id != 0


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

