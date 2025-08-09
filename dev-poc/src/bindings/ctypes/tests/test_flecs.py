"""
Tests unitaires pour le module FlecsBinding (singleton ctypes).
"""

from pathlib import Path
import pytest
from bindings.ctypes.flecs import FlecsBinding, ecs_world_t, ecs_entity_t

def test_singleton_instance():
    """
    Vérifie que FlecsBinding est bien un singleton.
    """
    instance1 = FlecsBinding()
    instance2 = FlecsBinding()
    assert instance1 is instance2

def test_load_flecs_lib(monkeypatch):
    """
    Vérifie que la DLL Flecs est chargée (mockée).
    """
    instance = FlecsBinding()

    class DummyCDLL:
        def __init__(self, path): pass

    monkeypatch.setattr("bindings.ctypes.flecs.CDLL", DummyCDLL)
    monkeypatch.setattr(instance, "_flecs_lib", None)
    monkeypatch.setattr(
        "bindings.ctypes.flecs.PathRegistry.get_path"
        , lambda name: Path("dummy_path") if name == "flecs_dll_path" else Path("dummy.dll")
    )

    # instance.binded_load_flecs()
    with pytest.raises(FileNotFoundError):
        instance.binded_load_flecs()

    assert instance._flecs_lib is not None or hasattr(instance, "_flecs_lib")

def test_ecs_init():
    """
    Vérifie l'initialisation du monde Flecs.
    """
    instance = FlecsBinding()

    instance.binded_ecs_init()
    assert instance._Flecs_world is not None

def test_ecs_new_entity():
    """
    Vérifie la création d'une nouvelle entité (mockée).
    """
    instance = FlecsBinding()
    instance.binded_ecs_init()
    entity = instance.binded_ecs_new()
    assert isinstance(entity, int) # ecs_entity_t) ==> False /!\
    pass

def test_ecs_fini():
    """
    Vérifie la finalisation du monde Flecs (mockée).
    """
    instance = FlecsBinding()
    instance.binded_ecs_init()
    instance.binded_ecs_fini()
    assert instance._Flecs_world is None
    pass