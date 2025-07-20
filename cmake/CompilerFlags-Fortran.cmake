# if not found, try -DCMAKE_fortran_PATH="path/gfortran"
# remove unused option -m64

include(CheckFortranCompilerFlag)

# Windows MSYS2/MinGW特殊处理
if(WIN32 AND MINGW)
  message(STATUS "  Fortran compiler: Windows MinGW GFORTRAN")
  # 在Windows MinGW环境下，先不设置复杂的标志，让编译器识别成功
  if(NOT CMAKE_Fortran_FLAGS)
    set(CMAKE_Fortran_FLAGS "")
  endif()
  # 在配置完成后再添加必要的标志
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -fcray-pointer -fdefault-integer-8 -std=legacy -fno-sign-zero -fno-range-check")

# set known compiler flags
elseif ("${CMAKE_Fortran_COMPILER_ID}" MATCHES "GNU")
  message(STATUS "  Fortran compiler: GNU GFORTRAN")
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -fcray-pointer -fdefault-integer-8 -std=legacy -fno-sign-zero -fno-range-check")

elseif ("${CMAKE_Fortran_COMPILER_ID}" MATCHES "Intel")
  message(STATUS "  Fortran compiler: Intel Fortran")
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -w -O -Qsafe-cray-ptr -integer-size=64 -assume:nominus0 -QRimplicit-import-")


# try using flags for unknown compiler
else()

message(STATUS "  Fortran compiler: ${CMAKE_Fortran_COMPILER_ID}")
check_fortran_compiler_flag("${CMAKE_Fortran_FLAGS}" _my_flags)
if(_my_flags)
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -fcray-pointer -fdefault-integer-8 -std=legacy -fno-sign-zero -fno-range-check")
else()
  message(STATUS "  cmake/CompilerFlags-Fortran.cmake: FLAGS NOT SET")
endif()

endif()

