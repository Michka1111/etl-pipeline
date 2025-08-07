from types import SimpleNamespace
from pathlib import Path
from typing import Union

class _PathRegistry:
    def __init__(self):
        self._paths = SimpleNamespace()
        self._initialized = False
        self._default_paths = {
            "flecs_dll_path": Path("dev-poc/lib/flecs.dll"),
            "world_data_in_path": Path("dev-poc/src/data_in"),
            "world_data_out_path": Path("dev-poc/src/data_out")
        }
        self.init(self._default_paths.items())

    def init(self, entries: list[tuple[str, Union[str, Path]]]):
        if self._initialized:
            raise RuntimeError("PathRegistry already initialized.")
        for name, value in entries:
            setattr(self._paths, name, Path(value))
        self._initialized = True

    def get_path(self, name: str) -> Path:
        if not hasattr(self._paths, name):
            raise KeyError(f"Path '{name}' not found.")
        return getattr(self._paths, name)

    def add_path(self, name: str, value: Union[str, Path]):
        setattr(self._paths, name, Path(value))

# Singleton instance
PathRegistry = _PathRegistry()
# Example usage:
# from singleton_registry_path import PathRegistry
# path = PathRegistry.get_path("flecs_dll_path")