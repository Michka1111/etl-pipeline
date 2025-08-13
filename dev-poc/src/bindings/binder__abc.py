from abc import abstractmethod
from pathlib import Path
from typing import Any


class BaseBinder:

    @abstractmethod
    def bind_tool_tuple(self, p_dll_path: Path) -> tuple[Any, Any]:
        """Retourne le tuple (BIND_cmd, BIND_lib) selon la bind-techno.
        CFFI:   (FFI(), lib)
        CTYPES: (None, CDLL())"""
        BIND_cmd = None
        BIND_lib = None
        return (BIND_cmd, BIND_lib)

    @abstractmethod
    def get_metalog_type_c_value(self, p_result: Any):
        """Calcule la valeur de la dimension "type_c" de la méta-log selon la bind-techno.
        CFFI:   le type en langage C du retour d'appel de fonction de la DLL liée.
        CTYPES: TODO"""
        raise NotImplementedError

    @property
    @abstractmethod
    def lib(self):
        """Accès direct à la bibliothèque chargée"""
        pass

    def add_binding_method_to_binder(self, lib_func_name: str, business_value: Any = None):
        raise NotImplementedError

