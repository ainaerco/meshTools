include_directories(
  "${CMAKE_SOURCE_DIR}"
  "${CMAKE_SOURCE_DIR}/bezier"
)

nanobind_add_module(_bezier module_bezier.cpp)
target_link_libraries(_bezier PRIVATE bezier)

# When built by scikit-build-core (pip install), install into package dir
if(DEFINED SKBUILD)
  set(_ext_install_dir "${SKBUILD_PLATLIB_DIR}/meshTools")
else()
  set(_ext_install_dir scripts)
endif()
install(TARGETS _bezier
  LIBRARY DESTINATION ${_ext_install_dir}
  RUNTIME DESTINATION ${_ext_install_dir}
)
