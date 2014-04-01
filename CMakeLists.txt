#===============================================================================
# Project information

project(ngtTools)
cmake_minimum_required(VERSION 2.8)

# Add path for custom modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}" )

set(PACKAGE_VERSION "0.1")
set(PACKAGE_NAME "NGT Tools")
set(PACKAGE_STRING "${PACKAGE_NAME} ${PACKAGE_VERSION}")
set(PACKAGE_BUGREPORT "scott.t.mcmichael@nasa.gov")


#===============================================================================
# Configuration options

# --- Directory paths ---
set(BASESYSTEM_INSTALL_DIR "" CACHE FILEPATH "Path to AutoTools installation directory")
if(NOT BASESYSTEM_INSTALL_DIR)
  message(SEND_ERROR "You need to set BASESYSTEM_INSTALL_DIR: ${BASESYSTEM_INSTALL_DIR}")
endif()

set(VISIONWORKBENCH_INSTALL_DIR "" CACHE FILEPATH "Path to Vision Workbench installation directory")
if(NOT VISIONWORKBENCH_INSTALL_DIR)
  message(SEND_ERROR "You need to set VISIONWORKBENCH_INSTALL_DIR: ${VISIONWORKBENCH_INSTALL_DIR}")
endif()

set(STEREOPIPELINE_INSTALL_DIR "" CACHE FILEPATH "Path to Stereo Pipeline installation directory")
if(NOT STEREOPIPELINE_INSTALL_DIR)
  message(SEND_ERROR "You need to set STEREOPIPELINE_INSTALL_DIR: ${STEREOPIPELINE_INSTALL_DIR}")
endif()

message("Base System path      = ${BASESYSTEM_INSTALL_DIR}")
message("Vision Workbench path = ${VISIONWORKBENCH_INSTALL_DIR}")
message("Stereo Pipeline path  = ${STEREOPIPELINE_INSTALL_DIR}")

# Copy the nice input variable names to the messy internal names
set(VISIONWORKBENCH_ROOT   ${VISIONWORKBENCH_INSTALL_DIR})
set(StereoPipeline_ROOT    ${STEREOPIPELINE_INSTALL_DIR})

# --- Custom options ---
option(BUILD_SHARED_LIBS "Produce shared libraries." TRUE)

# --- Fixed options ---
set(Boost_USE_STATIC_LIBS   OFF)
set(Boost_USE_MULTITHREADED ON )
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})


#==================================================================================
# Find dependencies

#find_package(Boost 1.50.0
#  COMPONENTS
#  program_options
#  system
#  filesystem
#  thread
#  )

message("--------------------------------------------------------------")
message("Searching for boost...")

set(BOOST_ROOT "${BASESYSTEM_INSTALL_DIR}/include/boost-1_55")
set(BOOST_LIBRARYDIR  "${BASESYSTEM_INSTALL_DIR}/lib")
set(BOOST_INCLUDEDIR "${BASESYSTEM_INSTALL_DIR}/include/boost-1_55/boost")
set(Boost_NO_SYSTEM_PATHS ON) #This does not seem to work
#set(Boost_DEBUG 1) # Uncomment for useful finding boost debug output
set(BOOST_MIN_VERSION "1.55.0")
set(REQUIRED_BOOST_LIBS program_options system filesystem regex date_time thread iostreams)

find_package(Boost ${BOOST_MIN_VERSION} REQUIRED COMPONENTS ${REQUIRED_BOOST_LIBS})

if(Boost_FOUND)
    message("Successfully found Boost version ${Boost_VERSION}!")
    message("---Boost Include Dir = ${Boost_INCLUDE_DIR}")
    #set(Boost_LIBRARY_DIR ${BASESYSTEM_INSTALL_DIR}/lib) # Override this value
    message("---Boost Library Dir = ${Boost_LIBRARY_DIRS}")
    message("---Boost libraries = ${Boost_LIBRARIES}")
    include_directories(${Boost_INCLUDE_DIR})
    link_directories(${Boost_LIBRARY_DIR})
endif(Boost_FOUND)
message("--------------------------------------------------------------")


message("--------------------------------------------------------------")
message("Searching for QT...")
# TODO: Make sure this finds the correct install!
#set (QT_QMAKE_EXECUTABLE  ${BASESYSTEM_INSTALL_DIR}/bin/qmake)
#SET(CMAKE_PREFIX_PATH ${BASESYSTEM_INSTALL_DIR} ${CMAKE_PREFIX_PATH}) 
#set(REQUIRED_QT_LIBS QtCore QtXml QtGui ) #TODO: Figure this out
#find_package(Qt4 4.8.5 REQUIRED )# ${REQUIRED_QT_LIBS})

# Testing: Manual QT settings
set(QT_FOUND True)

set(QT_INCLUDE_DIRS ${BASESYSTEM_INSTALL_DIR}/include/Qt
            ${BASESYSTEM_INSTALL_DIR}/include/Qt3Support
            ${BASESYSTEM_INSTALL_DIR}/include/QtCore
            ${BASESYSTEM_INSTALL_DIR}/include/QtDesigner
            ${BASESYSTEM_INSTALL_DIR}/include/QtGui
            ${BASESYSTEM_INSTALL_DIR}/include/QtHelp
            ${BASESYSTEM_INSTALL_DIR}/include/QtMultimedia
            ${BASESYSTEM_INSTALL_DIR}/include/QtNetwork
            ${BASESYSTEM_INSTALL_DIR}/include/QtSql
            ${BASESYSTEM_INSTALL_DIR}/include/QtSvg
            ${BASESYSTEM_INSTALL_DIR}/include/QtTest
            ${BASESYSTEM_INSTALL_DIR}/include/QtUiTools
            ${BASESYSTEM_INSTALL_DIR}/include/QtXml
            ${BASESYSTEM_INSTALL_DIR}/include/QtXmlPatterns)
set(QT_LIBRARY_DIR  ${BASESYSTEM_INSTALL_DIR}/lib)
set(QT_LIBRARIES  libQt3Support.so
          libQtCLucene.so
          libQtCore.so
          libQtDesignerComponents.so
          libQtDesigner.so
          libQtGui.so
          libQtHelp.so
          libQtMultimedia.so
          libQtNetwork.so
          libQtSql.so
          libQtSvg.so
          libQtTest.so
          libQtXmlPatterns.so
          libQtXml.so )

if(QT_FOUND)
    message("QT include dirs  " ${QT_INCLUDE_DIRS})
    include_directories(${QT_INCLUDE_DIRS})
    link_directories(${QT_LIBRARY_DIR})
endif(QT_FOUND)
message("--------------------------------------------------------------")

# Get NAIF includes (Needed for reading/writing SPICE data)
set(NAIF_FOUND True)
set(NAIF_INCLUDE_DIRS ${BASESYSTEM_INSTALL_DIR}/include/naif/)



find_package(VisionWorkbench REQUIRED
  COMPONENTS
  core
  math
  image
  camera
  fileio
  cartography
  geometry
  interestPoint
  stereo
  mosaic
  )

message("Found vision workbench include directory: ${VISIONWORKBENCH_INCLUDE_DIRS}")


find_package(StereoPipeline REQUIRED COMPONENTS core spiceIO isisIO)



message("Found stereo pipeline include directory: ${StereoPipeline_INCLUDE_DIR}")


set(PROTOBUF_FOUND)
set(PROTOBUF_INCLUDE_DIR ${BASESYSTEM_INSTALL_DIR}/include   )
set(PROTOBUF_LIBRARY     ${BASESYSTEM_INSTALL_DIR}/lib/libprotobuf.so)
include_directories("${PROTOBUF_INCLUDE_DIR}")
include_directories("${QT_INCLUDE_DIRS}")
include_directories("${NAIF_INCLUDE_DIRS}")


include_directories(${VISIONWORKBENCH_INCLUDE_DIRS})
include_directories(${StereoPipeline_INCLUDE_DIR})
include_directories(${Boost_INCLUDE_DIRS})
include_directories(${PROTOBUF_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

link_directories(${Boost_LIBRARY_DIRS})


#===================================================================================
# Executables


add_executable(imagestats imagestats.cc) 
target_link_libraries(imagestats  ${VISIONWORKBENCH_LIBRARIES}) 

add_executable(lola_compare lola_compare.cc) 
target_link_libraries(lola_compare  ${VISIONWORKBENCH_LIBRARIES}) 


add_executable(matchBinaryToCsv matchBinaryToCsv.cc) 
target_link_libraries(matchBinaryToCsv  ${VISIONWORKBENCH_LIBRARIES}) 

add_executable(getLatLonBounds getLatLonBounds.cc) 
target_link_libraries(getLatLonBounds  ${VISIONWORKBENCH_LIBRARIES} ${Boost_LIBRARIES})

add_executable(maskFromIntersectError maskFromIntersectError.cc) 
target_link_libraries(maskFromIntersectError  ${VISIONWORKBENCH_LIBRARIES} ${Boost_LIBRARIES}) 

add_executable(stereoIpFind stereoIpFind.cc)
target_link_libraries(stereoIpFind  ${VISIONWORKBENCH_LIBRARIES}  ${StereoPipeline_LIBRARIES}) 

add_executable(pixelPairsFromStereo pixelPairsFromStereo.cc) 
target_link_libraries(pixelPairsFromStereo  ${VISIONWORKBENCH_LIBRARIES}  ${StereoPipeline_LIBRARIES}) 

add_executable(point_to_dem_dist point_to_dem_dist.cc) 
target_link_libraries(point_to_dem_dist  ${VISIONWORKBENCH_LIBRARIES} ${StereoPipeline_LIBRARIES}) 

add_executable(dem_mean_std dem_mean_std.cc) 
target_link_libraries(dem_mean_std  ${VISIONWORKBENCH_LIBRARIES} ${StereoPipeline_LIBRARIES}) 
