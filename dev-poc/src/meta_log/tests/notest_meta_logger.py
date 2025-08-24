class FakeCDataFlecs:
    def __init__(self):
        self._type = "flecs"
    def get_casted(self):
        return self

class DummyObject:
    pass

class FakeBinder:
    def __init__(self):
        self.called_with = None

    def get_metalog_type_c_value(self, obj):
        self.called_with = obj
        return "SimulatedTypeC"

import pytest
from meta_log.meta_logger import MetaLogger
from meta_log.config_flags import MetaConfigFlags

def test_meta_log_with_cdata(monkeypatch):
    binder = FakeBinder()

    # Monkeypatch le singleton pour qu’il retourne notre faux binder
    def fake_get(name):
        return binder if name == "binder" else None

    class FakeSingleton:
        def get(self, name):
            return fake_get(name)

    # Monkeypatch l'import du singleton dans MetaLogger
    monkeypatch.setitem(__import__("sys").modules, "flecs_singleton", {"FlecsWorld": lambda: FakeSingleton()})

    config = MetaConfigFlags()
    # (Par défaut) config.enable("type_c")
    logger = MetaLogger() # Init automatique de la config, mais pas du Binder.
    logger._binder = None  # Simule un logger sans binder

    result = FakeCDataFlecs()
    logger.meta_log(result, "create")

    assert logger._meta_log[-1]["type_c"] == "SimulatedTypeC"
    assert binder.called_with == result

def test_meta_log_without_cdata(monkeypatch):
    binder = FakeBinder()

    config = MetaConfigFlags()
    # (par défaut) config.enable("type_c")
    logger = MetaLogger()
    logger._binder = binder  # Binder déjà présent

    result = DummyObject()
    logger.meta_log(result, "noop")

    assert logger._meta_log[-1]["type_c"] == "n/a"
    assert binder.called_with is None
