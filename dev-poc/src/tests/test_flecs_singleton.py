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
