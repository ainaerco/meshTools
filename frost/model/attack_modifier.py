"""
Attack modifier deck related classes.
"""
import enum

AttackModifierType = enum.IntEnum("AttackModifierType", [
    "plus0",
    "plus1",
    "plus2",
    "plus3",
    "plus4",
    "plusX",
    "minus1",
    "minus2",
    "null",
    "double",
    "bless",
    "curse",
    "empower",
    "enfeeble",
    "invalid",
])

AttackModifierValueType = enum.IntEnum("AttackModifierValueType", [
    "plus",
    "minus",
    "multiply"
])

AttackModifierEffectType = enum.IntEnum("AttackModifierEffectType", [
    "area",
    "changeType",
    "condition",
    "custom",
    "element",
    "elementConsume",
    "elementHalf",
    "heal",
    "pierce",
    "pull",
    "push",
    "range",
    "refreshItem",
    "refreshSpentItem",
    "recoverRandomDiscard",
    "retaliate",
    "shield",
    "specialTarget",
    "summon",
    "swing",
    "target",
    "attack",
    "or"
])

class AttackModifier:
    """ AttackModifier. """
    def __init__(self, **kwargs):
        self.type = AttackModifierType[kwargs.get("type", "invalid")]
        self.modifier_id = kwargs.get("id") or self.type
        self.value = kwargs.get("value", 0)
        self.value_type = AttackModifierValueType[kwargs.get("valueType", "plus")]
        self.shuffle = kwargs.get("shuffle", False)
        self.effects = kwargs.get("effects", [])
        self.rolling = kwargs.get("rolling", False)
        self.active = kwargs.get("active", True)
        self.revealed = kwargs.get("revealed", False)
        self.character = kwargs.get("character", False)

        if self.type == AttackModifierType.plus0:
            self.value = 0
        elif self.type == AttackModifierType.plus1:
            self.value = 1
        elif self.type == AttackModifierType.plus2:
            self.value = 2
        elif self.type == AttackModifierType.plus3:
            self.value = 3
        elif self.type == AttackModifierType.plus4:
            self.value = 4
        elif self.type == AttackModifierType.minus1:
            self.value_type = AttackModifierValueType.minus
            self.value = 1
        elif self.type == AttackModifierType.minus2:
            self.value_type = AttackModifierValueType.minus
            self.value = 2
        elif self.type == AttackModifierType.null:
            self.value_type = AttackModifierValueType.multiply
            self.value = 0
            self.shuffle = True

        elif self.type == AttackModifierType.double:
            self.value_type = AttackModifierValueType.multiply
            self.value = 2
            self.shuffle = True

        elif self.type == AttackModifierType.bless:
            self.value_type = AttackModifierValueType.multiply
            self.value = 2

        elif self.type == AttackModifierType.curse:
            self.value_type = AttackModifierValueType.multiply
            self.value = 0


class AttackModifierEffect:
    """ AttackModifierEffect. """
    def __init__(self, **kwargs):
        self.type = AttackModifierEffectType[kwargs.get("type", "invalid")]
        self.value = kwargs.get("value", "")
        self.hint = kwargs.get("hint", "")
        self.effects = kwargs.get("effects", [])
        self.icon = kwargs.get("icon", False)


DEFAULT_ATTACK_MODIFIERS = [
    AttackModifier(type="plus0"),
    AttackModifier(type="plus1"),
    AttackModifier(type="minus1"),
    AttackModifier(type="plus2"),
    AttackModifier(type="minus2"),
    AttackModifier(type="double"),
    AttackModifier(type="null"),
    AttackModifier(type="bless"),
    AttackModifier(type="curse")
]

DEFAULT_ATTACK_MODIFIER_CARDS = [
    "plus0", "plus0", "plus0", "plus0", "plus0", "plus0",
    "plus1", "plus1", "plus1", "plus1", "plus1",
    "minus1", "minus1", "minus1", "minus1", "minus1",
    "plus2",
    "minus2",
    "double",
    "null"
]


class AttackModifierDeck:
    """ AttackModifierDeck. """

    def __init__(self, **kwargs):
        self.attack_modifiers = DEFAULT_ATTACK_MODIFIERS
        self.current = -1
        self.cards = [self.card_by_id(x) for x in DEFAULT_ATTACK_MODIFIER_CARDS]
        self.discarded = []

    def card_by_id(self, modifier_id):
        """
        Return AttackModifier by id.
        """
        for card in self.attack_modifiers:
            if card.modifier_id == modifier_id:
                return card
        return None
