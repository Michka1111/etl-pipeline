"""
Module de tests pour singleton_registry_path
--------------------------------------------

Ce module contient des tests unitaires pour la classe PathRegistry,
qui permet d'enregistrer et de récupérer des chemins nommés dans l'application.

Fonctions de test :
    test_default_paths_exist -- Vérifie l'existence et la validité des chemins par défaut.
    test_add_new_path -- Vérifie l'ajout et la récupération d'un nouveau chemin.
    test_missing_path_raises -- Vérifie que l'accès à un chemin non défini lève une exception.
"""

import pytest
from ..singleton_registry_path import PathRegistry
# L'import instancie le singleton PathRegistry

def test_default_paths_exist():
    """
    Vérifie que les chemins par défaut sont bien enregistrés et corrects.
    """
    assert PathRegistry.get_path("flecs_dll_path").name == "flecs.dll"
    assert PathRegistry.get_path("world_data_in_path").parts[-2:] == ("src", "data_in")
    assert PathRegistry.get_path("world_data_out_path").parts[-2:] == ("src", "data_out")

def test_add_new_path():
    """
    Vérifie l'ajout et la récupération d'un nouveau chemin nommé.
    """
    PathRegistry.add_path("config_path", "dev-poc/config/settings.json")
    path = PathRegistry.get_path("config_path")
    assert path.name == "settings.json"
    assert "config" in path.parts

def test_missing_path_raises():
    """
    Vérifie qu’un chemin non défini lève une exception KeyError.
    """
    with pytest.raises(KeyError):
        PathRegistry.get_path("non_existent_path")

