import pytest
from ..singleton_registry_path import PathRegistry
# L'import instancie le singleton PathRegistry

def test_default_paths_exist():
    # Vérifie que les chemins par défaut sont bien enregistrés
    assert PathRegistry.get_path("flecs_dll_path").name == "flecs.dll"
    # Vérifie que les chemins par défaut sont des sous-dossiers de 'dev-poc/src'
    assert PathRegistry.get_path("world_data_in_path").parts[-2:] == ("src", "data_in")
    assert PathRegistry.get_path("world_data_out_path").parts[-2:] == ("src", "data_out")

def test_add_new_path():
    # Ajoute un nouveau chemin et vérifie son enregistrement
    PathRegistry.add_path("config_path", "dev-poc/config/settings.json")
    path = PathRegistry.get_path("config_path")
    assert path.name == "settings.json"
    assert "config" in path.parts

def test_missing_path_raises():
    # Vérifie qu’un chemin non défini lève une exception
    with pytest.raises(KeyError):
        PathRegistry.get_path("non_existent_path") 
 
