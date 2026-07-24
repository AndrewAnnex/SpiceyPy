cmake_minimum_required(VERSION 3.15...3.26)

# SPICEYPY_CSPICE_ONLY: build and install *only* the CSPICE dependency into
# CMAKE_INSTALL_PREFIX, then stop -- no Python, no Cython, no cyice.
#
# CI uses this to build CSPICE once per cibuildwheel job instead of once per
# Python version (CSPICE is ~2200 C files and does not depend on Python at all).
# The resulting prefix is handed back to the per-wheel builds via the
# SPICEYPY_CSPICE_PREFIX environment variable, handled further down.
#
# This deliberately lives in *this* file rather than a separate mini-project so
# that the pinned cspice-cmake-spiceypy ref and the shared-library naming
# overrides below cannot drift between the two build paths -- a mismatch there
# would produce a wheel whose CSPICE loads under CMake but not under the ctypes
# fallback in spiceypy/utils/libspicehelper.py.
option(SPICEYPY_CSPICE_ONLY "Build and install only the CSPICE dependency" OFF)

# scikit-build-core defines SKBUILD_PROJECT_NAME; a SPICEYPY_CSPICE_ONLY
# configure is driven by plain cmake, so supply a default.
if(NOT DEFINED SKBUILD_PROJECT_NAME)
  set(SKBUILD_PROJECT_NAME spiceypy)
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

if(NOT SPICEYPY_CSPICE_ONLY)
  find_package(
    Python
    COMPONENTS Interpreter Development.Module NumPy
    REQUIRED)
endif()

include(FetchContent)

if(DEFINED EMSCRIPTEN)
  set(CMAKE_VERBOSE_MAKEFILE ON)
  set(CMAKE_RULE_MESSAGES ON)
  # might be needed for emscripten
  set_property(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
endif()


##############################################################################
# Acquire CSPICE. Three paths, in priority order:
#
#   1. SPICEYPY_CSPICE_PREFIX -- a CSPICE that a SPICEYPY_CSPICE_ONLY configure
#      already built and installed. Vendored into the wheel exactly like path 3,
#      so the shipped layout is byte-for-byte the same either way.
#   2. A system/conda libcspice on the default search paths. Used as-is and
#      deliberately NOT vendored: it belongs to the environment, not to us.
#   3. FetchContent -- build it from source in this build tree.
#
# Paths 1 and 3 must agree on shared-library naming, which is why the overrides
# live in the macro below rather than being written out twice. Both the wheel's
# cyice extension and the pure-ctypes half of SpiceyPy depend on it:
# spiceypy/utils/libspicehelper.py falls back to loading the library by its
# exact unversioned filename (libcspice.so / libcspice.dylib / cspice.dll) from
# next to the package, so a versioned SONAME here would leave cyice working
# while silently breaking every ctypes-based function.
##############################################################################

# Make the built artifact unversioned, so its SONAME is the plain filename and
# consumers record `NEEDED: libcspice.so` instead of an absolute build path.
macro(spiceypy_unversion_cspice)
  set_target_properties(cspice PROPERTIES
    VERSION ""      # no libcspice.so.X.Y.Z
    SOVERSION ""    # no libcspice.so.X
    NO_SONAME ON    # don't encode a versioned soname
  )
endmacro()

# The pinned upstream CSPICE CMake project, used by paths 1 and 3 alike.
macro(spiceypy_declare_cspice)
  FetchContent_Declare(
    cspice
    GIT_REPOSITORY https://github.com/AndrewAnnex/cspice-cmake-spiceypy.git
    GIT_TAG        276e13b29280382054fda80ef75b222490df4238
  )
endmacro()

if(SPICEYPY_CSPICE_ONLY)
  # Stock GNUInstallDirs layout so the prefix is consumable by find_package.
  # Pin LIBDIR to "lib": GNUInstallDirs picks "lib64" on the RHEL-derived
  # manylinux images, and a predictable prefix keeps the consuming side simple.
  set(CMAKE_INSTALL_LIBDIR "lib" CACHE INTERNAL "")
  spiceypy_declare_cspice()
  FetchContent_MakeAvailable(cspice)
  spiceypy_unversion_cspice()
  message(STATUS "SPICEYPY_CSPICE_ONLY: building CSPICE for install into ${CMAKE_INSTALL_PREFIX}")
  # Nothing else in this file applies -- no Python, no Cython, no cyice.
  return()
endif()

set(_spiceypy_cspice_prefix "$ENV{SPICEYPY_CSPICE_PREFIX}")
if(SPICEYPY_CSPICE_PREFIX)
  set(_spiceypy_cspice_prefix "${SPICEYPY_CSPICE_PREFIX}")
endif()

if(_spiceypy_cspice_prefix)
  message(STATUS "Using prebuilt CSPICE from SPICEYPY_CSPICE_PREFIX: ${_spiceypy_cspice_prefix}")
  find_package(cspice REQUIRED CONFIG
    PATHS "${_spiceypy_cspice_prefix}"
    NO_DEFAULT_PATH)
  # Unlike a system/conda CSPICE, this one is ours and must ship in the wheel.
  # Vendor it to the same place the FetchContent path installs it, and take the
  # loader-relative rpath branch below so cyice can find it at runtime.
  set(manual_patch_cspice_origin 'yes')
  install(FILES $<TARGET_FILE:CSPICE::cspice> DESTINATION spiceypy/utils/)
else()

# Try system/conda first
find_library(CSPICE_LIB NAMES cspice)

if(CSPICE_LIB)
  message(STATUS "Found system CSPICE: ${CSPICE_LIB}")
  add_library(CSPICE::cspice UNKNOWN IMPORTED)
  set_target_properties(CSPICE::cspice PROPERTIES IMPORTED_LOCATION "${CSPICE_LIB}")
  # look for the headers
  find_path(CSPICE_INCLUDE_DIR NAMES SpiceUsr.h PATH_SUFFIXES cspice)
  if (CSPICE_INCLUDE_DIR)
    message(STATUS "Found system CSPICE include: ${CSPICE_INCLUDE_DIR}")
    set_target_properties(CSPICE::cspice PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CSPICE_INCLUDE_DIR}")
  else()
    message(WARNING "CSPICE library found, but headers not found")
  endif()
else()
  message(STATUS "System CSPICE not found, falling back to FetchContent")
  # we need to use this for the INSTALL_RPATH property
  set(manual_patch_cspice_origin 'yes')  

  # Put CSPICE libs inside our package
  if(DEFINED EMSCRIPTEN)
    set(CMAKE_INSTALL_LIBDIR "spiceypy.libs/" CACHE INTERNAL "")
  else()
    set(CMAKE_INSTALL_LIBDIR "spiceypy/utils/" CACHE INTERNAL "")
  endif()
  
  if(MSVC)
    # Force DLLs to install alongside LIBs instead of bin/
    set(CMAKE_INSTALL_BINDIR "spiceypy/utils/" CACHE INTERNAL "")
  endif()
  
  # Put CSPICE headers somewhere harmless in our package
  set(CMAKE_INSTALL_INCLUDEDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")
  
  # Also redirect data root to avoid polluting share/ etc.
  set(CMAKE_INSTALL_DATAROOTDIR ${SKBUILD_NULL_DIR} CACHE INTERNAL "")
  
  # Bring in your CSPICE CMake project
  spiceypy_declare_cspice()
  FetchContent_MakeAvailable(cspice)

  # disable versioned/
  spiceypy_unversion_cspice()

endif()

endif()

##############################################################################
# cyice specifics below if not on EMSCRIPTEN

if(NOT DEFINED EMSCRIPTEN)


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

# Make Python extension using full dotted name for emscripten
python_add_library(cyice MODULE ${C_FILE} WITH_SOABI)
# Adjust properties using the same target name
set_target_properties(cyice PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/spiceypy/cyice"
  OUTPUT_NAME "cyice"
)

# Link to the CSPICE target exposed by the subproject
target_include_directories(cyice PRIVATE ${Python_NumPy_INCLUDE_DIRS})

# Set numpy options to ensure no deprecated apis older than 1.7
target_compile_definitions(cyice
    PRIVATE
        NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
)

# Link CSPICE + math lib (only on UNIX)
if(UNIX AND NOT WIN32 AND NOT MINGW)
    target_link_libraries(cyice PRIVATE CSPICE::cspice m)
else()
    target_link_libraries(cyice PRIVATE CSPICE::cspice)
endif()

# Fix runtime search paths so extension finds libcspice in same dir if we manually install cspice
if(DEFINED manual_patch_cspice_origin)
  if(APPLE)
    set_target_properties(cyice PROPERTIES
      INSTALL_RPATH "@loader_path/../utils"
      BUILD_WITH_INSTALL_RPATH ON
    )
  elseif(UNIX AND NOT DEFINED EMSCRIPTEN)
    set_target_properties(cyice PROPERTIES
      INSTALL_RPATH "$ORIGIN/../utils"
      BUILD_WITH_INSTALL_RPATH ON
    )
  elseif(DEFINED EMSCRIPTEN)
    message(NOTICE "SETTING RPATH for emscripten") 
    set_target_properties(cyice PROPERTIES
      INSTALL_RPATH "$ORIGIN/../../spiceypy.libs"
      BUILD_RPATH "$ORIGIN/../../spiceypy.libs"
      BUILD_WITH_INSTALL_RPATH ON
    )
    target_link_options(cyice PRIVATE
      -Wl,-rpath,$ORIGIN/../../spiceypy.libs 
    )
  endif()
endif()

# install cyice
install(TARGETS cyice DESTINATION spiceypy/cyice/)

endif()