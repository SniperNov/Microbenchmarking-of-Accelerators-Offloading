/****************************************************************************
*                                                                           *
*             OpenMP MicroBenchmark Suite - Version 4.0                     *
*                                                                           *
*                            produced by                                    *
*                                                                           *
*                             Mark Bull                                     *
*                                                                           *
*                                at                                         *
*                                                                           *
*                   EPCC, University of Edinburgh                           *
*                                                                           *
*                    email: m.bull@epcc.ed.ac.uk                            *
*                                                                           *
*                                                                           *
*      This version copyright (c) The University of Edinburgh, 2023.        *
*                                                                           *
*                                                                           *
*  Licensed under the Apache License, Version 2.0 (the "License");          *
*  you may not use this file except in compliance with the License.         *
*  You may obtain a copy of the License at                                  *
*                                                                           *
*      http://www.apache.org/licenses/LICENSE-2.0                           *
*                                                                           *
*  Unless required by applicable law or agreed to in writing, software      *
*  distributed under the License is distributed on an "AS IS" BASIS,        *
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
*  See the License for the specific language governing permissions and      *
*  limitations under the License.                                           *
*                                                                           *
****************************************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>

#include "common.h"
#include "schedbench.h"

int cksz, itersperthr = 1024;
char testName[32];
extern char type[120];
int main(int argc, char **argv) {

    init(argc, argv);
    // Also print itersperthr
    printf("\t%d iterations per thread\n", itersperthr);

    /* GENERATE REFERENCE TIME */
    reference("reference time", &refer);

    /* TEST STATIC */
    if((strcmp("STATIC",type)==0)||(strcmp("ALL",type)==0)){
      benchmark("STATIC", &teststatic);
    }
    /* TEST STATIC on device */
    if ((strcmp("DEVICE", type) == 0) || (strcmp("ALL", type) == 0))
    {
      benchmark("STATIC_DEVICE", &device_teststatic);
    }

    /* TEST STATIC MONO */
    if((strcmp("STATIC_MONOTONIC",type)==0)||(strcmp("ALL",type)==0)){
      benchmark("STATIC_MONOTONIC", &teststaticmono);
    }
    /* TEST STATIC MONO on device */
    if ((strcmp("DEVICE", type) == 0) || (strcmp("ALL", type) == 0)){
      benchmark("STATIC_MONOTONIC_DEVICE", &device_teststaticmono);
    }

    /* TEST STATIC,n */
    if((strcmp("STATICN",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1024;
      while (cksz <= itersperthr) {
        sprintf(testName, "STATIC %d", cksz);
        benchmark(testName, &teststaticn);
        cksz *= 2;
      }
    }
    // /* TEST STATIC,n ON DEVICE*/
    // if ((strcmp("STATICN", type) == 0) || (strcmp("ALL", type) == 0))
    // {
    //   cksz = 1024;
    //   while (cksz <= itersperthr)
    //   {
    //     sprintf(testName, "ON DEVICE STATIC %d", cksz);
    //     benchmark(testName, &device_teststaticn);
    //     cksz *= 2;
    //   }
    // }

    /* TEST STATIC MONO,n */
    if((strcmp("STATICN_MONOTONIC",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1024;
      while (cksz <= itersperthr) {
        sprintf(testName, "STATIC_MONOTONIC %d", cksz);
        benchmark(testName, &teststaticnmono);
        cksz *= 2;
      }
    }
    // /* TEST STATIC MONO ON DEVICE,n */
    //     if ((strcmp("STATICN_MONOTONIC", type) == 0) || (strcmp("ALL", type) == 0))
    // {
    //   cksz = 1024;
    //   while (cksz <= itersperthr)
    //   {
    //     sprintf(testName, "ON DEVICE STATIC_MONOTONIC %d", cksz);
    //     benchmark(testName, &device_teststaticnmono);
    //     cksz *= 2;
    //   }
    // }

    /* TEST DYNAMIC,n */
    if((strcmp("DYNAMIC",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1;
      while (cksz <= itersperthr) {
        sprintf(testName, "DYNAMIC %d", cksz);
        benchmark(testName, &testdynamicn);
        cksz *= 2;
      }
    }

    if((strcmp("DYNAMIC_MONOTONIC",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1;
      while (cksz <= itersperthr) {
        sprintf(testName, "DYNAMIC_MONOTONIC %d", cksz);
        benchmark(testName, &testdynamicnmono);
        cksz *= 2;
      }
    }

    /* TEST GUIDED,n */
    if((strcmp("GUIDED",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1;
      while (cksz <= itersperthr / nthreads) {
        sprintf(testName, "GUIDED %d", cksz);
        benchmark(testName, &testguidedn);
      cksz *= 2;
      }
    }

    if((strcmp("GUIDED_MONOTONIC",type)==0)||(strcmp("ALL",type)==0)){
      cksz = 1;
      while (cksz <= itersperthr / nthreads) {
        sprintf(testName, "GUIDED_MONOTONIC %d", cksz);
        benchmark(testName, &testguidednmono);
        cksz *= 2;
      }
    }

    // if((strcmp("TASKLOOP",type)==0)||(strcmp("ALL",type)==0)){
    //   cksz = 1;
    //   while (cksz <= itersperthr / nthreads) {
    //     sprintf(testName, "TASKLOOP %d", cksz);
    //     benchmark(testName, &taskloopn);
    //     cksz *= 2;
    //   }
    // }

    finalise();
    return EXIT_SUCCESS;

  }

void refer() {
    int i, j;
    for (j = 0; j < innerreps; j++) {
      for (i = 0; i < itersperthr; i++) {
        delay(delaylength);
      }
    }
}

void teststatic() {

    int i, j;
#pragma omp parallel private(j)
    {
	for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(static)
	    for (i = 0; i < itersperthr * nthreads; i++) {
		delay(delaylength);
	    }
	}
    }
}

void device_teststatic() {

  int i, j;
  // calculated before the offloaded region to ensure that the total number of iterations aligns with your intended distribution across threads and iterations per thread.
#pragma omp parallel private(j)
  for (j = 0; j < innerreps; j++)
  {
// Offload the entire parallel region to the device
#pragma omp target
#pragma omp parallel for schedule(static)
    for (i = 0; i < itersperthr * nthreads; i++)
    {
      delay(delaylength);
    }
  }
  // because GPU threads (within the same warp or wavefront, depending on the architecture) naturally 
  // synchronize at the end of the kernel execution or are managed differently through the hardware and runtime environment. 
}

void teststaticmono() {

    int i, j;
#pragma omp parallel private(j)
    {
	for (j = 0; j < innerreps; j++) {
#pragma omp parallel for schedule(monotonic:static)
	    for (i = 0; i < itersperthr * nthreads; i++) {
		delay(delaylength);
	    }
	}
    }
}

void device_teststaticmono()
{

  int i, j;
#pragma omp parallel private(j)
  for (j = 0; j < innerreps; j++)
  {
// Offload the entire parallel region to the device
#pragma omp target
#pragma omp for schedule(monotonic : static)
    for (i = 0; i < itersperthr * nthreads; i++)
    {
      delay(delaylength);
    }
  }
}

void teststaticn() {
    int i, j;
#pragma omp parallel private(j)
    {
	for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(static,cksz)
	    for (i = 0; i < itersperthr * nthreads; i++) {
		delay(delaylength);
	    }
	}
    }
}

// void device_teststaticn()
// {
//   int i, j;
//   for (j = 0; j < innerreps; j++){
// // Offload the entire parallel region to the device
// #pragma omp target teams distribute parallel for private(j) schedule(static, cksz)
//   for (i = 0; i < itersperthr * nthreads; i++)
//     {
//       delay(delaylength);
//     }
//   }
// }


void teststaticnmono() {
    int i, j;
#pragma omp parallel private(j)
    {
    for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(monotonic:static,cksz)
        for (i = 0; i < itersperthr * nthreads; i++) {
        delay(delaylength);
        }
      }
    }
}

// void device_teststaticnmono()
// {
//   int i, j;
//   for (j = 0; j < innerreps; j++)
//   {
// // Offload the entire structured block to the device
// #pragma omp target teams distribute parallel for private(j) schedule(static, cksz)
//     for (i = 0; i < itersperthr * nthreads; i++)
//     {
//       delay(delaylength);
//     }
//   }
// }

void testdynamicn() {
    int i, j;
#pragma omp parallel private(j)
    {
    for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(dynamic,cksz)
        for (i = 0; i < itersperthr * nthreads; i++) {
        delay(delaylength);
        }
      }
    }
}

// void device_testdynamicn()
// {
//   int i, j;
//   int iters = itersperthr * nthreads; // Calculate total iterations

// // Offload the entire parallel region to the device
// #pragma omp target teams distribute parallel for private(j) schedule(dynamic, cksz)
//   for (i = 0; i < iters; i++)
//   {
//     for (j = 0; j < innerreps; j++)
//     {
//       delay(delaylength);
//     }
//   }
// }

void testdynamicnmono() {
    int i, j;
#pragma omp parallel private(j)
    {
    for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(monotonic:dynamic,cksz)
        for (i = 0; i < itersperthr * nthreads; i++) {
        delay(delaylength);
        }
    }
    }
}

// void device_testdynamicnmono()
// {
//   int i, j;
//   int iters = itersperthr * nthreads; // Total iterations based on threads and per-thread iterations

// // Offload the entire computation
// #pragma omp target teams distribute parallel for private(j) schedule(monotonic:dynamic, cksz)
//   for (i = 0; i < iters; i++)
//   {
//     for (j = 0; j < innerreps; j++)
//     {
//       delay(delaylength);
//     }
//   }
// }

void testguidedn() {
    int i, j;
#pragma omp parallel private(j)
    {
    for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(guided,cksz)
        for (i = 0; i < itersperthr * nthreads; i++) {
        delay(delaylength);
        }
      }
    }
}

// void testguidedn_device()
// {
//   int i, j;
//   int iters = itersperthr * nthreads; // Calculate total iterations based on threads and per-thread iterations

// // Offload the computation to the device
// #pragma omp target teams distribute parallel for private(j) schedule(guided, cksz)
//   for (i = 0; i < iters; i++)
//   {
//     for (j = 0; j < innerreps; j++)
//     {
//       delay(delaylength);
//     }
//   }
// }

void testguidednmono() {
    int i, j;
#pragma omp parallel private(j)
    {
    for (j = 0; j < innerreps; j++) {
#pragma omp for schedule(monotonic:guided,cksz)
        for (i = 0; i < itersperthr * nthreads; i++) {
        delay(delaylength);
        }
      }
    }
}

// void testguidednmono_device()
// {
//   int i, j;
//   int iters = itersperthr * nthreads; // Total iterations based on threads and per-thread iterations

// // Offload the computation to the device
// #pragma omp target teams distribute parallel for private(j) schedule(monotonic:guided, cksz)
//   for (i = 0; i < iters; i++)
//   {
//     for (j = 0; j < innerreps; j++)
//     {
//       delay(delaylength);
//     }
//   }
// }

// void taskloopn() {
//   int i, j;
// #pragma omp parallel private(j)
//   {
//     #pragma omp master
//     {
//       for (j = 0; j < innerreps; j++) {
//         #pragma omp taskloop num_tasks((itersperthr*nthreads)/cksz)
//         for (i = 0; i < itersperthr * nthreads; i++) {
//           delay(delaylength);
//         }
//       }
//     }
//   }
// }
