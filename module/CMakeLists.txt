SET( CXX_FILES
  module_geometry.cpp
)

include_directories(
	${PYTHON_INCLUDE_PATH}
	${Boost_INCLUDE_DIR}
	"../"
)

ADD_LIBRARY( _geometry SHARED ${CXX_FILES} )
set_target_properties(_geometry PROPERTIES SUFFIX ${PYPREFIX} PREFIX "")
target_link_libraries(
  _geometry
  geometry
  ${PYTHON_LIBRARY}
  ${Boost_PYTHON_LIBRARY}
)

SET( CXX_FILES
  module_mesh.cpp
)

ADD_LIBRARY( _mesh SHARED ${CXX_FILES} )
set_target_properties(_mesh	PROPERTIES SUFFIX ${PYPREFIX} PREFIX "")
target_link_libraries(
  _mesh
  geometry
  mesh
  ${PYTHON_LIBRARY}
  ${Boost_PYTHON_LIBRARY}
)

INSTALL(TARGETS _mesh _geometry
         LIBRARY DESTINATION scripts
         RUNTIME DESTINATION scripts
)