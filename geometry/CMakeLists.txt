SET( CXX_FILES
	Bbox.cpp
	lists.cpp
	math.cpp
	Ray.cpp
	Transform.cpp
	Vector.cpp
	Polygon.cpp
)
SET( H_FILES
	Bbox.h
	lists.h
	math.h
	Ray.h
	Transform.h
	Vector.h
	Polygon.h
)

SET( SOURCE_FILES ${CXX_FILES} ${H_FILES} )
include_directories(
	${Boost_INCLUDE_DIR}
	"../"
)

ADD_LIBRARY( geometry ${SOURCE_FILES} )
INSTALL(TARGETS geometry
         ARCHIVE DESTINATION lib
)