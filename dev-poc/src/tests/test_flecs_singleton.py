# tests/test_logger.py
import pytest
from flecs_singleton import FlecsWorld

def test_transaction_logging():
    fw = FlecsWorld()
    fw.flecs_lib = type("MockLib", (), {
        "ecs_new": lambda self: "entity_42"
    })()

    fw.bind_function("ecs_new", business_value="bob")
    result = fw.binded_ecs_new()

    assert result == "entity_42"
    assert len(fw.transaction_logger._meta_log) == 1
    entry = fw.transaction_logger._meta_log[0]
    assert entry["operation"] == "ecs_new"
    assert entry["business"] == "bob"
    assert entry["value"] == "entity_42"
    pass
