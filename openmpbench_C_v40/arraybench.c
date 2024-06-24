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
#include <math.h>
#include <omp.h>
#include <string.h>
#include "common.h"
#include "arraybench.h"

// double btest[IDA];
double atest[IDA];
double btest[IDA];
#pragma omp threadprivate(btest)
double atest_device[IDA]; // Consider that on the device, we work with pointers.

int main(int argc, char **argv) {

    init(argc, argv);

    char testName[32];
    extern char type[120];



    /* GENERATE REFERENCE TIME */
    // reference("reference", &refer);
    reference("reference_Device", &device_refer);


    /* TEST  PRIVATE */
    if((strcmp("PRIVATE",type)==0)||(strcmp("ALL",type)==0)){
      sprintf(testName, "PRIVATE_%d", IDA);
      benchmark(testName, &testprivnew);
    }

    /****************************************************************************/
    /* TEST offload to target */
    if ((strcmp("DEVICE", type) == 0) ||(strcmp("TARGET", type) == 0)|| (strcmp("ALL", type) == 0))
    {
        sprintf(testName, "TARGET_DEVICE_%d", IDA); // 
     
     
        benchmark(testName, &device_target);    // Use the device version of the test
    }
    /****************************************************************************/

    /****************************************************************************/
    /* TEST PRIVATE on Device */
    if ((strcmp("DEVICE", type) == 0) || (strcmp("ALL", type) == 0))
    {
        sprintf(testName, "PRIVATE_DEVICE_%d", IDA); // Name changed to indicate device
     
     
        benchmark(testName, &device_testprivnew);    // Use the device version of the test
    }
    /****************************************************************************/

    /* TEST  FIRSTPRIVATE */
    if((strcmp("FIRSTPRIVATE",type)==0)||(strcmp("ALL",type)==0)){
      sprintf(testName, "FIRSTPRIVATE_%d", IDA);
      benchmark(testName, &testfirstprivnew);
    }


    /****************************************************************************/
    /* TEST  FIRSTPRIVATE ON DEVICE*/
    if ((strcmp("DEVICE", type) == 0) || (strcmp("ALL", type) == 0))
    {
        sprintf(testName, "FIRSTPRIVATE_DEVICE_%d", IDA);
        benchmark(testName, &device_testfirstprivnew);
    }
    /****************************************************************************/

    /* TEST  COPYPRIVATE */
    if((strcmp("COPYPRIVATE",type)==0)||(strcmp("ALL",type)==0)){
      sprintf(testName, "COPYPRIVATE_%d", IDA);
      benchmark(testName, &testcopyprivnew);
    }

    // /* TEST  THREADPRIVATE - COPYIN */
    // if((strcmp("COPYIN",type)==0)||(strcmp("ALL",type)==0)){
    //   sprintf(testName, "COPYIN_%d", IDA);
    //   benchmark(testName, &testthrprivnew);
    // }

    finalise();
    return EXIT_SUCCESS;

}
void refer() {
    int j;
    double a[1];
    for (j = 0; j < innerreps; j++) {
	array_delay(delaylength, a);
    }
}

void device_refer() {
    int j;
    double a[1];
    a[0]=0;
#pragma omp target map(tofrom:a)
    for (j = 0; j < innerreps; j++) {
        array_delay(delaylength, a);
        a[0]+=1;
    }
    if (a[0] < 0)
    {
        printf("%f \n", a[0]);
    }
}

void testprivnew() {
    int j;
    atest[0] = 0;
    for (j = 0; j < innerreps; j++) {
#pragma omp parallel private(atest)
	{
	    array_delay(delaylength, atest);
        atest[0]+=1;
	}
    }
    if (atest[0] < 0)
    {
        printf("%f \n", atest[0]);
    }
}

void device_target() {
    int j;
    double a[1];
    a[0]=0;
    for (j = 0; j < innerreps; j++) {
    
 #pragma omp target map(tofrom:a)
        array_delay(delaylength, a);
        a[0]+=1;
    }
    if (a[0]<0){
        printf("%f \n", a[0]);
    }
}

void device_testprivnew()
{
    int j;
    atest[0]=0;
    // Map the entire loop to the device
    for (j = 0; j < innerreps; j++)
    {
#pragma omp target map(tofrom : atest) // Mapping 'atest'
#pragma omp parallel private(atest) // Distribute the outer loop among teams
        {
            array_delay(delaylength, atest);
        }
        atest[0] += 1;
    }
    if (atest[0] < 0)
    {
        printf("%f \n", atest[0]);
    }
}

void testfirstprivnew() {
    int j;
    for (j = 0; j < innerreps; j++) {
#pragma omp parallel firstprivate(atest)
	{
	    array_delay(delaylength, atest);
	}
    }
}

void device_testfirstprivnew()
{
    int j;
    for (j = 0; j < innerreps; j++)
    {
#pragma omp target map(tofrom : atest) // Mapping 'atest'
#pragma omp parallel firstprivate(atest) // Ensuring 'atest' array is available on the device
        {
            array_delay(delaylength, atest);
        }
    }
}

void testcopyprivnew()
{
    int j;
    for (j=0; j<innerreps; j++) {
#pragma omp parallel private(atest)
	{
#pragma omp single copyprivate(atest)
		{
	    	array_delay(delaylength, atest);
		}
    	}
    }
}


// void testthrprivnew() {
//     int j;
//     for (j = 0; j < innerreps; j++) {
// #pragma omp parallel copyin(btest)
// 	{
// 	    array_delay(delaylength, btest);
// 	}
//     }

// }

