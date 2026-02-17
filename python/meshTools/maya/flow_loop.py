"""Maya flowLoop command: flow loop operation on mesh edge selection.

Registers a scripted command that operates on selected edges to perform
flow loop. Requires Maya OpenMayaMPx.
"""

import logging
import sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

from meshTools.maya.mesh import MayaMesh, kGeotype

logger = logging.getLogger(__name__)

kPluginCmdName = "flowLoop"


# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self, argList):
        logger.debug("doIt()")
        self.redoIt()

    def redoIt(self):
        logger.debug("redoIt()")
        self.dagModifier = OpenMaya.MDagModifier()
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selectionList)
        dagPath = OpenMaya.MDagPath()
        selectionList.getDagPath(0, dagPath)
        m = MayaMesh(
            dag=dagPath, vertices=1, faces=1, edges=1, normals=1, build=1
        )

        edgeIt = OpenMaya.MItMeshEdge(dagPath)
        selection = []

        while not edgeIt.isDone():
            if selectionList.hasItem(dagPath, edgeIt.currentItem()):
                selection += [edgeIt.index()]
            edgeIt.next()
        m.selectionType = kGeotype.edge
        m.flowLoop(selection)

    def undoIt(self):
        logger.debug("undoIt()")
        self.dagModifier.undoIt()

    def isUndoable(self):
        logger.debug("isUndoable()")
        return True


# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(scriptedCommand())


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except Exception:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except Exception:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
