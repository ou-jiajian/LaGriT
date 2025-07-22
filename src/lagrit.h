c
c----------------------------------------------------------------
c
c This is a template for the lagrit program banner
c Substitute the TAG strings with Date and Operating System
c Compile library with updated lagrit.h used in writinit()
c This template is preserved in lagrit.h.in
c
c----------------------------------------------------------------
c
      integer        v_major, v_minor, v_patch
      parameter      (v_major=3)
      parameter      (v_minor=3)
      parameter      (v_patch=4)

      character*22   date_compile
      character*8    os_name
      character*16   my_name
      character*26    compiler_name
      character*23    compiler_version

      data my_name      /'lagritgen'/
      data os_name      /'Windows '/
      data date_compile /'2025/07/21 '/
      data compiler_name /'GNU '/
      data compiler_version /'15.1.0 '/

      integer         NCall
      save            NCall
      character*8     Version
      save            Version
c
c----------------------------------------------------------------
c
