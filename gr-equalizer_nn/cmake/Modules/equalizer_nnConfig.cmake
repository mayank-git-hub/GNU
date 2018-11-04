INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_EQUALIZER_NN equalizer_nn)

FIND_PATH(
    EQUALIZER_NN_INCLUDE_DIRS
    NAMES equalizer_nn/api.h
    HINTS $ENV{EQUALIZER_NN_DIR}/include
        ${PC_EQUALIZER_NN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    EQUALIZER_NN_LIBRARIES
    NAMES gnuradio-equalizer_nn
    HINTS $ENV{EQUALIZER_NN_DIR}/lib
        ${PC_EQUALIZER_NN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(EQUALIZER_NN DEFAULT_MSG EQUALIZER_NN_LIBRARIES EQUALIZER_NN_INCLUDE_DIRS)
MARK_AS_ADVANCED(EQUALIZER_NN_LIBRARIES EQUALIZER_NN_INCLUDE_DIRS)

