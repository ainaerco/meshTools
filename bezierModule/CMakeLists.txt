SET( CXX_FILES
  module_bezier.cpp
)

SET( SOURCE_FILES ${CXX_FILES} )
include_directories(
	${PYTHON_INCLUDE_PATH}
	${Boost_INCLUDE_DIR}
	"../bezier"
)

ADD_LIBRARY( pybezier SHARED ${SOURCE_FILES} )
set_target_properties(pybezier PROPERTIES SUFFIX ${PYPREFIX})
target_link_libraries(
  pybezier
  bezier
  ${PYTHON_LIBRARY}
  ${Boost_PYTHON_LIBRARY}
)

INSTALL(TARGETS pybezier
         LIBRARY DESTINATION scripts
         RUNTIME DESTINATION scripts
)