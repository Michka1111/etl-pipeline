class FlecsId:
    __slots__ = ("_value", "_type", "_ffi")

    def __init__(self, value, type_str, ffi):
        self._ffi = ffi
        self._type = type_str
        self._value = ffi.cast(type_str, value)

    def __repr__(self):
        return f"<{self._type}: {int(self._value)}>"

    def get(self):
        return self._value

    def __int__(self):
        raise TypeError("Conversion en int interdite")

    def __add__(self, other):
        raise TypeError("Opération interdite sur FlecsId")

    def __eq__(self, other):
        if isinstance(other, FlecsId):
            return int(self._value) == int(other._value)
        return False

    def __setattr__(self, name, value):
        if name in self.__slots__ and hasattr(self, name):
            raise AttributeError(f"{name} est en lecture seule")
        super().__setattr__(name, value)
