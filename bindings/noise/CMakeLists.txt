include_directories("${CMAKE_SOURCE_DIR}/src")

nanobind_add_module(_noise module_noise.cpp)
target_link_libraries(_noise PRIVATE noise)

if(DEFINED SKBUILD)
  set(_ext_install_dir "${SKBUILD_PLATLIB_DIR}/meshTools")
else()
  set(_ext_install_dir scripts)
endif()
install(TARGETS _noise
  LIBRARY DESTINATION ${_ext_install_dir}
  RUNTIME DESTINATION ${_ext_install_dir}
)
