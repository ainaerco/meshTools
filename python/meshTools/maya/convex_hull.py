"""Maya convex hull: generate low-poly hull from mesh.

Loads selected mesh, runs generateConvexHull with configurable point count,
and writes result to a new mesh node.
"""

import logging
from time import time

import maya.OpenMaya as OpenMaya

from meshTools.maya.mesh import MayaMesh

logger = logging.getLogger(__name__)


def perform(**kwargs):
    """Build convex hull from selected mesh. kwargs: pointCount (default 1000), node_path (optional)."""
    pointCount = kwargs.get("pointCount", 1000)
    node = kwargs.get("node_path", None)

    selectionList = OpenMaya.MSelectionList()
    dagPath = OpenMaya.MDagPath()

    if not node:
        OpenMaya.MGlobal.getActiveSelectionList(selectionList)
    else:
        selectionList.add(node)

    selectionList.getDagPath(0, dagPath)
    name = dagPath.fullPathName()
    start_time = time()
    m = MayaMesh(dag=dagPath)
    elapsed_time = time() - start_time
    logger.info("%s Elapsed on loading to mesh class", elapsed_time)
    start_time = time()
    m.generateConvexHull(pointCount, m.meshFn.numVertices())
    ret = m.meshToMaya(name="low_" + name)
    elapsed_time = time() - start_time
    logger.info("%s Elapsed", elapsed_time)
    return ret
