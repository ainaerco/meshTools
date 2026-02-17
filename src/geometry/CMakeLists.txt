set(CXX_FILES
	bbox.cpp
	math.cpp
	ray.cpp
	transform.cpp
	vector.cpp
	polygon.cpp
)
set(H_FILES
	bbox.h
	lists.h
	math.h
	ray.h
	transform.h
	vector.h
	polygon.h
)

set(SOURCE_FILES ${CXX_FILES} ${H_FILES})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/..")

add_library(geometry ${SOURCE_FILES})
install(TARGETS geometry
	ARCHIVE DESTINATION lib
)
