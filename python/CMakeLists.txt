SET(PY_FILES
	convexHull.py
	flowLoop.py
	mesh_maya.py
	mesh_maya_scatter.py
	mesh_maya_tube.py
	module_geometry_tests.py
	obb.py
	tubeDeformer.py)
INSTALL( DIRECTORY meshTools DESTINATION scripts )
INSTALL( FILES ${PY_FILES} DESTINATION scripts )