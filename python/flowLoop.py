import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from meshTools_maya.mesh_maya import MayaMesh, kGeotype

kPluginCmdName = "flowLoop"


# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self, argList):
        print("doIt()")

        self.redoIt()

    def redoIt(self):

        print("redoIt()")
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
        print("undoIt()")
        self.dagModifier.undoIt()

    def isUndoable(self):
        print("isUndoable()")
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
