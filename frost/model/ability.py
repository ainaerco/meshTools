"""
Module containing ability related classes.
"""


class Ability:
    """ Ability data entry. """
    def __init__(self, **kwargs):
        self.card_id = kwargs.get("cardId", -1)
        self.name = kwargs.get("name", "")
        self.initiative = kwargs.get("initiative", -1)
        self.level = kwargs.get("level", 0)
        self.shuffle = kwargs.get("shuffle", False)
        self.actions = kwargs.get("actions", [])
        self.lost = kwargs.get("lost", False)
        self.bottom_actions = kwargs.get("bottomActions", [])
        self.bottom_lost = kwargs.get("bottomLost", False)
        self.hint = kwargs.get("hint", "")
        self.revealed = kwargs.get("revealed", False)

    def __repr__(self):
        return "Ability" + str(vars(self))