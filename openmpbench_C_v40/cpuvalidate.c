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
#include "cpuvalidate.h"

double btest[27];
double atest[27];

#pragma omp threadprivate(btest)

int main(int argc, char **argv)
{

    init(argc, argv);

    extern char type[120];

    /* GENERATE REFERENCE TIME */
    reference("reference time", &func2);

    /* TEST  PRIVATE */
    if ((strcmp("TEST", type) == 0) || (strcmp("ALL", type) == 0))
    {
        benchmark2("testall",&func2,&func1);
        benchmark("test1",&func1);
        // benchmark("test2", &func2);
    }

    finalise();
    return EXIT_SUCCESS;
}

void func1()
{
    double a[1];
    // #pragma omp target map(tofrom : a)
    for (int j = 0; j < innerreps; j++)
    {
        array_delay(500, a);
        a[0] += 1.0; // Simulate combined operations
        // Print the current value of 'a' to force sequential execution
        printf("func1: Iteration %d, a[0] = %f\n", j, a[0]);
    }
}

void func2()
{
    double a[1] = {0.0};
// #pragma omp target map(tofrom : a)
    for (int j = 0; j < innerreps; j++)
    {
        array_delay(delaylength, a);
        a[0] += 2.0; // Simulate a subset or different operations
        // Print the current value of 'a' to force sequential execution
        printf("func1: Iteration %d, a[0] = %f\n", j, a[0]);
    }
}
