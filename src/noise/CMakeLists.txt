set(CXX_FILES noise.cpp)
set(H_FILES noise.h noise_tables.h)
set(SOURCE_FILES ${CXX_FILES} ${H_FILES})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/..")

add_library(noise ${SOURCE_FILES})
install(TARGETS noise
  ARCHIVE DESTINATION lib
)
