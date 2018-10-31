# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND lms_equaliser_sources
)

set(lms_equaliser_sources "${lms_equaliser_sources}" PARENT_SCOPE)
if(NOT lms_equaliser_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT lms_equaliser_sources)

add_library(gnuradio-lms_equaliser SHARED ${lms_equaliser_sources})
target_link_libraries(gnuradio-lms_equaliser ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-lms_equaliser PROPERTIES DEFINE_SYMBOL "gnuradio_lms_equaliser_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-lms_equaliser PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-lms_equaliser
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_lms_equaliser_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_lms_equaliser.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_lms_equaliser.cc
)

add_executable(test-lms_equaliser ${test_lms_equaliser_sources})

target_link_libraries(
  test-lms_equaliser
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-lms_equaliser
)

GR_ADD_TEST(test_lms_equaliser test-lms_equaliser)
