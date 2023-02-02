import enum

ConditionName = enum.IntEnum("ConditionName", [
    "stun",
    "immobilize",
    "disarm",
    "wound",
    "muddle",
    "poison",
    "invisible",
    "strengthen",
    "curse",
    "bless",
    "regenerate",
    "chill",
    "infect",
    "ward",
    "bane",
    "brittle",
    "impair",
    "rupture",
    "dodge",
    "empower",
    "enfeeble",
    "poison_x",
    "wound_x",
])

ConditionType = enum.IntEnum("ConditionType", [
    "action",
    "standard",
    "entity",
    "character",
    "monster",
    "upgrade",
    "stack",
    "turn",
    "expire",
    "value",
    "clearHeal",
    "preventHeal",
    "apply",
    "positive",
    "negative"
])

EntityConditionState = enum.IntEnum("EntityConditionState", [
    "normal",
    "expire",
    "turn"
])
