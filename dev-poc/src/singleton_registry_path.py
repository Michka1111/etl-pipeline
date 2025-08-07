"""
Module singleton_registry_path
-----------------------------

Ce module fournit un singleton PathRegistry pour enregistrer et récupérer des chemins nommés dans l'application.

Classes:
    _PathRegistry -- Gestionnaire de chemins nommés.

Variables:
    PathRegistry -- Instance singleton de _PathRegistry.
"""

from types import SimpleNamespace
from pathlib import Path
from typing import Union

class _PathRegistry:
    """
    Singleton pour l'enregistrement et la récupération de chemins nommés.

    Attributs:
        _paths (SimpleNamespace): Stocke les chemins enregistrés.
        _initialized (bool): Indique si le registre a été initialisé.
        _default_paths (dict): Chemins par défaut à l'initialisation.

    Méthodes:
        init(entries): Initialise le registre avec une liste de tuples (nom, chemin).
        get_path(name): Retourne le chemin associé au nom donné.
        add_path(name, value): Ajoute ou remplace un chemin nommé.
    """
    def __init__(self):
        """Initialise le registre avec les chemins par défaut."""
        self._paths = SimpleNamespace()
        self._initialized = False
        self._default_paths = {
            "flecs_dll_path": Path("dev-poc/lib")
            , "flecs_dll_name": "flecs410.dll"
            , "world_data_in_path": Path("dev-poc/src/data_in")
            , "world_data_out_path": Path("dev-poc/src/data_out")
        }
        self.init(self._default_paths.items())

    def init(self, entries: list[tuple[str, Union[str, Path]]]):
        """
        Initialise le registre avec une liste de tuples (nom, chemin).

        Args:
            entries (list): Liste de tuples (nom, chemin).

        Raises:
            RuntimeError: Si le registre est déjà initialisé.
        """
        if self._initialized:
            raise RuntimeError("PathRegistry already initialized.")
        for name, value in entries:
            setattr(self._paths, name, Path(value))
        self._initialized = True

    def get_path(self, name: str) -> Path:
        """
        Retourne le chemin associé au nom donné.

        Args:
            name (str): Nom du chemin.

        Returns:
            Path: Chemin correspondant.

        Raises:
            KeyError: Si le nom n'est pas enregistré.
        """
        if not hasattr(self._paths, name):
            raise KeyError(f"Path '{name}' not found.")
        return getattr(self._paths, name)

    def add_path(self, name: str, value: Union[str, Path]):
        """
        Ajoute ou remplace un chemin nommé.

        Args:
            name (str): Nom du chemin.
            value (str | Path): Chemin à enregistrer.
        """
        setattr(self._paths, name, Path(value))

# Singleton instance
PathRegistry = _PathRegistry()
# Example usage:
# from singleton_registry_path import PathRegistry
# path = PathRegistry.get_path("flecs_dll_path")