set(CXX_FILES chull.cpp)
set(H_FILES chull.h)
set(SOURCE_FILES ${CXX_FILES} ${H_FILES})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/..")

add_library(chull ${SOURCE_FILES})
target_link_libraries(chull PUBLIC geometry)
install(TARGETS chull
  ARCHIVE DESTINATION lib
)
