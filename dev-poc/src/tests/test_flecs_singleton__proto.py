"""
Tests unitaires pour le module FlecsBinding (singleton ctypes).
"""

from pathlib import Path
import pytest
from bindings.cffi.flecs_singleton import *

# FlecsBinding, ecs_world_t, ecs_entity_t

def test_singleton_instance():
    """
    Vérifie que FlecsBinding est bien un singleton.
    """
    instance1 = FlecsBindings()
    instance2 = FlecsBindings()
    assert instance1 is instance2
    pass

def test_bind_load_flecs():
    """
    Teste le chargement de la bibliothèque Flecs.
    """
    instance = FlecsBindings()
    instance.binded_load_flecs()
    assert instance.flecs_lib is not None
    assert hasattr(instance.flecs_lib, 'ecs_init')
    assert hasattr(instance.flecs_lib, 'ecs_fini')
    pass

def test_ecs_init():
    """
    Teste l'initialisation de l'environnement Flecs.
    """
    instance = FlecsBindings()
    instance.binded_load_flecs()
    instance.binded_ecs_init()
    assert instance.flecs_world is not None
    _is = instance.is_binded_type(instance.flecs_world, "ecs_world_t *")
    assert _is
    # Nettoyage
    instance.binded_shutdown()
    assert instance.flecs_world is None
    pass