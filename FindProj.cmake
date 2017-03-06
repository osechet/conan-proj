# FindProj
# --------
#
# Locate Proj
#
# This module accepts the following environment variables:
#
# ::
#
#     PROJ_DIR or PROJ_ROOT - Specify the location of Proj
#
#
# Imported targets
# ^^^^^^^^^^^^^^^^
#
# This module defines the following :prop_tgt:`IMPORTED` targets:
#
# ``Proj::Proj``
#   The Proj library, if found
#
#
# Result variables
# ^^^^^^^^^^^^^^^^
#
# This module defines the following CMake variables:
#
# ::
#
#     PROJ_FOUND - True if libproj is found
#     PROJ_LIBRARY - A variable pointing to the Proj library
#     PROJ_INCLUDE_DIR - Where to find the headers
#     PROJ_SHARE_DIR - The path to the shared data
#
# The library variables below are set as normal variables.  These
# contain debug/optimized keywords when a debugging library is found.
#
# ``PROJ_LIBRARIES``
#   The Proj library
#

FIND_PATH(PROJ_INCLUDE_DIR proj_api.h
    HINTS
        ENV PROJ_DIR
        ENV PROJ_ROOT
    PATH_SUFFIXES
        include/proj
        include
    PATHS
        ~/Library/Frameworks/proj.framework/Headers
        /Library/Frameworks/proj.framework/Headers
        /sw # Fink
        /opt/local # DarwinPorts
        /opt/csw # Blastwave
        /opt
)

find_library(PROJ_LIBRARY
    NAMES proj_i proj
    HINTS
        ENV GDAL_DIR
        ENV GDAL_ROOT
    PATH_SUFFIXES lib
    PATHS
        /sw
        /opt/local
        /opt/csw
        /opt
        /usr/freeware
)

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PROJ DEFAULT_MSG PROJ_LIBRARY PROJ_INCLUDE_DIR)

set(PROJ_LIBRARIES ${PROJ_LIBRARY})
set(PROJ_INCLUDE_DIRS ${PROJ_INCLUDE_DIR})

IF (PROJ_FOUND)
    mark_as_advanced(PROJ_INCLUDE_DIR)
    mark_as_advanced(PROJ_LIBRARY)

    find_path(PROJ_SHARE_DIR epsg
        HINTS
            $ENV{PROJ_ROOT_DIR}
            ${PROJ_ROOT_DIR}
        PATH_SUFFIXES
            data
            share/proj
    )
    mark_as_advanced(PROJ_SHARE_DIR)

    if(NOT TARGET Proj::Proj)
        add_library(Proj::Proj SHARED IMPORTED)
        if(PROJ_INCLUDE_DIRS)
            set_target_properties(Proj::Proj PROPERTIES
                INTERFACE_INCLUDE_DIRECTORIES "${PROJ_INCLUDE_DIRS}")
        endif()
        if(EXISTS "${PROJ_LIBRARY}")
            set_target_properties(Proj::Proj PROPERTIES
                IMPORTED_LINK_INTERFACE_LANGUAGES "CXX"
                IMPORTED_LOCATION "${PROJ_LIBRARY}")
        endif()
    endif()
ENDIF (PROJ_FOUND)
