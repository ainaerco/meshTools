set(CXX_FILES delaunay.cpp)
set(H_FILES delaunay.h)
set(SOURCE_FILES ${CXX_FILES} ${H_FILES})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/..")

add_library(delaunay ${SOURCE_FILES})
target_link_libraries(delaunay PUBLIC geometry)
install(TARGETS delaunay
  ARCHIVE DESTINATION lib
)
