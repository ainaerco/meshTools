import enum

LootClass = enum.IntEnum("LootClass", [
    "money",
    "material_resources",
    "herb_resources",
    "random_item",
    "special"
])

LootType = enum.IntEnum("LootType", [
    "money",
    "lumber",
    "metal",
    "hide",
    "arrowvine",
    "axenut",
    "corpsecap",
    "flamefruit",
    "rockroot",
    "snowthistle",
    "random_item",
    "special1",
    "special2"
])
