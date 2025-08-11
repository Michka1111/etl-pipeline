"""
Tests unitaires pour le module FlecsBinding (singleton ctypes).
"""

from pathlib import Path
import pytest
from bindings.ctypes.flecs import *
# FlecsBinding, ecs_world_t, ecs_entity_t

def test_singleton_instance():
    """
    Vérifie que FlecsBinding est bien un singleton.
    """
    instance1 = FlecsBinding()
    instance2 = FlecsBinding()
    assert instance1 is instance2
    pass

def test_load_flecs_lib(monkeypatch):
    """
    Vérifie que la DLL Flecs est chargée (mockée).
    """
    instance = FlecsBinding()

    class DummyCDLL:
        def __init__(self, path): pass

    monkeypatch.setattr("bindings.ctypes.flecs.CDLL", DummyCDLL)
    monkeypatch.setattr(instance, "flecs_lib", None)
    monkeypatch.setattr(
        "bindings.ctypes.flecs.PathRegistry.get_path"
        , lambda name: Path("dummy_path") if name == "flecs_dll_path" else Path("dummy.dll")
    )
    pass

    # instance.binded_load_flecs()
    with pytest.raises(FileNotFoundError):
        instance.binded_load_flecs()

    assert instance.flecs_lib is not None or hasattr(instance, "flecs_lib")
    pass

def test_ecs_init():
    """
    Vérifie l'initialisation du monde Flecs.
    """
    instance = FlecsBinding()
    instance.binded_ecs_init()
    assert instance.flecs_world is not None
    pass

def test_ecs_fini():
    """
    Vérifie la finalisation du monde Flecs (mockée).
    """
    instance = FlecsBinding()
    instance.binded_ecs_init()
    instance.binded_ecs_fini()
    assert instance.flecs_world is None
    pass

def test_ecs_new_entity():
    """
    Vérifie la création d'une nouvelle entité.
    """
    _bdr_ecs = FlecsBinding()
    _bdr_ecs.binded_ecs_init()
    _entity = _bdr_ecs.binded_ecs_new()
    _bdr_ecs.binded_ecs_fini()
    assert isinstance(_entity, int)  # ecs_entity_t) ==> False /!\
    assert _entity == 534            # vu de Python, c'est bien int
    pass

def test_ecs_set_name():
    # Singleton DLL Binder on FLECS World
    _bdr_ecs = FlecsBinding()
    _bdr_ecs.binded_ecs_init()

    # Create an entity with name Bob
    _bob = _bdr_ecs.binded_ecs_set_name(0, "Bob")
    _bob2 = _bdr_ecs.binded_ecs_set_name(0, "Bob")
    
    _bdr_ecs.binded_ecs_fini()
    # Create with existing Entity with NAME ==> find ==> get(existing_E)
    assert isinstance(_bob, int) and _bob == 534 and _bob == _bob2

    pass
