from ctypes import (
    Structure
    , c_double
)
#import pytest

from bindings.ctypes.component import ecs_add_component, register_dataclass_component
from bindings.ctypes.flecs import *

class Position(Structure):
    _fields_ = [
        (  "x", c_double)
        , ("y", c_double)
    ]

def test_component_POSITION():
    _singleton = FlecsBinding()
    _singleton.binded_ecs_init()
    # Test Register Component Position
    _component_id = register_dataclass_component(
        Position # type: ignore
    )
    assert isinstance(_component_id, int)
    assert _component_id != 0
    # Add Component to an existing Entity
    _e = _singleton.binded_ecs_new()
    ecs_add_component(_e, _component_id)
    # Vérifie que l'entité a un composant de cet id, y compris hérité
    _has = _singleton.binded_ecs_has_id(_e, _component_id)
    assert _has
    # Vérifie que l'entité possède le composant de cet id, hors héritage
    _owns = _singleton.binded_ecs_owns_id(_e, _component_id)
    assert _owns
    # Fin du monde
    _singleton.binded_ecs_fini()
    return


#
# Application : Structure C pour un composant HTML
#
# Définition d'une classe C pour représenter un composant HTML
#class CHTMLComponent(Structure):
#    _fields_ = [("html", c_char * 256)]  # taille fixe pour l’exemple

# Définition de l'enregistrement du composant HTML
#def register_html_component(world):
#    return ecs_register_component_struct(world, "HTMLComponent", CHTMLComponent)

# Entitisation du composant HTML 
# à une entité métier fournie, 
# avec des données HTML fournies (non-contrôlées)
#def set_html_component(world, entity, component_id, html_str: str):
#    html = CHTMLComponent()
#    html.html = html_str.encode("utf-8")[:255]
#    ecs_add_component(world, entity, component_id)
#    ecs_set_component_data(world, entity, component_id, html)

