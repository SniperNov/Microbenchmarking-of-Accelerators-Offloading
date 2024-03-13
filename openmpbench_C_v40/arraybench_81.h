# 1 "arraybench.h"
# 1 "/mnt/lustre/indy2lfs/sw/nvidia/hpcsdk-2211/Linux_x86_64/22.11/compilers/include/_cplus_macros.h" 1 3
# 1 "arraybench.h" 2
# 1 "/mnt/lustre/indy2lfs/sw/nvidia/hpcsdk-2211/Linux_x86_64/22.11/compilers/include/_cplus_preinclude.h" 1 3
 




 

struct __va_list_tag {
  unsigned int gp_offset;
  unsigned int fp_offset;
  char *overflow_arg_area;
  char *reg_save_area;
};

# 27 "/mnt/lustre/indy2lfs/sw/nvidia/hpcsdk-2211/Linux_x86_64/22.11/compilers/include/_cplus_preinclude.h" 3

typedef struct __va_list_tag __pgi_va_list[1];



# 41 "/mnt/lustre/indy2lfs/sw/nvidia/hpcsdk-2211/Linux_x86_64/22.11/compilers/include/_cplus_preinclude.h" 3











# 1 "arraybench.h" 2






























 




void refer();

void testfirstprivnew();
void device_testfirstprivnew();

void testprivnew();
void device_testprivnew();

void testcopyprivnew();

void testthrprivnew();

void stats(double*, double*);

