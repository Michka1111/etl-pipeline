from ctypes import (
    CDLL, Structure
    , c_int32, c_uint64, c_size_t, c_char_p, c_void_p, c_bool
    , POINTER, byref, sizeof, alignment
)
from bindings.ctypes.flecs import *

'''
Nan, erreur de manip, l'éditeur de prompt est vraiment basique, g pas fini de taper et je fais [ENTER] au lieu de [MAJ+ENTER] ! Voici le code.
Bon, Voila, j'ai reconstitué ce que fait Flecs pour créer un component ECS, avec le fragment de langage C suivant, qui se voit incorporé dans une fonction C comme main(), à l'intérieur des '{' et '}' du corps de fonction. Ça donne comme suit. 
---C 

/* ------------------------------ */
typedef struct { … ; } TYPENAME ; 
/* ------------------------------ */

main() {
 /* Autre code C, init World ECS, ... */ 
/* Ce define est écrit par le développeur Flecs */
/* ------------------------------ */
/* #define ECS_COMPONENT( W, TYPENAME) ; */
/* Ce qui suit est généré par le Macro-(pré)-compilateur */ 
/* ------------------------------ ECS_COMPONENT(W, T) */
ecs_entity_t FLECS_ID_TYPENAME_ID_ = 0 ; 
/* ------------------------------ ECS_COMPONENT_DEFINE(W, T) */
{
ecs_component_desc_t desc = {0} ; 
ecs_entity_desc_t edesc = {0} ; 
edesc.id = FLECS_ID_TYPENAME_ID_ ; 
edesc.use_low_id = true ; 
edesc.name = #TYPENAME ; 
edesc.symbol = #TYPENAME ; 
desc.entity = ecs_entity_init( W, &edesc) ; 
desc.type.size = ECS_SIZEOF( TYPENAME) ; 
desc.type.alignment = ECS_ALIGNOF( TYPENAME) ; 
FLECS_ID_TYPENAME_ID_ = ecs_component_init( W, &desc) ;
}
assert( FLECS_ID_TYPENAME_ID_ != 0, ECS_INVALID_PARAMETER \
             , "Failed to create component %s", #TYPENAME ) ;
/* ------------------------------ ECS_COMPONENT(W, T) */
(void)FLECS_ID_TYPENAME_ID_ ;
/* ------------------------------ */
/* AUTRE CODE POUR GÉRER LE COMPONENT */
/* Code Fin du Monde W */
} /* Fin du main() */
---
Je penses que tu aura compris ? Il faut comprendre que c'est compilé et ensuite exécuté, ce qui est différent du Python interprété.
quand "#TYPENAME", c'est la str du nom du type défini.
quand "&desc", c'est l'adresse de la variable desc en mémoire.
"ecs_entity_init()" est de l'API C Flecs, et il faut l'écrire à la sauce CTYPES/CDLL pour appeler cette fonction dans la librairie flecs.dll.
Pareil pour "ecs_component_init()".
FLECS_ID_TYPENAME_ID_ est une variable dont le nom est générée dynamiquement avec des #define, à partir du nom TYPENAME du typedef initial. 
En Python, ce typedef se traduit par la data classe utilisateur dont on veut enregistrer le component dans le monde Flecs.
Maintenant, génère l'équivalent Python, stp.
'''

# Types de base (correspondance directe avec ctypes.c_*)
ecs_world_t         = c_void_p
ecs_id_t            = c_uint64
ecs_size_t          = c_size_t
bool_t              = c_bool
true_t              = c_bool(True)
int32_t             = c_int32
const_char_p        = c_char_p
# Types dérivés
ecs_entity_t        = ecs_id_t  # typedef uint64_t ecs_entity_t;
# Types généricisés
ecs_type_hooks_t    = c_void_p  # typedef struct ecs_type_hooks_t ecs_type_hooks_t
const_ecs_id_t_p    = c_void_p  # const ecs_id_t *
const_ecs_value_t_p = c_void_p  # const ecs_value_t *
#
# Structures Flecs complètes (champs publics de la doc officielle)
#
# ecs_type_info_t
class EcsTypeInfo(Structure):       # ECS_TYPE_INFO_T
    _fields_ = [                    # https://www.flecs.dev/flecs/structecs__type__info__t.html
        (  "size",      ecs_size_t)        # NOT NULL
        , ("alignment", ecs_size_t)        # NOT NULL
        , ("hooks",     ecs_type_hooks_t)  # not used
        , ("component", ecs_entity_t)      # not used ("do not set")
        , ("name",      const_char_p)      # not used
    ]
# ecs_entity_desc_t
class EcsEntityDesc(Structure):     # ECS_ENTITY_DESC_T
    _fields_ = [                    # https://www.flecs.dev/flecs/structecs__entity__desc__t.html
        (  "_canary",       int32_t)        # NULL
        , ("id",            ecs_entity_t)   # FLECS_ID_TYPENAME_ID_
        , ("parent",        ecs_entity_t)   # not used
        , ("name",          const_char_p)   # #TYPENAME
        , ("sep",           const_char_p)   # not used
        , ("root_sep",      const_char_p)   # not used
        , ("symbol",        const_char_p)   # #TYPENAME
        , ("use_low_id",    bool_t)         # c_bool(True)
        , ("add",           const_ecs_id_t_p)       # not used
        , ("set",           const_ecs_value_t_p)    # not used
        , ("add_expr",      const_char_p)           # not used
    ]

class EcsComponentDesc(Structure):      # ECS_COMPONENT_DESC_T
    _fields_ = [                        # https://www.flecs.dev/flecs/structecs__component__desc__t.html
        (  "_canary",   int32_t)        # ZERO-SET for validation ==> assert error
        , ("entity",    ecs_entity_t)   # looked-up for existing, zero-set for creation
        , ("type",      EcsTypeInfo)    # ecs_type_info_t)   # See Above
    ]

def register_dataclass_component(
    p_world_ptr
    , p_data_cls
    , p_flecs_lib: CDLL
    ) -> c_uint64:

    _name = p_data_cls.__name__
    _size = sizeof(p_data_cls)
    _align = alignment(p_data_cls)

    _edesc = EcsEntityDesc()
    _edesc._canary = 0
    _edesc.id = 0
    _edesc.name = _name.encode("utf-8")
    _edesc.symbol = _name.encode("utf-8")
    _edesc.use_low_id = c_bool(True)

    p_flecs_lib.ecs_entity_init.argtypes = [c_void_p, POINTER(EcsEntityDesc)]
    p_flecs_lib.ecs_entity_init.restype = c_uint64

    _entity_id = p_flecs_lib.ecs_entity_init(
        p_world_ptr
        , byref(_edesc)
    )

    _desc = EcsComponentDesc()
    _desc._canary = 0
    _desc.entity = _entity_id
    _desc.type = EcsTypeInfo(_size, _align)
    _desc.name = _name.encode("utf-8")
    _desc.symbol = _name.encode("utf-8")
    _desc.use_low_id = c_bool(True)

    p_flecs_lib.ecs_component_init.argtypes = [c_void_p, POINTER(EcsComponentDesc)]
    p_flecs_lib.ecs_component_init.restype = c_uint64

    _component_id = p_flecs_lib.ecs_component_init(
        p_world_ptr
        , byref(_desc)
    )

    assert _component_id != 0, f"Failed to register component {_name}"

    return _component_id


# Ajout d’un composant à une entité
def ecs_add_component(world, entity, component_id):
    lib = binded_load_flecs()
    lib.ecs_add_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_entity_t]
    lib.ecs_add_id(world, entity, component_id)

# Écriture des données d’un composant
def ecs_set_component_data(world, entity, component_id, data: Structure):
    lib = binded_load_flecs()
    lib.ecs_get_mut_id.restype = c_void_p
    lib.ecs_get_mut_id.argtypes = [ecs_world_t, ecs_entity_t, ecs_entity_t, POINTER(c_bool)]
    is_added = c_bool()
    ptr = lib.ecs_get_mut_id(world, entity, component_id, byref(is_added))
    memmove(ptr, byref(data), sizeof(data))

# Récupération du composant
def get_component_data(world, entity: c_uint64, component_id: c_uint64, struct_cls: type):
    lib = world.lib
    lib.ecs_get_id.restype = c_void_p
    lib.ecs_get_id.argtypes = [c_void_p, c_uint64, c_uint64]
    ptr = lib.ecs_get_id(world.world, entity, component_id)
    if not ptr:
        return None
    data = struct_cls()
    memmove(byref(data), ptr, sizeof(data))
    return data
