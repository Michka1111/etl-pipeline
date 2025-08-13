# tests/test_logger.py
import pytest
from flecs_singleton import FlecsWorld

def test_meta_logging_real_flecs(): 
    fw = FlecsWorld()
    _len_meta_log = len(fw._meta_logger._meta_log)
    fw.binded_load_flecs()  # Ensure the flecs library is loaded
    assert fw.flecs_lib is not None
    assert len(fw._meta_logger._meta_log) > _len_meta_log

    # Initialize the ECS world
    _len_meta_log = len(fw._meta_logger._meta_log)
    fw.binded_ecs_init()
    assert fw.flecs_world is not None
    assert len(fw._meta_logger._meta_log) > _len_meta_log
    assert fw._meta_logger._meta_log[-1]["operation"] == "ecs_init"
    assert fw._meta_logger._meta_log[-1]["type_c"] == "ecs_world_t *"

    # Create a new entity
    _len_meta_log = len(fw._meta_logger._meta_log)
    entity = fw.binded_ecs_new()
    assert entity is not None and isinstance(entity, int) # Vu du Python
    assert len(fw._meta_logger._meta_log) > _len_meta_log

    # Check the meta log for the ecs_new operation
    entry = fw._meta_logger._meta_log[-1]
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
    fw._binder.add_binding_method_to_binder(
        "ecs_set_name"
        , business_value="Create named entity"
        , p_cdata_type= _cdata_type
    )
    
    _bind_added = getattr(fw._binder, "binded_ecs_set_name")
    assert _bind_added is not None
    assert callable(_bind_added)
    _n = fw.bind_cmd.new("char[]", b"MyNamedEntity") # new et non cast, "but of course" (doc cffi)
    _named_entity_id = fw._binder.binded_ecs_set_name(  # type: ignore
        fw.flecs_world
        , 0
        , _n
    )
    assert _named_entity_id is not None
    _cdata_type_named_entity = fw._binder._ffi.typeof(_named_entity_id) if isinstance(_named_entity_id, fw._binder._ffi.CData) else "n/a"
    assert _cdata_type_named_entity != "n/a"
    _python_type_named_entity = type(_named_entity_id).__name__ if hasattr(_named_entity_id, '__class__') else "n/a"
    assert _python_type_named_entity == "_CDataBase"
    # assert _python_type_named_entity.cname == _cdata_type # type: ignore
    pass