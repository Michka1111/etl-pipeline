# tests/test_logger.py
import pytest
from flecs_singleton import FlecsWorld

def test_meta_logging_mocklib():
    fw = FlecsWorld()
    fw.flecs_lib = type("MockLib", (), { # type: ignore
        "ecs_new": lambda self: "entity_42"
    })()

    fw.bind_function("ecs_new", business_value="bob")
    result = fw.binded_ecs_new()

    assert result == "entity_42"
    assert len(fw._meta_logger._meta_log) == 1
    entry = fw._meta_logger._meta_log[0]
    assert entry["operation"] == "ecs_new"
    assert entry["business"] == "bob"
    assert entry["value"] == "entity_42"
    pass

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