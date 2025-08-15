from datetime import datetime
import time
from typing import Any

from meta_log.config_flags import MetaConfigFlags
# from bindings.binder__abc import BaseBinder

class MetaLogger:
    def __init__(self):
        self._meta_log = []
        self._user_view = []
        self._config_flags = MetaConfigFlags()
        self._binder = None
        # { "timestamp": True, "type_c": True, "business": True, "operation": True, }
        
    def initialize(self):
        self.meta_log(p_result=self, p_operation="initialize", p_business_value="Meta-Logger Initialized")
        # Import local pour éviter le'import circulaire
        from flecs_singleton import FlecsWorld as iFW
        iFW().register(name="meta_logger", system=self)
        # Pas de return dans __init__()

    # cffi_utils.py

    def is_flecs_cdata(self, obj: Any) -> bool:
        """
        Détecte si l'objet est un CData CFFI ou un wrapper métier Flecs.
        """
        # Cas 1 : wrapper métier avec attributs spécifiques
        if hasattr(obj, "_type") and hasattr(obj, "get_casted"):
            return True

        # Cas 2 : CData brut (ffi.new, ffi.cast, etc.)
        if repr(obj).startswith("<cdata ") or str(type(obj)).startswith("<class 'cffi."):
            return True

        return False

    def meta_log(self, p_result: Any, p_operation, p_business_value=None):
        entry = {}
        if self._config_flags.is_enabled("timestamp"):
            entry["timestamp"] = time.time() # lequel est déprécié ? /?\
        if self._config_flags.is_enabled("type_c"):
            # Ce champ dépend du binder
            # Ne demande le binder que si p_result est un CData Flecs
            _is_flecs_cdata = self.is_flecs_cdata(p_result)
            if _is_flecs_cdata and self._binder is None:
                # Import local pour éviter le'import circulaire
                from flecs_singleton import FlecsWorld as iFW
                self._binder = iFW().get(name="binder")
            if _is_flecs_cdata and self._binder:
                entry["type_c"] = self._binder.get_metalog_type_c_value(p_result) # type: ignore
            elif not _is_flecs_cdata:
                # p_result n'est pas un CData Flecs
                entry["type_c"] = "n/a"
            else:
                # cas d'erreur Flecs CData sans Binder
                entry["type_c"] = "Meta-Log: CData and Binder Not Set ?!"
        if self._config_flags.is_enabled("business"):
            entry["business"] = p_business_value or "n/a"
        if self._config_flags.is_enabled("operation"):
            entry["operation"] = p_operation
        entry["value"] = p_result
        self._meta_log.append(entry)
        self.print_entry(entry)
        pass

    def print_entry(self, p_entry) -> None:
        _op = p_entry.get("operation", "n/a")
        _bv = str(p_entry.get("business", "n/a"))
        _tc = p_entry.get("type_c", "n/a")
        print((
            f"Méta-log: "
            f"[{datetime.fromtimestamp(p_entry['timestamp']).strftime("%H:%M:%S.%f")[:-3]}] "
            f"{(_op[:20] + '…' if len(_op) > 20 else _op + ' ').ljust(22)}|"
            f"{(_bv[:30] + '…' if len(_bv) > 30 else _bv + ' ').ljust(32)}|"
            f"{(_tc[:50] + '…' if len(_tc) > 50 else _tc + ' ').ljust(52)}|"
            #f"{p_entry.get('type_c', 'n/a')}"
        ))
        pass

    def filter_view(self, **criteria):
        self._user_view = [
            entry for entry in self._meta_log
            if all(entry.get(k) == v for k, v in criteria.items())
        ]
        return self._user_view
