"""
Magic elements.
"""
import enum

Element = enum.IntEnum("Element", [
    "any",
    "fire",
    "ice",
    "air",
    "earth",
    "light",
    "dark"
])

ElementState = enum.IntEnum("ElementState", [
    "strong",
    "waning",
    "inert",
    "new",
])
