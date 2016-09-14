from time import time
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from mesh_maya import MayaMesh

def perform(**kwargs):
    """
    kwargs = [(pointCount,1000),(node_path,)]
    """
    pointCount = kwargs.get('pointCount',1000)
    node       = kwargs.get('node_path',None)

selectionList = OpenMaya.MSelectionList()
dagPath = OpenMaya.MDagPath()

if not node:
    OpenMaya.MGlobal.getActiveSelectionList(selectionList)
else:
    selectionList.add( node )

selectionList.getDagPath(0, dagPath)
name = dagPath.fullPathName()
start_time = time()
m = MayaMesh(dag=dagPath)
elapsed_time = time() - start_time
print(str(elapsed_time)+" Elapsed on loading to mesh class")
start_time = time()
m.generateConvexHull(pointCount,m.meshFn.numVertices())
ret = m.meshToMaya(name = 'low_'+name)
elapsed_time = time() - start_time
print(str(elapsed_time)+" Elapsed")
return ret