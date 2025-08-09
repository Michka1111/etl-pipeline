from ctypes import (
    CDLL, Structure
    , c_double
    , c_void_p
)

from flecs_component_register import register_component_struct

class Position(Structure):
    _fields_ = [
        ("x", c_double)
        , ("y", c_double)
    ]

def test_register_position_component():
    _flecs_lib = CDLL("path/to/flecs.dll")  # adapte le chemin
    _flecs_lib.ecs_init.restype = c_void_p
    _world_ptr = _flecs_lib.ecs_init()

    _component_id = register_component_struct(
        p_world_ptr=_world_ptr
        , p_struct_cls=Position
        , p_flecs_lib=_flecs_lib
    )

    assert isinstance(_component_id, int)
    assert _component_id != 0
