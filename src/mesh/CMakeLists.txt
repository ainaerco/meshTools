set(CXX_FILES mesh.cpp)
set(H_FILES mesh.h)

set(SOURCE_FILES ${CXX_FILES} ${H_FILES})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/..")

add_library(mesh ${SOURCE_FILES})
install(TARGETS mesh
	ARCHIVE DESTINATION lib
)
