cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(FetchContent)

# Try system/conda first
find_library(CSPICE_LIB cspice)

if(CSPICE_LIB)
  message(STATUS "Found system CSPICE: ${CSPICE_LIB}")
else()
  message(STATUS "System CSPICE not found, falling back to FetchContent")
  # Put CSPICE libs inside our package, not top-level lib/
  set(CMAKE_INSTALL_LIBDIR "spiceypy/utils/" CACHE INTERNAL "")
  
  if(MSVC)
    # Force DLLs to install alongside LIBs instead of bin/
    set(CMAKE_INSTALL_BINDIR "spiceypy/utils/" CACHE INTERNAL "")
  endif()
  
  # Put CSPICE headers somewhere harmless in our package
  set(CMAKE_INSTALL_INCLUDEDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")
  
  # Also redirect data root to avoid polluting share/ etc.
  set(CMAKE_INSTALL_DATAROOTDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")
  
  # Bring in your CSPICE CMake project 
  FetchContent_Declare(
    cspice
    GIT_REPOSITORY https://github.com/AndrewAnnex/cspice-cmake-spiceypy.git
    GIT_TAG        c326ce3563a3f059871c601f5ed1fca53bef17be # tag v0.0.2
  )
  FetchContent_MakeAvailable(cspice)
  
  # disable versioned/
  set_target_properties(cspice PROPERTIES
    VERSION ""      # no libmyclibrary.so.X.Y.Z
    SOVERSION ""    # no libmyclibrary.so.X
    NO_SONAME ON    # don't encode a soname
  )
  # The target name depends on your cspice CMake setup
  set(CSPICE_LIB cspice)

endif()


# Convert pyx to c
set(PYX_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/spiceypy/cyice/cyice.pyx)
set(PXD_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/spiceypy/cyice/cyice.pxd)
set(C_FILE ${CMAKE_CURRENT_BINARY_DIR}/spiceypy/cyice/cyice.c)

add_custom_command(
  OUTPUT ${C_FILE}
  COMMAND Python::Interpreter -m cython ${PYX_FILE} --output-file ${C_FILE}
  DEPENDS ${PYX_FILE} ${PXD_FILE}
  COMMENT "Cythonizing ${PYX_FILE} to ${C_FILE}"
  VERBATIM)

# Make Python extension
python_add_library(cyice MODULE ${C_FILE} WITH_SOABI)

# Link to the CSPICE target exposed by the subproject
target_include_directories(cyice PRIVATE ${Python_NumPy_INCLUDE_DIRS})

# Link CSPICE + math lib (only on UNIX)
if(UNIX AND NOT WIN32 AND NOT MINGW)
    target_link_libraries(cyice PRIVATE ${CSPICE_LIB} m)
else()
    target_link_libraries(cyice PRIVATE ${CSPICE_LIB})
endif()

# Fix runtime search paths so extension finds libcspice in same dir
if(APPLE)
  set_target_properties(cyice PROPERTIES
    INSTALL_RPATH "@loader_path/../utils"
    BUILD_WITH_INSTALL_RPATH ON
  )
elseif(UNIX)
  set_target_properties(cyice PROPERTIES
    INSTALL_RPATH "$ORIGIN/../utils"
    BUILD_WITH_INSTALL_RPATH ON
  )
endif()

# install cyice
install(TARGETS cyice DESTINATION spiceypy/cyice/)