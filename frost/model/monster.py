"""
Module containing monster related classes.
"""
import enum


class MonsterType(enum.IntEnum):
    """ Monster types. """
    NORMAL = 0
    ELITE = 1
    BOSS = 2


class Monster:
    """ Monster data entry. """
    def __init__(self, **kwargs):
        self.monster_id = kwargs.get("id", "")
        self.name = kwargs.get("name", "")
        self.edition = kwargs.get("edition", 0)
        self.level = kwargs.get("level", 0)
        self.off = kwargs.get("off", False)
        self.active = kwargs.get("active", False)
        self.draw_extra = kwargs.get("drawExtra", False)
        self.last_draw = kwargs.get("lastDraw", -1)
        self.ability = kwargs.get("ability", -1)
        self.abilities = kwargs.get("abilities", [])
        self.entities = kwargs.get("entities", [])
        self.is_ally = kwargs.get("isAlly", False)

    def __repr__(self):
        return "Monster" + str(vars(self))


class MonsterStat:
    """ MonsterStat data entry. """
    def __init__(self, **kwargs):
        # type is custom attr present in the data
        self.type = kwargs.get("type", "normal")
        self.level = kwargs.get("level", -1)
        self.health = kwargs.get("health", -1)
        self.movement = kwargs.get("movement", -1)
        self.attack = kwargs.get("attack", -1)
        self.range = kwargs.get("range", -1)
        self.actions = kwargs.get("actions", [])
        self.immunities = kwargs.get("immunities", [])
        self.special = kwargs.get("special", [])
        self.note = kwargs.get("note", "")

    def __repr__(self):
        return "MonsterStat" + str(vars(self))
