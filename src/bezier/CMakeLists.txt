set(CXX_FILES curves.cpp)
set(H_FILES curves.h)

set(SOURCE_FILES ${CXX_FILES} ${H_FILES})

add_library(bezier ${SOURCE_FILES})

install(TARGETS bezier
	ARCHIVE DESTINATION lib
)
