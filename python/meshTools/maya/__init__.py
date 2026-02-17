"""Optional Maya subpackage: use only inside Autodesk Maya.

This subpackage requires the Maya Python environment (maya.OpenMaya, maya.cmds).
Import only when running inside Maya; the core meshTools package has no Maya dependency.
"""

from meshTools.maya.mesh import MayaMesh, kGeotype
from meshTools.maya.tube import MayaTube

__all__ = [
    "MayaMesh",
    "kGeotype",
    "MayaTube",
]
