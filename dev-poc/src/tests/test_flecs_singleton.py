# tests/test_logger.py
import pytest
from flecs_singleton import FlecsWorld

def test_singleton_instance():
    """
    Vérifie que FlecsBinding est bien un singleton.
    """
    instance1 = FlecsWorld()
    instance2 = FlecsWorld()
    assert instance1 is instance2
    pass


def test_meta_logging_real_flecs(): 
    print("\nTest de la méta-log avec Flecs")
    fw = FlecsWorld()
    _mtlg = fw.get(name="meta_logger")._meta_log
    _len_meta_log = len(_mtlg)
    fw.binded_load_flecs()
    _fl = fw.get(name="flecs_lib")  # Ensure the flecs library is loaded
    assert _fl is not None
#    assert len(_mtlg) > _len_meta_log

    # Initialize the ECS world
    _len_meta_log = len(_mtlg)
    fw.binded_ecs_init()
    assert fw.get(name="flecs_world") is not None
    assert len(_mtlg) > _len_meta_log
    assert _mtlg[-1]["operation"] == "ecs_init"
    assert _mtlg[-1]["type_c"] == "ecs_world_t *"

    # Create a new entity
    _len_meta_log = len(_mtlg)
    entity = fw.binded_ecs_new()
    assert entity is not None and isinstance(entity, int) # Vu du Python
    assert len(_mtlg) > _len_meta_log

    # Check the meta log for the ecs_new operation
    entry = _mtlg[-1]
    assert entry["operation"] == "ecs_new"
    assert entry["type_c"] == "n/a" # Python int does not have a CData type
    assert entry["business"] == 534

    # Shutdown the ECS world
    fw.binded_shutdown()
    assert fw.flecs_world is None
    pass

def test_generate_binding_method():
    fw = FlecsWorld()
    fw.binded_ecs_init()
    _cdata_type = "ecs_entity_t"
    _binder = fw.get(name="binder")
    assert _binder is not None
    _binder.add_binding_method_to_binder(
        "ecs_set_name"
        , business_value="Create named entity"
        , p_cdata_type= _cdata_type
    )

    _bind_added = getattr(_binder, "binded_ecs_set_name")
    assert _bind_added is not None
    assert callable(_bind_added)
    _bind_cmd = fw.get(name="bind_cmd")
    _new_char_string_name = _bind_cmd.new("char[]", b"MyNamedEntity") # new et non cast, "but of course" (doc cffi)
    _world = fw.get(name="flecs_world")
    _named_entity_id = _binder.binded_ecs_set_name(  # type: ignore
        _world
        , 0
        , _new_char_string_name
    )
    assert _named_entity_id is not None
    _cdata_type_named_entity = _bind_cmd.typeof(_named_entity_id) if isinstance(_named_entity_id, _bind_cmd.CData) else "n/a"
    assert _cdata_type_named_entity != "n/a"
    _python_type_named_entity = type(_named_entity_id).__name__ if hasattr(_named_entity_id, '__class__') else "n/a"
    assert _python_type_named_entity == "_CDataBase"
    # assert _python_type_named_entity.cname == _cdata_type # type: ignore
    pass

#if __name__ == "__main__":
#    import pytest
#    # print "Bonjour, je suis le test de flecs_singleton.py"
#    pytest.main(["-v", __file__ + "::test_meta_logging_real_flecs"])
