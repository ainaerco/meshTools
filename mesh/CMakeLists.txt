SET( CXX_FILES
	Mesh.cpp
)
SET( H_FILES
	Mesh.h
)

SET( SOURCE_FILES ${CXX_FILES} ${H_FILES} )
include_directories(
	${Boost_INCLUDE_DIR}
	"../"
)

ADD_LIBRARY( mesh ${SOURCE_FILES} )
INSTALL(TARGETS mesh
         ARCHIVE DESTINATION lib
)