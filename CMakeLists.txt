cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(FetchContent)

if(DEFINED EMSCRIPTEN)
  set(CMAKE_VERBOSE_MAKEFILE ON)
  set(CMAKE_RULE_MESSAGES ON)
  # might be needed for emscripten
  set_property(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
endif()


# Try system/conda first
find_library(CSPICE_LIB NAMES cspice)

if(CSPICE_LIB)
  message(STATUS "Found system CSPICE: ${CSPICE_LIB}")
  add_library(cspice UNKNOWN IMPORTED)
  set_target_properties(cspice PROPERTIES IMPORTED_LOCATION "${CSPICE_LIB}")
  # look for the headers
  find_path(CSPICE_INCLUDE_DIR NAMES SpiceUsr.h PATH_SUFFIXES cspice)
  if (CSPICE_INCLUDE_DIR)
    message(STATUS "Found system CSPICE include: ${CSPICE_INCLUDE_DIR}")
    set_target_properties(cspice PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CSPICE_INCLUDE_DIR}")
  else()
    message(WARNING "CSPICE library found, but headers not found")
  endif()
else()
  message(STATUS "System CSPICE not found, falling back to FetchContent")
  # we need to use this for the INSTALL_RPATH property
  set(manual_patch_cspice_origin 'yes')  
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
    GIT_TAG        1975069e3a43391a664dadf7034c5f24d0142cf8 # unreleased version with emscripten builds better supported.
  )
  FetchContent_MakeAvailable(cspice)
  
  # disable versioned/
  set_target_properties(cspice PROPERTIES
    VERSION ""      # no libmyclibrary.so.X.Y.Z
    SOVERSION ""    # no libmyclibrary.so.X
    NO_SONAME ON    # don't encode a soname
  )

  if(DEFINED EMSCRIPTEN)
    target_link_options(cspice PRIVATE -Wl,-soname,libcspice.wasm)
  endif()
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

# Make Python extension using full dotted name for emscripten
python_add_library(spiceypy.cyice.cyice MODULE ${C_FILE} WITH_SOABI)
# Adjust properties using the same target name
set_target_properties(spiceypy.cyice.cyice PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/spiceypy/cyice"
  OUTPUT_NAME "cyice"
)

message(NOTICE "---- Toolchain / Globals ----")
message(NOTICE "CMAKE_SYSTEM_NAME           = ${CMAKE_SYSTEM_NAME}")
message(NOTICE "CMAKE_C_COMPILER_ID         = ${CMAKE_C_COMPILER_ID}")
message(NOTICE "CMAKE_C_COMPILER            = ${CMAKE_C_COMPILER}")
message(NOTICE "CMAKE_TOOLCHAIN_FILE        = ${CMAKE_TOOLCHAIN_FILE}")
message(NOTICE "CMAKE_BUILD_TYPE            = ${CMAKE_BUILD_TYPE}")
message(NOTICE "CMAKE_SHARED_LINKER_FLAGS   = ${CMAKE_SHARED_LINKER_FLAGS}")
message(NOTICE "CMAKE_EXE_LINKER_FLAGS      = ${CMAKE_EXE_LINKER_FLAGS}")
message(NOTICE "-----------------------------")
get_property(SRCS  TARGET cspice PROPERTY SOURCES)
get_property(OBJS  TARGET cspice PROPERTY OBJECTS)
get_property(LIBS  TARGET cspice PROPERTY LINK_LIBRARIES)
get_property(OPTS  TARGET cspice PROPERTY LINK_OPTIONS)
message(NOTICE "cspice SOURCES: ${SRCS}")
message(NOTICE "cspice OBJECTS: ${OBJS}")
message(NOTICE "cspice LINK_LIBRARIES: ${LIBS}")
message(NOTICE "cspice LINK_OPTIONS: ${OPTS}")

# Link to the CSPICE target exposed by the subproject
target_include_directories(spiceypy.cyice.cyice PRIVATE ${Python_NumPy_INCLUDE_DIRS})

# Set numpy options to ensure no deprecated apis older than 1.7
target_compile_definitions(spiceypy.cyice.cyice
    PRIVATE
        NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
)

# Link CSPICE + math lib (only on UNIX)
if(UNIX AND NOT WIN32 AND NOT MINGW)
    target_link_libraries(spiceypy.cyice.cyice PRIVATE cspice m)
else()
    target_link_libraries(spiceypy.cyice.cyice PRIVATE cspice)
endif()

# Fix runtime search paths so extension finds libcspice in same dir if we manually install cspice
if(DEFINED manual_patch_cspice_origin)
  if(APPLE)
    set_target_properties(spiceypy.cyice.cyice PROPERTIES
      INSTALL_RPATH "@loader_path/../utils"
      BUILD_WITH_INSTALL_RPATH ON
    )
  elseif(UNIX OR DEFINED EMSCRIPTEN)
    set_target_properties(spiceypy.cyice.cyice PROPERTIES
      INSTALL_RPATH "$ORIGIN/../utils"
      BUILD_WITH_INSTALL_RPATH ON
    )
  endif()
endif()

if(DEFINED EMSCRIPTEN)
   target_link_options(spiceypy.cyice.cyice PRIVATE
    -shared
    -Wl,--export=PyInit_spiceypy__cyice__cyice
  )
endif()


get_target_property(_type spiceypy.cyice.cyice TYPE)
get_target_property(_opts spiceypy.cyice.cyice LINK_OPTIONS)
message(NOTICE "cyice TYPE=${_type}")
message(NOTICE "cyice LINK_OPTIONS=${_opts}")
get_directory_property(_dir_link_opts LINK_OPTIONS)
message(NOTICE "DIRECTORY LINK_OPTIONS=${_dir_link_opts}")


# install cyice
install(TARGETS spiceypy.cyice.cyice DESTINATION spiceypy/cyice/)