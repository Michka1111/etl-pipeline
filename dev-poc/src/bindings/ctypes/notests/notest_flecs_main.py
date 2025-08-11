from ctypes import Structure, c_double
from bindings.ctypes.flecs import *
from bindings.ctypes.component import *

class Position(Structure):
    _fields_ = [
        (  "x", c_double)
        , ("y", c_double)
    ]

# See https://github.com/SanderMertens/flecs/blob/master/examples/c/entities/basics/src/main.c
def test_ecs_example_BASICS_component():
    # Singleton DLL Binder on FLECS World
    _bdr_ecs = FlecsBinding()
    _bdr_ecs.binded_ecs_init()

    # ECS_COMPONENT(ecs, Position);
    _component_POSITION_id = register_dataclass_component(Position) # type: ignore
    
    _type_info = _bdr_ecs.binded_ecs_get_type_info(_component_POSITION_id)
    assert _type_info is not None, "Type info should not be None"
    assert _type_info.size == sizeof(Position), "Type size should match Position structure size"
    assert _type_info.alignment == sizeof(c_double), "Type alignment should match c_double size"
    
    # Create an entity with name Bob
    _bob = _bdr_ecs.binded_ecs_set_name(0, "Bob")
    # Test si _bob a le component enregistré (ne devrait pas)
    # _has = _bdr_ecs.binded_ecs_has_id(_bob, _component_POSITION_id)
    # assert not _has, f"Entity {_bob} should not have component {_component_POSITION_id}"
    # Ajout d'un component Position vide
    # _bdr_ecs.binded_ecs_add_id(_bob, _component_POSITION_id)
    # Test si _bob a le component enregistré (ne devrait pas)
    # _has = _bdr_ecs.binded_ecs_has_id(_bob, _component_POSITION_id)
    # assert _has, f"Entity {_bob} should have component {_component_POSITION_id}"

    _bob_position = Position()
    _bob_position.x = 10.0
    _bob_position.y = 20.0
    # // The set operation finds or creates a component, and sets it.
    # ecs_set(ecs, bob, Position, {10, 20}); 
    # # flecs.h : #define ecs_set(...) ecs_set_id(...)
    # void 	ecs_set_id (ecs_world_t *world, ecs_entity_t entity, ecs_id_t component, size_t size, const void *ptr)
    #_bdr_ecs.binded_ecs_set_id(_bob, Position, _bob_position)
    
    # _bdr_ecs.binded_ecs_set_id(_bob, _component_POSITION_id, _bob_position)
    _lib = _bdr_ecs.flecs_lib
    _lib.ecs_set_id.restype = None      # type: ignore
    _lib.ecs_set_id.argtypes = [        # type: ignore
        c_void_p    # ecs_world_t
        , c_uint64  # ecs_entity_t
        , c_uint64  # ecs_id_t
        , c_size_t
        , c_void_p  # _ptr_values_instance 
    ]               # c_void_p ou POINTER(Position) si connu (GitHub Copilot)
    _sz_c_values = sizeof(_bob_position)
    _ptr_data = cast(pointer(_bob_position), c_void_p) # c_void_p(addressof(p_c_value)) # cast(pointer(p_c_value), c_void_p)
    _lib.ecs_set_id( # type: ignore
        _bdr_ecs.flecs_world
        , _bob
        , _component_POSITION_id
        , _sz_c_values # sizeof(p_c_value)
        , _ptr_data # byref(p_c_value) # p_c_value 
    )
    pass

#PAS ENCORE POUR TOUT DE SUITE
#if __name__ == "__main__":
    # AVEC SINGLETON, PLUS BESOIN DE SE TRIMBALER
    # Monde

    # Composant HTML
    # 1 REGISTER
    #html_component_id = register_html_component(world)
    # 2 SET
    # Entité métier à composant HTML avec contenu HTML
    #set_html_component(world, entity, html_component_id, "<html>Test</html>")

    # Attente
    #time.sleep(5)

    # 3. RETRIEVE
    # Récupération du composant
    #retrieved = get_component_data(world, entity, html_component_id, CHTMLComponent)
    #if retrieved:
    #    html_str = bytes(retrieved.html).decode("utf-8").rstrip("\x00")
    #    print("Contenu HTML extrait du composant de l'entité :", html_str)

    # Terminer le monde
    #binded_ecs_fini(world)
