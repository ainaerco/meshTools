"""
Module containing action related classes.
"""
import enum

ActionType = enum.IntEnum("ActionType", [
    "area",
    "attack",
    "card",
    "condition",
    "custom",
    "element",
    "elementHalf",
    "fly",
    "heal",
    "grant",
    "jump",
    "loot",
    "monsterType",
    "move",
    "pierce",
    "pull",
    "push",
    "range",
    "retaliate",
    "shield",
    "spawn",
    "special",
    "specialTarget",
    "summon",
    "swing",
    "target",
    "teleport",
    "trigger",
    "concatenation",
    "grid",
    "box",
])

ActionValueType = enum.IntEnum("ActionValueType", [
    "plus",
    "minus",
    "add",
    "subtract",
    "fixed",
])

class Action:
    """ Action data entry. """
    def __init__(self, **kwargs):
        self.type = ActionType[kwargs.get("type", "custom")]
        self.value = kwargs.get("value")
        self.value_type = ActionValueType[kwargs.get("valueType", "fixed")]
        self.sub_actions = kwargs.get("subActions", [])
        self.small = kwargs.get("small", False)

    def __repr__(self):
        return "Action" + str(vars(self))
